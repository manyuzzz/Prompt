import { useState, useEffect, useCallback } from 'react'
import { aptitudeAPI } from '../services/api'
import { useToast } from '../hooks/useToast'
import { Brain, CheckCircle, XCircle, Timer, RefreshCw, BarChart3 } from 'lucide-react'

const CATEGORIES = ['quantitative', 'logical', 'verbal']
const CATEGORY_ICONS = { quantitative: '🔢', logical: '🧩', verbal: '📖' }

export default function Aptitude() {
  const [questions, setQuestions] = useState([])
  const [currentIdx, setCurrentIdx] = useState(0)
  const [selected, setSelected] = useState(null)
  const [result, setResult] = useState(null)
  const [stats, setStats] = useState(null)
  const [category, setCategory] = useState('')
  const [view, setView] = useState('quiz') // quiz | stats
  const [timeLeft, setTimeLeft] = useState(null)
  const [loading, setLoading] = useState(false)
  const [submitting, setSubmitting] = useState(false)
  const [sessionResults, setSessionResults] = useState([])
  const toast = useToast()

  const loadQuestions = useCallback(async (cat = category) => {
    setLoading(true)
    setCurrentIdx(0); setSelected(null); setResult(null); setSessionResults([])
    try {
      const params = { limit: 10 }
      if (cat) params.category = cat
      const { data } = await aptitudeAPI.getQuestions(params)
      setQuestions(data.questions || [])
      if (data.questions?.[0]?.time_limit_seconds) {
        setTimeLeft(data.questions[0].time_limit_seconds)
      }
    } catch { toast.error('Failed to load questions') }
    finally { setLoading(false) }
  }, [category])

  useEffect(() => { loadQuestions() }, [])

  useEffect(() => {
    aptitudeAPI.getStats().then(r => setStats(r.data)).catch(() => {})
  }, [])

  // Timer
  useEffect(() => {
    if (timeLeft === null || timeLeft <= 0 || result || selected !== null) return
    const t = setTimeout(() => setTimeLeft(t => t - 1), 1000)
    return () => clearTimeout(t)
  }, [timeLeft, result, selected])

  const current = questions[currentIdx]

  const submitAnswer = async (optionIdx) => {
    if (selected !== null || submitting) return
    setSelected(optionIdx)
    setSubmitting(true)
    try {
      const { data } = await aptitudeAPI.submit({
        question_id: current.id,
        selected_option: optionIdx,
        time_taken: current.time_limit_seconds ? current.time_limit_seconds - (timeLeft || 0) : 30,
      })
      setResult(data)
      setSessionResults(prev => [...prev, { correct: data.correct, question: current.question }])
    } catch { toast.error('Submission failed') }
    finally { setSubmitting(false) }
  }

  const next = () => {
    if (currentIdx < questions.length - 1) {
      setCurrentIdx(i => i + 1)
      setSelected(null); setResult(null)
      if (questions[currentIdx + 1]?.time_limit_seconds) {
        setTimeLeft(questions[currentIdx + 1].time_limit_seconds)
      }
    } else {
      toast.success(`Session complete! ${sessionResults.filter(r => r.correct).length}/${questions.length} correct`)
    }
  }

  if (loading) return <div className="flex justify-center py-20"><div className="animate-spin w-8 h-8 border-2 border-primary-500 border-t-transparent rounded-full" /></div>

  return (
    <div className="space-y-6 animate-fade-in max-w-3xl">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white">Aptitude Practice</h1>
          <p className="text-gray-400 mt-1">Sharpen your Quantitative, Logical, and Verbal skills</p>
        </div>
        <div className="flex gap-2">
          <button onClick={() => setView(view === 'quiz' ? 'stats' : 'quiz')} className="btn-secondary text-sm flex items-center gap-2">
            <BarChart3 size={14} /> {view === 'quiz' ? 'Stats' : 'Quiz'}
          </button>
          <button onClick={() => loadQuestions()} className="btn-ghost p-2"><RefreshCw size={16} /></button>
        </div>
      </div>

      {/* Category Filter */}
      <div className="flex gap-2 flex-wrap">
        <button onClick={() => { setCategory(''); loadQuestions('') }}
          className={`px-4 py-2 rounded-lg text-sm border transition-colors ${!category ? 'bg-primary-600 border-primary-600 text-white' : 'border-gray-700 text-gray-400 hover:border-gray-600'}`}>
          All
        </button>
        {CATEGORIES.map(c => (
          <button key={c} onClick={() => { setCategory(c); loadQuestions(c) }}
            className={`px-4 py-2 rounded-lg text-sm capitalize border transition-colors ${category === c ? 'bg-primary-600 border-primary-600 text-white' : 'border-gray-700 text-gray-400 hover:border-gray-600'}`}>
            {CATEGORY_ICONS[c]} {c}
          </button>
        ))}
      </div>

      {view === 'stats' && stats && (
        <div className="card space-y-4">
          <h3 className="font-semibold text-white">Your Aptitude Stats</h3>
          <div className="grid grid-cols-3 gap-4 text-center">
            <div className="bg-gray-800/50 rounded-lg p-4">
              <div className="text-2xl font-bold text-white">{stats.total || 0}</div>
              <div className="text-xs text-gray-500 mt-1">Total Attempted</div>
            </div>
            <div className="bg-gray-800/50 rounded-lg p-4">
              <div className="text-2xl font-bold text-green-400">{stats.correct || 0}</div>
              <div className="text-xs text-gray-500 mt-1">Correct</div>
            </div>
            <div className="bg-gray-800/50 rounded-lg p-4">
              <div className="text-2xl font-bold text-primary-400">{Math.round(stats.accuracy || 0)}%</div>
              <div className="text-xs text-gray-500 mt-1">Accuracy</div>
            </div>
          </div>
          {stats.by_category && (
            <div>
              <h4 className="text-sm font-medium text-gray-400 mb-3">By Category</h4>
              {Object.entries(stats.by_category).map(([cat, s]) => (
                <div key={cat} className="mb-3">
                  <div className="flex justify-between text-sm mb-1">
                    <span className="text-gray-300 capitalize">{cat}</span>
                    <span className="text-gray-500">{Math.round(s.accuracy || 0)}% accuracy</span>
                  </div>
                  <div className="progress-bar">
                    <div className="progress-fill bg-primary-500" style={{ width: `${s.accuracy || 0}%` }} />
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {view === 'quiz' && current && (
        <div className="space-y-4">
          {/* Progress */}
          <div className="flex items-center justify-between text-sm">
            <span className="text-gray-400">Question {currentIdx + 1} of {questions.length}</span>
            <div className="flex items-center gap-3">
              {sessionResults.length > 0 && (
                <span className="text-green-400">{sessionResults.filter(r => r.correct).length} ✓</span>
              )}
              {timeLeft !== null && (
                <span className={`flex items-center gap-1 font-mono ${timeLeft <= 10 ? 'text-red-400' : 'text-gray-400'}`}>
                  <Timer size={14} /> {timeLeft}s
                </span>
              )}
            </div>
          </div>

          <div className="progress-bar">
            <div className="progress-fill bg-primary-500" style={{ width: `${((currentIdx) / questions.length) * 100}%` }} />
          </div>

          <div className="card">
            <div className="flex items-start gap-3 mb-4">
              <span className="badge badge-blue capitalize">{current.category}</span>
              {current.subcategory && <span className="badge badge-purple">{current.subcategory}</span>}
            </div>
            <p className="text-gray-100 text-base leading-relaxed mb-6">{current.question}</p>

            <div className="space-y-3">
              {current.options?.map((opt, i) => {
                let style = 'border-gray-700 hover:border-gray-600 bg-transparent'
                if (selected !== null) {
                  if (opt.is_correct) style = 'border-green-500 bg-green-900/20'
                  else if (i === selected && !opt.is_correct) style = 'border-red-500 bg-red-900/20'
                  else style = 'border-gray-800 opacity-50'
                }
                return (
                  <button key={i} onClick={() => submitAnswer(i)}
                    className={`w-full text-left px-4 py-3 rounded-lg border transition-all ${style} flex items-center gap-3`}>
                    <span className="w-6 h-6 rounded-full border border-current flex items-center justify-center text-xs shrink-0">
                      {String.fromCharCode(65 + i)}
                    </span>
                    <span className="text-gray-200">{opt.text}</span>
                    {selected !== null && opt.is_correct && <CheckCircle size={16} className="text-green-400 ml-auto shrink-0" />}
                    {selected !== null && i === selected && !opt.is_correct && <XCircle size={16} className="text-red-400 ml-auto shrink-0" />}
                  </button>
                )
              })}
            </div>

            {result && (
              <div className={`mt-4 p-3 rounded-lg border ${result.correct ? 'border-green-700 bg-green-900/10' : 'border-red-700 bg-red-900/10'}`}>
                <div className="flex items-center gap-2 mb-1">
                  {result.correct ? <CheckCircle size={16} className="text-green-400" /> : <XCircle size={16} className="text-red-400" />}
                  <span className={`font-medium text-sm ${result.correct ? 'text-green-400' : 'text-red-400'}`}>
                    {result.correct ? `Correct! +${result.xp_awarded} XP` : 'Incorrect'}
                  </span>
                </div>
                {result.explanation && <p className="text-sm text-gray-400">{result.explanation}</p>}
                <button onClick={next} className="btn-primary mt-3 text-sm">
                  {currentIdx < questions.length - 1 ? 'Next Question →' : 'Finish Session'}
                </button>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  )
}
