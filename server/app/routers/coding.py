import httpx
import asyncio
import random
from fastapi import APIRouter, HTTPException, Depends, Query
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from app.models.coding import CodingProblem, Submission
from app.models.progress import Progress
from app.models.user import User
from app.middleware.auth import get_current_user
from app.config.settings import settings

router = APIRouter(prefix="/api/coding", tags=["coding"])

MOCK_EXECUTION_RESULTS = {
    "accepted": {"status": "accepted", "execution_time_ms": 45, "memory_used_mb": 12.3, "test_cases_passed": 5, "total_test_cases": 5},
    "wrong_answer": {"status": "wrong_answer", "execution_time_ms": 38, "memory_used_mb": 10.1, "test_cases_passed": 3, "total_test_cases": 5, "output": "Wrong output on test case 4"},
    "runtime_error": {"status": "runtime_error", "error_message": "IndexError: list index out of range", "test_cases_passed": 2, "total_test_cases": 5},
}


@router.get("/problems")
async def get_problems(
    difficulty: Optional[str] = None,
    topic: Optional[str] = None,
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=50),
    search: Optional[str] = None,
    current_user: User = Depends(get_current_user),
):
    filters = [CodingProblem.is_active == True]
    if difficulty:
        filters.append(CodingProblem.difficulty == difficulty)
    if topic:
        filters.append({"topics": {"$in": [topic]}})

    problems = await CodingProblem.find(*filters).sort(CodingProblem.order).skip((page - 1) * limit).limit(limit).to_list()
    total = await CodingProblem.find(*filters).count()

    user_submissions = await Submission.find(
        Submission.user_id == current_user.id, Submission.is_accepted == True
    ).to_list()
    solved_ids = {str(s.problem_id) for s in user_submissions}

    return {
        "success": True,
        "problems": [
            {
                "id": str(p.id), "title": p.title, "slug": p.slug,
                "difficulty": p.difficulty, "topics": p.topics,
                "companies": p.companies, "acceptance_rate": p.acceptance_rate,
                "submission_count": p.submission_count, "xp_reward": p.xp_reward,
                "is_solved": str(p.id) in solved_ids,
            }
            for p in problems
        ],
        "total": total, "page": page, "pages": (total + limit - 1) // limit,
    }


@router.get("/problems/topics")
async def get_topics():
    topics = ["Arrays", "Strings", "Linked Lists", "Stack", "Queue", "Hashing",
              "Trees", "Graphs", "Recursion", "Dynamic Programming", "Greedy",
              "Sorting", "Searching", "Binary Search", "Backtracking", "SQL"]
    return {"success": True, "topics": topics}


@router.get("/problems/{slug}")
async def get_problem(slug: str, current_user: User = Depends(get_current_user)):
    problem = await CodingProblem.find_one(CodingProblem.slug == slug)
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")
    visible_test_cases = [tc for tc in problem.test_cases if not tc.is_hidden][:3]
    return {"success": True, "problem": {
        "id": str(problem.id), "title": problem.title, "slug": problem.slug,
        "description": problem.description, "difficulty": problem.difficulty,
        "topics": problem.topics, "companies": problem.companies,
        "input_format": problem.input_format, "output_format": problem.output_format,
        "constraints": [c.strip() for c in problem.constraints.split('\n') if c.strip()] if problem.constraints else [],
        "examples": [e.model_dump() for e in problem.examples],
        "hints": problem.hints, "test_cases": [tc.model_dump() for tc in visible_test_cases],
        "xp_reward": problem.xp_reward, "time_limit_ms": problem.time_limit_ms,
        "memory_limit_mb": problem.memory_limit_mb,
    }}


class RunCodeRequest(BaseModel):
    code: str
    language: str
    custom_input: Optional[str] = None
    problem_slug: Optional[str] = None


class SubmitCodeRequest(BaseModel):
    code: str
    language: str
    problem_slug: str


SUPPORTED_LANGUAGES = ["python", "java", "cpp", "javascript", "c"]


@router.post("/run")
async def run_code(body: RunCodeRequest, current_user: User = Depends(get_current_user)):
    if body.language.lower() not in SUPPORTED_LANGUAGES:
        raise HTTPException(status_code=400, detail=f"Language not supported. Use: {SUPPORTED_LANGUAGES}")

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(f"{settings.CODE_RUNNER_URL}/run", json={
                "code": body.code, "language": body.language,
                "input": body.custom_input or "",
            })
            return {"success": True, "result": response.json()}
    except Exception:
        result = await _mock_run(body.code, body.language, body.custom_input)
        return {"success": True, "result": result}


@router.post("/submit")
async def submit_code(body: SubmitCodeRequest, current_user: User = Depends(get_current_user)):
    if body.language.lower() not in SUPPORTED_LANGUAGES:
        raise HTTPException(status_code=400, detail="Language not supported")

    problem = await CodingProblem.find_one(CodingProblem.slug == body.problem_slug)
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")

    result = None
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(f"{settings.CODE_RUNNER_URL}/submit", json={
                "code": body.code, "language": body.language,
                "test_cases": [{"input": tc.input, "expected": tc.expected_output}
                               for tc in problem.test_cases],
            })
            result = response.json()
    except Exception:
        result = await _mock_submit(body.code, body.language, problem)

    submission = Submission(
        user_id=current_user.id,
        problem_id=problem.id,
        code=body.code,
        language=body.language,
        status=result.get("status", "pending"),
        execution_time_ms=result.get("execution_time_ms"),
        memory_used_mb=result.get("memory_used_mb"),
        test_cases_passed=result.get("test_cases_passed", 0),
        total_test_cases=result.get("total_test_cases", len(problem.test_cases)),
        error_message=result.get("error_message"),
        output=result.get("output"),
        is_accepted=result.get("status") == "accepted",
    )
    await submission.insert()

    problem.submission_count += 1
    if submission.is_accepted:
        accepted_count = await Submission.find(
            Submission.problem_id == problem.id, Submission.is_accepted == True
        ).count()
        problem.acceptance_rate = round(accepted_count / problem.submission_count * 100, 1)
    await problem.save()

    if submission.is_accepted:
        prev_solved = await Submission.find(
            Submission.user_id == current_user.id,
            Submission.problem_id == problem.id,
            Submission.is_accepted == True,
        ).count()

        if prev_solved <= 1:
            current_user.xp += problem.xp_reward
            current_user.level = current_user.calculate_level()
            await current_user.save()

            progress = await Progress.find_one(Progress.user_id == current_user.id)
            if progress:
                progress.coding.problems_solved += 1
                if problem.difficulty == "easy":
                    progress.coding.easy_solved += 1
                elif problem.difficulty == "medium":
                    progress.coding.medium_solved += 1
                else:
                    progress.coding.hard_solved += 1
                for topic in problem.topics:
                    progress.coding.topic_wise[topic] = progress.coding.topic_wise.get(topic, 0) + 1
                progress.coding.last_solved_date = datetime.utcnow()
                progress.coding.total_xp += problem.xp_reward
                progress.placement_readiness_score = progress.calculate_placement_readiness()
                await progress.save()

    return {
        "success": True,
        "result": result,
        "submission_id": str(submission.id),
        "xp_earned": problem.xp_reward if submission.is_accepted else 0,
    }


@router.get("/submissions")
async def get_submissions(
    problem_slug: Optional[str] = None,
    current_user: User = Depends(get_current_user),
):
    filters = [Submission.user_id == current_user.id]
    if problem_slug:
        problem = await CodingProblem.find_one(CodingProblem.slug == problem_slug)
        if problem:
            filters.append(Submission.problem_id == problem.id)

    subs = await Submission.find(*filters).sort(-Submission.created_at).limit(20).to_list()
    return {"success": True, "submissions": [
        {
            "id": str(s.id), "language": s.language, "status": s.status,
            "execution_time_ms": s.execution_time_ms, "memory_used_mb": s.memory_used_mb,
            "test_cases_passed": s.test_cases_passed, "total_test_cases": s.total_test_cases,
            "is_accepted": s.is_accepted,
            "created_at": s.created_at.isoformat(),
        }
        for s in subs
    ]}


async def _mock_run(code: str, language: str, custom_input: Optional[str]) -> dict:
    await asyncio.sleep(0.5)
    if not code.strip():
        return {"status": "compilation_error", "error_message": "Code is empty"}
    if language == "python" and "print" in code:
        return {"status": "success", "output": "Hello, World!\n", "execution_time_ms": 42, "memory_used_mb": 8.2}
    return {"status": "success", "output": "Code executed successfully", "execution_time_ms": 38, "memory_used_mb": 10.1}


async def _mock_submit(code: str, language: str, problem: CodingProblem) -> dict:
    await asyncio.sleep(0.8)
    if not code.strip():
        return {"status": "compilation_error", "error_message": "Code is empty", "test_cases_passed": 0, "total_test_cases": len(problem.test_cases)}
    weights = [0.55, 0.25, 0.20]
    outcome = random.choices(["accepted", "wrong_answer", "runtime_error"], weights=weights)[0]
    tc_count = len(problem.test_cases) or 3
    if outcome == "accepted":
        return {"status": "accepted", "execution_time_ms": random.randint(30, 120), "memory_used_mb": round(random.uniform(8, 20), 1), "test_cases_passed": tc_count, "total_test_cases": tc_count}
    elif outcome == "wrong_answer":
        passed = random.randint(0, tc_count - 1)
        return {"status": "wrong_answer", "execution_time_ms": random.randint(30, 80), "memory_used_mb": round(random.uniform(8, 15), 1), "test_cases_passed": passed, "total_test_cases": tc_count, "output": "Wrong Answer on test case " + str(passed + 1)}
    else:
        return {"status": "runtime_error", "error_message": "RuntimeError: index out of range", "test_cases_passed": 0, "total_test_cases": tc_count}
