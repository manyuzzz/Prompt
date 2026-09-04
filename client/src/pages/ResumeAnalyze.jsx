import { useState, useEffect } from 'react'
import { useLocation } from 'react-router-dom'
import { resumeAPI } from '../services/api'
import { useToast } from '../hooks/useToast'
import { getScoreColor, getScoreBg } from '../utils/helpers'
import { AlertCircle, CheckCircle, ChevronDown, ChevronUp, Loader } from 'lucide-react'

function ScoreBar({ label, score }) {
  return (
    <div>
      <div className="flex justify-between text-sm mb-1">
        <span className="text-gray-400">{label}</span>
        <span className={getScoreColor(score)}>{score}/100</span>
      </div>
      <div className="progress-bar">
        <div className={`progress-fill ${getScoreBg(score)}`} style={{ width: `${score}%` }} />
      </div>
    </div>
  )
}

export default function ResumeAnalyze() {
  const location = useLocation()
  const [resumes, setResumes] = useState([])
  const [selectedId, setSelectedId] = useState(location.state?.resumeId || '')
  const [jd, setJd] = useState('')
  const [analysis, setAnalysis] = useState(null)
  const [loading, setLoading] = useState(false)
  const [showSuggestions, setShowSuggestions] = useState(true)
  const toast = useToast()

  useEffect(() => {
    resumeAPI.getAll().then(r => setResumes(r.data.resumes || [])).catch(console.error)
    if (location.state?.resumeId) {
      runAnalysis(location.state.resumeId)
    }
  }, [])

  const runAnalysis = async (id = selectedId) => {
    if (!id) { toast.warn('Select a resume first'); return }
    setLoading(true)
    try {
      const { data } = await resumeAPI.analyze(id)
      setAnalysis(data.analysis)
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Analysis failed')
    } finally { setLoading(false) }
  }

  const overallScore = analysis?.scores?.overall || 0

  return (
    <div className="space-y-6 animate-fade-in">
      <div>
        <h1 className="text-2xl font-bold text-white">Resume Analyzer</h1>
        <p className="text-gray-400 mt-1">Get ATS scores, JD matching, and AI improvement suggestions</p>
      </div>

      <div className="card space-y-4">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="label">Select Resume</label>
            <select className="input" value={selectedId} onChange={e => setSelectedId(e.target.value)}>
              <option value="">Choose a resume...</option>
              {resumes.map(r => (
                <option key={r.id} value={r.id}>{r.personal_info?.name || r.id}</option>
              ))}
            </select>
          </div>
          <div className="flex items-end">
            <button onClick={() => runAnalysis()} disabled={loading || !selectedId} className="btn-primary w-full flex items-center justify-center gap-2">
              {loading ? <><Loader size={16} className="animate-spin" /> Analyzing...</> : 'Analyze Resume'}
            </button>
          </div>
        </div>
        <div>
          <label className="label">Job Description (optional — for JD matching)</label>
          <textarea className="input h-28 resize-none" placeholder="Paste job description here to check match percentage..."
            value={jd} onChange={e => setJd(e.target.value)} />
        </div>
      </div>

      {analysis && (
        <div className="space-y-6">
          {/* Overall Score */}
          <div className="card text-center py-8">
            <div className={`text-6xl font-bold ${getScoreColor(overallScore)}`}>{overallScore}</div>
            <div className="text-gray-400 mt-2">Overall ATS Score</div>
            <div className="progress-bar w-48 mx-auto mt-4">
              <div className={`progress-fill ${getScoreBg(overallScore)}`} style={{ width: `${overallScore}%` }} />
            </div>
          </div>

          {/* Score Breakdown */}
          <div className="card space-y-4">
            <h3 className="font-semibold text-white">Score Breakdown</h3>
            <ScoreBar label="Content Quality" score={analysis.scores?.content || 0} />
            <ScoreBar label="Format & Structure" score={analysis.scores?.format || 0} />
            <ScoreBar label="ATS Compatibility" score={analysis.scores?.ats_compatibility || 0} />
            <ScoreBar label="Keywords" score={analysis.scores?.keywords || 0} />
            <ScoreBar label="Sections" score={analysis.scores?.sections || 0} />
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {/* Strengths */}
            <div className="card">
              <h3 className="font-semibold text-white mb-3 flex items-center gap-2">
                <CheckCircle size={16} className="text-green-400" /> Strengths
              </h3>
              <ul className="space-y-2">
                {analysis.strengths?.map((s, i) => (
                  <li key={i} className="text-sm text-gray-300 flex gap-2">
                    <span className="text-green-400 shrink-0">✓</span> {s}
                  </li>
                ))}
              </ul>
            </div>

            {/* Weaknesses */}
            <div className="card">
              <h3 className="font-semibold text-white mb-3 flex items-center gap-2">
                <AlertCircle size={16} className="text-red-400" /> Areas to Improve
              </h3>
              <ul className="space-y-2">
                {analysis.weaknesses?.map((w, i) => (
                  <li key={i} className="text-sm text-gray-300 flex gap-2">
                    <span className="text-red-400 shrink-0">✗</span> {w}
                  </li>
                ))}
              </ul>
            </div>
          </div>

          {/* Keywords */}
          <div className="card">
            <h3 className="font-semibold text-white mb-3">Keywords</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <p className="text-xs text-gray-500 mb-2 uppercase tracking-wider">Present</p>
                <div className="flex flex-wrap gap-2">
                  {analysis.present_keywords?.map(k => (
                    <span key={k} className="badge badge-green">{k}</span>
                  ))}
                </div>
              </div>
              <div>
                <p className="text-xs text-gray-500 mb-2 uppercase tracking-wider">Missing</p>
                <div className="flex flex-wrap gap-2">
                  {analysis.missing_keywords?.map(k => (
                    <span key={k} className="badge badge-red">{k}</span>
                  ))}
                </div>
              </div>
            </div>
          </div>

          {/* Suggestions */}
          <div className="card">
            <button onClick={() => setShowSuggestions(!showSuggestions)}
              className="w-full flex items-center justify-between">
              <h3 className="font-semibold text-white">AI Suggestions ({analysis.suggestions?.length || 0})</h3>
              {showSuggestions ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
            </button>
            {showSuggestions && (
              <div className="mt-4 space-y-3">
                {analysis.suggestions?.map((s, i) => (
                  <div key={i} className={`p-3 rounded-lg border ${
                    s.priority === 'high' ? 'border-red-800 bg-red-900/10' :
                    s.priority === 'medium' ? 'border-yellow-800 bg-yellow-900/10' :
                    'border-gray-700 bg-gray-800/30'
                  }`}>
                    <div className="flex items-center gap-2 mb-1">
                      <span className="badge badge-blue">{s.section}</span>
                      <span className={`badge ${s.priority === 'high' ? 'badge-red' : s.priority === 'medium' ? 'badge-yellow' : 'badge-green'}`}>
                        {s.priority}
                      </span>
                    </div>
                    <p className="text-sm text-gray-300">{s.suggestion}</p>
                    {s.example && <p className="text-xs text-gray-500 mt-1 italic">Example: {s.example}</p>}
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  )
}
