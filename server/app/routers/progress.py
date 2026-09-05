from fastapi import APIRouter, Depends
from app.models.progress import Progress
from app.models.user import User
from app.models.coding import Submission
from app.middleware.auth import get_current_user

router = APIRouter(prefix="/api/progress", tags=["progress"])


@router.get("/")
async def get_progress(current_user: User = Depends(get_current_user)):
    progress = await Progress.find_one(Progress.user_id == current_user.id)
    if not progress:
        progress = Progress(user_id=current_user.id)
        await progress.insert()

    progress.placement_readiness_score = progress.calculate_placement_readiness()
    await progress.save()

    return {
        "success": True,
        "progress": progress.model_dump(),
        "user": {
            "xp": current_user.xp,
            "level": current_user.level,
            "streak": current_user.streak,
            "badges": current_user.badges,
        },
        "placement_readiness": {
            "score": progress.placement_readiness_score,
            "breakdown": {
                "resume": progress.resume.current_score,
                "coding": min(100, int(progress.coding.problems_solved / 1.5)),
                "aptitude": int(progress.aptitude.accuracy),
                "interview": int(progress.interview.average_score),
                "roadmap": int(progress.roadmap.completion_percentage),
                "streak": min(100, progress.coding.streak * 3),
            },
        },
    }


@router.get("/dashboard")
async def get_dashboard(current_user: User = Depends(get_current_user)):
    progress = await Progress.find_one(Progress.user_id == current_user.id)
    if not progress:
        progress = Progress(user_id=current_user.id)
        await progress.insert()

    recent_submissions = await Submission.find(
        Submission.user_id == current_user.id
    ).sort(-Submission.created_at).limit(5).to_list()

    from app.models.roadmap import Roadmap
    active_roadmap = await Roadmap.find_one(
        Roadmap.user_id == current_user.id, Roadmap.is_active == True
    )
    todays_tasks = []
    if active_roadmap:
        todays_tasks = [
            {"id": t.id, "title": t.title, "type": t.type,
             "estimated_time": t.estimated_time, "completed": t.completed, "priority": t.priority}
            for t in (active_roadmap.todays_tasks or [])
        ]

    from app.models.interview import Interview
    recent_interviews = await Interview.find(
        Interview.user_id == current_user.id, Interview.status == "completed"
    ).sort(-Interview.completed_at).limit(3).to_list()

    weekly_data = await _generate_weekly_chart(current_user.id, progress)

    return {
        "success": True,
        "user": {
            "name": current_user.name,
            "xp": current_user.xp,
            "level": current_user.level,
            "streak": current_user.streak,
        },
        "summary": {
            "placement_readiness": progress.calculate_placement_readiness(),
            "resume_score": progress.resume.current_score,
            "problems_solved": progress.coding.problems_solved,
            "aptitude_accuracy": progress.aptitude.accuracy,
            "interview_score": progress.interview.average_score,
            "roadmap_completion": progress.roadmap.completion_percentage,
        },
        "todays_tasks": todays_tasks,
        "recent_submissions": [
            {"language": s.language, "status": s.status, "created_at": s.created_at.isoformat()}
            for s in recent_submissions
        ],
        "recent_interviews": [
            {"type": i.type, "score": i.overall_scores.overall, "completed_at": i.completed_at.isoformat() if i.completed_at else None}
            for i in recent_interviews
        ],
        "weekly_chart": weekly_data,
        "coding_stats": {
            "easy": progress.coding.easy_solved,
            "medium": progress.coding.medium_solved,
            "hard": progress.coding.hard_solved,
            "total": progress.coding.problems_solved,
            "streak": progress.coding.streak,
            "topic_wise": progress.coding.topic_wise,
        },
        "aptitude_stats": {
            "total": progress.aptitude.total_attempted,
            "correct": progress.aptitude.total_correct,
            "accuracy": progress.aptitude.accuracy,
            "by_category": {
                "quantitative": progress.aptitude.quantitative.model_dump(),
                "logical": progress.aptitude.logical.model_dump(),
                "verbal": progress.aptitude.verbal.model_dump(),
            },
        },
    }


async def _generate_weekly_chart(user_id, progress: Progress) -> list:
    from datetime import datetime, timedelta, timezone
    from app.models.coding import Submission

    today = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    week_start = today - timedelta(days=6)

    submissions = await Submission.find(
        Submission.user_id == user_id,
        Submission.created_at >= week_start,
        Submission.status == "accepted",
    ).to_list()

    coding_by_day: dict = {}
    for sub in submissions:
        day_key = sub.created_at.strftime("%Y-%m-%d")
        coding_by_day[day_key] = coding_by_day.get(day_key, 0) + 1

    data = []
    for i in range(7):
        day = today + timedelta(days=i - 6)
        day_key = day.strftime("%Y-%m-%d")
        data.append({
            "day": day.strftime("%a"),
            "date": day_key,
            "coding": coding_by_day.get(day_key, 0),
            "aptitude": 0,
        })
    return data
