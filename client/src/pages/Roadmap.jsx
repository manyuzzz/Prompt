import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { roadmapAPI, companiesAPI } from '../services/api'
import { useToast } from '../hooks/useToast'
import { timeAgo } from '../utils/helpers'
import { Map, Plus, Loader, ChevronRight, CheckCircle, Clock, Zap } from 'lucide-react'

const ROLES = ['Software Development Engineer', 'Data Scientist', 'Full Stack Developer', 'Backend Engineer', 'Frontend Engineer', 'ML Engineer', 'DevOps Engineer']
const DSA_LEVELS = ['beginner', 'intermediate', 'advanced']
const HOURS = [1, 2, 3, 4, 5, 6]

export default function Roadmap() {
  const [roadmaps, setRoadmaps] = useState([])
  const [companies, setCompanies] = useState([])
  const [generating, setGenerating] = useState(false)
  const [loading, setLoading] = useState(true)
  const [showForm, setShowForm] = useState(false)
  const [form, setForm] = useState({
    target_company: '', target_role: ROLES[0], dsa_level: 'beginner',
    aptitude_level: 'beginner', available_hours: 2, weak_areas: [],
  })
  const navigate = useNavigate()
  const toast = useToast()

  useEffect(() => {
    Promise.all([
      roadmapAPI.getAll().then(r => setRoadmaps(r.data.roadmaps || [])),
      companiesAPI.getAll().then(r => setCompanies(r.data.companies || [])),
    ]).catch(console.error).finally(() => setLoading(false))
  }, [])

  const generate = async () => {
    setGenerating(true)
    try {
      const { data } = await roadmapAPI.generate(form)
      setRoadmaps(prev => [data.roadmap, ...prev.filter(r => !r.is_active)])
      toast.success('Roadmap generated!')
      navigate(`/roadmap/${data.roadmap.id}`)
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Generation failed')
    } finally { setGenerating(false) }
  }

  if (loading) return <div className="flex justify-center py-20"><div className="animate-spin w-8 h-8 border-2 border-primary-500 border-t-transparent rounded-full" /></div>

  return (
    <div className="space-y-6 animate-fade-in">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white">Placement Roadmap</h1>
          <p className="text-gray-400 mt-1">AI-generated personalized 12-week preparation plan</p>
        </div>
        <button onClick={() => setShowForm(!showForm)} className="btn-primary flex items-center gap-2">
          <Plus size={16} /> Generate Roadmap
        </button>
      </div>

      {showForm && (
        <div className="card space-y-4">
          <h3 className="font-semibold text-white">Generate Personalized Roadmap</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="label">Target Company</label>
              <select className="input" value={form.target_company} onChange={e => setForm({ ...form, target_company: e.target.value })}>
                <option value="">Any / General</option>
                {companies.map(c => <option key={c.id} value={c.name}>{c.name}</option>)}
              </select>
            </div>
            <div>
              <label className="label">Target Role</label>
              <select className="input" value={form.target_role} onChange={e => setForm({ ...form, target_role: e.target.value })}>
                {ROLES.map(r => <option key={r}>{r}</option>)}
              </select>
            </div>
            <div>
              <label className="label">DSA Level</label>
              <select className="input" value={form.dsa_level} onChange={e => setForm({ ...form, dsa_level: e.target.value })}>
                {DSA_LEVELS.map(l => <option key={l} className="capitalize">{l}</option>)}
              </select>
            </div>
            <div>
              <label className="label">Available Hours/Day</label>
              <select className="input" value={form.available_hours} onChange={e => setForm({ ...form, available_hours: +e.target.value })}>
                {HOURS.map(h => <option key={h} value={h}>{h} hour{h > 1 ? 's' : ''}</option>)}
              </select>
            </div>
          </div>
          <div className="flex gap-3 pt-2">
            <button onClick={generate} disabled={generating} className="btn-primary flex items-center gap-2">
              {generating ? <><Loader size={15} className="animate-spin" /> Generating...</> : <><Zap size={15} /> Generate</>}
            </button>
            <button onClick={() => setShowForm(false)} className="btn-secondary">Cancel</button>
          </div>
        </div>
      )}

      {roadmaps.length === 0 ? (
        <div className="card text-center py-16">
          <Map size={48} className="mx-auto mb-4 text-gray-600" />
          <h3 className="text-lg font-semibold text-white mb-2">No Roadmap Yet</h3>
          <p className="text-gray-400 mb-6">Generate a personalized 12-week placement roadmap based on your goals</p>
          <button onClick={() => setShowForm(true)} className="btn-primary inline-flex items-center gap-2">
            <Plus size={16} /> Generate Your Roadmap
          </button>
        </div>
      ) : (
        <div className="space-y-4">
          {roadmaps.map(roadmap => (
            <div key={roadmap.id}
              onClick={() => navigate(`/roadmap/${roadmap.id}`)}
              className="card cursor-pointer hover:border-gray-700 transition-colors group">
              <div className="flex items-start justify-between">
                <div>
                  <div className="flex items-center gap-2 mb-1">
                    <h3 className="font-semibold text-white">{roadmap.title}</h3>
                    {roadmap.is_active && <span className="badge badge-green">Active</span>}
                  </div>
                  <p className="text-sm text-gray-400">{roadmap.target_company || 'General'} · {roadmap.target_role}</p>
                  <p className="text-xs text-gray-600 mt-1">{timeAgo(roadmap.created_at)}</p>
                </div>
                <div className="flex items-center gap-3">
                  <div className="text-right">
                    <div className="text-2xl font-bold text-primary-400">{Math.round(roadmap.completion_percentage || 0)}%</div>
                    <div className="text-xs text-gray-500">complete</div>
                  </div>
                  <ChevronRight size={18} className="text-gray-600 group-hover:text-gray-400" />
                </div>
              </div>
              <div className="progress-bar mt-3">
                <div className="progress-fill bg-primary-500" style={{ width: `${roadmap.completion_percentage || 0}%` }} />
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
