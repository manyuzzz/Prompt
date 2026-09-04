from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from app.models.interview import Interview, QuestionResponse, QuestionScores, InterviewSettings
from app.models.progress import Progress
from app.models.user import User
from app.middleware.auth import get_current_user
from app.services.ai.interview_service import interview_ai_service

router = APIRouter(prefix="/api/interviews", tags=["interviews"])


class StartInterviewRequest(BaseModel):
    type: str  # hr | technical | behavioral | company-specific
    target_company: Optional[str] = None
    target_role: Optional[str] = None
    difficulty: str = "medium"
    number_of_questions: int = 8
    enable_speech: bool = True


class SubmitAnswerRequest(BaseModel):
    interview_id: str
    question_id: str
    answer: str
    duration: Optional[int] = None


class EndInterviewRequest(BaseModel):
    interview_id: str


@router.get("/")
async def get_interviews(current_user: User = Depends(get_current_user)):
    interviews = await Interview.find(
        Interview.user_id == current_user.id
    ).sort(-Interview.created_at).limit(20).to_list()
    return {"success": True, "interviews": [
        {
            "id": str(i.id), "type": i.type, "status": i.status,
            "target_company": i.target_company, "target_role": i.target_role,
            "overall_score": i.overall_scores.overall,
            "questions_count": len(i.questions),
            "created_at": i.created_at.isoformat(),
            "completed_at": i.completed_at.isoformat() if i.completed_at else None,
        }
        for i in interviews
    ]}


@router.post("/start")
async def start_interview(body: StartInterviewRequest, current_user: User = Depends(get_current_user)):
    questions_list = interview_ai_service.get_questions(
        body.type, body.target_company, body.number_of_questions
    )

    question_responses = [
        QuestionResponse(question=q, question_type=body.type)
        for q in questions_list
    ]

    interview = Interview(
        user_id=current_user.id,
        type=body.type,
        target_company=body.target_company,
        target_role=body.target_role,
        status="ongoing",
        questions=question_responses,
        started_at=datetime.utcnow(),
        settings=InterviewSettings(
            difficulty=body.difficulty,
            number_of_questions=body.number_of_questions,
            enable_speech=body.enable_speech,
        ),
    )
    await interview.insert()

    return {
        "success": True,
        "interview_id": str(interview.id),
        "first_question": {
            "id": question_responses[0].id,
            "question": question_responses[0].question,
            "question_number": 1,
            "total_questions": len(question_responses),
        },
    }


@router.post("/respond")
async def submit_answer(body: SubmitAnswerRequest, current_user: User = Depends(get_current_user)):
    interview = await Interview.get(body.interview_id)
    if not interview or interview.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Interview not found")
    if interview.status != "ongoing":
        raise HTTPException(status_code=400, detail="Interview is not active")

    question = next((q for q in interview.questions if q.id == body.question_id), None)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    evaluation = await interview_ai_service.evaluate_answer(
        question.question, body.answer, interview.type
    )

    question.user_answer = body.answer
    question.duration = body.duration
    question.word_count = len(body.answer.split())
    filler_words = ["um", "uh", "like", "you know", "basically", "actually"]
    question.filler_word_count = sum(body.answer.lower().count(f) for f in filler_words)

    scores = evaluation.get("scores", {})
    question.scores = QuestionScores(**scores)
    question.feedback = evaluation.get("feedback", "")
    question.follow_up_question = evaluation.get("follow_up", "")
    interview.updated_at = datetime.utcnow()

    answered = [q for q in interview.questions if q.user_answer]
    current_idx = next((i for i, q in enumerate(interview.questions) if q.id == body.question_id), 0)
    next_idx = current_idx + 1

    if next_idx < len(interview.questions):
        next_q = interview.questions[next_idx]
        next_question = {
            "id": next_q.id,
            "question": next_q.question,
            "question_number": next_idx + 1,
            "total_questions": len(interview.questions),
        }
        if evaluation.get("follow_up"):
            next_question["follow_up"] = evaluation["follow_up"]
    else:
        next_question = None

    await interview.save()

    return {
        "success": True,
        "evaluation": {
            "feedback": evaluation.get("feedback"),
            "scores": scores,
            "strengths": evaluation.get("strengths", []),
            "improvements": evaluation.get("improvements", []),
        },
        "next_question": next_question,
        "progress": {"answered": len(answered) + 1, "total": len(interview.questions)},
    }


@router.post("/end")
async def end_interview(body: EndInterviewRequest, current_user: User = Depends(get_current_user)):
    interview = await Interview.get(body.interview_id)
    if not interview or interview.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Interview not found")

    answered = [q for q in interview.questions if q.user_answer]
    questions_data = [
        {"scores": q.scores.model_dump(), "question": q.question, "answer": q.user_answer}
        for q in answered if q.user_answer
    ]

    report = await interview_ai_service.generate_report(questions_data, interview.type)

    from app.models.interview import OverallScores, InterviewFeedback
    interview.status = "completed"
    interview.completed_at = datetime.utcnow()
    interview.overall_scores = OverallScores(**report.get("overall_scores", {}))
    interview.feedback = InterviewFeedback(
        strengths=report.get("strengths", []),
        areas_to_improve=report.get("areas_to_improve", []),
        recommended_practice=report.get("recommended_practice", []),
        summary=report.get("summary", ""),
    )
    if interview.started_at:
        interview.duration = int((interview.completed_at - interview.started_at).total_seconds())
    await interview.save()

    score = interview.overall_scores.overall
    xp_earned = int(score / 2)
    current_user.xp += xp_earned
    current_user.level = current_user.calculate_level()
    await current_user.save()

    progress = await Progress.find_one(Progress.user_id == current_user.id)
    if progress:
        progress.interview.total_interviews += 1
        all_scores = [score, progress.interview.average_score * (progress.interview.total_interviews - 1)]
        progress.interview.average_score = round(sum(all_scores) / progress.interview.total_interviews, 1)
        if score > progress.interview.best_score:
            progress.interview.best_score = score
        progress.interview.last_interview_date = datetime.utcnow()
        progress.interview.total_xp += xp_earned
        progress.placement_readiness_score = progress.calculate_placement_readiness()
        await progress.save()

    return {
        "success": True,
        "report": report,
        "xp_earned": xp_earned,
        "interview_id": str(interview.id),
    }


@router.get("/{interview_id}")
async def get_interview(interview_id: str, current_user: User = Depends(get_current_user)):
    interview = await Interview.get(interview_id)
    if not interview or interview.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Interview not found")
    return {"success": True, "interview": interview.model_dump()}
