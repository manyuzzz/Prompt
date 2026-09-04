import json
import re
import random
from typing import List, Dict, Optional, Any
from app.services.ai.ai_service import ai_service


HR_QUESTIONS = [
    "Tell me about yourself.",
    "Why do you want to join our company?",
    "What are your greatest strengths?",
    "What is your biggest weakness? How are you working on it?",
    "Where do you see yourself in 5 years?",
    "Why should we hire you over other candidates?",
    "Describe a challenging situation you faced and how you handled it.",
    "Tell me about a time you worked in a team. What was your role?",
    "What motivates you to do your best work?",
    "Do you have any questions for us?",
]

TECHNICAL_QUESTIONS = [
    "Explain the difference between a stack and a queue.",
    "What is object-oriented programming? Explain its four pillars.",
    "Explain the difference between a linked list and an array.",
    "What is a binary search tree? What are its time complexities?",
    "Explain what happens when you type a URL in the browser.",
    "What is normalization in databases? Explain 1NF, 2NF, 3NF.",
    "Explain the difference between TCP and UDP.",
    "What is a deadlock in OS? How can you prevent it?",
    "Explain the difference between GET and POST HTTP methods.",
    "What are indexes in databases? When should you use them?",
    "Explain the SOLID principles of software design.",
    "What is the time complexity of quicksort? When does it degrade?",
]

BEHAVIORAL_QUESTIONS = [
    "Tell me about a time you showed leadership.",
    "Describe a situation where you had to work under pressure.",
    "Give an example of a time you failed and what you learned.",
    "Tell me about a time you had a conflict with a team member. How did you resolve it?",
    "Describe a project you are most proud of and why.",
    "Tell me about a time you had to learn something quickly.",
    "Give an example of when you went above and beyond in your work.",
    "Tell me about a time you had to adapt to a significant change.",
]


class InterviewAIService:
    def get_questions(self, interview_type: str, company: Optional[str] = None, count: int = 10) -> List[str]:
        if interview_type == "hr":
            pool = HR_QUESTIONS
        elif interview_type == "technical":
            pool = TECHNICAL_QUESTIONS
        elif interview_type == "behavioral":
            pool = BEHAVIORAL_QUESTIONS
        elif interview_type == "company-specific":
            pool = HR_QUESTIONS + TECHNICAL_QUESTIONS
        else:
            pool = HR_QUESTIONS + TECHNICAL_QUESTIONS

        selected = random.sample(pool, min(count, len(pool)))
        if interview_type == "company-specific" and company:
            selected[0] = f"Why do you specifically want to work at {company}?"
        return selected

    async def evaluate_answer(self, question: str, answer: str, interview_type: str) -> Dict[str, Any]:
        if ai_service.provider == "mock" or not answer.strip():
            return self._mock_evaluation(question, answer, interview_type)

        prompt = f"""Evaluate this interview answer:

Question: {question}
Answer: {answer}
Interview Type: {interview_type}

Return JSON with scores (0-100) and feedback:
{{
  "scores": {{
    "relevance": 75, "technical": 70, "communication": 80,
    "clarity": 75, "confidence": 65, "completeness": 70
  }},
  "feedback": "Specific feedback here",
  "follow_up": "A follow-up question",
  "strengths": ["strength1"],
  "improvements": ["improvement1"]
}}"""
        try:
            response = await ai_service.chat(
                [{"role": "user", "content": prompt}],
                system_prompt="You are an expert interview evaluator. Be objective and constructive.",
                temperature=0.3,
            )
            m = re.search(r'\{[\s\S]*\}', response)
            if m:
                return json.loads(m.group())
        except Exception:
            pass
        return self._mock_evaluation(question, answer, interview_type)

    async def generate_report(self, questions_responses: List[Dict], interview_type: str) -> Dict[str, Any]:
        if not questions_responses:
            return self._empty_report()

        scores = [r.get("scores", {}) for r in questions_responses if r.get("scores")]
        if not scores:
            return self._empty_report()

        def avg(key):
            vals = [s.get(key, 0) for s in scores if s.get(key)]
            return round(sum(vals) / len(vals)) if vals else 0

        overall_scores = {
            "communication": avg("communication"),
            "technical_knowledge": avg("technical"),
            "confidence": avg("confidence"),
            "problem_solving": avg("completeness"),
            "clarity": avg("clarity"),
            "answer_quality": avg("relevance"),
        }
        overall_scores["overall"] = round(sum(overall_scores.values()) / len(overall_scores))

        if ai_service.provider == "mock":
            return self._mock_report(overall_scores, interview_type)

        prompt = f"""Based on these interview scores, generate a detailed feedback report:
Scores: {json.dumps(overall_scores)}
Interview Type: {interview_type}

Return JSON:
{{
  "strengths": ["strength1", "strength2"],
  "areas_to_improve": ["area1", "area2"],
  "recommended_practice": ["practice1", "practice2"],
  "summary": "Overall summary..."
}}"""
        try:
            response = await ai_service.chat([{"role": "user", "content": prompt}], temperature=0.5)
            m = re.search(r'\{[\s\S]*\}', response)
            if m:
                result = json.loads(m.group())
                result["overall_scores"] = overall_scores
                return result
        except Exception:
            pass
        return self._mock_report(overall_scores, interview_type)

    def _mock_evaluation(self, question: str, answer: str, interview_type: str) -> Dict[str, Any]:
        word_count = len(answer.split()) if answer else 0
        base = 60
        if word_count > 50:
            base += 10
        if word_count > 100:
            base += 5
        scores = {
            "relevance": min(90, base + random.randint(-5, 10)),
            "technical": min(88, base + random.randint(-10, 5)),
            "communication": min(92, base + random.randint(-3, 12)),
            "clarity": min(90, base + random.randint(-5, 8)),
            "confidence": min(88, base + random.randint(-8, 8)),
            "completeness": min(85, base + random.randint(-10, 8)),
        }
        feedbacks = [
            "Good answer structure. Try to add specific examples to make it more impactful.",
            "Clear communication. Consider quantifying your achievements with numbers.",
            "Shows understanding of the topic. Adding real-world experience will strengthen this.",
            "Well-structured response. Use the STAR method to make behavioral answers more compelling.",
        ]
        follow_ups = [
            "Can you elaborate on a specific example from your experience?",
            "How would you handle this differently if given another chance?",
            "What tools or technologies did you use in that situation?",
            "What was the outcome, and what did you learn from it?",
        ]
        return {
            "scores": scores,
            "feedback": random.choice(feedbacks),
            "follow_up": random.choice(follow_ups),
            "strengths": ["Clear communication", "Shows knowledge of the subject"],
            "improvements": ["Add specific examples", "Quantify achievements"],
        }

    def _mock_report(self, overall_scores: Dict, interview_type: str) -> Dict[str, Any]:
        score = overall_scores.get("overall", 70)
        strengths = []
        improvements = []
        practice = []

        if score >= 75:
            strengths.append("Good overall performance across all parameters")
        if overall_scores.get("communication", 0) >= 75:
            strengths.append("Clear and articulate communication style")
        else:
            improvements.append("Work on communication clarity and reduce filler words")
            practice.append("Practice answers aloud and record yourself")

        if overall_scores.get("technical_knowledge", 0) >= 75:
            strengths.append("Solid technical knowledge demonstrated")
        else:
            improvements.append("Strengthen technical fundamentals (DSA, DBMS, OS)")
            practice.append("Revise core CS subjects and solve more coding problems")

        if overall_scores.get("confidence", 0) < 70:
            improvements.append("Build confidence through more mock interview practice")
            practice.append("Take 2-3 AI mock interviews per week")

        strengths.append("Willingness to engage with all questions")
        improvements.append("Structure answers using STAR method for behavioral questions")
        practice.append("Practice 10 company-specific interview questions daily")

        summary = f"Overall Score: {score}/100. "
        if score >= 80:
            summary += "Excellent performance! You are well-prepared for placements."
        elif score >= 70:
            summary += "Good performance with room for improvement in specific areas."
        elif score >= 60:
            summary += "Decent attempt. Focus on the improvement areas and practice more."
        else:
            summary += "Needs significant improvement. Regular practice with AI mock interviews will help."

        return {
            "overall_scores": overall_scores,
            "strengths": strengths[:3],
            "areas_to_improve": improvements[:3],
            "recommended_practice": practice[:3],
            "summary": summary,
        }

    def _empty_report(self) -> Dict[str, Any]:
        return {
            "overall_scores": {"overall": 0, "communication": 0, "technical_knowledge": 0,
                               "confidence": 0, "problem_solving": 0, "clarity": 0, "answer_quality": 0},
            "strengths": [],
            "areas_to_improve": ["Complete the interview to get feedback"],
            "recommended_practice": ["Start an AI mock interview session"],
            "summary": "No interview data to analyze.",
        }


interview_ai_service = InterviewAIService()
