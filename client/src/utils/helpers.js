export const formatDate = (dateStr) => {
  if (!dateStr) return 'N/A'
  return new Date(dateStr).toLocaleDateString('en-IN', {
    day: 'numeric', month: 'short', year: 'numeric',
  })
}

export const formatTime = (dateStr) => {
  if (!dateStr) return ''
  return new Date(dateStr).toLocaleTimeString('en-IN', {
    hour: '2-digit', minute: '2-digit',
  })
}

export const timeAgo = (dateStr) => {
  if (!dateStr) return ''
  const diff = Date.now() - new Date(dateStr).getTime()
  const mins = Math.floor(diff / 60000)
  if (mins < 1) return 'just now'
  if (mins < 60) return `${mins}m ago`
  const hrs = Math.floor(mins / 60)
  if (hrs < 24) return `${hrs}h ago`
  const days = Math.floor(hrs / 24)
  if (days < 7) return `${days}d ago`
  return formatDate(dateStr)
}

export const getDifficultyColor = (difficulty) => {
  const map = { easy: 'text-green-400', medium: 'text-yellow-400', hard: 'text-red-400' }
  return map[difficulty?.toLowerCase()] || 'text-gray-400'
}

export const getDifficultyBg = (difficulty) => {
  const map = {
    easy: 'bg-green-900/30 text-green-400 border-green-800',
    medium: 'bg-yellow-900/30 text-yellow-400 border-yellow-800',
    hard: 'bg-red-900/30 text-red-400 border-red-800',
  }
  return map[difficulty?.toLowerCase()] || 'bg-gray-800 text-gray-400 border-gray-700'
}

export const getScoreColor = (score) => {
  if (score >= 80) return 'text-green-400'
  if (score >= 60) return 'text-yellow-400'
  if (score >= 40) return 'text-orange-400'
  return 'text-red-400'
}

export const getScoreBg = (score) => {
  if (score >= 80) return 'bg-green-500'
  if (score >= 60) return 'bg-yellow-500'
  if (score >= 40) return 'bg-orange-500'
  return 'bg-red-500'
}

export const getLevelTitle = (level) => {
  const titles = ['Fresher', 'Beginner', 'Learner', 'Developer', 'Engineer',
    'Senior Engineer', 'Lead', 'Architect', 'Expert', 'Placement Pro']
  return titles[Math.min(level - 1, titles.length - 1)] || 'Placement Pro'
}

export const truncate = (str, len = 100) =>
  str && str.length > len ? str.slice(0, len) + '...' : str

export const capitalize = (s) => s ? s.charAt(0).toUpperCase() + s.slice(1) : ''

export const slugify = (s) =>
  s?.toLowerCase().replace(/\s+/g, '-').replace(/[^\w-]+/g, '')

export const copyToClipboard = async (text) => {
  try {
    await navigator.clipboard.writeText(text)
    return true
  } catch {
    return false
  }
}

export const LANGUAGES = [
  { id: 'python', label: 'Python', ext: '.py' },
  { id: 'javascript', label: 'JavaScript', ext: '.js' },
  { id: 'java', label: 'Java', ext: '.java' },
  { id: 'cpp', label: 'C++', ext: '.cpp' },
  { id: 'c', label: 'C', ext: '.c' },
]

export const LANGUAGE_STARTERS = {
  python: '# Write your solution here\ndef solution():\n    pass\n',
  javascript: '// Write your solution here\nfunction solution() {\n  \n}\n',
  java: 'class Solution {\n    public static void main(String[] args) {\n        // Write your solution here\n    }\n}\n',
  cpp: '#include <bits/stdc++.h>\nusing namespace std;\n\nint main() {\n    // Write your solution here\n    return 0;\n}\n',
  c: '#include <stdio.h>\n\nint main() {\n    // Write your solution here\n    return 0;\n}\n',
}
