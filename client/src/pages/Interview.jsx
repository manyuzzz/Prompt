import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { interviewAPI } from '../services/api'
import { timeAgo, getScoreColor } from '../utils/helpers'
import { Mic, Play, ChevronRight, Trophy } from 'lucide-react'

export default function Interview() {
  const [interviews, setInterviews] = useState([])
  const [loading, setLoading] = useState(true)
  const navigate = useNavigate()

  useEffect(() => {
    interviewAPI.getAll()
      .then(r => setInterviews(r.data.interviews || []))
      .catch(console.error)
      .finally(() => setLoading(false))
  }, [])

  const TYPES = [
    { id: 'hr', label: 'HR Interview', desc: 'Tell me about yourself, strengths, weaknesses, career goals', icon: '🎯', color: 'border-blue-600/30' },
    { id: 'technical', label: 'Technical Interview', desc: 'DSA, problem-solving, data structures, algorithms', icon: '💻', color: 'border-green-600/30' },
    { id: 'behavioral', label: 'Behavioral Interview', desc: 'STAR-based questions, leadership, teamwork', icon: '🤝', color: 'border-yellow-600/30' },
    { id: 'company_specific', label: 'Company-Specific', desc: 'Questions tailored to a specific company', icon: '🏢', color: 'border-purple-600/30' },
  ]

  if (loading) return <div className="flex justify-center py-20"><div className="animate-spin w-8 h-8 border-2 border-primary-500 border-t-transparent rounded-full" /></div>

  return (
    <div className="space-y-6 animate-fade-in">
      <div>
        <h1 className="text-2xl font-bold text-white">AI Mock Interview</h1>
        <p className="text-gray-400 mt-1">Practice interviews with AI feedback on every answer</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {TYPES.map(type => (
          <div key={type.id} className={`card cursor-pointer hover:border-gray-600 transition-colors group ${type.color}`}
            onClick={() => navigate('/interview/setup', { state: { type: type.id } })}>
            <div className="flex items-start justify-between">
              <div className="text-3xl mb-3">{type.icon}</div>
              <ChevronRight size={16} className="text-gray-600 group-hover:text-gray-400 transition-colors mt-1" />
            </div>
            <h3 className="font-semibold text-white mb-1">{type.label}</h3>
            <p className="text-sm text-gray-400">{type.desc}</p>
            <button className="mt-4 btn-primary text-sm flex items-center gap-2">
              <Play size={14} /> Start Practice
            </button>
          </div>
        ))}
      </div>

      {interviews.length > 0 && (
        <div>
          <h3 className="font-semibold text-white mb-3 flex items-center gap-2">
            <Trophy size={16} className="text-yellow-400" /> Past Interviews
          </h3>
          <div className="space-y-3">
            {interviews.slice(0, 10).map(interview => (
              <div key={interview.id}
                onClick={() => interview.status === 'completed' ? navigate(`/interview/result/${interview.id}`) : navigate(`/interview/session/${interview.id}`)}
                className="card flex items-center justify-between cursor-pointer hover:border-gray-700 transition-colors group">
                <div className="flex items-center gap-3">
                  <div className="w-10 h-10 rounded-full bg-gray-800 flex items-center justify-center">
                    <Mic size={16} className="text-gray-400" />
                  </div>
                  <div>
                    <p className="font-medium text-white capitalize">{interview.type.replace('_', ' ')} Interview</p>
                    <p className="text-xs text-gray-500">{timeAgo(interview.created_at)}</p>
                  </div>
                </div>
                <div className="flex items-center gap-3">
                  {interview.status === 'completed' && interview.overall_scores && (
                    <span className={`font-bold ${getScoreColor(interview.overall_scores.overall)}`}>
                      {Math.round(interview.overall_scores.overall)}%
                    </span>
                  )}
                  <span className={`badge ${interview.status === 'completed' ? 'badge-green' : 'badge-yellow'}`}>
                    {interview.status}
                  </span>
                  <ChevronRight size={16} className="text-gray-600 group-hover:text-gray-400" />
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
