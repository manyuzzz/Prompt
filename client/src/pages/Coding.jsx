import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { codingAPI } from '../services/api'
import { getDifficultyBg, getDifficultyColor } from '../utils/helpers'
import { Code2, CheckCircle2, Search, Filter } from 'lucide-react'

const DIFFICULTIES = ['all', 'easy', 'medium', 'hard']

export default function Coding() {
  const [problems, setProblems] = useState([])
  const [topics, setTopics] = useState([])
  const [loading, setLoading] = useState(true)
  const [filters, setFilters] = useState({ difficulty: 'all', topic: '', search: '' })
  const navigate = useNavigate()

  useEffect(() => {
    codingAPI.getTopics().then(r => setTopics(r.data.topics || [])).catch(() => {})
    loadProblems()
  }, [])

  const loadProblems = async (f = filters) => {
    setLoading(true)
    const params = {}
    if (f.difficulty !== 'all') params.difficulty = f.difficulty
    if (f.topic) params.topic = f.topic
    try {
      const { data } = await codingAPI.getProblems(params)
      let probs = data.problems || []
      if (f.search) probs = probs.filter(p => p.title.toLowerCase().includes(f.search.toLowerCase()))
      setProblems(probs)
    } catch { }
    finally { setLoading(false) }
  }

  const setFilter = (key, val) => {
    const f = { ...filters, [key]: val }
    setFilters(f)
    loadProblems(f)
  }

  return (
    <div className="space-y-6 animate-fade-in">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white">Coding Practice</h1>
          <p className="text-gray-400 mt-1">Solve problems and improve your algorithmic thinking</p>
        </div>
        <div className="text-sm text-gray-400">
          {problems.length} problems
        </div>
      </div>

      {/* Filters */}
      <div className="flex flex-wrap gap-3">
        <div className="relative flex-1 min-w-48">
          <Search size={15} className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-500" />
          <input className="input pl-9" placeholder="Search problems..."
            value={filters.search}
            onChange={e => setFilter('search', e.target.value)} />
        </div>
        <div className="flex gap-2">
          {DIFFICULTIES.map(d => (
            <button key={d} onClick={() => setFilter('difficulty', d)}
              className={`px-3 py-2 rounded-lg text-sm capitalize border transition-colors ${
                filters.difficulty === d ? 'bg-primary-600 border-primary-600 text-white' : 'border-gray-700 text-gray-400 hover:border-gray-600'
              }`}>{d}
            </button>
          ))}
        </div>
        <select className="input w-auto" value={filters.topic} onChange={e => setFilter('topic', e.target.value)}>
          <option value="">All Topics</option>
          {topics.map(t => <option key={t} value={t}>{t}</option>)}
        </select>
      </div>

      {loading ? (
        <div className="flex justify-center py-20"><div className="animate-spin w-8 h-8 border-2 border-primary-500 border-t-transparent rounded-full" /></div>
      ) : (
        <div className="space-y-2">
          {problems.map((problem, i) => (
            <div key={problem.id}
              onClick={() => navigate(`/technical/problem/${problem.slug}`)}
              className="card flex items-center gap-4 cursor-pointer hover:border-gray-700 transition-colors group">
              <div className="w-8 text-center text-gray-600 text-sm shrink-0">{i + 1}</div>
              {problem.solved && <CheckCircle2 size={16} className="text-green-400 shrink-0" />}
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2">
                  <span className="font-medium text-white group-hover:text-primary-400 transition-colors">{problem.title}</span>
                  <span className={`badge border ${getDifficultyBg(problem.difficulty)} text-xs`}>{problem.difficulty}</span>
                </div>
                <div className="flex flex-wrap gap-1.5 mt-1.5">
                  {problem.topics?.slice(0, 4).map(t => (
                    <span key={t} className="badge badge-blue text-xs">{t}</span>
                  ))}
                </div>
              </div>
              <div className="text-right shrink-0">
                <div className="text-xs text-gray-500">Acceptance</div>
                <div className="text-sm font-medium text-gray-300">{problem.acceptance_rate?.toFixed(0) || '65'}%</div>
              </div>
            </div>
          ))}
          {problems.length === 0 && (
            <div className="card text-center py-12">
              <Code2 size={40} className="mx-auto mb-3 text-gray-600" />
              <p className="text-gray-400">No problems match your filters</p>
            </div>
          )}
        </div>
      )}
    </div>
  )
}
