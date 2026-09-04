import { useState } from 'react'
import { useNavigate, useLocation } from 'react-router-dom'
import { interviewAPI, companiesAPI } from '../services/api'
import { useToast } from '../hooks/useToast'
import { useEffect } from 'react'
import { Play, ArrowLeft, Loader } from 'lucide-react'

export default function InterviewSetup() {
  const location = useLocation()
  const [form, setForm] = useState({
    type: location.state?.type || 'hr',
    company: '',
    role: 'Software Development Engineer',
    difficulty: 'medium',
    num_questions: 5,
  })
  const [companies, setCompanies] = useState([])
  const [starting, setStarting] = useState(false)
  const navigate = useNavigate()
  const toast = useToast()

  useEffect(() => {
    companiesAPI.getAll().then(r => setCompanies(r.data.companies || [])).catch(() => {})
  }, [])

  const start = async () => {
    setStarting(true)
    try {
      const { data } = await interviewAPI.start(form)
      navigate(`/interview/session/${data.interview_id}`)
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Failed to start')
    } finally { setStarting(false) }
  }

  return (
    <div className="max-w-lg mx-auto space-y-6 animate-fade-in">
      <div className="flex items-center gap-3">
        <button onClick={() => navigate('/interview')} className="btn-ghost p-2"><ArrowLeft size={18} /></button>
        <div>
          <h1 className="text-2xl font-bold text-white">Interview Setup</h1>
          <p className="text-gray-400 mt-0.5">Configure your mock interview session</p>
        </div>
      </div>

      <div className="card space-y-5">
        <div>
          <label className="label">Interview Type</label>
          <div className="grid grid-cols-2 gap-2">
            {[['hr', '🎯 HR'], ['technical', '💻 Technical'], ['behavioral', '🤝 Behavioral'], ['company_specific', '🏢 Company-Specific']].map(([v, l]) => (
              <button key={v} onClick={() => setForm({ ...form, type: v })}
                className={`py-2.5 px-3 rounded-lg text-sm border transition-colors ${form.type === v ? 'bg-primary-600 border-primary-600 text-white' : 'border-gray-700 text-gray-400 hover:border-gray-600'}`}>
                {l}
              </button>
            ))}
          </div>
        </div>

        {form.type === 'company_specific' && (
          <div>
            <label className="label">Company</label>
            <select className="input" value={form.company} onChange={e => setForm({ ...form, company: e.target.value })}>
              <option value="">Select company...</option>
              {companies.map(c => <option key={c.id} value={c.name}>{c.name}</option>)}
            </select>
          </div>
        )}

        <div>
          <label className="label">Role</label>
          <input className="input" value={form.role} onChange={e => setForm({ ...form, role: e.target.value })} />
        </div>

        <div>
          <label className="label">Difficulty</label>
          <div className="flex gap-2">
            {['easy', 'medium', 'hard'].map(d => (
              <button key={d} onClick={() => setForm({ ...form, difficulty: d })}
                className={`flex-1 py-2 rounded-lg text-sm capitalize border transition-colors ${form.difficulty === d ? 'bg-primary-600 border-primary-600 text-white' : 'border-gray-700 text-gray-400 hover:border-gray-600'}`}>
                {d}
              </button>
            ))}
          </div>
        </div>

        <div>
          <label className="label">Number of Questions: {form.num_questions}</label>
          <input type="range" min={3} max={10} value={form.num_questions}
            onChange={e => setForm({ ...form, num_questions: +e.target.value })}
            className="w-full accent-primary-500" />
          <div className="flex justify-between text-xs text-gray-600 mt-1"><span>3</span><span>10</span></div>
        </div>

        <button onClick={start} disabled={starting} className="btn-primary w-full py-3 flex items-center justify-center gap-2">
          {starting ? <><Loader size={16} className="animate-spin" /> Starting...</> : <><Play size={16} /> Start Interview</>}
        </button>
      </div>
    </div>
  )
}
