import os
import aiofiles
from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Form
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from app.models.resume import Resume, ResumeAnalysis, PersonalInfo, Education, Experience, Project, Skills, Certification
from app.models.progress import Progress
from app.models.user import User
from app.middleware.auth import get_current_user
from app.utils.file_parser import extract_text_from_pdf, extract_text_from_docx, validate_resume_file
from app.services.ai.resume_service import resume_ai_service
from app.config.settings import settings

router = APIRouter(prefix="/api/resumes", tags=["resumes"])


@router.get("/")
async def get_resumes(current_user: User = Depends(get_current_user)):
    resumes = await Resume.find(Resume.user_id == current_user.id).sort(-Resume.created_at).to_list()
    return {"success": True, "resumes": [
        {"id": str(r.id), "title": r.title, "template": r.template,
         "is_uploaded": r.is_uploaded, "is_generated": r.is_generated,
         "created_at": r.created_at.isoformat()} for r in resumes
    ]}


@router.get("/{resume_id}")
async def get_resume(resume_id: str, current_user: User = Depends(get_current_user)):
    resume = await Resume.get(resume_id)
    if not resume or resume.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Resume not found")
    return {"success": True, "resume": resume.model_dump()}


@router.post("/upload")
async def upload_resume(
    file: UploadFile = File(...),
    job_description: Optional[str] = Form(None),
    current_user: User = Depends(get_current_user),
):
    file_bytes = await file.read()
    error = validate_resume_file(file.filename, len(file_bytes), settings.MAX_FILE_SIZE)
    if error:
        raise HTTPException(status_code=400, detail=error)

    ext = file.filename.rsplit('.', 1)[-1].lower()
    if ext == 'pdf':
        text = await extract_text_from_pdf(file_bytes)
    elif ext in ('docx', 'doc'):
        text = await extract_text_from_docx(file_bytes)
    else:
        raise HTTPException(status_code=400, detail="Unsupported file type")

    if not text or len(text) < 50:
        text = f"Resume uploaded: {file.filename}. Text extraction limited — consider uploading a text-based PDF."

    upload_dir = settings.UPLOAD_DIR
    os.makedirs(upload_dir, exist_ok=True)
    import uuid
    filename = f"{uuid.uuid4().hex}_{file.filename}"
    filepath = os.path.join(upload_dir, filename)
    async with aiofiles.open(filepath, 'wb') as f:
        await f.write(file_bytes)

    resume = Resume(
        user_id=current_user.id,
        title=file.filename.rsplit('.', 1)[0],
        raw_text=text,
        is_uploaded=True,
        uploaded_file={"original_name": file.filename, "path": filepath, "mime_type": file.content_type},
    )
    await resume.insert()

    analysis_data = await resume_ai_service.analyze(text, job_description)
    analysis = ResumeAnalysis(
        user_id=current_user.id,
        resume_id=resume.id,
        scores=analysis_data.get("scores", {}),
        extracted_info=analysis_data.get("extracted_info", {}),
        strengths=analysis_data.get("strengths", []),
        weaknesses=analysis_data.get("weaknesses", []),
        suggestions=analysis_data.get("suggestions", []),
        missing_keywords=analysis_data.get("missing_keywords", []),
        present_keywords=analysis_data.get("present_keywords", []),
    )
    if analysis_data.get("job_match"):
        from app.models.resume import JobMatch
        analysis.job_match = JobMatch(**analysis_data["job_match"])
    await analysis.insert()

    progress = await Progress.find_one(Progress.user_id == current_user.id)
    if progress:
        progress.resume.uploads_count += 1
        progress.resume.analysis_count += 1
        progress.resume.current_score = analysis_data.get("scores", {}).get("overall", 0)
        progress.resume.last_analyzed_date = datetime.utcnow()
        await progress.save()

    return {"success": True, "resume_id": str(resume.id), "analysis_id": str(analysis.id), "analysis": analysis_data}


@router.post("/analyze/{resume_id}")
async def analyze_resume(
    resume_id: str,
    job_description: Optional[str] = None,
    current_user: User = Depends(get_current_user),
):
    resume = await Resume.get(resume_id)
    if not resume or resume.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Resume not found")
    text = resume.raw_text or str(resume.model_dump())
    analysis_data = await resume_ai_service.analyze(text, job_description)
    return {"success": True, "analysis": analysis_data}


class CreateResumeRequest(BaseModel):
    title: Optional[str] = "My Resume"
    template: Optional[str] = "ats-professional"
    personal_info: Optional[dict] = None
    education: Optional[List[dict]] = None
    experience: Optional[List[dict]] = None
    projects: Optional[List[dict]] = None
    skills: Optional[dict] = None
    certifications: Optional[List[dict]] = None
    achievements: Optional[List[str]] = None
    coding_profiles: Optional[List[dict]] = None


@router.post("/create")
async def create_resume(body: CreateResumeRequest, current_user: User = Depends(get_current_user)):
    resume = Resume(
        user_id=current_user.id,
        title=body.title or "My Resume",
        template=body.template or "ats-professional",
        is_generated=True,
    )
    if body.personal_info:
        resume.personal_info = PersonalInfo(**body.personal_info)
    if body.education:
        resume.education = [Education(**e) for e in body.education]
    if body.skills:
        resume.skills = Skills(**body.skills)
    if body.projects:
        resume.projects = [Project(**p) for p in body.projects]
    if body.experience:
        resume.experience = [Experience(**e) for e in body.experience]
    if body.certifications:
        resume.certifications = [Certification(**c) for c in body.certifications]
    if body.achievements:
        resume.achievements = body.achievements
    await resume.insert()
    return {"success": True, "resume": resume.model_dump(), "resume_id": str(resume.id)}


@router.put("/{resume_id}")
async def update_resume(resume_id: str, body: CreateResumeRequest, current_user: User = Depends(get_current_user)):
    resume = await Resume.get(resume_id)
    if not resume or resume.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Resume not found")
    update_data = body.model_dump(exclude_none=True)
    for k, v in update_data.items():
        setattr(resume, k, v)
    resume.updated_at = datetime.utcnow()
    await resume.save()
    return {"success": True, "resume": resume.model_dump()}


@router.delete("/{resume_id}")
async def delete_resume(resume_id: str, current_user: User = Depends(get_current_user)):
    resume = await Resume.get(resume_id)
    if not resume or resume.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Resume not found")
    await resume.delete()
    return {"success": True, "message": "Resume deleted"}


@router.get("/analyses/latest")
async def get_latest_analysis(current_user: User = Depends(get_current_user)):
    analysis = await ResumeAnalysis.find(
        ResumeAnalysis.user_id == current_user.id
    ).sort(-ResumeAnalysis.created_at).first_or_none()
    if not analysis:
        return {"success": True, "analysis": None}
    return {"success": True, "analysis": analysis.model_dump()}
