import json
import re
from typing import Optional, Dict, Any
from app.services.ai.ai_service import ai_service

ANALYZE_PROMPT = """You are an expert ATS specialist and senior recruiter. Analyze the provided resume and return a detailed JSON analysis.

Return ONLY valid JSON in this exact format:
{
  "scores": {
    "overall": 75, "ats": 70, "skills": 80, "projects": 72,
    "experience": 65, "education": 85, "keywords": 68, "formatting": 78
  },
  "extracted_info": {
    "name": "Detected Name",
    "email": "email@example.com",
    "phone": "phone number",
    "skills": ["Python", "Java", "SQL"],
    "education": [{"degree": "B.Tech", "branch": "CSE", "cgpa": "8.5", "institution": "XYZ University"}],
    "experience": [],
    "projects": [{"title": "Project", "tech": ["React"]}],
    "certifications": []
  },
  "strengths": ["Strength 1", "Strength 2"],
  "weaknesses": ["Weakness 1", "Weakness 2"],
  "suggestions": [
    {"category": "Projects", "suggestion": "Add metrics to descriptions", "priority": "high"}
  ],
  "missing_keywords": ["Docker", "AWS", "CI/CD"],
  "present_keywords": ["Python", "Machine Learning"]
}"""


class ResumeAIService:
    async def analyze(self, resume_text: str, job_description: Optional[str] = None) -> Dict[str, Any]:
        if ai_service.provider == "mock":
            return self._mock_analysis(resume_text, job_description)

        prompt = f"Resume:\n{resume_text}\n"
        if job_description:
            prompt += f"\nJob Description:\n{job_description}\n"
        prompt += "\nAnalyze this resume and return the JSON as specified."

        try:
            response = await ai_service.chat(
                [{"role": "user", "content": prompt}],
                ANALYZE_PROMPT,
                temperature=0.3,
                max_tokens=3000,
            )
            json_match = re.search(r'\{[\s\S]*\}', response)
            if json_match:
                result = json.loads(json_match.group())
                if job_description:
                    result["job_match"] = self._compute_job_match(resume_text, job_description)
                return result
        except Exception:
            pass
        return self._mock_analysis(resume_text, job_description)

    async def generate_improvement(self, section: str, content: str, target_role: str = "") -> Dict[str, Any]:
        if ai_service.provider == "mock":
            return {
                "improved": f"• Developed and deployed {content.strip()} achieving measurable performance improvements",
                "changes": ["Added action verb", "Quantified impact", "Added relevant keywords"],
            }
        prompt = f"""Improve this {section} section for a {target_role or 'software engineer'} role.
Original: {content}
Return JSON: {{"improved": "...", "changes": ["change1"]}}"""
        response = await ai_service.chat([{"role": "user", "content": prompt}], temperature=0.5)
        try:
            m = re.search(r'\{[\s\S]*\}', response)
            if m:
                return json.loads(m.group())
        except Exception:
            pass
        return {"improved": response, "changes": []}

    def _mock_analysis(self, resume_text: str, job_description: Optional[str] = None) -> Dict[str, Any]:
        words = resume_text.lower()
        has_skills = "skill" in words
        has_project = "project" in words
        has_education = any(w in words for w in ["b.tech", "b.e", "education", "university", "college"])
        has_links = "github" in words or "linkedin" in words
        word_count = len(resume_text.split())

        base = 58
        base += 10 if has_skills else 0
        base += 8 if has_project else 0
        base += 5 if has_education else 0
        base += 5 if has_links else 0
        base += 5 if 200 < word_count < 800 else 0
        overall = min(92, base)

        result = {
            "scores": {
                "overall": overall,
                "ats": max(50, overall - 8),
                "skills": min(90, overall + 5) if has_skills else 48,
                "projects": min(88, overall + 3) if has_project else 45,
                "experience": 60,
                "education": 85 if has_education else 50,
                "keywords": max(45, overall - 12),
                "formatting": min(85, overall + 2),
            },
            "extracted_info": {
                "name": "Detected from resume",
                "email": "Detected from resume",
                "phone": "Detected from resume",
                "skills": ["Python", "JavaScript", "SQL", "Java"],
                "education": [{"degree": "B.Tech", "branch": "Computer Science", "cgpa": "8.0", "institution": "University"}],
                "experience": [],
                "projects": [{"title": "Web Project", "tech": ["React", "Node.js", "MongoDB"]}],
                "certifications": [],
            },
            "strengths": [
                "Resume covers essential sections",
                "Technical skills are listed" if has_skills else "Structured layout",
                "Projects demonstrate practical experience" if has_project else "Academic background is present",
            ],
            "weaknesses": [
                "Missing quantified achievements in project descriptions",
                "No GitHub or LinkedIn profile links" if not has_links else "Could add more professional profiles",
                "Skills section lacks proficiency indicators",
                "Resume may benefit from a stronger summary statement",
            ],
            "suggestions": [
                {"category": "Projects", "suggestion": "Add metrics: 'Improved page load by 40%', 'Served 1000+ users'", "priority": "high"},
                {"category": "Skills", "suggestion": "Group by category: Languages | Frameworks | Databases | Tools", "priority": "high"},
                {"category": "ATS", "suggestion": "Include job description keywords throughout resume", "priority": "high"},
                {"category": "Action Verbs", "suggestion": "Start every bullet with a strong verb: Built, Designed, Implemented, Optimized", "priority": "medium"},
                {"category": "Links", "suggestion": "Add GitHub and LinkedIn URLs in header", "priority": "high" if not has_links else "low"},
                {"category": "Format", "suggestion": "Use consistent date format (Month YYYY) throughout", "priority": "low"},
            ],
            "missing_keywords": ["Docker", "AWS", "CI/CD", "REST API", "Agile", "Microservices"],
            "present_keywords": ["Python", "Development", "Technical", "Project"] if has_skills else ["Technical"],
        }

        if job_description:
            result["job_match"] = self._compute_job_match(resume_text, job_description)
        return result

    def _compute_job_match(self, resume_text: str, job_description: str) -> Dict[str, Any]:
        common_skills = ["python", "java", "sql", "javascript", "react", "node", "aws",
                         "docker", "machine learning", "data analysis", "git", "linux", "rest api"]
        resume_lower = resume_text.lower()
        jd_lower = job_description.lower()
        matched = [s for s in common_skills if s in jd_lower and s in resume_lower]
        missing = [s for s in common_skills if s in jd_lower and s not in resume_lower]
        total = len(matched) + len(missing)
        pct = round((len(matched) / total * 100) if total > 0 else 0)
        suitability = "Strong fit" if pct >= 70 else "Good fit" if pct >= 50 else "Moderate fit" if pct >= 30 else "Needs improvement"
        return {
            "match_percentage": pct,
            "matched_skills": [s.title() for s in matched],
            "missing_skills": [s.title() for s in missing],
            "relevant_keywords": matched[:5],
            "role_suitability": suitability,
            "missing_experience": ["Cloud deployment experience", "Production-level project work"],
        }


resume_ai_service = ResumeAIService()
