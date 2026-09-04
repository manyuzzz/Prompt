import json
import re
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from app.services.ai.ai_service import ai_service
from app.models.roadmap import RoadmapPhase, RoadmapWeek, RoadmapTask, RoadmapResource, StudentProfile


class RoadmapAIService:
    async def generate(self, profile: StudentProfile, company: Optional[str], role: Optional[str]) -> Dict[str, Any]:
        if ai_service.provider == "mock":
            return self._mock_roadmap(profile, company, role)

        prompt = self._build_prompt(profile, company, role)
        try:
            response = await ai_service.chat(
                [{"role": "user", "content": prompt}],
                system_prompt="""You are an expert placement strategist. Generate a detailed, personalized placement preparation roadmap as JSON.""",
                temperature=0.5,
                max_tokens=4000,
            )
            m = re.search(r'\{[\s\S]*\}', response)
            if m:
                return json.loads(m.group())
        except Exception:
            pass
        return self._mock_roadmap(profile, company, role)

    def _build_prompt(self, profile: StudentProfile, company: Optional[str], role: Optional[str]) -> str:
        return f"""Generate a placement preparation roadmap for:
Company: {company or 'General placements'}
Role: {role or 'Software Developer'}
Student: Year {profile.current_year}, {profile.branch}, CGPA {profile.cgpa}
DSA Level: {profile.dsa_level}, Aptitude: {profile.aptitude_level}
Skills: {', '.join(profile.current_skills) if profile.current_skills else 'Basic programming'}
Available: {profile.available_hours_per_day} hours/day

Return a JSON roadmap with phases, weeks, and daily tasks."""

    def _mock_roadmap(self, profile: StudentProfile, company: Optional[str], role: Optional[str]) -> Dict[str, Any]:
        dsa_weeks = self._get_dsa_weeks(profile.dsa_level)
        company_name = company or "General"
        role_name = role or "Software Developer"
        duration = 12

        phases = [
            {
                "phase_number": 1,
                "title": "Foundation",
                "description": "Build strong fundamentals in programming and core CS subjects",
                "weeks": [
                    {
                        "week_number": 1,
                        "title": "Programming & Aptitude Basics",
                        "theme": "Foundation Building",
                        "goals": ["Master programming basics", "Start aptitude preparation", "Set up coding environment"],
                        "topics": ["Python/Java basics", "OOP fundamentals", "Percentages", "Ratios", "Number Systems"],
                        "tasks": [
                            {"title": "Practice 10 Array problems (Easy)", "type": "coding", "estimated_time": "1.5 hours", "xp_reward": 50, "priority": "high"},
                            {"title": "Solve 20 Quantitative Aptitude questions", "type": "aptitude", "estimated_time": "45 mins", "xp_reward": 20, "priority": "high"},
                            {"title": "Study OOP concepts (Inheritance, Polymorphism)", "type": "reading", "estimated_time": "1 hour", "xp_reward": 15, "priority": "high"},
                            {"title": "Create/update GitHub profile", "type": "project", "estimated_time": "30 mins", "xp_reward": 10, "priority": "medium"},
                            {"title": "Review 5 HR Questions", "type": "interview", "estimated_time": "30 mins", "xp_reward": 10, "priority": "medium"},
                        ],
                    },
                    {
                        "week_number": 2,
                        "title": "Strings, Arrays & Verbal",
                        "theme": "Core Programming",
                        "goals": ["Master string manipulation", "Learn sorting algorithms", "Improve verbal ability"],
                        "topics": ["String operations", "Sorting algorithms", "Verbal Ability", "Sentence Correction"],
                        "tasks": [
                            {"title": "Solve 15 String problems", "type": "coding", "estimated_time": "2 hours", "xp_reward": 60, "priority": "high"},
                            {"title": "Learn Bubble, Selection, Insertion, Merge Sort", "type": "reading", "estimated_time": "1 hour", "xp_reward": 20, "priority": "high"},
                            {"title": "Complete 20 Verbal ability questions", "type": "aptitude", "estimated_time": "45 mins", "xp_reward": 20, "priority": "medium"},
                            {"title": "Write and memorize 'Tell me about yourself'", "type": "interview", "estimated_time": "30 mins", "xp_reward": 15, "priority": "high"},
                        ],
                    },
                ],
            },
            {
                "phase_number": 2,
                "title": "DSA Mastery",
                "description": "Deep dive into data structures and algorithms",
                "weeks": [
                    {
                        "week_number": 3,
                        "title": "Linked Lists, Stack & Queue",
                        "theme": "Linear Data Structures",
                        "goals": ["Implement linked list operations", "Understand stack/queue applications", "Solve medium problems"],
                        "topics": ["Singly/Doubly Linked Lists", "Stack", "Queue", "Deque", "Priority Queue"],
                        "tasks": [
                            {"title": "Implement Linked List from scratch", "type": "coding", "estimated_time": "1.5 hours", "xp_reward": 40, "priority": "high"},
                            {"title": "Solve 10 Stack/Queue problems", "type": "coding", "estimated_time": "2 hours", "xp_reward": 60, "priority": "high"},
                            {"title": "Practice Logical Reasoning - Blood Relations", "type": "aptitude", "estimated_time": "45 mins", "xp_reward": 20, "priority": "medium"},
                            {"title": "Study SQL JOINs (INNER, LEFT, RIGHT)", "type": "reading", "estimated_time": "1 hour", "xp_reward": 20, "priority": "high"},
                        ],
                    },
                    {
                        "week_number": 4,
                        "title": "Trees & Binary Search",
                        "theme": "Non-linear Structures",
                        "goals": ["Master tree traversals", "Understand BST operations", "Apply binary search"],
                        "topics": ["Binary Trees", "BST", "Tree Traversals", "Binary Search"],
                        "tasks": [
                            {"title": "Solve 15 Tree problems", "type": "coding", "estimated_time": "2.5 hours", "xp_reward": 70, "priority": "high"},
                            {"title": "Practice 10 Binary Search variations", "type": "coding", "estimated_time": "1.5 hours", "xp_reward": 50, "priority": "high"},
                            {"title": "Study Normalization (1NF, 2NF, 3NF)", "type": "reading", "estimated_time": "1 hour", "xp_reward": 20, "priority": "high"},
                            {"title": "Mock aptitude test (30 questions, timed)", "type": "aptitude", "estimated_time": "45 mins", "xp_reward": 30, "priority": "medium"},
                        ],
                    },
                ],
            },
            {
                "phase_number": 3,
                "title": "Core CS Subjects",
                "description": "Master DBMS, OS, Computer Networks, and OOP",
                "weeks": [
                    {
                        "week_number": 5,
                        "title": "DBMS & SQL Deep Dive",
                        "theme": "Database Mastery",
                        "goals": ["Master SQL queries", "Understand normalization", "Practice DB design"],
                        "topics": ["SQL Queries", "Joins", "Transactions", "Indexes", "ACID Properties"],
                        "tasks": [
                            {"title": "Practice 20 SQL query problems", "type": "coding", "estimated_time": "2 hours", "xp_reward": 60, "priority": "high"},
                            {"title": "Study DBMS theory (ER Diagrams, Normalization)", "type": "reading", "estimated_time": "1.5 hours", "xp_reward": 25, "priority": "high"},
                            {"title": "Solve 25 Quantitative Aptitude problems", "type": "aptitude", "estimated_time": "1 hour", "xp_reward": 25, "priority": "medium"},
                            {"title": "Prepare answers for 5 technical interview questions", "type": "interview", "estimated_time": "1 hour", "xp_reward": 25, "priority": "high"},
                        ],
                    },
                    {
                        "week_number": 6,
                        "title": "OS & Computer Networks",
                        "theme": "Systems Knowledge",
                        "goals": ["Understand process management", "Learn networking basics", "Master OS concepts"],
                        "topics": ["Process/Thread", "Memory Management", "File Systems", "TCP/IP", "HTTP", "DNS"],
                        "tasks": [
                            {"title": "Study OS: Process, Thread, Scheduling", "type": "reading", "estimated_time": "2 hours", "xp_reward": 30, "priority": "high"},
                            {"title": "Study CN: OSI, TCP/IP, HTTP, DNS", "type": "reading", "estimated_time": "2 hours", "xp_reward": 30, "priority": "high"},
                            {"title": "Practice 15 mixed coding problems", "type": "coding", "estimated_time": "2 hours", "xp_reward": 60, "priority": "high"},
                            {"title": "Complete full aptitude mock test", "type": "aptitude", "estimated_time": "1 hour", "xp_reward": 40, "priority": "medium"},
                        ],
                    },
                ],
            },
            {
                "phase_number": 4,
                "title": "Coding Practice Sprint",
                "description": f"Intense coding practice with {company_name}-style problems",
                "weeks": [
                    {
                        "week_number": 7,
                        "title": "Medium Coding Problems",
                        "theme": "Problem Solving",
                        "goals": ["Solve 30+ medium problems", "Master DP basics", "Practice under time constraints"],
                        "topics": ["Dynamic Programming", "Graphs", "Greedy", "Recursion"],
                        "tasks": [
                            {"title": "Solve 20 medium-level coding problems", "type": "coding", "estimated_time": "3 hours", "xp_reward": 100, "priority": "high"},
                            {"title": "Study Dynamic Programming basics (Fibonacci, Knapsack)", "type": "reading", "estimated_time": "1.5 hours", "xp_reward": 30, "priority": "high"},
                            {"title": "Timed aptitude mock test (60 mins)", "type": "aptitude", "estimated_time": "1 hour", "xp_reward": 40, "priority": "medium"},
                            {"title": "Update and polish your resume", "type": "project", "estimated_time": "1 hour", "xp_reward": 20, "priority": "high"},
                        ],
                    },
                    {
                        "week_number": 8,
                        "title": f"{company_name}-Specific Practice",
                        "theme": "Company Focus",
                        "goals": [f"Complete {company_name} mock test", "Solve company-tagged problems", "Practice coding under pressure"],
                        "topics": ["Company-specific patterns", "Previous year questions", "Speed optimization"],
                        "tasks": [
                            {"title": f"Solve 15 {company_name}-tagged coding problems", "type": "coding", "estimated_time": "3 hours", "xp_reward": 100, "priority": "high"},
                            {"title": f"Take full {company_name} mock aptitude test", "type": "aptitude", "estimated_time": "1.5 hours", "xp_reward": 50, "priority": "high"},
                            {"title": "Practice graph algorithms (BFS, DFS)", "type": "coding", "estimated_time": "2 hours", "xp_reward": 60, "priority": "medium"},
                            {"title": "Prepare project explanations (3-min pitch)", "type": "interview", "estimated_time": "1 hour", "xp_reward": 25, "priority": "high"},
                        ],
                    },
                ],
            },
            {
                "phase_number": 5,
                "title": "Interview Preparation",
                "description": "Technical and HR interview preparation",
                "weeks": [
                    {
                        "week_number": 9,
                        "title": "Technical Interview Prep",
                        "theme": "Interview Ready",
                        "goals": ["Practice explaining code", "Master STAR method", "Revise all technical topics"],
                        "topics": ["Interview communication", "Problem-solving approach", "Code review", "STAR method"],
                        "tasks": [
                            {"title": "Take AI Mock Technical Interview", "type": "interview", "estimated_time": "1 hour", "xp_reward": 80, "priority": "high"},
                            {"title": "Revise all OS, DBMS, CN concepts", "type": "reading", "estimated_time": "2 hours", "xp_reward": 30, "priority": "high"},
                            {"title": "Practice explaining 3 projects clearly", "type": "interview", "estimated_time": "1 hour", "xp_reward": 30, "priority": "high"},
                            {"title": "Solve 10 coding problems while explaining aloud", "type": "coding", "estimated_time": "2 hours", "xp_reward": 60, "priority": "high"},
                        ],
                    },
                ],
            },
            {
                "phase_number": 6,
                "title": "Mock Interviews & Final Polish",
                "description": "Simulate real interview conditions and refine everything",
                "weeks": [
                    {
                        "week_number": 10,
                        "title": "AI Mock Interviews",
                        "theme": "Interview Simulation",
                        "goals": ["Complete 3 AI mock interviews", "Analyze feedback", "Improve weak areas"],
                        "topics": ["HR questions", "Technical questions", "Behavioral questions"],
                        "tasks": [
                            {"title": "Complete AI HR Mock Interview", "type": "interview", "estimated_time": "45 mins", "xp_reward": 80, "priority": "high"},
                            {"title": "Complete AI Technical Mock Interview", "type": "interview", "estimated_time": "1 hour", "xp_reward": 100, "priority": "high"},
                            {"title": "Review interview feedback and improve", "type": "reading", "estimated_time": "45 mins", "xp_reward": 20, "priority": "high"},
                            {"title": "Solve 15 mixed difficulty problems", "type": "coding", "estimated_time": "2.5 hours", "xp_reward": 80, "priority": "medium"},
                        ],
                    },
                    {
                        "week_number": 11,
                        "title": "Behavioral & Communication",
                        "theme": "Soft Skills",
                        "goals": ["Master behavioral questions", "Improve communication", "Build confidence"],
                        "topics": ["Leadership examples", "Conflict resolution", "Teamwork stories", "Growth mindset"],
                        "tasks": [
                            {"title": "Prepare 10 STAR method answers", "type": "interview", "estimated_time": "2 hours", "xp_reward": 50, "priority": "high"},
                            {"title": "Complete Behavioral Mock Interview", "type": "interview", "estimated_time": "45 mins", "xp_reward": 80, "priority": "high"},
                            {"title": "Finalize resume with latest improvements", "type": "project", "estimated_time": "1 hour", "xp_reward": 20, "priority": "high"},
                            {"title": "Practice 20 aptitude questions daily", "type": "aptitude", "estimated_time": "45 mins", "xp_reward": 25, "priority": "medium"},
                        ],
                    },
                ],
            },
            {
                "phase_number": 7,
                "title": "Final Preparation",
                "description": "Final revision, full mock tests, and placement day preparation",
                "weeks": [
                    {
                        "week_number": 12,
                        "title": "Placement Ready!",
                        "theme": "Final Sprint",
                        "goals": ["Complete full revision", "Peak performance on mock tests", "Finalize everything"],
                        "topics": ["Full revision", "Speed practice", "Mindset preparation"],
                        "tasks": [
                            {"title": f"Complete full {company_name} mock test simulation", "type": "aptitude", "estimated_time": "3 hours", "xp_reward": 100, "priority": "high"},
                            {"title": "Solve 20 mixed problems under time limit", "type": "coding", "estimated_time": "2.5 hours", "xp_reward": 100, "priority": "high"},
                            {"title": "Final AI Mock Interview (full session)", "type": "interview", "estimated_time": "1.5 hours", "xp_reward": 120, "priority": "high"},
                            {"title": "Review all technical topics summary notes", "type": "reading", "estimated_time": "2 hours", "xp_reward": 30, "priority": "high"},
                            {"title": "Prepare questions to ask the interviewer", "type": "interview", "estimated_time": "30 mins", "xp_reward": 10, "priority": "medium"},
                        ],
                    },
                ],
            },
        ]

        todays_tasks = [
            {"title": "Solve 5 Array problems", "type": "coding", "estimated_time": "45 mins", "xp_reward": 25, "priority": "high"},
            {"title": "Complete 20 Aptitude questions", "type": "aptitude", "estimated_time": "30 mins", "xp_reward": 15, "priority": "high"},
            {"title": "Study OOP concepts for 30 mins", "type": "reading", "estimated_time": "30 mins", "xp_reward": 10, "priority": "medium"},
            {"title": "Practice 'Tell me about yourself'", "type": "interview", "estimated_time": "20 mins", "xp_reward": 10, "priority": "high"},
        ]

        end_date = datetime.utcnow() + timedelta(weeks=duration)
        return {
            "title": f"{company_name} {role_name} — {duration}-Week Roadmap",
            "phases": phases,
            "todays_tasks": todays_tasks,
            "duration": duration,
            "estimated_end_date": end_date.isoformat(),
        }

    def _get_dsa_weeks(self, level: str) -> int:
        return {"beginner": 4, "intermediate": 3, "advanced": 2}.get(level, 4)


roadmap_ai_service = RoadmapAIService()
