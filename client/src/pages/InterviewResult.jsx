import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { interviewAPI } from '../services/api'
import { getScoreColor, getScoreBg } from '../utils/helpers'
import { Trophy, ArrowLeft, RefreshCw } from 'lucide-react'

function ScoreBar({ label, score }) {
  return (
    <div>
      <div className="flex justify-between text-sm mb-1.5">
        <span className="text-gray-400">{label}</span>
        <span className={`font-medium ${getScoreColor(score)}`}>{Math.round(score)}%</span>
      </div>
      <div className="progress-bar">
        <div className={`progress-fill ${getScoreBg(score)}`} style={{ width: `${score}%` }} />
      </div>
    </div>
  )
}

export default function InterviewResult() {
  const { id } = useParams()
  const [interview, setInterview] = useState(null)
  const navigate = useNavigate()

  useEffect(() => {
    interviewAPI.getOne(id).then(r => setInterview(r.data.interview)).catch(console.error)
  }, [id])

  if (!interview) return <div className="flex justify-center py-20"><div className="animate-spin w-8 h-8 border-2 border-primary-500 border-t-transparent rounded-full" /></div>

  const scores = interview.overall_scores || {}
  const feedback = interview.feedback || {}
  const overall = scores.overall || 0

  return (
    <div className="max-w-3xl mx-auto space-y-6 animate-fade-in">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-3">
          <button onClick={() => navigate('/interview')} className="btn-ghost p-2"><ArrowLeft size={18} /></button>
          <h1 className="text-2xl font-bold text-white">Interview Results</h1>
        </div>
        <button onClick={() => navigate('/interview/setup')} className="btn-secondary flex items-center gap-2 text-sm">
          <RefreshCw size={14} /> Practice Again
        </button>
      </div>

      {/* Overall Score */}
      <div className="card text-center py-10">
        <Trophy size={36} className={`mx-auto mb-3 ${overall >= 70 ? 'text-yellow-400' : 'text-gray-500'}`} />
        <div className={`text-6xl font-bold ${getScoreColor(overall)}`}>{Math.round(overall)}%</div>
        <div className="text-gray-400 mt-2 capitalize">{interview.type?.replace('_', ' ')} Interview</div>
        <div className={`badge mt-3 ${overall >= 80 ? 'badge-green' : overall >= 60 ? 'badge-yellow' : 'badge-red'}`}>
          {overall >= 80 ? 'Excellent' : overall >= 60 ? 'Good' : 'Needs Improvement'}
        </div>
      </div>

      {/* Score Breakdown */}
      <div className="card space-y-4">
        <h3 className="font-semibold text-white">Score Breakdown</h3>
        <ScoreBar label="Communication" score={scores.communication || 0} />
        <ScoreBar label="Technical Knowledge" score={scores.technical_knowledge || 0} />
        <ScoreBar label="Confidence" score={scores.confidence || 0} />
        <ScoreBar label="Problem Solving" score={scores.problem_solving || 0} />
        <ScoreBar label="Clarity" score={scores.clarity || 0} />
        <ScoreBar label="Answer Quality" score={scores.answer_quality || 0} />
      </div>

      {/* Feedback */}
      {feedback.summary && (
        <div className="card">
          <h3 className="font-semibold text-white mb-3">AI Feedback</h3>
          <p className="text-gray-300 text-sm leading-relaxed">{feedback.summary}</p>
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {feedback.strengths?.length > 0 && (
          <div className="card">
            <h3 className="font-semibold text-white mb-3 flex items-center gap-2">
              <span className="text-green-400">✓</span> Strengths
            </h3>
            <ul className="space-y-1.5">
              {feedback.strengths.map((s, i) => (
                <li key={i} className="text-sm text-gray-300">• {s}</li>
              ))}
            </ul>
          </div>
        )}
        {feedback.improvements?.length > 0 && (
          <div className="card">
            <h3 className="font-semibold text-white mb-3 flex items-center gap-2">
              <span className="text-yellow-400">→</span> Improvements
            </h3>
            <ul className="space-y-1.5">
              {feedback.improvements.map((s, i) => (
                <li key={i} className="text-sm text-gray-300">• {s}</li>
              ))}
            </ul>
          </div>
        )}
      </div>

      {/* Q&A Review */}
      {interview.responses?.length > 0 && (
        <div className="card">
          <h3 className="font-semibold text-white mb-4">Question-by-Question Review</h3>
          <div className="space-y-4">
            {interview.responses.map((r, i) => (
              <div key={i} className="border border-gray-800 rounded-lg p-4">
                <p className="text-sm font-medium text-gray-200 mb-2">Q{i + 1}: {r.question}</p>
                <p className="text-sm text-gray-400 mb-3">Your answer: {r.answer}</p>
                <p className="text-xs text-gray-500 italic">{r.feedback}</p>
                <div className="mt-2">
                  <span className={`text-sm font-bold ${getScoreColor(r.scores?.overall || 0)}`}>
                    Score: {Math.round(r.scores?.overall || 0)}%
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
