import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { useToast } from '../hooks/useToast'
import { Zap, Eye, EyeOff } from 'lucide-react'

const COLLEGES = ['IIT Bombay', 'IIT Delhi', 'NIT Trichy', 'VIT', 'SRM', 'BITS Pilani', 'IIIT Hyderabad', 'Other']
const BRANCHES = ['Computer Science', 'Information Technology', 'Electronics & Communication', 'Electrical', 'Mechanical', 'Civil', 'Other']

export default function Register() {
  const [form, setForm] = useState({
    name: '', email: '', password: '',
    college: '', branch: '', graduation_year: new Date().getFullYear() + 1,
  })
  const [showPw, setShowPw] = useState(false)
  const [loading, setLoading] = useState(false)
  const { register } = useAuth()
  const toast = useToast()
  const navigate = useNavigate()

  const set = (k) => (e) => setForm({ ...form, [k]: e.target.value })

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (form.password.length < 6) { toast.error('Password must be at least 6 characters'); return }
    setLoading(true)
    try {
      await register(form)
      navigate('/dashboard')
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Registration failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gray-950 flex items-center justify-center p-4">
      <div className="w-full max-w-md">
        <div className="text-center mb-8">
          <div className="w-12 h-12 rounded-xl bg-primary-600 flex items-center justify-center mx-auto mb-4">
            <Zap size={24} className="text-white" />
          </div>
          <h1 className="text-2xl font-bold text-white">Create your account</h1>
          <p className="text-gray-400 mt-1">Start your placement journey</p>
        </div>

        <div className="card">
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="label">Full Name</label>
              <input type="text" required className="input" placeholder="Your name" value={form.name} onChange={set('name')} />
            </div>
            <div>
              <label className="label">Email</label>
              <input type="email" required className="input" placeholder="you@example.com" value={form.email} onChange={set('email')} />
            </div>
            <div>
              <label className="label">Password</label>
              <div className="relative">
                <input
                  type={showPw ? 'text' : 'password'} required className="input pr-10"
                  placeholder="Min 6 characters" value={form.password} onChange={set('password')}
                />
                <button type="button" onClick={() => setShowPw(!showPw)}
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-500 hover:text-gray-300">
                  {showPw ? <EyeOff size={16} /> : <Eye size={16} />}
                </button>
              </div>
            </div>
            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="label">College</label>
                <select className="input" value={form.college} onChange={set('college')}>
                  <option value="">Select</option>
                  {COLLEGES.map(c => <option key={c} value={c}>{c}</option>)}
                </select>
              </div>
              <div>
                <label className="label">Branch</label>
                <select className="input" value={form.branch} onChange={set('branch')}>
                  <option value="">Select</option>
                  {BRANCHES.map(b => <option key={b} value={b}>{b}</option>)}
                </select>
              </div>
            </div>
            <div>
              <label className="label">Graduation Year</label>
              <input type="number" className="input" min={2024} max={2030}
                value={form.graduation_year} onChange={set('graduation_year')} />
            </div>
            <button type="submit" disabled={loading} className="btn-primary w-full py-3">
              {loading ? 'Creating account...' : 'Create Account'}
            </button>
          </form>
          <p className="text-center text-sm text-gray-500 mt-4">
            Already have an account?{' '}
            <Link to="/login" className="text-primary-400 hover:text-primary-300">Sign in</Link>
          </p>
        </div>
      </div>
    </div>
  )
}
