from fastapi import APIRouter, HTTPException, Depends, Query
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from app.models.aptitude import AptitudeQuestion, AptitudeAttempt
from app.models.progress import Progress
from app.models.user import User
from app.middleware.auth import get_current_user

router = APIRouter(prefix="/api/aptitude", tags=["aptitude"])


@router.get("/questions")
async def get_questions(
    category: Optional[str] = None,
    difficulty: Optional[str] = None,
    subcategory: Optional[str] = None,
    limit: int = Query(20, ge=1, le=50),
    current_user: User = Depends(get_current_user),
):
    filters = [AptitudeQuestion.is_active == True]
    if category:
        filters.append(AptitudeQuestion.category == category)
    if difficulty:
        filters.append(AptitudeQuestion.difficulty == difficulty)
    if subcategory:
        filters.append(AptitudeQuestion.subcategory == subcategory)

    from beanie.operators import In
    questions = await AptitudeQuestion.find(*filters).limit(limit).to_list()

    return {"success": True, "questions": [
        {
            "id": str(q.id), "question": q.question,
            "options": [{"text": o.text} for o in q.options],
            "category": q.category, "subcategory": q.subcategory,
            "difficulty": q.difficulty, "time_limit_seconds": q.time_limit_seconds,
            "xp_reward": q.xp_reward,
        }
        for q in questions
    ], "total": len(questions)}


@router.get("/categories")
async def get_categories():
    return {
        "success": True,
        "categories": [
            {
                "id": "quantitative",
                "name": "Quantitative Aptitude",
                "icon": "Calculator",
                "subcategories": ["Percentages", "Profit & Loss", "Time & Work", "Time Speed Distance",
                                  "Ratios", "Averages", "Probability", "Permutations", "Number Systems",
                                  "Simple Interest", "Compound Interest"],
            },
            {
                "id": "logical",
                "name": "Logical Reasoning",
                "icon": "Brain",
                "subcategories": ["Number Series", "Coding-Decoding", "Blood Relations", "Directions",
                                  "Seating Arrangement", "Syllogisms", "Puzzles"],
            },
            {
                "id": "verbal",
                "name": "Verbal Ability",
                "icon": "BookOpen",
                "subcategories": ["Grammar", "Vocabulary", "Reading Comprehension",
                                  "Sentence Correction", "Para Jumbles"],
            },
        ],
    }


class SubmitAnswerRequest(BaseModel):
    question_id: str
    selected_option: int
    time_taken_seconds: int = 0


@router.post("/submit")
async def submit_answer(body: SubmitAnswerRequest, current_user: User = Depends(get_current_user)):
    question = await AptitudeQuestion.get(body.question_id)
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    is_correct = body.selected_option == question.correct_answer

    attempt = AptitudeAttempt(
        user_id=current_user.id,
        question_id=question.id,
        selected_option=body.selected_option,
        is_correct=is_correct,
        time_taken_seconds=body.time_taken_seconds,
        category=question.category,
    )
    await attempt.insert()

    xp_earned = question.xp_reward if is_correct else 0
    if xp_earned:
        current_user.xp += xp_earned
        current_user.level = current_user.calculate_level()
        await current_user.save()

    progress = await Progress.find_one(Progress.user_id == current_user.id)
    if progress:
        cat = question.category
        progress.aptitude.total_attempted += 1
        if is_correct:
            progress.aptitude.total_correct += 1
            progress.aptitude.total_xp += xp_earned

        cat_prog = getattr(progress.aptitude, cat, None)
        if cat_prog is not None:
            cat_prog.attempted += 1
            if is_correct:
                cat_prog.correct += 1

        if progress.aptitude.total_attempted > 0:
            progress.aptitude.accuracy = round(
                progress.aptitude.total_correct / progress.aptitude.total_attempted * 100, 1
            )
        progress.placement_readiness_score = progress.calculate_placement_readiness()
        await progress.save()

    return {
        "success": True,
        "is_correct": is_correct,
        "correct_answer": question.correct_answer,
        "explanation": question.explanation,
        "xp_earned": xp_earned,
    }


class BatchSubmitRequest(BaseModel):
    answers: List[SubmitAnswerRequest]


@router.post("/submit-batch")
async def submit_batch(body: BatchSubmitRequest, current_user: User = Depends(get_current_user)):
    results = []
    for answer in body.answers:
        question = await AptitudeQuestion.get(answer.question_id)
        if not question:
            continue
        is_correct = answer.selected_option == question.correct_answer
        results.append({
            "question_id": answer.question_id,
            "is_correct": is_correct,
            "correct_answer": question.correct_answer,
            "explanation": question.explanation,
        })

        attempt = AptitudeAttempt(
            user_id=current_user.id,
            question_id=question.id,
            selected_option=answer.selected_option,
            is_correct=is_correct,
            time_taken_seconds=answer.time_taken_seconds,
            category=question.category,
        )
        await attempt.insert()

    correct = sum(1 for r in results if r["is_correct"])
    xp_earned = correct * 5
    if xp_earned:
        current_user.xp += xp_earned
        await current_user.save()

    return {
        "success": True, "results": results,
        "score": correct, "total": len(results),
        "percentage": round(correct / len(results) * 100) if results else 0,
        "xp_earned": xp_earned,
    }


@router.get("/stats")
async def get_stats(current_user: User = Depends(get_current_user)):
    progress = await Progress.find_one(Progress.user_id == current_user.id)
    if not progress:
        return {"success": True, "stats": {}}
    return {"success": True, "stats": progress.aptitude.model_dump()}
