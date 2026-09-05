"""
Seed data for AI Placement Preparation Platform.
Run with: python seeds/seed_data.py
"""
import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

from app.config.settings import settings
from app.models.company import Company, RecruitmentStage, CompanyRole, SalaryRange
from app.models.coding import CodingProblem, TestCase, Example, Solution
from app.models.aptitude import AptitudeQuestion, Option


COMPANIES = [
    {
        "name": "TCS",
        "slug": "tcs",
        "description": "Tata Consultancy Services - India's largest IT services company",
        "industry": "IT Services", "size": "500,000+", "headquarters": "Mumbai, India",
        "tier": "tier2",
        "overview": "TCS (Tata Consultancy Services) is a global leader in IT services, consulting, and business solutions. It is one of the largest employers in India and recruits heavily from engineering colleges.",
        "roles": [
            {"title": "Systems Engineer", "type": "technical", "description": "Entry-level software development role"},
            {"title": "Assistant System Engineer", "type": "technical", "description": "Fresher role with training"},
            {"title": "Business Analyst", "type": "business", "description": "Analyze business requirements"},
        ],
        "eligibility": {
            "cgpa": "60%+ in 10th, 12th, and Degree",
            "backlogs": "No active backlogs during drive",
            "branches": ["CSE", "IT", "ECE", "EEE", "Mechanical", "Civil", "All branches"],
            "degrees": ["B.E.", "B.Tech", "M.E.", "M.Tech", "MCA", "M.Sc"],
        },
        "recruitment_process": [
            {"stage": "1. NQT (TCS National Qualifier Test)", "description": "Online aptitude + coding test. 3 hours duration.", "tips": ["Practice on TCS iON platform", "Focus on speed", "All sections are important"]},
            {"stage": "2. Technical Interview", "description": "Face-to-face technical discussion on CS fundamentals", "tips": ["Know your programming language well", "Prepare DSA basics", "Explain your projects clearly"]},
            {"stage": "3. HR Interview", "description": "Cultural fit and communication assessment", "tips": ["Research TCS values", "Prepare 'Tell me about yourself'", "Know about TCS products"]},
        ],
        "aptitude_pattern": {
            "description": "TCS NQT has multiple sections",
            "sections": [
                {"name": "Numerical Ability", "questions": "26 questions", "time": "40 mins", "topics": ["Number Systems", "Percentages", "Time & Work", "Probability"]},
                {"name": "Verbal Ability", "questions": "24 questions", "time": "30 mins", "topics": ["Grammar", "Vocabulary", "Reading Comprehension"]},
                {"name": "Reasoning Ability", "questions": "30 questions", "time": "50 mins", "topics": ["Logical Reasoning", "Arrangements", "Series"]},
                {"name": "Programming Logic", "questions": "10 questions", "time": "15 mins", "topics": ["Output prediction", "Algorithms"]},
                {"name": "Coding", "questions": "2 problems", "time": "45 mins", "topics": ["Basic algorithms", "String manipulation"]},
            ],
            "difficulty": "Easy to Medium",
            "cutoff": "50-60% overall",
        },
        "coding_pattern": {
            "description": "2 coding problems in 45 minutes",
            "languages": ["C", "C++", "Java", "Python", "Perl"],
            "difficulty": "Easy to Medium",
            "topics": ["String manipulation", "Basic math", "Pattern printing", "Simple algorithms"],
            "numberOfQuestions": "2",
            "time": "45 minutes",
        },
        "technical_topics": ["OOP in Java/Python/C++", "Basic DSA", "SQL basics", "OS concepts", "Computer Networks basics", "DBMS fundamentals"],
        "hr_topics": ["Why TCS?", "Tell me about yourself", "Team player examples", "5-year plan", "Relocation willingness"],
        "frequently_asked_topics": ["TCS values (IIDEA)", "TCS products", "Digital transformation", "OOP principles"],
        "preparation_strategy": "Focus on TCS NQT pattern. Practice on TCS iON platform. 60%+ in all sections is the target. Technical round covers CS fundamentals and your preferred programming language.",
        "salary_range": {"min": "3.36 LPA", "max": "7 LPA", "currency": "INR"},
        "tier": "tier2",
    },
    {
        "name": "Infosys",
        "slug": "infosys",
        "description": "Infosys Limited - Global leader in next-generation digital services",
        "industry": "IT Services", "size": "300,000+", "headquarters": "Bangalore, India",
        "tier": "tier2",
        "overview": "Infosys is a global leader in next-generation digital services and consulting. Known for its InfyTQ platform for fresher training and assessment.",
        "roles": [
            {"title": "Systems Engineer", "type": "technical", "description": "Software development and maintenance"},
            {"title": "Digital Specialist Engineer", "type": "technical", "description": "Digital transformation projects"},
            {"title": "Power Programmer", "type": "technical", "description": "High-performance role for top performers"},
        ],
        "eligibility": {
            "cgpa": "60%+ throughout academics (10th, 12th, Degree)",
            "backlogs": "No active backlogs",
            "branches": ["CSE", "IT", "ECE", "EEE", "Mechanical", "All engineering branches"],
            "degrees": ["B.E.", "B.Tech", "M.E.", "M.Tech", "MCA", "M.Sc"],
        },
        "recruitment_process": [
            {"stage": "1. Online Assessment (InfyTQ)", "description": "Aptitude + Pseudocode + Coding", "tips": ["Practice on InfyTQ platform", "Complete InfyTQ certifications", "Time management is key"]},
            {"stage": "2. Pseudocode Round", "description": "Algorithm understanding without specific syntax", "tips": ["Practice flowcharts", "Understand algorithm logic", "Practice Python pseudocode"]},
            {"stage": "3. Technical Interview", "description": "CS fundamentals, projects, and programming", "tips": ["Know OOPS well", "Prepare project explanations", "SQL queries practice"]},
            {"stage": "4. HR Interview", "description": "Personality and cultural fit assessment", "tips": ["Research Infosys values", "Prepare STAR answers", "Show growth mindset"]},
        ],
        "aptitude_pattern": {
            "description": "InfyTQ Assessment",
            "sections": [
                {"name": "Aptitude", "questions": "10 questions", "time": "25 mins", "topics": ["Quantitative", "Logical", "Data Interpretation"]},
                {"name": "English", "questions": "20 questions", "time": "35 mins", "topics": ["Grammar", "Reading Comprehension", "Vocabulary"]},
                {"name": "Pseudocode", "questions": "5 questions", "time": "25 mins", "topics": ["Algorithm tracing", "Logic evaluation"]},
                {"name": "Coding", "questions": "2 problems", "time": "3 hours (separate round)", "topics": ["Basic to medium algorithms"]},
            ],
            "difficulty": "Easy to Medium",
            "cutoff": "Varies by stream (SE: ~40%, DSE: ~60%+)",
        },
        "coding_pattern": {
            "description": "2 coding problems",
            "languages": ["C", "C++", "Java", "Python"],
            "difficulty": "Easy to Medium",
            "topics": ["Array manipulation", "String operations", "Mathematical problems"],
            "numberOfQuestions": "2",
            "time": "3 hours",
        },
        "technical_topics": ["OOP concepts", "Java/Python basics", "DBMS & SQL", "Basic DSA", "OS concepts", "Computer Networks"],
        "hr_topics": ["Why Infosys?", "Career goals", "Strengths and weaknesses", "Team leadership examples"],
        "frequently_asked_topics": ["Infosys business segments", "Digital transformation", "Agile methodology", "OOP pillars"],
        "preparation_strategy": "Register on InfyTQ and complete certifications. Practice pseudocode questions. The SE track has lower cutoffs but the DSE track is more competitive.",
        "salary_range": {"min": "3.6 LPA", "max": "9 LPA", "currency": "INR"},
        "tier": "tier2",
    },
    {
        "name": "Wipro",
        "slug": "wipro",
        "description": "Wipro Limited - Global information technology, consulting, and business process services company",
        "industry": "IT Services", "size": "200,000+", "headquarters": "Bangalore, India",
        "tier": "tier2",
        "overview": "Wipro is a leading global IT and consulting company. Their WILP (Wipro Integrated Level Programs) offer industry-integrated education.",
        "roles": [
            {"title": "Project Engineer", "type": "technical", "description": "Software engineering and development"},
            {"title": "Wipro Turbo", "type": "technical", "description": "Higher package role for strong performers"},
        ],
        "eligibility": {
            "cgpa": "60%+ throughout",
            "backlogs": "No backlogs",
            "branches": ["All engineering branches", "MCA"],
            "degrees": ["B.E.", "B.Tech", "M.Tech", "MCA"],
        },
        "recruitment_process": [
            {"stage": "1. Online Test (NLTH)", "description": "Aptitude + Logical + English + Coding", "tips": ["Practice typing speed", "Time management is crucial"]},
            {"stage": "2. Technical Interview", "description": "CS subjects and programming", "tips": ["Focus on your core subjects", "Explain projects confidently"]},
            {"stage": "3. HR Interview", "description": "Personality assessment", "tips": ["Research Wipro values", "Prepare situational answers"]},
        ],
        "technical_topics": ["Programming basics", "DSA fundamentals", "DBMS", "OOP", "OS basics"],
        "preparation_strategy": "Practice Wipro NLTH pattern. Focus on aptitude speed. Technical round is straightforward for CS fundamentals.",
        "salary_range": {"min": "3.5 LPA", "max": "6.5 LPA", "currency": "INR"},
        "tier": "tier2",
    },
    {
        "name": "Amazon",
        "slug": "amazon",
        "description": "Amazon.com Inc - Global e-commerce and cloud computing company",
        "industry": "Technology", "size": "1,500,000+", "headquarters": "Seattle, USA",
        "tier": "tier1",
        "overview": "Amazon is one of the world's most valuable companies with massive engineering teams. Amazon India has major development centers in Bangalore, Hyderabad, and Chennai. Known for its Leadership Principles.",
        "roles": [
            {"title": "SDE-1 (Software Development Engineer)", "type": "technical", "description": "Entry-level software engineering"},
            {"title": "Data Engineer", "type": "technical", "description": "Data pipeline and analytics"},
            {"title": "Business Intelligence Engineer", "type": "technical", "description": "SQL, data analysis, and BI tools"},
        ],
        "eligibility": {
            "cgpa": "No strict cutoff; strong problem-solving skills required",
            "backlogs": "Backlogs may affect eligibility",
            "branches": ["CSE", "IT", "ECE preferred"],
            "degrees": ["B.Tech", "M.Tech", "MCA"],
        },
        "recruitment_process": [
            {"stage": "1. Online Assessment", "description": "2-3 coding problems + Work Simulation", "tips": ["Solve 200+ LeetCode problems", "Focus on medium-hard difficulty", "Amazon tags on LeetCode"]},
            {"stage": "2. Phone Screen", "description": "1 coding problem + LPs discussion", "tips": ["Practice coding interviews", "Prepare 2 stories per LP", "STAR method"]},
            {"stage": "3. Onsite Loop (3-4 rounds)", "description": "Coding + Design + Bar Raiser + LP", "tips": ["System design basics", "All 16 Leadership Principles", "Think aloud always"]},
            {"stage": "4. HR Round", "description": "Offer discussion and salary negotiation", "tips": ["Know your market value", "Be ready to negotiate"]},
        ],
        "technical_topics": ["Advanced DSA (Trees, Graphs, DP)", "System Design basics", "Object-Oriented Design", "SQL", "Amazon Leadership Principles"],
        "hr_topics": ["Amazon Leadership Principles (all 16)", "STAR method examples", "Failure stories", "Innovation examples"],
        "frequently_asked_topics": ["Leadership Principles", "Scalability", "Customer obsession examples", "Algorithm optimization"],
        "preparation_strategy": "Master all 16 Amazon Leadership Principles with STAR stories. Solve 200+ LeetCode (40% Medium, 30% Hard for SDE roles). Practice system design basics. Amazon is very LP-focused.",
        "salary_range": {"min": "25 LPA", "max": "40+ LPA", "currency": "INR"},
        "tier": "tier1",
    },
    {
        "name": "Microsoft",
        "slug": "microsoft",
        "description": "Microsoft Corporation - Global technology company",
        "industry": "Technology", "size": "220,000+", "headquarters": "Redmond, USA",
        "tier": "tier1",
        "overview": "Microsoft is a global technology giant with major India development centers. Known for its growth mindset culture and emphasis on learning.",
        "roles": [
            {"title": "SDE-1 (Software Engineer)", "type": "technical", "description": "Entry-level software development"},
            {"title": "Data Scientist", "type": "technical", "description": "ML and data analysis"},
            {"title": "Product Manager", "type": "management", "description": "Product strategy and development"},
        ],
        "eligibility": {
            "cgpa": "7+ CGPA preferred; strong problem-solving skills",
            "backlogs": "No backlogs",
            "branches": ["CSE", "IT", "ECE preferred"],
            "degrees": ["B.Tech", "M.Tech", "MCA"],
        },
        "recruitment_process": [
            {"stage": "1. Online Assessment", "description": "2-3 coding problems", "tips": ["Medium-hard LeetCode", "Focus on Trees, DP, Graphs"]},
            {"stage": "2-3. Technical Interviews", "description": "Coding + CS fundamentals", "tips": ["Explain approach before coding", "Consider edge cases", "Clean code matters"]},
            {"stage": "4. System Design (for experienced)", "description": "High-level and low-level design", "tips": ["Study HLD and LLD basics", "SOLID principles", "Common patterns"]},
            {"stage": "5. HR/As Appropriate", "description": "Culture and values fit", "tips": ["Growth mindset stories", "Collaboration examples"]},
        ],
        "technical_topics": ["Advanced DSA", "System Design", "OOP", "SOLID principles", ".NET basics (optional)", "Azure (optional)"],
        "preparation_strategy": "Microsoft values clean code and growth mindset. Practice 150-200 LeetCode. Study system design basics. Be prepared to discuss time/space complexity.",
        "salary_range": {"min": "20 LPA", "max": "35+ LPA", "currency": "INR"},
        "tier": "tier1",
    },
    {
        "name": "Accenture",
        "slug": "accenture",
        "description": "Accenture - Global professional services company",
        "industry": "IT Consulting", "size": "700,000+", "headquarters": "Dublin, Ireland",
        "tier": "tier2",
        "overview": "Accenture is one of the world's largest IT consulting firms. It offers roles in technology, digital, and cloud services.",
        "roles": [
            {"title": "Associate Software Engineer", "type": "technical", "description": "Entry-level development"},
            {"title": "Advanced App Engineering Analyst", "type": "technical", "description": "Higher-level engineering role"},
        ],
        "eligibility": {
            "cgpa": "65%+ throughout",
            "backlogs": "No active backlogs",
            "branches": ["All engineering branches"],
            "degrees": ["B.E.", "B.Tech", "M.Tech", "MCA"],
        },
        "recruitment_process": [
            {"stage": "1. Cognitive Assessment + Technical Assessment", "description": "Aptitude + coding + communication", "tips": ["Practice aptitude thoroughly", "Read questions carefully"]},
            {"stage": "2. Communication Assessment", "description": "English speaking and writing", "tips": ["Speak clearly and confidently", "Use proper grammar"]},
            {"stage": "3. Interview", "description": "Technical + HR combined", "tips": ["Research Accenture services", "Prepare role-based answers"]},
        ],
        "technical_topics": ["Programming basics", "OOP", "Database basics", "Cloud basics"],
        "preparation_strategy": "Accenture focuses on communication and aptitude. Practice English communication. Technical requirements are moderate.",
        "salary_range": {"min": "4.5 LPA", "max": "8 LPA", "currency": "INR"},
        "tier": "tier2",
    },
    {
        "name": "Deloitte",
        "slug": "deloitte",
        "description": "Deloitte - Global consulting, financial advisory, and technology company",
        "industry": "Consulting", "size": "300,000+", "headquarters": "London, UK",
        "tier": "tier2",
        "overview": "Deloitte is one of the Big Four professional services firms. Their UST (Unified Services Team) hires technical engineers from campuses.",
        "roles": [
            {"title": "Business Technology Analyst", "type": "technical", "description": "Technology consulting and development"},
            {"title": "Software Engineer", "type": "technical", "description": "Core software development"},
        ],
        "eligibility": {
            "cgpa": "60%+, some roles require 70%+",
            "branches": ["CSE", "IT", "ECE preferred"],
            "degrees": ["B.Tech", "MCA"],
        },
        "recruitment_process": [
            {"stage": "1. Online Test", "description": "Aptitude + Logical + Technical MCQs", "tips": ["Strong aptitude preparation needed"]},
            {"stage": "2. Case Study / GD", "description": "Group discussion or case analysis", "tips": ["Develop analytical thinking", "Practice case studies"]},
            {"stage": "3. Technical Interview", "description": "Core CS and domain knowledge", "tips": ["Know your chosen specialization well"]},
            {"stage": "4. HR Interview", "description": "Fit assessment", "tips": ["Research Deloitte culture", "Leadership examples"]},
        ],
        "technical_topics": ["Programming", "Data analysis basics", "SQL", "Problem solving"],
        "preparation_strategy": "Deloitte values analytical thinking. Prepare for case studies and group discussions. Technical round focuses on fundamentals and problem-solving approach.",
        "salary_range": {"min": "6 LPA", "max": "12 LPA", "currency": "INR"},
        "tier": "tier2",
    },
    {
        "name": "Cognizant",
        "slug": "cognizant",
        "description": "Cognizant Technology Solutions - Global IT services and consulting company",
        "industry": "IT Services", "size": "300,000+", "headquarters": "Teaneck, USA",
        "tier": "tier2",
        "overview": "Cognizant is a multinational IT services company, one of the largest in the world. Known for large-scale fresher hiring through GenC programs.",
        "roles": [
            {"title": "Programmer Analyst Trainee", "type": "technical", "description": "GenC - Standard entry role"},
            {"title": "Programmer Analyst", "type": "technical", "description": "GenC Pro - Higher package"},
            {"title": "GenC Elevate", "type": "technical", "description": "Premium engineering role"},
        ],
        "recruitment_process": [
            {"stage": "1. GenC Test (AMCAT based)", "description": "Aptitude + Coding + Communication", "tips": ["Practice AMCAT pattern", "Strong verbal skills needed"]},
            {"stage": "2. Technical Interview", "description": "Programming and CS basics", "tips": ["Know C/C++/Java/Python well"]},
            {"stage": "3. HR Interview", "description": "Personality and values", "tips": ["Relocation flexibility is important"]},
        ],
        "technical_topics": ["C/C++/Java programming", "Basic DSA", "DBMS", "OOP", "OS"],
        "preparation_strategy": "Cognizant uses AMCAT for assessment. Strong aptitude and communication skills are needed. Technical round is moderate.",
        "salary_range": {"min": "4 LPA", "max": "8 LPA", "currency": "INR"},
        "tier": "tier2",
    },
    {
        "name": "Google",
        "slug": "google",
        "description": "Google LLC - Multinational technology company",
        "industry": "Technology", "size": "180,000+", "headquarters": "Mountain View, USA",
        "tier": "tier1",
        "overview": "Google is one of the world's most valuable companies. Getting into Google requires exceptional problem-solving skills and algorithmic thinking.",
        "roles": [
            {"title": "Software Engineer L3", "type": "technical", "description": "Entry-level SWE"},
            {"title": "SWE Intern → Full Time", "type": "technical", "description": "Common entry path"},
        ],
        "eligibility": {
            "cgpa": "No strict cutoff; exceptional problem-solving required",
            "branches": ["CSE", "IT preferred; all branches eligible"],
            "degrees": ["B.Tech", "M.Tech"],
        },
        "recruitment_process": [
            {"stage": "1. Online Assessment", "description": "2-3 hard algorithmic problems", "tips": ["Practice competitive programming", "400+ LeetCode problems recommended"]},
            {"stage": "2. Phone Screen", "description": "1-2 coding problems", "tips": ["Think aloud", "Optimal solution expected"]},
            {"stage": "3. Onsite (4-5 rounds)", "description": "Coding + System Design + Googleyness", "tips": ["Advanced system design", "CLRS study recommended", "Leadership examples"]},
        ],
        "technical_topics": ["Advanced algorithms", "System design", "Distributed systems", "Problem solving at scale"],
        "preparation_strategy": "Google requires the highest level of DSA preparation. Aim for 400+ LeetCode problems, focus on Hard. Study system design thoroughly. Practice competitive programming.",
        "salary_range": {"min": "40 LPA", "max": "80+ LPA", "currency": "INR"},
        "tier": "tier1",
    },
    {
        "name": "IBM",
        "slug": "ibm",
        "description": "International Business Machines - Global technology and consulting company",
        "industry": "Technology", "size": "280,000+", "headquarters": "Armonk, USA",
        "tier": "tier2",
        "overview": "IBM is a global technology leader with expertise in AI, cloud, and blockchain. They hire from campuses for various technical and consulting roles.",
        "roles": [
            {"title": "Application Developer", "type": "technical", "description": "Software development"},
            {"title": "Data Engineer", "type": "technical", "description": "Data and analytics"},
            {"title": "Cloud Engineer", "type": "technical", "description": "IBM Cloud services"},
        ],
        "recruitment_process": [
            {"stage": "1. Cognitive Assessment", "description": "IBM's cognitive ability test", "tips": ["Practice spatial reasoning", "Speed is important"]},
            {"stage": "2. Technical Interview", "description": "Domain-specific technical questions", "tips": ["Choose your strongest domain", "Know IBM technologies: Watson, Cloud"]},
            {"stage": "3. HR Interview", "description": "Values and cultural fit", "tips": ["Research IBM's THINK culture", "Innovation examples"]},
        ],
        "technical_topics": ["Programming", "Cloud basics", "AI/ML fundamentals", "Database", "API development"],
        "preparation_strategy": "IBM focuses on cognitive skills and specific domain knowledge. Choose cloud, AI, or software development track and prepare accordingly.",
        "salary_range": {"min": "6 LPA", "max": "12 LPA", "currency": "INR"},
        "tier": "tier2",
    },
]


CODING_PROBLEMS = [
    {
        "title": "Two Sum",
        "slug": "two-sum",
        "description": """Given an array of integers `nums` and an integer `target`, return indices of the two numbers such that they add up to `target`.

You may assume that each input would have exactly one solution, and you may not use the same element twice.

You can return the answer in any order.""",
        "difficulty": "easy",
        "topics": ["Arrays", "Hashing"],
        "companies": ["Amazon", "Google", "Microsoft", "TCS"],
        "input_format": "An array of integers and a target integer",
        "output_format": "Array of two indices",
        "constraints": "2 <= nums.length <= 10^4\n-10^9 <= nums[i] <= 10^9\n-10^9 <= target <= 10^9\nOnly one valid answer exists.",
        "examples": [
            {"input": "nums = [2,7,11,15], target = 9", "output": "[0,1]", "explanation": "Because nums[0] + nums[1] == 9, we return [0, 1]."},
            {"input": "nums = [3,2,4], target = 6", "output": "[1,2]"},
        ],
        "test_cases": [
            {"input": "[2,7,11,15]\n9", "expected_output": "[0,1]", "is_hidden": False},
            {"input": "[3,2,4]\n6", "expected_output": "[1,2]", "is_hidden": False},
            {"input": "[3,3]\n6", "expected_output": "[0,1]", "is_hidden": True},
        ],
        "hints": ["Think about using a hash map to store seen values", "For each element, check if target - element exists in the map"],
        "solutions": [{"language": "python", "code": "def twoSum(nums, target):\n    seen = {}\n    for i, num in enumerate(nums):\n        complement = target - num\n        if complement in seen:\n            return [seen[complement], i]\n        seen[num] = i\n    return []", "explanation": "Use hash map for O(n) solution"}],
        "xp_reward": 50, "order": 1,
    },
    {
        "title": "Valid Parentheses",
        "slug": "valid-parentheses",
        "description": """Given a string `s` containing just the characters `'('`, `')'`, `'{'`, `'}'`, `'['` and `']'`, determine if the input string is valid.

An input string is valid if:
1. Open brackets must be closed by the same type of brackets.
2. Open brackets must be closed in the correct order.
3. Every close bracket has a corresponding open bracket of the same type.""",
        "difficulty": "easy",
        "topics": ["Stack", "Strings"],
        "companies": ["Amazon", "Microsoft", "Infosys", "TCS"],
        "input_format": "String s containing bracket characters",
        "output_format": "Boolean true/false",
        "constraints": "1 <= s.length <= 10^4\ns consists of parentheses only '()[]{}'",
        "examples": [
            {"input": 's = "()"', "output": "true"},
            {"input": 's = "()[]{}"', "output": "true"},
            {"input": 's = "(]"', "output": "false"},
        ],
        "test_cases": [
            {"input": "()", "expected_output": "true", "is_hidden": False},
            {"input": "()[]{}", "expected_output": "true", "is_hidden": False},
            {"input": "(]", "expected_output": "false", "is_hidden": True},
            {"input": "([)]", "expected_output": "false", "is_hidden": True},
        ],
        "hints": ["Use a stack", "For each closing bracket, check if it matches the top of the stack"],
        "solutions": [{"language": "python", "code": "def isValid(s):\n    stack = []\n    mapping = {')': '(', '}': '{', ']': '['}\n    for char in s:\n        if char in mapping:\n            top = stack.pop() if stack else '#'\n            if mapping[char] != top:\n                return False\n        else:\n            stack.append(char)\n    return not stack"}],
        "xp_reward": 50, "order": 2,
    },
    {
        "title": "Reverse Linked List",
        "slug": "reverse-linked-list",
        "description": """Given the `head` of a singly linked list, reverse the list, and return the reversed list.

**Example:**
Input: 1 -> 2 -> 3 -> 4 -> 5 -> NULL
Output: 5 -> 4 -> 3 -> 2 -> 1 -> NULL""",
        "difficulty": "easy",
        "topics": ["Linked Lists"],
        "companies": ["Amazon", "Microsoft", "Wipro"],
        "input_format": "Head of a linked list",
        "output_format": "Head of the reversed linked list",
        "constraints": "The number of nodes in the list is in the range [0, 5000].\n-5000 <= Node.val <= 5000",
        "examples": [
            {"input": "head = [1,2,3,4,5]", "output": "[5,4,3,2,1]"},
            {"input": "head = [1,2]", "output": "[2,1]"},
        ],
        "test_cases": [
            {"input": "1 2 3 4 5", "expected_output": "5 4 3 2 1", "is_hidden": False},
            {"input": "1 2", "expected_output": "2 1", "is_hidden": True},
        ],
        "hints": ["Maintain previous, current, and next pointers", "Can also be done recursively"],
        "solutions": [{"language": "python", "code": "def reverseList(head):\n    prev = None\n    curr = head\n    while curr:\n        next_node = curr.next\n        curr.next = prev\n        prev = curr\n        curr = next_node\n    return prev"}],
        "xp_reward": 50, "order": 3,
    },
    {
        "title": "Maximum Subarray",
        "slug": "maximum-subarray",
        "description": """Given an integer array `nums`, find the subarray with the largest sum, and return its sum.

This is the classic Kadane's Algorithm problem.""",
        "difficulty": "medium",
        "topics": ["Arrays", "Dynamic Programming"],
        "companies": ["Amazon", "Microsoft", "Google", "TCS"],
        "input_format": "Array of integers",
        "output_format": "Maximum subarray sum",
        "constraints": "1 <= nums.length <= 10^5\n-10^4 <= nums[i] <= 10^4",
        "examples": [
            {"input": "nums = [-2,1,-3,4,-1,2,1,-5,4]", "output": "6", "explanation": "The subarray [4,-1,2,1] has the largest sum 6."},
            {"input": "nums = [1]", "output": "1"},
        ],
        "test_cases": [
            {"input": "-2 1 -3 4 -1 2 1 -5 4", "expected_output": "6", "is_hidden": False},
            {"input": "1", "expected_output": "1", "is_hidden": False},
            {"input": "-1 -2 -3", "expected_output": "-1", "is_hidden": True},
        ],
        "hints": ["Kadane's Algorithm", "Keep track of current sum and maximum sum"],
        "solutions": [{"language": "python", "code": "def maxSubArray(nums):\n    max_sum = curr_sum = nums[0]\n    for num in nums[1:]:\n        curr_sum = max(num, curr_sum + num)\n        max_sum = max(max_sum, curr_sum)\n    return max_sum"}],
        "xp_reward": 75, "order": 4,
    },
    {
        "title": "Binary Search",
        "slug": "binary-search",
        "description": """Given an array of integers `nums` which is sorted in ascending order, and an integer `target`, write a function to search `target` in `nums`. If `target` exists, return its index. Otherwise, return `-1`.

You must write an algorithm with O(log n) runtime complexity.""",
        "difficulty": "easy",
        "topics": ["Binary Search", "Arrays"],
        "companies": ["Amazon", "TCS", "Infosys"],
        "input_format": "Sorted array and target integer",
        "output_format": "Index of target or -1",
        "constraints": "1 <= nums.length <= 10^4\n-10^4 <= nums[i], target <= 10^4\nAll integers in nums are unique.\nnums is sorted in ascending order.",
        "examples": [
            {"input": "nums = [-1,0,3,5,9,12], target = 9", "output": "4"},
            {"input": "nums = [-1,0,3,5,9,12], target = 2", "output": "-1"},
        ],
        "test_cases": [
            {"input": "-1 0 3 5 9 12\n9", "expected_output": "4", "is_hidden": False},
            {"input": "-1 0 3 5 9 12\n2", "expected_output": "-1", "is_hidden": True},
        ],
        "hints": ["Use left and right pointers", "Check mid element each iteration"],
        "solutions": [{"language": "python", "code": "def search(nums, target):\n    left, right = 0, len(nums) - 1\n    while left <= right:\n        mid = (left + right) // 2\n        if nums[mid] == target:\n            return mid\n        elif nums[mid] < target:\n            left = mid + 1\n        else:\n            right = mid - 1\n    return -1"}],
        "xp_reward": 50, "order": 5,
    },
    {
        "title": "Climbing Stairs",
        "slug": "climbing-stairs",
        "description": """You are climbing a staircase. It takes `n` steps to reach the top.

Each time you can either climb `1` or `2` steps. In how many distinct ways can you climb to the top?""",
        "difficulty": "easy",
        "topics": ["Dynamic Programming", "Recursion"],
        "companies": ["Amazon", "Google", "TCS", "Wipro"],
        "input_format": "Integer n (number of stairs)",
        "output_format": "Number of distinct ways",
        "constraints": "1 <= n <= 45",
        "examples": [
            {"input": "n = 2", "output": "2", "explanation": "1+1, 2 - two ways"},
            {"input": "n = 3", "output": "3", "explanation": "1+1+1, 1+2, 2+1 - three ways"},
        ],
        "test_cases": [
            {"input": "2", "expected_output": "2", "is_hidden": False},
            {"input": "3", "expected_output": "3", "is_hidden": False},
            {"input": "10", "expected_output": "89", "is_hidden": True},
        ],
        "hints": ["Similar to Fibonacci", "dp[i] = dp[i-1] + dp[i-2]"],
        "solutions": [{"language": "python", "code": "def climbStairs(n):\n    if n <= 2:\n        return n\n    a, b = 1, 2\n    for _ in range(3, n + 1):\n        a, b = b, a + b\n    return b"}],
        "xp_reward": 50, "order": 6,
    },
    {
        "title": "Longest Common Subsequence",
        "slug": "longest-common-subsequence",
        "description": """Given two strings `text1` and `text2`, return the length of their longest common subsequence.

A subsequence is a sequence that can be derived from another sequence by deleting some elements (possibly zero) without changing the order of the remaining elements.

A common subsequence is a subsequence of both strings.""",
        "difficulty": "medium",
        "topics": ["Dynamic Programming", "Strings"],
        "companies": ["Amazon", "Google", "Microsoft"],
        "input_format": "Two strings text1 and text2",
        "output_format": "Length of longest common subsequence",
        "constraints": "1 <= text1.length, text2.length <= 1000",
        "examples": [
            {"input": 'text1 = "abcde", text2 = "ace"', "output": "3", "explanation": "LCS is 'ace'"},
            {"input": 'text1 = "abc", text2 = "abc"', "output": "3"},
        ],
        "test_cases": [
            {"input": "abcde\nace", "expected_output": "3", "is_hidden": False},
            {"input": "abc\nabc", "expected_output": "3", "is_hidden": True},
        ],
        "hints": ["2D DP table", "if chars match: dp[i][j] = dp[i-1][j-1] + 1"],
        "solutions": [{"language": "python", "code": "def longestCommonSubsequence(text1, text2):\n    m, n = len(text1), len(text2)\n    dp = [[0] * (n + 1) for _ in range(m + 1)]\n    for i in range(1, m + 1):\n        for j in range(1, n + 1):\n            if text1[i-1] == text2[j-1]:\n                dp[i][j] = dp[i-1][j-1] + 1\n            else:\n                dp[i][j] = max(dp[i-1][j], dp[i][j-1])\n    return dp[m][n]"}],
        "xp_reward": 75, "order": 7,
    },
    {
        "title": "Number of Islands",
        "slug": "number-of-islands",
        "description": """Given an `m x n` 2D binary grid which represents a map of '1's (land) and '0's (water), return the number of islands.

An island is surrounded by water and is formed by connecting adjacent lands horizontally or vertically.""",
        "difficulty": "medium",
        "topics": ["Graphs", "BFS", "DFS"],
        "companies": ["Amazon", "Google", "Microsoft", "Facebook"],
        "input_format": "2D grid of '1' and '0'",
        "output_format": "Number of islands",
        "constraints": "m == grid.length\nn == grid[i].length\n1 <= m, n <= 300",
        "examples": [
            {"input": 'grid = [["1","1","1","1","0"],["1","1","0","1","0"],["1","1","0","0","0"],["0","0","0","0","0"]]', "output": "1"},
            {"input": 'grid = [["1","1","0","0","0"],["1","1","0","0","0"],["0","0","1","0","0"],["0","0","0","1","1"]]', "output": "3"},
        ],
        "test_cases": [
            {"input": "1 1 1 1 0\n1 1 0 1 0\n1 1 0 0 0\n0 0 0 0 0", "expected_output": "1", "is_hidden": False},
            {"input": "1 1 0\n0 0 1\n0 0 1", "expected_output": "2", "is_hidden": True},
        ],
        "hints": ["Use DFS or BFS to explore each island", "Mark visited cells as '0' to avoid revisiting"],
        "solutions": [{"language": "python", "code": "def numIslands(grid):\n    if not grid:\n        return 0\n    count = 0\n    def dfs(r, c):\n        if r < 0 or r >= len(grid) or c < 0 or c >= len(grid[0]) or grid[r][c] == '0':\n            return\n        grid[r][c] = '0'\n        dfs(r+1, c); dfs(r-1, c); dfs(r, c+1); dfs(r, c-1)\n    for r in range(len(grid)):\n        for c in range(len(grid[0])):\n            if grid[r][c] == '1':\n                count += 1\n                dfs(r, c)\n    return count"}],
        "xp_reward": 75, "order": 8,
    },
    {
        "title": "Merge Intervals",
        "slug": "merge-intervals",
        "description": """Given an array of `intervals` where `intervals[i] = [starti, endi]`, merge all overlapping intervals, and return an array of the non-overlapping intervals that cover all the intervals in the input.""",
        "difficulty": "medium",
        "topics": ["Arrays", "Sorting"],
        "companies": ["Amazon", "Google", "Microsoft", "Facebook"],
        "input_format": "Array of intervals [start, end]",
        "output_format": "Merged non-overlapping intervals",
        "constraints": "1 <= intervals.length <= 10^4\n0 <= starti <= endi <= 10^4",
        "examples": [
            {"input": "intervals = [[1,3],[2,6],[8,10],[15,18]]", "output": "[[1,6],[8,10],[15,18]]", "explanation": "Intervals [1,3] and [2,6] overlap, merge to [1,6]"},
            {"input": "intervals = [[1,4],[4,5]]", "output": "[[1,5]]"},
        ],
        "test_cases": [
            {"input": "1 3\n2 6\n8 10\n15 18", "expected_output": "1 6\n8 10\n15 18", "is_hidden": False},
        ],
        "hints": ["Sort intervals by start time", "If current interval overlaps with previous, merge them"],
        "solutions": [{"language": "python", "code": "def merge(intervals):\n    intervals.sort(key=lambda x: x[0])\n    merged = [intervals[0]]\n    for start, end in intervals[1:]:\n        if start <= merged[-1][1]:\n            merged[-1][1] = max(merged[-1][1], end)\n        else:\n            merged.append([start, end])\n    return merged"}],
        "xp_reward": 75, "order": 9,
    },
    {
        "title": "Trapping Rain Water",
        "slug": "trapping-rain-water",
        "description": """Given `n` non-negative integers representing an elevation map where the width of each bar is `1`, compute how much water it can trap after raining.""",
        "difficulty": "hard",
        "topics": ["Arrays", "Dynamic Programming", "Two Pointers"],
        "companies": ["Amazon", "Google", "Microsoft", "Facebook"],
        "input_format": "Array of non-negative integers representing heights",
        "output_format": "Total units of trapped water",
        "constraints": "n == height.length\n1 <= n <= 2 * 10^4\n0 <= height[i] <= 10^5",
        "examples": [
            {"input": "height = [0,1,0,2,1,0,1,3,2,1,2,1]", "output": "6"},
            {"input": "height = [4,2,0,3,2,5]", "output": "9"},
        ],
        "test_cases": [
            {"input": "0 1 0 2 1 0 1 3 2 1 2 1", "expected_output": "6", "is_hidden": False},
            {"input": "4 2 0 3 2 5", "expected_output": "9", "is_hidden": True},
        ],
        "hints": ["Two pointer approach: left and right", "Water at i = min(max_left, max_right) - height[i]"],
        "solutions": [{"language": "python", "code": "def trap(height):\n    left, right = 0, len(height) - 1\n    left_max = right_max = water = 0\n    while left < right:\n        if height[left] < height[right]:\n            if height[left] >= left_max:\n                left_max = height[left]\n            else:\n                water += left_max - height[left]\n            left += 1\n        else:\n            if height[right] >= right_max:\n                right_max = height[right]\n            else:\n                water += right_max - height[right]\n            right -= 1\n    return water"}],
        "xp_reward": 100, "order": 10,
    },
    # --- 25 additional problems (orders 11-35) ---
    {
        "title": "Contains Duplicate",
        "slug": "contains-duplicate",
        "description": "Given an integer array `nums`, return `true` if any value appears at least twice in the array, and return `false` if every element is distinct.",
        "difficulty": "easy",
        "topics": ["Arrays", "Hashing"],
        "companies": ["Amazon", "Microsoft", "TCS", "Infosys"],
        "input_format": "An array of integers",
        "output_format": "Boolean true or false",
        "constraints": "1 <= nums.length <= 10^5\n-10^9 <= nums[i] <= 10^9",
        "examples": [
            {"input": "nums = [1,2,3,1]", "output": "true", "explanation": "1 appears twice."},
            {"input": "nums = [1,2,3,4]", "output": "false"},
        ],
        "test_cases": [
            {"input": "1 2 3 1", "expected_output": "true", "is_hidden": False},
            {"input": "1 2 3 4", "expected_output": "false", "is_hidden": False},
            {"input": "1 1 1 3 3 4 3 2 4 2", "expected_output": "true", "is_hidden": True},
        ],
        "hints": ["Use a hash set to track seen numbers"],
        "solutions": [{"language": "python", "code": "def containsDuplicate(nums):\n    return len(nums) != len(set(nums))"}],
        "xp_reward": 50, "order": 11,
    },
    {
        "title": "Valid Anagram",
        "slug": "valid-anagram",
        "description": "Given two strings `s` and `t`, return `true` if `t` is an anagram of `s`, and `false` otherwise.\n\nAn anagram is a word or phrase formed by rearranging the letters of a different word or phrase.",
        "difficulty": "easy",
        "topics": ["Strings", "Hashing"],
        "companies": ["Google", "Microsoft", "Amazon"],
        "input_format": "Two strings s and t",
        "output_format": "Boolean true or false",
        "constraints": "1 <= s.length, t.length <= 5 * 10^4\ns and t consist of lowercase English letters.",
        "examples": [
            {"input": "s = 'anagram', t = 'nagaram'", "output": "true"},
            {"input": "s = 'rat', t = 'car'", "output": "false"},
        ],
        "test_cases": [
            {"input": "anagram\nnagaram", "expected_output": "true", "is_hidden": False},
            {"input": "rat\ncar", "expected_output": "false", "is_hidden": False},
        ],
        "hints": ["Sort both strings and compare", "Or use a frequency counter (hash map)"],
        "solutions": [{"language": "python", "code": "from collections import Counter\ndef isAnagram(s, t):\n    return Counter(s) == Counter(t)"}],
        "xp_reward": 50, "order": 12,
    },
    {
        "title": "Best Time to Buy and Sell Stock",
        "slug": "best-time-to-buy-and-sell-stock",
        "description": "You are given an array `prices` where `prices[i]` is the price of a given stock on the `i`th day.\n\nYou want to maximize your profit by choosing a single day to buy one stock and choosing a different day in the future to sell that stock.\n\nReturn the maximum profit you can achieve from this transaction. If you cannot achieve any profit, return `0`.",
        "difficulty": "easy",
        "topics": ["Arrays", "Sliding Window"],
        "companies": ["Amazon", "Microsoft", "Google", "TCS", "Wipro"],
        "input_format": "An array of stock prices",
        "output_format": "Maximum profit as integer",
        "constraints": "1 <= prices.length <= 10^5\n0 <= prices[i] <= 10^4",
        "examples": [
            {"input": "prices = [7,1,5,3,6,4]", "output": "5", "explanation": "Buy on day 2 (price=1), sell on day 5 (price=6). Profit = 6-1 = 5."},
            {"input": "prices = [7,6,4,3,1]", "output": "0", "explanation": "No transaction gives profit."},
        ],
        "test_cases": [
            {"input": "7 1 5 3 6 4", "expected_output": "5", "is_hidden": False},
            {"input": "7 6 4 3 1", "expected_output": "0", "is_hidden": False},
        ],
        "hints": ["Track the minimum price seen so far", "At each step, calculate profit if you sold today"],
        "solutions": [{"language": "python", "code": "def maxProfit(prices):\n    min_price = float('inf')\n    max_profit = 0\n    for p in prices:\n        min_price = min(min_price, p)\n        max_profit = max(max_profit, p - min_price)\n    return max_profit"}],
        "xp_reward": 50, "order": 13,
    },
    {
        "title": "Reverse String",
        "slug": "reverse-string",
        "description": "Write a function that reverses a string. The input is given as an array of characters `s`.\n\nYou must do this by modifying the input array in-place with O(1) extra memory.",
        "difficulty": "easy",
        "topics": ["Strings", "Two Pointers"],
        "companies": ["Amazon", "TCS", "Infosys"],
        "input_format": "Array of characters",
        "output_format": "The reversed array (in-place)",
        "constraints": "1 <= s.length <= 10^5\ns[i] is a printable ASCII character.",
        "examples": [
            {"input": "s = ['h','e','l','l','o']", "output": "['o','l','l','e','h']"},
            {"input": "s = ['H','a','n','n','a','h']", "output": "['h','a','n','n','a','H']"},
        ],
        "test_cases": [
            {"input": "hello", "expected_output": "olleh", "is_hidden": False},
            {"input": "Hannah", "expected_output": "hannaH", "is_hidden": False},
        ],
        "hints": ["Use two pointers from both ends", "Swap characters moving inward"],
        "solutions": [{"language": "python", "code": "def reverseString(s):\n    left, right = 0, len(s) - 1\n    while left < right:\n        s[left], s[right] = s[right], s[left]\n        left += 1\n        right -= 1"}],
        "xp_reward": 50, "order": 14,
    },
    {
        "title": "Single Number",
        "slug": "single-number",
        "description": "Given a non-empty array of integers `nums`, every element appears twice except for one. Find that single one.\n\nYou must implement a solution with O(n) runtime complexity and O(1) extra space.",
        "difficulty": "easy",
        "topics": ["Arrays", "Bit Manipulation"],
        "companies": ["Amazon", "Google", "Microsoft"],
        "input_format": "Array of integers",
        "output_format": "The single integer",
        "constraints": "1 <= nums.length <= 3 * 10^4\n-3 * 10^4 <= nums[i] <= 3 * 10^4\nEach element appears twice except for one.",
        "examples": [
            {"input": "nums = [2,2,1]", "output": "1"},
            {"input": "nums = [4,1,2,1,2]", "output": "4"},
        ],
        "test_cases": [
            {"input": "2 2 1", "expected_output": "1", "is_hidden": False},
            {"input": "4 1 2 1 2", "expected_output": "4", "is_hidden": False},
        ],
        "hints": ["XOR of a number with itself is 0", "XOR of a number with 0 is the number itself"],
        "solutions": [{"language": "python", "code": "def singleNumber(nums):\n    result = 0\n    for n in nums:\n        result ^= n\n    return result"}],
        "xp_reward": 50, "order": 15,
    },
    {
        "title": "Move Zeroes",
        "slug": "move-zeroes",
        "description": "Given an integer array `nums`, move all `0`'s to the end of it while maintaining the relative order of the non-zero elements.\n\nNote that you must do this in-place without making a copy of the array.",
        "difficulty": "easy",
        "topics": ["Arrays", "Two Pointers"],
        "companies": ["Facebook", "Amazon", "Microsoft"],
        "input_format": "Array of integers",
        "output_format": "Modified array with zeros at end",
        "constraints": "1 <= nums.length <= 10^4\n-2^31 <= nums[i] <= 2^31 - 1",
        "examples": [
            {"input": "nums = [0,1,0,3,12]", "output": "[1,3,12,0,0]"},
            {"input": "nums = [0]", "output": "[0]"},
        ],
        "test_cases": [
            {"input": "0 1 0 3 12", "expected_output": "1 3 12 0 0", "is_hidden": False},
            {"input": "0", "expected_output": "0", "is_hidden": False},
        ],
        "hints": ["Use a slow pointer for the position to place next non-zero"],
        "solutions": [{"language": "python", "code": "def moveZeroes(nums):\n    pos = 0\n    for n in nums:\n        if n != 0:\n            nums[pos] = n\n            pos += 1\n    for i in range(pos, len(nums)):\n        nums[i] = 0"}],
        "xp_reward": 50, "order": 16,
    },
    {
        "title": "Missing Number",
        "slug": "missing-number",
        "description": "Given an array `nums` containing `n` distinct numbers in the range `[0, n]`, return the only number in the range that is missing from the array.",
        "difficulty": "easy",
        "topics": ["Arrays", "Math", "Bit Manipulation"],
        "companies": ["Microsoft", "Amazon", "TCS"],
        "input_format": "Array of n distinct integers in range [0, n]",
        "output_format": "The missing integer",
        "constraints": "n == nums.length\n1 <= n <= 10^4\n0 <= nums[i] <= n\nAll nums are unique.",
        "examples": [
            {"input": "nums = [3,0,1]", "output": "2"},
            {"input": "nums = [0,1]", "output": "2"},
        ],
        "test_cases": [
            {"input": "3 0 1", "expected_output": "2", "is_hidden": False},
            {"input": "0 1", "expected_output": "2", "is_hidden": False},
        ],
        "hints": ["Sum of [0..n] is n*(n+1)/2", "Subtract the actual sum from expected sum"],
        "solutions": [{"language": "python", "code": "def missingNumber(nums):\n    n = len(nums)\n    return n * (n + 1) // 2 - sum(nums)"}],
        "xp_reward": 50, "order": 17,
    },
    {
        "title": "Majority Element",
        "slug": "majority-element",
        "description": "Given an array `nums` of size `n`, return the majority element.\n\nThe majority element is the element that appears more than `⌊n / 2⌋` times. You may assume that the majority element always exists in the array.",
        "difficulty": "easy",
        "topics": ["Arrays", "Hashing", "Divide and Conquer"],
        "companies": ["Amazon", "Microsoft", "Google"],
        "input_format": "Array of integers",
        "output_format": "The majority element",
        "constraints": "n == nums.length\n1 <= n <= 5 * 10^4\n-10^9 <= nums[i] <= 10^9",
        "examples": [
            {"input": "nums = [3,2,3]", "output": "3"},
            {"input": "nums = [2,2,1,1,1,2,2]", "output": "2"},
        ],
        "test_cases": [
            {"input": "3 2 3", "expected_output": "3", "is_hidden": False},
            {"input": "2 2 1 1 1 2 2", "expected_output": "2", "is_hidden": False},
        ],
        "hints": ["Boyer-Moore Voting Algorithm: maintain a candidate and count", "When count reaches 0, update candidate"],
        "solutions": [{"language": "python", "code": "def majorityElement(nums):\n    candidate, count = None, 0\n    for n in nums:\n        if count == 0:\n            candidate = n\n        count += 1 if n == candidate else -1\n    return candidate"}],
        "xp_reward": 50, "order": 18,
    },
    {
        "title": "Longest Common Prefix",
        "slug": "longest-common-prefix",
        "description": "Write a function to find the longest common prefix string amongst an array of strings.\n\nIf there is no common prefix, return an empty string `\"\"`.",
        "difficulty": "easy",
        "topics": ["Strings"],
        "companies": ["Google", "Amazon", "TCS", "Infosys"],
        "input_format": "Array of strings",
        "output_format": "Longest common prefix string",
        "constraints": "1 <= strs.length <= 200\n0 <= strs[i].length <= 200\nstrs[i] consists of only lowercase English letters.",
        "examples": [
            {"input": "strs = ['flower','flow','flight']", "output": "'fl'"},
            {"input": "strs = ['dog','racecar','car']", "output": "''"},
        ],
        "test_cases": [
            {"input": "flower flow flight", "expected_output": "fl", "is_hidden": False},
            {"input": "dog racecar car", "expected_output": "", "is_hidden": False},
        ],
        "hints": ["Sort the array, then compare first and last strings"],
        "solutions": [{"language": "python", "code": "def longestCommonPrefix(strs):\n    if not strs: return ''\n    prefix = strs[0]\n    for s in strs[1:]:\n        while not s.startswith(prefix):\n            prefix = prefix[:-1]\n            if not prefix: return ''\n    return prefix"}],
        "xp_reward": 50, "order": 19,
    },
    {
        "title": "Palindrome Number",
        "slug": "palindrome-number",
        "description": "Given an integer `x`, return `true` if `x` is a palindrome, and `false` otherwise.\n\nA palindrome is a number that reads the same backward as forward.",
        "difficulty": "easy",
        "topics": ["Math"],
        "companies": ["Amazon", "TCS", "Wipro", "Capgemini"],
        "input_format": "Integer x",
        "output_format": "Boolean true or false",
        "constraints": "-2^31 <= x <= 2^31 - 1",
        "examples": [
            {"input": "x = 121", "output": "true"},
            {"input": "x = -121", "output": "false", "explanation": "Negative numbers are not palindromes."},
            {"input": "x = 10", "output": "false"},
        ],
        "test_cases": [
            {"input": "121", "expected_output": "true", "is_hidden": False},
            {"input": "-121", "expected_output": "false", "is_hidden": False},
            {"input": "10", "expected_output": "false", "is_hidden": True},
        ],
        "hints": ["Convert to string and check if it equals its reverse", "Negative numbers are never palindromes"],
        "solutions": [{"language": "python", "code": "def isPalindrome(x):\n    if x < 0: return False\n    s = str(x)\n    return s == s[::-1]"}],
        "xp_reward": 50, "order": 20,
    },
    {
        "title": "Linked List Cycle",
        "slug": "linked-list-cycle",
        "description": "Given `head`, the head of a linked list, determine if the linked list has a cycle in it.\n\nThere is a cycle in a linked list if there is some node in the list that can be reached again by continuously following the `next` pointer.",
        "difficulty": "easy",
        "topics": ["Linked Lists", "Two Pointers"],
        "companies": ["Amazon", "Google", "Microsoft", "TCS"],
        "input_format": "Head of a linked list",
        "output_format": "Boolean true if cycle exists",
        "constraints": "The number of nodes is in the range [0, 10^4].\n-10^5 <= Node.val <= 10^5",
        "examples": [
            {"input": "head = [3,2,0,-4], pos = 1", "output": "true", "explanation": "There is a cycle where tail connects to node index 1."},
            {"input": "head = [1], pos = -1", "output": "false"},
        ],
        "test_cases": [
            {"input": "3 2 0 -4\n1", "expected_output": "true", "is_hidden": False},
            {"input": "1\n-1", "expected_output": "false", "is_hidden": False},
        ],
        "hints": ["Floyd's cycle detection: slow and fast pointers", "If fast ever equals slow, there's a cycle"],
        "solutions": [{"language": "python", "code": "def hasCycle(head):\n    slow = fast = head\n    while fast and fast.next:\n        slow = slow.next\n        fast = fast.next.next\n        if slow == fast:\n            return True\n    return False"}],
        "xp_reward": 50, "order": 21,
    },
    {
        "title": "3Sum",
        "slug": "3sum",
        "description": "Given an integer array `nums`, return all the triplets `[nums[i], nums[j], nums[k]]` such that `i != j`, `i != k`, `j != k`, and `nums[i] + nums[j] + nums[k] == 0`.\n\nThe solution set must not contain duplicate triplets.",
        "difficulty": "medium",
        "topics": ["Arrays", "Two Pointers", "Sorting"],
        "companies": ["Amazon", "Google", "Microsoft", "Facebook"],
        "input_format": "An array of integers",
        "output_format": "List of unique triplets that sum to zero",
        "constraints": "3 <= nums.length <= 3000\n-10^5 <= nums[i] <= 10^5",
        "examples": [
            {"input": "nums = [-1,0,1,2,-1,-4]", "output": "[[-1,-1,2],[-1,0,1]]"},
            {"input": "nums = [0,1,1]", "output": "[]"},
        ],
        "test_cases": [
            {"input": "-1 0 1 2 -1 -4", "expected_output": "[[-1,-1,2],[-1,0,1]]", "is_hidden": False},
            {"input": "0 0 0", "expected_output": "[[0,0,0]]", "is_hidden": False},
        ],
        "hints": ["Sort the array first", "Fix one element and use two pointers for the rest", "Skip duplicates to avoid duplicate triplets"],
        "solutions": [{"language": "python", "code": "def threeSum(nums):\n    nums.sort()\n    result = []\n    for i in range(len(nums) - 2):\n        if i > 0 and nums[i] == nums[i-1]:\n            continue\n        left, right = i + 1, len(nums) - 1\n        while left < right:\n            s = nums[i] + nums[left] + nums[right]\n            if s == 0:\n                result.append([nums[i], nums[left], nums[right]])\n                while left < right and nums[left] == nums[left+1]: left += 1\n                while left < right and nums[right] == nums[right-1]: right -= 1\n                left += 1; right -= 1\n            elif s < 0: left += 1\n            else: right -= 1\n    return result"}],
        "xp_reward": 75, "order": 22,
    },
    {
        "title": "Longest Substring Without Repeating Characters",
        "slug": "longest-substring-without-repeating-characters",
        "description": "Given a string `s`, find the length of the longest substring without repeating characters.",
        "difficulty": "medium",
        "topics": ["Strings", "Sliding Window", "Hashing"],
        "companies": ["Amazon", "Google", "Microsoft", "Facebook", "TCS"],
        "input_format": "A string s",
        "output_format": "Length of longest substring without repeats",
        "constraints": "0 <= s.length <= 5 * 10^4\ns consists of English letters, digits, symbols and spaces.",
        "examples": [
            {"input": "s = 'abcabcbb'", "output": "3", "explanation": "The answer is 'abc' with length 3."},
            {"input": "s = 'bbbbb'", "output": "1"},
            {"input": "s = 'pwwkew'", "output": "3"},
        ],
        "test_cases": [
            {"input": "abcabcbb", "expected_output": "3", "is_hidden": False},
            {"input": "bbbbb", "expected_output": "1", "is_hidden": False},
        ],
        "hints": ["Sliding window with a set or dict", "When duplicate found, shrink window from left"],
        "solutions": [{"language": "python", "code": "def lengthOfLongestSubstring(s):\n    char_index = {}\n    left = max_len = 0\n    for right, ch in enumerate(s):\n        if ch in char_index and char_index[ch] >= left:\n            left = char_index[ch] + 1\n        char_index[ch] = right\n        max_len = max(max_len, right - left + 1)\n    return max_len"}],
        "xp_reward": 75, "order": 23,
    },
    {
        "title": "Product of Array Except Self",
        "slug": "product-of-array-except-self",
        "description": "Given an integer array `nums`, return an array `answer` such that `answer[i]` is equal to the product of all the elements of `nums` except `nums[i]`.\n\nThe product of any prefix or suffix of `nums` is guaranteed to fit in a 32-bit integer.\n\nYou must write an algorithm that runs in O(n) time and without using the division operation.",
        "difficulty": "medium",
        "topics": ["Arrays", "Prefix Sum"],
        "companies": ["Amazon", "Microsoft", "Google", "Facebook"],
        "input_format": "An array of integers",
        "output_format": "Array where each element is product of all others",
        "constraints": "2 <= nums.length <= 10^5\n-30 <= nums[i] <= 30\nThe product fits in a 32-bit integer.",
        "examples": [
            {"input": "nums = [1,2,3,4]", "output": "[24,12,8,6]"},
            {"input": "nums = [-1,1,0,-3,3]", "output": "[0,0,9,0,0]"},
        ],
        "test_cases": [
            {"input": "1 2 3 4", "expected_output": "24 12 8 6", "is_hidden": False},
            {"input": "-1 1 0 -3 3", "expected_output": "0 0 9 0 0", "is_hidden": False},
        ],
        "hints": ["Build prefix products from left, then suffix products from right"],
        "solutions": [{"language": "python", "code": "def productExceptSelf(nums):\n    n = len(nums)\n    res = [1] * n\n    prefix = 1\n    for i in range(n):\n        res[i] = prefix\n        prefix *= nums[i]\n    suffix = 1\n    for i in range(n-1, -1, -1):\n        res[i] *= suffix\n        suffix *= nums[i]\n    return res"}],
        "xp_reward": 75, "order": 24,
    },
    {
        "title": "Group Anagrams",
        "slug": "group-anagrams",
        "description": "Given an array of strings `strs`, group the anagrams together. You can return the answer in any order.\n\nAn anagram is a word or phrase formed by rearranging the letters of a different word or phrase, typically using all the original letters exactly once.",
        "difficulty": "medium",
        "topics": ["Strings", "Hashing", "Sorting"],
        "companies": ["Amazon", "Google", "Microsoft", "Facebook"],
        "input_format": "Array of strings",
        "output_format": "List of groups of anagrams",
        "constraints": "1 <= strs.length <= 10^4\n0 <= strs[i].length <= 100\nstrs[i] consists of lowercase English letters.",
        "examples": [
            {"input": "strs = ['eat','tea','tan','ate','nat','bat']", "output": "[['bat'],['nat','tan'],['ate','eat','tea']]"},
            {"input": "strs = ['']", "output": "[['']]"},
        ],
        "test_cases": [
            {"input": "eat tea tan ate nat bat", "expected_output": "[['bat'],['nat','tan'],['ate','eat','tea']]", "is_hidden": False},
        ],
        "hints": ["Sort each string as a key", "Use defaultdict(list) to group strings by sorted key"],
        "solutions": [{"language": "python", "code": "from collections import defaultdict\ndef groupAnagrams(strs):\n    groups = defaultdict(list)\n    for s in strs:\n        groups[tuple(sorted(s))].append(s)\n    return list(groups.values())"}],
        "xp_reward": 75, "order": 25,
    },
    {
        "title": "Container With Most Water",
        "slug": "container-with-most-water",
        "description": "You are given an integer array `height` of length `n`. There are `n` vertical lines drawn such that the two endpoints of the `i`th line are `(i, 0)` and `(i, height[i])`.\n\nFind two lines that together with the x-axis form a container, such that the container contains the most water.\n\nReturn the maximum amount of water a container can store.",
        "difficulty": "medium",
        "topics": ["Arrays", "Two Pointers", "Greedy"],
        "companies": ["Amazon", "Google", "Microsoft", "Bloomberg"],
        "input_format": "Array of heights",
        "output_format": "Maximum area of water",
        "constraints": "n == height.length\n2 <= n <= 10^5\n0 <= height[i] <= 10^4",
        "examples": [
            {"input": "height = [1,8,6,2,5,4,8,3,7]", "output": "49"},
            {"input": "height = [1,1]", "output": "1"},
        ],
        "test_cases": [
            {"input": "1 8 6 2 5 4 8 3 7", "expected_output": "49", "is_hidden": False},
            {"input": "1 1", "expected_output": "1", "is_hidden": False},
        ],
        "hints": ["Use two pointers from both ends", "Move the pointer with smaller height inward"],
        "solutions": [{"language": "python", "code": "def maxArea(height):\n    left, right = 0, len(height) - 1\n    max_water = 0\n    while left < right:\n        water = min(height[left], height[right]) * (right - left)\n        max_water = max(max_water, water)\n        if height[left] < height[right]:\n            left += 1\n        else:\n            right -= 1\n    return max_water"}],
        "xp_reward": 75, "order": 26,
    },
    {
        "title": "Coin Change",
        "slug": "coin-change",
        "description": "You are given an integer array `coins` representing coins of different denominations and an integer `amount` representing a total amount of money.\n\nReturn the fewest number of coins that you need to make up that amount. If that amount of money cannot be made up by any combination of the coins, return `-1`.\n\nYou may assume that you have an infinite number of each kind of coin.",
        "difficulty": "medium",
        "topics": ["Dynamic Programming"],
        "companies": ["Amazon", "Google", "Microsoft", "Goldman Sachs"],
        "input_format": "Array of coin denominations and target amount",
        "output_format": "Minimum number of coins or -1",
        "constraints": "1 <= coins.length <= 12\n1 <= coins[i] <= 2^31 - 1\n0 <= amount <= 10^4",
        "examples": [
            {"input": "coins = [1,5,11], amount = 15", "output": "3", "explanation": "11+1+1+1 = 15... but 5+5+5=15 is 3 coins."},
            {"input": "coins = [2], amount = 3", "output": "-1"},
        ],
        "test_cases": [
            {"input": "1 5 11\n15", "expected_output": "3", "is_hidden": False},
            {"input": "2\n3", "expected_output": "-1", "is_hidden": False},
        ],
        "hints": ["Bottom-up DP: dp[i] = min coins to make amount i", "dp[0] = 0, dp[i] = min(dp[i-coin]+1) for each coin"],
        "solutions": [{"language": "python", "code": "def coinChange(coins, amount):\n    dp = [float('inf')] * (amount + 1)\n    dp[0] = 0\n    for i in range(1, amount + 1):\n        for coin in coins:\n            if coin <= i:\n                dp[i] = min(dp[i], dp[i - coin] + 1)\n    return dp[amount] if dp[amount] != float('inf') else -1"}],
        "xp_reward": 75, "order": 27,
    },
    {
        "title": "House Robber",
        "slug": "house-robber",
        "description": "You are a professional robber planning to rob houses along a street. Each house has a certain amount of money stashed. The only constraint stopping you is that adjacent houses have security systems connected, and it will automatically contact the police if two adjacent houses were broken into on the same night.\n\nGiven an integer array `nums` representing the amount of money of each house, return the maximum amount of money you can rob tonight without alerting the police.",
        "difficulty": "medium",
        "topics": ["Dynamic Programming"],
        "companies": ["Amazon", "Microsoft", "Google", "TCS"],
        "input_format": "Array of house values",
        "output_format": "Maximum money you can rob",
        "constraints": "1 <= nums.length <= 100\n0 <= nums[i] <= 400",
        "examples": [
            {"input": "nums = [1,2,3,1]", "output": "4", "explanation": "Rob house 1 (1) then house 3 (3). Total = 4."},
            {"input": "nums = [2,7,9,3,1]", "output": "12"},
        ],
        "test_cases": [
            {"input": "1 2 3 1", "expected_output": "4", "is_hidden": False},
            {"input": "2 7 9 3 1", "expected_output": "12", "is_hidden": False},
        ],
        "hints": ["At each house: rob it (prev_prev + curr) or skip (prev)", "Only two states needed"],
        "solutions": [{"language": "python", "code": "def rob(nums):\n    prev2, prev1 = 0, 0\n    for n in nums:\n        prev2, prev1 = prev1, max(prev1, prev2 + n)\n    return prev1"}],
        "xp_reward": 75, "order": 28,
    },
    {
        "title": "Search in Rotated Sorted Array",
        "slug": "search-in-rotated-sorted-array",
        "description": "There is an integer array `nums` sorted in ascending order (with distinct values). Prior to being passed to your function, `nums` is possibly rotated at an unknown pivot index `k`.\n\nGiven the array `nums` after the possible rotation and an integer `target`, return the index of `target` if it is in `nums`, or `-1` if it is not in `nums`.\n\nYou must write an algorithm with O(log n) runtime complexity.",
        "difficulty": "medium",
        "topics": ["Binary Search", "Arrays"],
        "companies": ["Amazon", "Google", "Microsoft", "Facebook"],
        "input_format": "A rotated sorted array and a target",
        "output_format": "Index of target or -1",
        "constraints": "1 <= nums.length <= 5000\n-10^4 <= nums[i] <= 10^4\nAll values in nums are unique.\n-10^4 <= target <= 10^4",
        "examples": [
            {"input": "nums = [4,5,6,7,0,1,2], target = 0", "output": "4"},
            {"input": "nums = [4,5,6,7,0,1,2], target = 3", "output": "-1"},
        ],
        "test_cases": [
            {"input": "4 5 6 7 0 1 2\n0", "expected_output": "4", "is_hidden": False},
            {"input": "4 5 6 7 0 1 2\n3", "expected_output": "-1", "is_hidden": False},
        ],
        "hints": ["Modified binary search: determine which half is sorted", "Check if target lies in the sorted half"],
        "solutions": [{"language": "python", "code": "def search(nums, target):\n    left, right = 0, len(nums) - 1\n    while left <= right:\n        mid = (left + right) // 2\n        if nums[mid] == target: return mid\n        if nums[left] <= nums[mid]:\n            if nums[left] <= target < nums[mid]:\n                right = mid - 1\n            else:\n                left = mid + 1\n        else:\n            if nums[mid] < target <= nums[right]:\n                left = mid + 1\n            else:\n                right = mid - 1\n    return -1"}],
        "xp_reward": 75, "order": 29,
    },
    {
        "title": "Validate Binary Search Tree",
        "slug": "validate-binary-search-tree",
        "description": "Given the `root` of a binary tree, determine if it is a valid binary search tree (BST).\n\nA valid BST is defined as follows:\n- The left subtree of a node contains only nodes with keys less than the node's key.\n- The right subtree of a node contains only nodes with keys greater than the node's key.\n- Both the left and right subtrees must also be binary search trees.",
        "difficulty": "medium",
        "topics": ["Trees", "Binary Search Tree", "DFS"],
        "companies": ["Amazon", "Google", "Microsoft", "Facebook"],
        "input_format": "Root of a binary tree",
        "output_format": "Boolean true if valid BST",
        "constraints": "The number of nodes is in the range [1, 10^4].\n-2^31 <= Node.val <= 2^31 - 1",
        "examples": [
            {"input": "root = [2,1,3]", "output": "true"},
            {"input": "root = [5,1,4,null,null,3,6]", "output": "false", "explanation": "The root node's value is 5 but its right child's value is 4."},
        ],
        "test_cases": [
            {"input": "2 1 3", "expected_output": "true", "is_hidden": False},
            {"input": "5 1 4 null null 3 6", "expected_output": "false", "is_hidden": False},
        ],
        "hints": ["Pass min/max bounds during recursion", "Each node must be within (min, max) range"],
        "solutions": [{"language": "python", "code": "def isValidBST(root, min_val=float('-inf'), max_val=float('inf')):\n    if not root: return True\n    if not (min_val < root.val < max_val): return False\n    return isValidBST(root.left, min_val, root.val) and isValidBST(root.right, root.val, max_val)"}],
        "xp_reward": 75, "order": 30,
    },
    {
        "title": "Combination Sum",
        "slug": "combination-sum",
        "description": "Given an array of distinct integers `candidates` and a target integer `target`, return a list of all unique combinations of `candidates` where the chosen numbers sum to `target`. You may return the combinations in any order.\n\nThe same number may be chosen from `candidates` an unlimited number of times. Two combinations are unique if the frequency of at least one of the chosen numbers is different.",
        "difficulty": "medium",
        "topics": ["Backtracking", "Arrays"],
        "companies": ["Amazon", "Google", "Facebook", "Microsoft"],
        "input_format": "Array of candidates and target",
        "output_format": "All unique combinations that sum to target",
        "constraints": "1 <= candidates.length <= 30\n2 <= candidates[i] <= 40\nAll candidates are distinct.\n1 <= target <= 40",
        "examples": [
            {"input": "candidates = [2,3,6,7], target = 7", "output": "[[2,2,3],[7]]"},
            {"input": "candidates = [2,3,5], target = 8", "output": "[[2,2,2,2],[2,3,3],[3,5]]"},
        ],
        "test_cases": [
            {"input": "2 3 6 7\n7", "expected_output": "[[2,2,3],[7]]", "is_hidden": False},
        ],
        "hints": ["Backtracking: include current candidate (can reuse) or move to next", "Sort candidates to prune early"],
        "solutions": [{"language": "python", "code": "def combinationSum(candidates, target):\n    result = []\n    def backtrack(start, current, remaining):\n        if remaining == 0:\n            result.append(current[:])\n            return\n        for i in range(start, len(candidates)):\n            if candidates[i] > remaining: break\n            current.append(candidates[i])\n            backtrack(i, current, remaining - candidates[i])\n            current.pop()\n    candidates.sort()\n    backtrack(0, [], target)\n    return result"}],
        "xp_reward": 75, "order": 31,
    },
    {
        "title": "Top K Frequent Elements",
        "slug": "top-k-frequent-elements",
        "description": "Given an integer array `nums` and an integer `k`, return the `k` most frequent elements. You may return the answer in any order.",
        "difficulty": "medium",
        "topics": ["Arrays", "Hashing", "Heap", "Sorting"],
        "companies": ["Amazon", "Google", "Facebook", "Microsoft"],
        "input_format": "An array of integers and k",
        "output_format": "Array of k most frequent elements",
        "constraints": "1 <= nums.length <= 10^5\n-10^4 <= nums[i] <= 10^4\nk is in the range [1, the number of unique elements].",
        "examples": [
            {"input": "nums = [1,1,1,2,2,3], k = 2", "output": "[1,2]"},
            {"input": "nums = [1], k = 1", "output": "[1]"},
        ],
        "test_cases": [
            {"input": "1 1 1 2 2 3\n2", "expected_output": "1 2", "is_hidden": False},
        ],
        "hints": ["Use a hash map to count frequencies", "Use a heap of size k or bucket sort"],
        "solutions": [{"language": "python", "code": "from collections import Counter\nimport heapq\ndef topKFrequent(nums, k):\n    count = Counter(nums)\n    return heapq.nlargest(k, count.keys(), key=count.get)"}],
        "xp_reward": 75, "order": 32,
    },
    {
        "title": "Subsets",
        "slug": "subsets",
        "description": "Given an integer array `nums` of unique elements, return all possible subsets (the power set).\n\nThe solution set must not contain duplicate subsets. Return the solution in any order.",
        "difficulty": "medium",
        "topics": ["Backtracking", "Arrays", "Bit Manipulation"],
        "companies": ["Amazon", "Google", "Facebook", "Microsoft"],
        "input_format": "Array of unique integers",
        "output_format": "All possible subsets",
        "constraints": "1 <= nums.length <= 10\n-10 <= nums[i] <= 10\nAll the numbers are unique.",
        "examples": [
            {"input": "nums = [1,2,3]", "output": "[[],[1],[2],[1,2],[3],[1,3],[2,3],[1,2,3]]"},
            {"input": "nums = [0]", "output": "[[],[0]]"},
        ],
        "test_cases": [
            {"input": "1 2 3", "expected_output": "[[],[1],[2],[1,2],[3],[1,3],[2,3],[1,2,3]]", "is_hidden": False},
        ],
        "hints": ["Start with empty set", "For each number, add it to existing subsets to create new ones"],
        "solutions": [{"language": "python", "code": "def subsets(nums):\n    result = [[]]\n    for n in nums:\n        result += [sub + [n] for sub in result]\n    return result"}],
        "xp_reward": 75, "order": 33,
    },
    {
        "title": "Minimum Window Substring",
        "slug": "minimum-window-substring",
        "description": "Given two strings `s` and `t` of lengths `m` and `n` respectively, return the minimum window substring of `s` such that every character in `t` (including duplicates) is included in the window. If there is no such substring, return the empty string `\"\"`.",
        "difficulty": "hard",
        "topics": ["Strings", "Sliding Window", "Hashing"],
        "companies": ["Amazon", "Google", "Facebook", "Microsoft"],
        "input_format": "Two strings s and t",
        "output_format": "Minimum window substring",
        "constraints": "m == s.length\nn == t.length\n1 <= m, n <= 10^5\ns and t consist of uppercase and lowercase English letters.",
        "examples": [
            {"input": "s = 'ADOBECODEBANC', t = 'ABC'", "output": "'BANC'"},
            {"input": "s = 'a', t = 'a'", "output": "'a'"},
        ],
        "test_cases": [
            {"input": "ADOBECODEBANC\nABC", "expected_output": "BANC", "is_hidden": False},
            {"input": "a\na", "expected_output": "a", "is_hidden": False},
        ],
        "hints": ["Sliding window with two frequency maps", "Expand right until window is valid, contract left to minimize"],
        "solutions": [{"language": "python", "code": "from collections import Counter\ndef minWindow(s, t):\n    need = Counter(t)\n    have, required = 0, len(need)\n    window = {}\n    res, res_len = [-1, -1], float('inf')\n    left = 0\n    for right, c in enumerate(s):\n        window[c] = window.get(c, 0) + 1\n        if c in need and window[c] == need[c]:\n            have += 1\n        while have == required:\n            if (right - left + 1) < res_len:\n                res = [left, right]\n                res_len = right - left + 1\n            window[s[left]] -= 1\n            if s[left] in need and window[s[left]] < need[s[left]]:\n                have -= 1\n            left += 1\n    l, r = res\n    return s[l:r+1] if res_len != float('inf') else ''"}],
        "xp_reward": 100, "order": 34,
    },
    {
        "title": "Word Search",
        "slug": "word-search",
        "description": "Given an `m x n` grid of characters `board` and a string `word`, return `true` if `word` exists in the grid.\n\nThe word can be constructed from letters of sequentially adjacent cells, where adjacent cells are horizontally or vertically neighboring. The same letter cell may not be used more than once.",
        "difficulty": "medium",
        "topics": ["Backtracking", "DFS", "Arrays"],
        "companies": ["Amazon", "Google", "Microsoft", "Facebook"],
        "input_format": "2D grid of characters and a target word",
        "output_format": "Boolean true if word exists",
        "constraints": "m == board.length\nn == board[i].length\n1 <= m, n <= 6\n1 <= word.length <= 15\nboard and word consist of only lowercase and uppercase English letters.",
        "examples": [
            {"input": "board = [['A','B','C','E'],['S','F','C','S'],['A','D','E','E']], word = 'ABCCED'", "output": "true"},
            {"input": "board = [['A','B','C','E'],['S','F','C','S'],['A','D','E','E']], word = 'SEE'", "output": "true"},
        ],
        "test_cases": [
            {"input": "ABCE/SFCS/ADEE\nABCCED", "expected_output": "true", "is_hidden": False},
        ],
        "hints": ["DFS from each cell that matches first character", "Mark visited cells, backtrack by restoring"],
        "solutions": [{"language": "python", "code": "def exist(board, word):\n    m, n = len(board), len(board[0])\n    def dfs(r, c, i):\n        if i == len(word): return True\n        if r < 0 or r >= m or c < 0 or c >= n or board[r][c] != word[i]:\n            return False\n        tmp, board[r][c] = board[r][c], '#'\n        found = any(dfs(r+dr, c+dc, i+1) for dr,dc in [(0,1),(0,-1),(1,0),(-1,0)])\n        board[r][c] = tmp\n        return found\n    return any(dfs(r, c, 0) for r in range(m) for c in range(n))"}],
        "xp_reward": 75, "order": 35,
    },
]


APTITUDE_QUESTIONS = [
    # Quantitative
    {
        "question": "A train 150m long passes a pole in 15 seconds. What is the speed of the train in km/h?",
        "options": [{"text": "36 km/h", "is_correct": True}, {"text": "45 km/h"}, {"text": "54 km/h"}, {"text": "30 km/h"}],
        "correct_answer": 0, "explanation": "Speed = 150/15 = 10 m/s = 10 × 18/5 = 36 km/h",
        "category": "quantitative", "subcategory": "Time Speed Distance", "difficulty": "easy",
    },
    {
        "question": "If a product is sold at 20% profit and the cost price is ₹500, find the selling price.",
        "options": [{"text": "₹550"}, {"text": "₹600", "is_correct": True}, {"text": "₹625"}, {"text": "₹575"}],
        "correct_answer": 1, "explanation": "SP = CP × (100 + Profit%) / 100 = 500 × 120/100 = ₹600",
        "category": "quantitative", "subcategory": "Profit & Loss", "difficulty": "easy",
    },
    {
        "question": "A can do a work in 12 days and B can do the same work in 18 days. How many days will they take working together?",
        "options": [{"text": "6 days"}, {"text": "7.2 days", "is_correct": True}, {"text": "8 days"}, {"text": "9 days"}],
        "correct_answer": 1, "explanation": "Together rate = 1/12 + 1/18 = 5/36. Days = 36/5 = 7.2 days",
        "category": "quantitative", "subcategory": "Time & Work", "difficulty": "medium",
    },
    {
        "question": "What is 35% of 280?",
        "options": [{"text": "95"}, {"text": "98", "is_correct": True}, {"text": "100"}, {"text": "105"}],
        "correct_answer": 1, "explanation": "35% of 280 = 35/100 × 280 = 98",
        "category": "quantitative", "subcategory": "Percentages", "difficulty": "easy",
    },
    {
        "question": "The simple interest on ₹8000 at 6% per annum for 3 years is:",
        "options": [{"text": "₹1340"}, {"text": "₹1440", "is_correct": True}, {"text": "₹1540"}, {"text": "₹1240"}],
        "correct_answer": 1, "explanation": "SI = P × R × T / 100 = 8000 × 6 × 3 / 100 = ₹1440",
        "category": "quantitative", "subcategory": "Simple Interest", "difficulty": "easy",
    },
    {
        "question": "In how many ways can a committee of 4 be selected from 8 people?",
        "options": [{"text": "56"}, {"text": "70", "is_correct": True}, {"text": "84"}, {"text": "112"}],
        "correct_answer": 1, "explanation": "C(8,4) = 8!/(4!×4!) = 70",
        "category": "quantitative", "subcategory": "Permutations", "difficulty": "medium",
    },
    {
        "question": "The average of first 50 natural numbers is:",
        "options": [{"text": "25"}, {"text": "25.5", "is_correct": True}, {"text": "26"}, {"text": "24.5"}],
        "correct_answer": 1, "explanation": "Sum of first n natural numbers = n(n+1)/2. Average = (n+1)/2 = 51/2 = 25.5",
        "category": "quantitative", "subcategory": "Averages", "difficulty": "easy",
    },
    {
        "question": "Two dice are rolled. Probability of getting a sum of 7:",
        "options": [{"text": "1/5"}, {"text": "1/6", "is_correct": True}, {"text": "5/36"}, {"text": "7/36"}],
        "correct_answer": 1, "explanation": "Favorable outcomes: (1,6),(2,5),(3,4),(4,3),(5,2),(6,1) = 6. Total = 36. P = 6/36 = 1/6",
        "category": "quantitative", "subcategory": "Probability", "difficulty": "medium",
    },
    {
        "question": "The ratio of A's and B's salary is 3:4. If B's salary is ₹48,000, what is A's salary?",
        "options": [{"text": "₹32,000"}, {"text": "₹36,000", "is_correct": True}, {"text": "₹40,000"}, {"text": "₹28,000"}],
        "correct_answer": 1, "explanation": "A/B = 3/4. A = 3/4 × 48000 = ₹36,000",
        "category": "quantitative", "subcategory": "Ratios", "difficulty": "easy",
    },
    {
        "question": "Find the compound interest on ₹10,000 at 10% per annum for 2 years.",
        "options": [{"text": "₹1,900"}, {"text": "₹2,000"}, {"text": "₹2,100", "is_correct": True}, {"text": "₹2,200"}],
        "correct_answer": 2, "explanation": "CI = P(1+r)^n - P = 10000(1.1)^2 - 10000 = 12100 - 10000 = ₹2100",
        "category": "quantitative", "subcategory": "Compound Interest", "difficulty": "medium",
    },
    # Logical Reasoning
    {
        "question": "Find the next number in the series: 2, 6, 12, 20, 30, ?",
        "options": [{"text": "40"}, {"text": "42", "is_correct": True}, {"text": "44"}, {"text": "36"}],
        "correct_answer": 1, "explanation": "Differences: 4,6,8,10,12. Next = 30+12 = 42. Pattern: n(n+1)",
        "category": "logical", "subcategory": "Number Series", "difficulty": "easy",
    },
    {
        "question": "If A is the brother of B, B is the sister of C, C is the father of D. How is D related to A?",
        "options": [{"text": "Brother"}, {"text": "Sister"}, {"text": "Nephew/Niece", "is_correct": True}, {"text": "Cousin"}],
        "correct_answer": 2, "explanation": "A's sister (B) is father(C)'s sister. D is C's child. So D is A's nephew or niece.",
        "category": "logical", "subcategory": "Blood Relations", "difficulty": "medium",
    },
    {
        "question": "In a code, COMPUTER is written as RFUVQNPC. How is MONITOR written?",
        "options": [{"text": "RMNFUQS"}, {"text": "NPOJUPS"}, {"text": "SQJUPOP"}, {"text": "OPOUJQS", "is_correct": True}],
        "correct_answer": 3, "explanation": "Each letter is shifted by +1 in the alphabet and then reversed.",
        "category": "logical", "subcategory": "Coding-Decoding", "difficulty": "medium",
    },
    {
        "question": "A person walks 4km North, then 3km East. How far is he from the starting point?",
        "options": [{"text": "6 km"}, {"text": "5 km", "is_correct": True}, {"text": "7 km"}, {"text": "4 km"}],
        "correct_answer": 1, "explanation": "Pythagorean theorem: √(4² + 3²) = √(16+9) = √25 = 5 km",
        "category": "logical", "subcategory": "Directions", "difficulty": "easy",
    },
    {
        "question": "All roses are flowers. Some flowers fade quickly. Therefore:",
        "options": [{"text": "All roses fade quickly"}, {"text": "Some roses fade quickly"}, {"text": "No roses fade quickly"}, {"text": "None of the above", "is_correct": True}],
        "correct_answer": 3, "explanation": "We cannot conclude anything definitive about roses fading from these premises.",
        "category": "logical", "subcategory": "Syllogisms", "difficulty": "medium",
    },
    {
        "question": "In a row, if A is 15th from left and 12th from right, how many students are in the row?",
        "options": [{"text": "24"}, {"text": "25"}, {"text": "26", "is_correct": True}, {"text": "27"}],
        "correct_answer": 2, "explanation": "Total = 15 + 12 - 1 = 26",
        "category": "logical", "subcategory": "Seating Arrangement", "difficulty": "easy",
    },
    {
        "question": "Find the missing number: 3, 9, 27, 81, ?",
        "options": [{"text": "162"}, {"text": "243", "is_correct": True}, {"text": "324"}, {"text": "729"}],
        "correct_answer": 1, "explanation": "Series is 3^1, 3^2, 3^3, 3^4, 3^5 = 243",
        "category": "logical", "subcategory": "Number Series", "difficulty": "easy",
    },
    # Verbal Ability
    {
        "question": "Choose the correct synonym for 'ELOQUENT':",
        "options": [{"text": "Silent"}, {"text": "Articulate", "is_correct": True}, {"text": "Confused"}, {"text": "Harsh"}],
        "correct_answer": 1, "explanation": "Eloquent means fluent and persuasive in speaking; articulate means the same.",
        "category": "verbal", "subcategory": "Vocabulary", "difficulty": "easy",
    },
    {
        "question": "The employees _____ working on the project since Monday.",
        "options": [{"text": "is"}, {"text": "was"}, {"text": "have been", "is_correct": True}, {"text": "has been"}],
        "correct_answer": 2, "explanation": "'Employees' is plural, so we use 'have been' (present perfect continuous).",
        "category": "verbal", "subcategory": "Grammar", "difficulty": "easy",
    },
    {
        "question": "Identify the correctly spelled word:",
        "options": [{"text": "Accomodate"}, {"text": "Accommodate", "is_correct": True}, {"text": "Acommodate"}, {"text": "Accommodaet"}],
        "correct_answer": 1, "explanation": "The correct spelling is 'Accommodate' with double 'c' and double 'm'.",
        "category": "verbal", "subcategory": "Vocabulary", "difficulty": "easy",
    },
]


async def seed_all():
    print("Initializing database connection...")
    client = AsyncIOMotorClient(settings.MONGODB_URI)
    from app.models.user import User
    from app.models.resume import Resume, ResumeAnalysis
    from app.models.roadmap import Roadmap
    from app.models.conversation import Conversation
    from app.models.interview import Interview
    from app.models.coding import CodingProblem, Submission
    from app.models.aptitude import AptitudeQuestion, AptitudeAttempt
    from app.models.progress import Progress

    await init_beanie(
        database=client[settings.DATABASE_NAME],
        document_models=[User, Resume, ResumeAnalysis, Company, Roadmap, Conversation,
                         Interview, CodingProblem, Submission, AptitudeQuestion, AptitudeAttempt, Progress],
    )
    print("Connected to MongoDB!")

    existing_companies = await Company.count()
    if existing_companies == 0:
        print("Seeding companies...")
        for company_data in COMPANIES:
            company = Company(**{
                k: v for k, v in company_data.items()
                if k not in ('recruitment_process', 'roles')
            })
            if 'recruitment_process' in company_data:
                company.recruitment_process = [RecruitmentStage(**s) for s in company_data['recruitment_process']]
            if 'roles' in company_data:
                company.roles = [CompanyRole(**r) for r in company_data['roles']]
            if 'salary_range' in company_data:
                company.salary_range = SalaryRange(**company_data['salary_range'])
            await company.insert()
        print(f"✓ Seeded {len(COMPANIES)} companies")
    else:
        print(f"Companies already seeded ({existing_companies} found), skipping...")

    print(f"Seeding coding problems (upsert by slug)... total in list: {len(CODING_PROBLEMS)}")
    inserted = skipped = errors = 0
    for prob_data in CODING_PROBLEMS:
        try:
            existing = await CodingProblem.find_one(CodingProblem.slug == prob_data["slug"])
            if existing:
                skipped += 1
                continue
            prob = CodingProblem(
                title=prob_data["title"],
                slug=prob_data["slug"],
                description=prob_data["description"],
                difficulty=prob_data["difficulty"],
                topics=prob_data.get("topics", []),
                companies=prob_data.get("companies", []),
                input_format=prob_data.get("input_format"),
                output_format=prob_data.get("output_format"),
                constraints=prob_data.get("constraints"),
                examples=[Example(**e) for e in prob_data.get("examples", [])],
                test_cases=[TestCase(**tc) for tc in prob_data.get("test_cases", [])],
                hints=prob_data.get("hints", []),
                solutions=[Solution(**s) for s in prob_data.get("solutions", [])],
                xp_reward=prob_data.get("xp_reward", 50),
                order=prob_data.get("order", 0),
            )
            await prob.insert()
            inserted += 1
            print(f"  + inserted: {prob_data['slug']}")
        except Exception as e:
            errors += 1
            print(f"  ✗ ERROR inserting {prob_data['slug']}: {e}")
    print(f"✓ Coding problems: {inserted} inserted, {skipped} skipped, {errors} errors")

    existing_questions = await AptitudeQuestion.count()
    if existing_questions == 0:
        print("Seeding aptitude questions...")
        for q_data in APTITUDE_QUESTIONS:
            q = AptitudeQuestion(
                question=q_data["question"],
                options=[Option(**o) for o in q_data["options"]],
                correct_answer=q_data["correct_answer"],
                explanation=q_data.get("explanation"),
                category=q_data["category"],
                subcategory=q_data.get("subcategory"),
                difficulty=q_data.get("difficulty", "medium"),
            )
            await q.insert()
        print(f"✓ Seeded {len(APTITUDE_QUESTIONS)} aptitude questions")
    else:
        print(f"Aptitude questions already seeded ({existing_questions} found), skipping...")

    print("\n✅ Database seeding completed!")
    print(f"Companies: {await Company.count()}")
    print(f"Coding Problems: {await CodingProblem.count()}")
    print(f"Aptitude Questions: {await AptitudeQuestion.count()}")


if __name__ == "__main__":
    asyncio.run(seed_all())
