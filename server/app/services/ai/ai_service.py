import asyncio
import json
import random
from typing import List, Dict, Optional
from loguru import logger
from app.config.settings import settings


class AIService:
    def __init__(self):
        self.provider = settings.AI_PROVIDER
        self.client = None
        self._gemini_model = None
        self._init_provider()

    def _init_provider(self):
        if self.provider == "openai" and settings.OPENAI_API_KEY:
            try:
                from openai import AsyncOpenAI
                self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
                logger.info("AI Provider: OpenAI initialized")
            except Exception as e:
                logger.warning(f"OpenAI init failed ({e}), falling back to mock")
                self.provider = "mock"
        elif self.provider == "gemini" and settings.GEMINI_API_KEY:
            try:
                import google.generativeai as genai
                genai.configure(api_key=settings.GEMINI_API_KEY)
                self._gemini_model = genai.GenerativeModel("gemini-1.5-flash")
                logger.info("AI Provider: Gemini initialized")
            except Exception as e:
                logger.warning(f"Gemini init failed ({e}), falling back to mock")
                self.provider = "mock"
        else:
            self.provider = "mock"
            logger.info("AI Provider: Mock mode. Set AI_PROVIDER=gemini and GEMINI_API_KEY for real AI.")

    async def chat(
        self,
        messages: List[Dict[str, str]],
        system_prompt: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 2048,
    ) -> str:
        if self.provider == "openai":
            return await self._openai_chat(messages, system_prompt, temperature, max_tokens)
        if self.provider == "gemini":
            return await self._gemini_chat(messages, system_prompt, temperature, max_tokens)
        return await self._mock_chat(messages, system_prompt)

    async def _openai_chat(self, messages, system_prompt, temperature, max_tokens) -> str:
        all_messages = []
        if system_prompt:
            all_messages.append({"role": "system", "content": system_prompt})
        all_messages.extend(messages)
        response = await self.client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=all_messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content

    async def _gemini_chat(self, messages, system_prompt, temperature, max_tokens) -> str:
        import asyncio
        parts = []
        if system_prompt:
            parts.append(system_prompt + "\n\n")
        for m in messages:
            parts.append(f"{m['role'].upper()}: {m['content']}\n")
        prompt = "".join(parts)
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(
            None,
            lambda: self._gemini_model.generate_content(
                prompt,
                generation_config={"temperature": temperature, "max_output_tokens": max_tokens},
            )
        )
        return response.text

    async def _mock_chat(self, messages: List[Dict], system_prompt: Optional[str] = None) -> str:
        await asyncio.sleep(0.5)
        last = messages[-1]["content"].lower() if messages else ""
        if "infosys" in last:
            return self._mock_company_response("Infosys")
        if "tcs" in last:
            return self._mock_company_response("TCS")
        if "amazon" in last or "sde" in last:
            return self._mock_company_response("Amazon")
        if "microsoft" in last:
            return self._mock_company_response("Microsoft")
        if "google" in last:
            return self._mock_company_response("Google")
        if any(w in last for w in ["resume", "cv", "ats"]):
            return self._mock_resume_advice()
        if any(w in last for w in ["dsa", "algorithm", "data structure", "array", "tree", "graph"]):
            return self._mock_dsa_response()
        if any(w in last for w in ["sql", "dbms", "database", "query"]):
            return self._mock_sql_response()
        if any(w in last for w in ["interview", "hr", "tell me about"]):
            return self._mock_interview_advice()
        if any(w in last for w in ["os", "operating system", "process", "thread"]):
            return self._mock_os_response()
        if any(w in last for w in ["network", "tcp", "http", "dns"]):
            return self._mock_network_response()
        return self._mock_general_response()

    def _mock_company_response(self, company: str) -> str:
        data = {
            "Infosys": {
                "eligibility": "60%+ throughout academics, no active backlogs",
                "rounds": "Online Test → Pseudocode/Coding → Technical Interview → HR",
                "aptitude": "Quantitative, Logical Reasoning, Verbal Ability (80 mins)",
                "coding": "2 coding questions, Easy-Medium level",
                "technical": "DSA, OOPS, DBMS, CN, OS, Programming basics",
                "tips": "Practice on InfyTQ platform. Focus on Python/Java basics.",
            },
            "TCS": {
                "eligibility": "60%+ throughout, no backlogs",
                "rounds": "NQT (National Qualifier Test) → Technical Interview → HR",
                "aptitude": "Numerical, Verbal, Reasoning, Coding (180 mins)",
                "coding": "2 coding problems, Basic-Medium level",
                "technical": "Any 1 language, OOP, basic DSA, SQL",
                "tips": "Solve TCS NQT mock tests. iON platform practice is useful.",
            },
            "Amazon": {
                "eligibility": "No specific CGPA cutoff for internship; strong DSA needed",
                "rounds": "OA (Coding) → Technical Round 1 → Technical Round 2 → Bar Raiser → HR",
                "aptitude": "Work Simulation + Coding Assessment",
                "coding": "2-3 medium-hard problems in OA",
                "technical": "DSA (Trees, Graphs, DP), System Design basics, LP principles",
                "tips": "Master Leadership Principles. Solve 200+ LeetCode problems.",
            },
            "Microsoft": {
                "eligibility": "7+ CGPA preferred; strong problem-solving skills",
                "rounds": "Online Test → 3-4 Technical Rounds → HR",
                "aptitude": "Coding Assessment (2 problems)",
                "coding": "Medium-Hard level, focus on Trees, DP, Graphs",
                "technical": "DSA, OOP, System Design, .NET/Azure basics for some roles",
                "tips": "Practice STAR method for behavioral. Microsoft values growth mindset.",
            },
            "Google": {
                "eligibility": "Strong DSA skills; no strict CGPA cutoff",
                "rounds": "OA → Phone Screen → 4-5 Onsite Rounds",
                "aptitude": "Competitive programming level problems",
                "coding": "Hard problems, algorithmic thinking emphasized",
                "technical": "Advanced DSA, System Design, Problem solving",
                "tips": "Practice 400+ LeetCode. Study CLRS. Think aloud during interviews.",
            },
        }
        info = data.get(company, data["Infosys"])
        return f"""## {company} Placement Preparation Guide

> **Note:** Recruitment patterns change frequently. Always verify current requirements on {company}'s official career portal.

### Eligibility
{info['eligibility']}

### Selection Process
{info['rounds']}

### Aptitude Test Pattern
{info['aptitude']}

### Coding Round
{info['coding']}

### Technical Interview Topics
{info['technical']}

### Expert Tips
{info['tips']}

### Recommended Timeline

| Week | Focus Area |
|------|-----------|
| 1-2 | Aptitude + Language Basics |
| 3-4 | DSA Fundamentals |
| 5-6 | Core CS Subjects |
| 7 | Coding Practice + Mock Tests |
| 8 | Mock Interviews + HR Prep |

Would you like me to generate a detailed personalized roadmap for {company}? Go to the **Roadmap** section!"""

    def _mock_resume_advice(self) -> str:
        return """## Resume Preparation Tips for Placements

### Essential Sections (in order)
1. **Contact Info** — Name, Email, Phone, LinkedIn, GitHub
2. **Education** — College, Degree, Branch, CGPA, Year
3. **Skills** — Organized by category
4. **Projects** — 2-3 strong technical projects
5. **Internship/Experience** — If applicable
6. **Certifications** — Relevant courses
7. **Achievements** — Hackathons, contests, ranks

### ATS Optimization
- Use keywords from the job description
- No tables, images, or special characters
- Use standard headings (Education, Skills, Projects)
- One page for freshers; save as PDF

### Writing Strong Project Bullets
**Formula:** Action Verb + What you built + Tech used + Impact

✅ *"Developed a real-time chat application using React, Socket.io, and MongoDB, supporting 500+ concurrent users with JWT authentication"*

❌ *"Made a chat app with React"*

### Skills Section Tips
```
Languages:   Python, Java, C++
Frameworks:  React, Django, Spring Boot
Databases:   MySQL, MongoDB, PostgreSQL
Tools:       Git, Docker, Postman, VS Code
Cloud:       AWS (basics), Heroku
```

### Common Mistakes
- ❌ Generic objective statements
- ❌ No GitHub/LinkedIn links
- ❌ Projects without measurable outcomes
- ❌ Listing soft skills like "hardworking"
- ❌ Photo on resume (for international applications)

**Use the Resume Analyzer tool to get a personalized score and improvement suggestions!**"""

    def _mock_dsa_response(self) -> str:
        return """## DSA Preparation Guide

### Learning Path
```
Week 1-2:  Arrays, Strings, Two Pointers
Week 3:    Linked Lists, Stack, Queue
Week 4:    Hashing, Recursion, Backtracking
Week 5:    Trees, BST, Binary Search
Week 6:    Heaps, Graphs (BFS/DFS)
Week 7-8:  Dynamic Programming
Week 9+:   Practice + Contest Problems
```

### Must-Know Patterns

| Pattern | Example Problems |
|---------|-----------------|
| Two Pointers | Container With Most Water, 3Sum |
| Sliding Window | Longest Substring Without Repeating |
| Fast & Slow Pointer | Linked List Cycle |
| BFS/DFS | Number of Islands, Shortest Path |
| Dynamic Programming | Fibonacci, Knapsack, LCS, LIS |
| Divide & Conquer | Merge Sort, Quick Sort |

### Problem Difficulty Strategy
- **Service Companies (TCS, Infosys):** 70% Easy, 30% Medium
- **Good Product Companies (Flipkart, Walmart):** 40% Easy, 50% Medium, 10% Hard
- **FAANG:** 20% Easy, 50% Medium, 30% Hard

### Quick Reference: Complexity
```python
# Common Time Complexities
Binary Search:    O(log n)
Merge Sort:       O(n log n)
Hash Table Ops:   O(1) average
BFS/DFS:          O(V + E) for graphs
DP (memoized):    O(n) or O(n²) typically
```

**Practice problems in the Coding Platform section!**"""

    def _mock_sql_response(self) -> str:
        return """## SQL & Database Interview Guide

### Top SQL Interview Questions

**1. Find the second highest salary:**
```sql
SELECT MAX(salary) AS second_highest
FROM employees
WHERE salary < (SELECT MAX(salary) FROM employees);
```

**2. Find duplicate emails:**
```sql
SELECT email, COUNT(*) as count
FROM users
GROUP BY email
HAVING COUNT(*) > 1;
```

**3. Employees earning more than their manager:**
```sql
SELECT e.name, e.salary
FROM employees e
JOIN employees m ON e.manager_id = m.id
WHERE e.salary > m.salary;
```

**4. Get nth highest salary (n = 3):**
```sql
SELECT DISTINCT salary
FROM employees
ORDER BY salary DESC
LIMIT 1 OFFSET 2;
```

### DBMS Key Concepts

| Topic | What to Know |
|-------|-------------|
| Normalization | 1NF, 2NF, 3NF, BCNF with examples |
| ACID | Atomicity, Consistency, Isolation, Durability |
| Indexes | B-Tree, Hash, Clustered vs Non-clustered |
| Joins | INNER, LEFT, RIGHT, FULL OUTER, CROSS, SELF |
| Transactions | BEGIN, COMMIT, ROLLBACK, SAVEPOINT |

### Common Interview Questions
- DELETE vs TRUNCATE vs DROP
- Primary Key vs Unique Key vs Foreign Key
- What is a VIEW? When to use stored procedures?
- What is a deadlock? How to prevent it?
- Explain UNION vs UNION ALL"""

    def _mock_os_response(self) -> str:
        return """## Operating Systems Interview Guide

### Process vs Thread
| Process | Thread |
|---------|--------|
| Independent program | Lightweight unit within process |
| Own memory space | Shares memory with parent process |
| More overhead | Less overhead |
| IPC needed for communication | Direct communication |
| Context switching is expensive | Faster context switching |

### Key Topics

**CPU Scheduling Algorithms:**
- FCFS (First Come First Served)
- SJF (Shortest Job First)
- Round Robin (with time quantum)
- Priority Scheduling
- MLFQ (Multi-Level Feedback Queue)

**Memory Management:**
- Paging vs Segmentation
- Virtual Memory + Page Tables
- Page Replacement: FIFO, LRU, Optimal
- Thrashing

**Synchronization:**
- Race Condition, Critical Section
- Mutex, Semaphore, Monitor
- Deadlock: Conditions, Prevention, Avoidance (Banker's Algorithm)

**File Systems:**
- Inode structure
- File allocation methods
- Directory structures

### Most Asked OS Questions
1. What is a system call?
2. Explain paging and page faults
3. What is a context switch?
4. Banker's algorithm for deadlock avoidance
5. Producer-Consumer problem solution"""

    def _mock_network_response(self) -> str:
        return """## Computer Networks Interview Guide

### OSI Model (7 Layers)
```
7. Application   - HTTP, FTP, DNS, SMTP
6. Presentation  - SSL/TLS, Encryption
5. Session       - Authentication, Sessions
4. Transport     - TCP, UDP
3. Network       - IP, Routers
2. Data Link     - MAC, Ethernet, Switches
1. Physical      - Cables, Signals
```

### TCP vs UDP

| TCP | UDP |
|-----|-----|
| Connection-oriented | Connectionless |
| Reliable, ordered | Unreliable, unordered |
| Slower | Faster |
| HTTP, FTP, Email | DNS, Video streaming, Gaming |

### HTTP Methods
- **GET** — Retrieve data (idempotent)
- **POST** — Create resource
- **PUT** — Update entire resource
- **PATCH** — Partial update
- **DELETE** — Remove resource

### DNS Resolution Process
```
Browser → OS Cache → Local DNS → Root DNS
→ TLD DNS (.com) → Authoritative DNS → IP returned
```

### Common Questions
1. What happens when you type google.com?
2. HTTP vs HTTPS (SSL/TLS handshake)
3. What is a subnet mask?
4. Three-way handshake (TCP connection setup)
5. ARP, DHCP, NAT explained"""

    def _mock_interview_advice(self) -> str:
        return """## Interview Preparation Guide

### HR Interview Tips

**Tell me about yourself — Formula:**
1. Current status (year, branch, college)
2. Technical skills & projects
3. Achievements
4. Why this company

**Common HR Questions & How to Answer:**
- **Why do you want to join us?** — Research the company, mention specific products/culture
- **Strength/Weakness?** — Be honest; show self-awareness and improvement on weakness
- **Where in 5 years?** — Show ambition aligned with the company's growth
- **Why should we hire you?** — Tie your skills directly to the job requirements

### STAR Method for Behavioral Questions
- **S**ituation — Set the context briefly
- **T**ask — What was your responsibility
- **A**ction — Steps you specifically took
- **R**esult — Quantifiable outcome

**Example:** *"Tell me about a time you worked under pressure"*
> S: Final semester, 3 project deadlines in one week
> T: I was team lead responsible for delivery
> A: Broke tasks into daily goals, held daily standups, used Trello
> R: All 3 delivered on time, team scored 95/100

### Technical Interview Tips
- Think aloud — explain your approach before coding
- Start brute force → optimize step by step
- Ask clarifying questions before diving in
- Test with edge cases (empty input, single element, large n)
- Know your time/space complexity

### Common Mistakes to Avoid
- ❌ Going silent when stuck — always talk through your thinking
- ❌ Jumping to code without understanding the problem
- ❌ Not knowing your own resume projects deeply
- ❌ Negative talk about previous experiences

**Practice with the Mock Interview section — it gives real-time feedback on your answers!**"""

    def _mock_general_response(self) -> str:
        return """## AI Placement Assistant — Ready to Help!

I'm your personal placement preparation mentor. Here's how I can help:

### What You Can Ask Me
- **"How to prepare for [company name]?"** — TCS, Infosys, Amazon, Google, etc.
- **"Explain [topic]"** — DSA, DBMS, OS, Networks, OOP concepts
- **"Give me practice questions on [subject]"**
- **"Tips for [interview type]"** — HR, Technical, Behavioral
- **"How to improve my resume?"**
- **"What projects should I build for [role]?"**

### Quick Start Suggestions

| Your Goal | Ask Me |
|-----------|--------|
| Target a company | "How to prepare for Wipro placement?" |
| Learn a topic | "Explain dynamic programming with examples" |
| Interview prep | "Common HR interview questions and answers" |
| Resume help | "How to write a strong project description" |
| Career advice | "Which skills should I learn for data analyst role?" |

### Platform Features
- 📝 **Resume Analyzer** — Get ATS score and improvement tips
- 🗺️ **Roadmap Generator** — Personalized preparation plan
- 💻 **Coding Practice** — 50+ problems with difficulty levels
- 🎤 **Mock Interview** — AI-powered interview simulation
- 📊 **Aptitude Practice** — Quantitative, Logical, Verbal

**What would you like to prepare for today?**"""


ai_service = AIService()
