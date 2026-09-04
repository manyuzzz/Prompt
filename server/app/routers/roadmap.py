from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from app.models.roadmap import Roadmap, RoadmapTask, StudentProfile
from app.models.progress import Progress
from app.models.user import User
from app.middleware.auth import get_current_user
from app.services.ai.roadmap_service import roadmap_ai_service

router = APIRouter(prefix="/api/roadmaps", tags=["roadmaps"])


class GenerateRoadmapRequest(BaseModel):
    target_company: Optional[str] = None
    target_role: Optional[str] = None
    current_year: Optional[str] = "3rd Year"
    degree: Optional[str] = "B.Tech"
    branch: Optional[str] = "Computer Science"
    cgpa: Optional[float] = 7.0
    current_skills: Optional[List[str]] = []
    programming_language: Optional[str] = "Python"
    dsa_level: Optional[str] = "beginner"
    aptitude_level: Optional[str] = "beginner"
    communication_level: Optional[str] = "average"
    available_hours_per_day: Optional[int] = 2
    has_projects: Optional[bool] = False
    has_internship: Optional[bool] = False
    has_previous_interviews: Optional[bool] = False


@router.get("/")
async def get_roadmaps(current_user: User = Depends(get_current_user)):
    roadmaps = await Roadmap.find(
        Roadmap.user_id == current_user.id
    ).sort(-Roadmap.created_at).to_list()
    return {"success": True, "roadmaps": [
        {
            "id": str(r.id), "title": r.title,
            "target_company": r.target_company, "target_role": r.target_role,
            "completion_percentage": r.completion_percentage,
            "duration": r.duration, "is_active": r.is_active,
            "start_date": r.start_date.isoformat(),
            "phases_count": len(r.phases),
        }
        for r in roadmaps
    ]}


@router.get("/active")
async def get_active_roadmap(current_user: User = Depends(get_current_user)):
    roadmap = await Roadmap.find_one(
        Roadmap.user_id == current_user.id,
        Roadmap.is_active == True
    )
    if not roadmap:
        return {"success": True, "roadmap": None}
    return {"success": True, "roadmap": roadmap.model_dump()}


@router.get("/{roadmap_id}")
async def get_roadmap(roadmap_id: str, current_user: User = Depends(get_current_user)):
    roadmap = await Roadmap.get(roadmap_id)
    if not roadmap or roadmap.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Roadmap not found")
    return {"success": True, "roadmap": roadmap.model_dump()}


@router.post("/generate")
async def generate_roadmap(body: GenerateRoadmapRequest, current_user: User = Depends(get_current_user)):
    profile = StudentProfile(
        current_year=body.current_year,
        degree=body.degree,
        branch=body.branch,
        cgpa=body.cgpa,
        current_skills=body.current_skills or [],
        programming_language=body.programming_language,
        dsa_level=body.dsa_level,
        aptitude_level=body.aptitude_level,
        communication_level=body.communication_level,
        available_hours_per_day=body.available_hours_per_day,
        has_projects=body.has_projects,
        has_internship=body.has_internship,
        has_previous_interviews=body.has_previous_interviews,
    )

    data = await roadmap_ai_service.generate(profile, body.target_company, body.target_role)

    await Roadmap.find(
        Roadmap.user_id == current_user.id,
        Roadmap.is_active == True
    ).update({"$set": {"is_active": False}})

    from app.models.roadmap import RoadmapPhase, RoadmapWeek
    phases = []
    for ph in data.get("phases", []):
        weeks = []
        for wk in ph.get("weeks", []):
            tasks = [RoadmapTask(**t) for t in wk.get("tasks", [])]
            weeks.append(RoadmapWeek(**{**wk, "tasks": tasks}))
        phases.append(RoadmapPhase(**{**ph, "weeks": weeks}))

    todays_tasks = [RoadmapTask(**t) for t in data.get("todays_tasks", [])]

    from datetime import timedelta
    end_date = datetime.utcnow() + timedelta(weeks=data.get("duration", 12))
    roadmap = Roadmap(
        user_id=current_user.id,
        title=data.get("title", f"{body.target_company or 'General'} Preparation Roadmap"),
        target_company=body.target_company,
        target_role=body.target_role,
        duration=data.get("duration", 12),
        student_profile=profile,
        phases=phases,
        todays_tasks=todays_tasks,
        estimated_end_date=end_date,
    )
    await roadmap.insert()

    progress = await Progress.find_one(Progress.user_id == current_user.id)
    if progress:
        progress.roadmap.active_roadmap_id = roadmap.id
        progress.roadmap.completion_percentage = 0
        await progress.save()

    return {"success": True, "roadmap": roadmap.model_dump(), "roadmap_id": str(roadmap.id)}


@router.patch("/{roadmap_id}/tasks/{task_id}")
async def complete_task(
    roadmap_id: str, task_id: str,
    completed: bool = True,
    current_user: User = Depends(get_current_user)
):
    roadmap = await Roadmap.get(roadmap_id)
    if not roadmap or roadmap.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Roadmap not found")

    task_found = False
    xp_earned = 0
    for phase in roadmap.phases:
        for week in phase.weeks:
            for task in week.tasks:
                if task.id == task_id:
                    task.completed = completed
                    task.completed_at = datetime.utcnow() if completed else None
                    xp_earned = task.xp_reward if completed else 0
                    task_found = True
                    break

    for task in roadmap.todays_tasks:
        if task.id == task_id:
            task.completed = completed
            task.completed_at = datetime.utcnow() if completed else None
            if not task_found:
                xp_earned = task.xp_reward if completed else 0
            task_found = True

    if not task_found:
        raise HTTPException(status_code=404, detail="Task not found")

    roadmap.completion_percentage = roadmap.calculate_completion()
    roadmap.updated_at = datetime.utcnow()
    await roadmap.save()

    if xp_earned and completed:
        current_user.xp += xp_earned
        current_user.level = current_user.calculate_level()
        await current_user.save()

    progress = await Progress.find_one(Progress.user_id == current_user.id)
    if progress:
        progress.roadmap.completion_percentage = roadmap.completion_percentage
        await progress.save()

    return {"success": True, "completion_percentage": roadmap.completion_percentage, "xp_earned": xp_earned}
