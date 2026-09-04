import { useState } from 'react'
import { useAuth } from '../context/AuthContext'
import { authAPI } from '../services/api'
import { useToast } from '../hooks/useToast'
import { getLevelTitle } from '../utils/helpers'
import { User, Save, Zap, Flame, Trophy, Star } from 'lucide-react'

const XP_LEVELS = [0, 500, 1500, 3000, 5000, 8000, 12000, 17000, 23000, 30000]

export default function Profile() {
  const { user, updateUser } = useAuth()
  const [form, setForm] = useState({
    name: user?.name || '',
    college: user?.college || '',
    branch: user?.branch || '',
    graduation_year: user?.graduation_year || '',
  })
  const [saving, setSaving] = useState(false)
  const toast = useToast()

  const set = (k) => (e) => setForm({ ...form, [k]: e.target.value })

  const save = async () => {
    setSaving(true)
    try {
      const { data } = await authAPI.updateProfile(form)
      updateUser(data.user)
      toast.success('Profile updated!')
    } catch { toast.error('Update failed') }
    finally { setSaving(false) }
  }

  const currentXP = user?.xp || 0
  const level = user?.level || 1
  const nextLevelXP = XP_LEVELS[level] || 30000
  const prevLevelXP = XP_LEVELS[level - 1] || 0
  const xpProgress = Math.min(100, ((currentXP - prevLevelXP) / (nextLevelXP - prevLevelXP)) * 100)

  const BADGE_ICONS = { 'first_solve': '🎯', 'streak_7': '🔥', 'streak_30': '💎', 'coding_10': '⚡', 'interview_ace': '🏆' }

  return (
    <div className="space-y-6 animate-fade-in max-w-2xl">
      <h1 className="text-2xl font-bold text-white">Profile</h1>

      {/* XP & Level */}
      <div className="card">
        <div className="flex items-center gap-4 mb-6">
          <div className="w-16 h-16 rounded-full bg-primary-600/30 border-2 border-primary-600/50 flex items-center justify-center text-2xl font-bold text-primary-400">
            {user?.name?.charAt(0)?.toUpperCase()}
          </div>
          <div>
            <h2 className="text-xl font-bold text-white">{user?.name}</h2>
            <p className="text-gray-400">{user?.email}</p>
            <div className="flex items-center gap-3 mt-1">
              <span className="badge badge-yellow">Lv.{level} · {getLevelTitle(level)}</span>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-3 gap-4 text-center mb-6">
          <div className="bg-gray-800/50 rounded-xl p-4">
            <Zap size={20} className="text-yellow-400 mx-auto mb-1.5" />
            <div className="text-xl font-bold text-white">{currentXP.toLocaleString()}</div>
            <div className="text-xs text-gray-500">Total XP</div>
          </div>
          <div className="bg-gray-800/50 rounded-xl p-4">
            <Flame size={20} className="text-orange-400 mx-auto mb-1.5" />
            <div className="text-xl font-bold text-white">{user?.streak || 0}</div>
            <div className="text-xs text-gray-500">Day Streak</div>
          </div>
          <div className="bg-gray-800/50 rounded-xl p-4">
            <Trophy size={20} className="text-yellow-400 mx-auto mb-1.5" />
            <div className="text-xl font-bold text-white">{user?.badges?.length || 0}</div>
            <div className="text-xs text-gray-500">Badges</div>
          </div>
        </div>

        {/* XP Progress to next level */}
        <div>
          <div className="flex justify-between text-xs text-gray-500 mb-1.5">
            <span>Level {level}</span>
            <span>{currentXP.toLocaleString()} / {nextLevelXP.toLocaleString()} XP</span>
            <span>Level {level + 1}</span>
          </div>
          <div className="progress-bar h-3">
            <div className="progress-fill bg-gradient-to-r from-primary-500 to-accent-purple"
              style={{ width: `${xpProgress}%` }} />
          </div>
        </div>

        {/* Badges */}
        {user?.badges?.length > 0 && (
          <div className="mt-4">
            <h4 className="text-sm text-gray-500 mb-2">Earned Badges</h4>
            <div className="flex flex-wrap gap-2">
              {user.badges.map(badge => (
                <div key={badge} className="flex items-center gap-1.5 px-3 py-1.5 bg-gray-800 border border-gray-700 rounded-full text-sm">
                  <span>{BADGE_ICONS[badge] || '🏅'}</span>
                  <span className="text-gray-300 capitalize">{badge.replace(/_/g, ' ')}</span>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Edit Profile */}
      <div className="card space-y-4">
        <h3 className="font-semibold text-white flex items-center gap-2"><User size={16} /> Edit Profile</h3>
        <div>
          <label className="label">Full Name</label>
          <input className="input" value={form.name} onChange={set('name')} />
        </div>
        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="label">College</label>
            <input className="input" value={form.college} onChange={set('college')} />
          </div>
          <div>
            <label className="label">Branch</label>
            <input className="input" value={form.branch} onChange={set('branch')} />
          </div>
        </div>
        <div>
          <label className="label">Graduation Year</label>
          <input type="number" className="input" value={form.graduation_year} onChange={set('graduation_year')} />
        </div>
        <button onClick={save} disabled={saving} className="btn-primary flex items-center gap-2">
          <Save size={16} /> {saving ? 'Saving...' : 'Save Changes'}
        </button>
      </div>
    </div>
  )
}
