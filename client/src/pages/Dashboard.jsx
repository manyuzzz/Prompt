import { useState, useEffect } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { progressAPI } from '../services/api'
import { useAuth } from '../context/AuthContext'
import { getScoreColor, getScoreBg, timeAgo } from '../utils/helpers'
import {
  AreaChart, Area, XAxis, YAxis, Tooltip, ResponsiveContainer,
} from 'recharts'
import {
  Code2, Brain, Mic, FileText, Map, Zap, Flame, Trophy,
  CheckCircle, Clock, ArrowRight, TrendingUp,
} from 'lucide-react'

export default function Dashboard() {
  const [data, setData] = useState(null)
  const [loading, setLoading] = useState(true)
  const { user } = useAuth()
  const navigate = useNavigate()

  useEffect(() => {
    progressAPI.getDashboard()
      .then(r => setData(r.data))
      .catch(console.error)
      .finally(() => setLoading(false))
  }, [])

  if (loading) return (
    <div className="flex items-center justify-center h-64">
      <div className="animate-spin w-8 h-8 border-2 border-primary-500 border-t-transparent rounded-full" />
    </div>
  )

  const summary = data?.summary || {}
  const weeklyChart = data?.weekly_chart || []
  const todaysTasks = data?.todays_tasks || []
  const recentInterviews = data?.recent_interviews || []
  const codingStats = data?.coding_stats || {}

  const readiness = summary.placement_readiness || 0
  const readinessColor = readiness >= 70 ? 'text-green-400' : readiness >= 40 ? 'text-yellow-400' : 'text-red-400'

  return (
    <div className="space-y-6 animate-fade-in">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white">
            Welcome back, {user?.name?.split(' ')[0]}! 👋
          </h1>
          <p className="text-gray-400 mt-1">Here's your placement readiness overview</p>
        </div>
        <div className="flex items-center gap-4 text-sm">
          <div className="flex items-center gap-1.5 text-yellow-400">
            <Zap size={16} />
            <span className="font-semibold">{user?.xp?.toLocaleString()} XP</span>
          </div>
          <div className="flex items-center gap-1.5 text-orange-400">
            <Flame size={16} />
            <span className="font-semibold">{user?.streak}d</span>
          </div>
        </div>
      </div>

      {/* Readiness + Stats */}
      <div className="grid grid-cols-1 lg:grid-cols-4 gap-4">
        <div className="card lg:col-span-1 flex flex-col items-center justify-center text-center py-8">
          <div className={`text-5xl font-bold ${readinessColor}`}>{readiness}%</div>
          <div className="text-gray-400 text-sm mt-2">Placement Readiness</div>
          <div className="progress-bar w-32 mt-4">
            <div className={`progress-fill ${getScoreBg(readiness)}`} style={{ width: `${readiness}%` }} />
          </div>
        </div>
        <div className="lg:col-span-3 grid grid-cols-2 md:grid-cols-3 gap-4">
          {[
            { icon: FileText, label: 'Resume Score', value: `${summary.resume_score || 0}%`, color: 'text-blue-400', to: '/resume' },
            { icon: Code2, label: 'Problems Solved', value: summary.problems_solved || 0, color: 'text-green-400', to: '/technical' },
            { icon: Brain, label: 'Aptitude Accuracy', value: `${Math.round(summary.aptitude_accuracy || 0)}%`, color: 'text-purple-400', to: '/aptitude' },
            { icon: Mic, label: 'Interview Score', value: `${Math.round(summary.interview_score || 0)}%`, color: 'text-pink-400', to: '/interview' },
            { icon: Map, label: 'Roadmap Done', value: `${Math.round(summary.roadmap_completion || 0)}%`, color: 'text-yellow-400', to: '/roadmap' },
            { icon: Trophy, label: 'Level', value: `Lv.${user?.level || 1}`, color: 'text-orange-400', to: '/profile' },
          ].map(({ icon: Icon, label, value, color, to }) => (
            <Link key={label} to={to} className="card hover:border-gray-700 transition-colors group">
              <div className="flex items-start justify-between">
                <Icon size={18} className={`${color} opacity-80`} />
                <ArrowRight size={14} className="text-gray-600 group-hover:text-gray-400 transition-colors" />
              </div>
              <div className={`text-2xl font-bold mt-3 ${color}`}>{value}</div>
              <div className="text-xs text-gray-500 mt-1">{label}</div>
            </Link>
          ))}
        </div>
      </div>

      {/* Weekly Chart */}
      <div className="card">
        <h3 className="font-semibold text-white mb-4 flex items-center gap-2">
          <TrendingUp size={18} className="text-primary-400" /> Weekly Activity
        </h3>
        <div className="h-48">
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={weeklyChart}>
              <defs>
                <linearGradient id="cg" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#8b5cf6" stopOpacity={0.4} />
                  <stop offset="95%" stopColor="#8b5cf6" stopOpacity={0} />
                </linearGradient>
                <linearGradient id="ag" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#06b6d4" stopOpacity={0.3} />
                  <stop offset="95%" stopColor="#06b6d4" stopOpacity={0} />
                </linearGradient>
              </defs>
              <XAxis dataKey="day" tick={{ fill: '#6b7280', fontSize: 12 }} axisLine={false} tickLine={false} />
              <YAxis hide />
              <Tooltip contentStyle={{ background: '#0d1230', border: '1px solid rgba(139,92,246,0.3)', borderRadius: 8, fontSize: 12 }} />
              <Area type="monotone" dataKey="coding" stroke="#8b5cf6" fill="url(#cg)" strokeWidth={2} name="Coding" />
              <Area type="monotone" dataKey="aptitude" stroke="#06b6d4" fill="url(#ag)" strokeWidth={2} name="Aptitude" />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        {/* Today's Tasks */}
        <div className="card">
          <h3 className="font-semibold text-white mb-4 flex items-center gap-2">
            <CheckCircle size={18} className="text-green-400" /> Today's Tasks
          </h3>
          {todaysTasks.length === 0 ? (
            <div className="text-center py-8 text-gray-500">
              <Map size={32} className="mx-auto mb-2 opacity-50" />
              <p className="text-sm">No roadmap active.</p>
              <Link to="/roadmap" className="text-primary-400 text-sm hover:underline mt-1 block">Generate your roadmap →</Link>
            </div>
          ) : (
            <div className="space-y-3">
              {todaysTasks.slice(0, 5).map((task) => (
                <div key={task.id} className={`flex items-start gap-3 p-3 rounded-lg border ${task.completed ? 'border-green-800/30 bg-green-900/10' : 'border-gray-800 bg-gray-800/30'}`}>
                  <CheckCircle size={16} className={task.completed ? 'text-green-400 mt-0.5' : 'text-gray-600 mt-0.5'} />
                  <div className="flex-1 min-w-0">
                    <p className={`text-sm font-medium ${task.completed ? 'text-gray-500 line-through' : 'text-white'}`}>{task.title}</p>
                    <div className="flex items-center gap-2 mt-1">
                      <span className="badge badge-blue">{task.type}</span>
                      <span className="text-xs text-gray-500 flex items-center gap-1"><Clock size={10} />{task.estimated_time}</span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Coding Stats */}
        <div className="card">
          <h3 className="font-semibold text-white mb-4 flex items-center gap-2">
            <Code2 size={18} className="text-green-400" /> Coding Stats
          </h3>
          <div className="grid grid-cols-3 gap-3 mb-4">
            {[
              { label: 'Easy', value: codingStats.easy || 0, color: 'text-green-400' },
              { label: 'Medium', value: codingStats.medium || 0, color: 'text-yellow-400' },
              { label: 'Hard', value: codingStats.hard || 0, color: 'text-red-400' },
            ].map(({ label, value, color }) => (
              <div key={label} className="bg-gray-800/50 rounded-lg p-3 text-center">
                <div className={`text-2xl font-bold ${color}`}>{value}</div>
                <div className="text-xs text-gray-500 mt-1">{label}</div>
              </div>
            ))}
          </div>
          <div className="border-t border-gray-800 pt-4 flex items-center justify-between">
            <div className="text-sm text-gray-400">
              Total: <span className="text-white font-semibold">{codingStats.total || 0}</span> solved
            </div>
            <Link to="/technical" className="text-primary-400 text-sm hover:underline flex items-center gap-1">
              Practice <ArrowRight size={14} />
            </Link>
          </div>
        </div>
      </div>
    </div>
  )
}
