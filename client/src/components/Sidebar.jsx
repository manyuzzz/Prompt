import { NavLink, useLocation } from 'react-router-dom'
import {
  LayoutDashboard, MessageSquare, FileText, Map, Mic,
  Code2, Brain, Building2, User, X, Zap,
} from 'lucide-react'
import { useAuth } from '../context/AuthContext'
import { getLevelTitle } from '../utils/helpers'

const navItems = [
  { to: '/dashboard', icon: LayoutDashboard, label: 'Dashboard' },
  { to: '/chat', icon: MessageSquare, label: 'AI Chatbot' },
  { to: '/resume', icon: FileText, label: 'Resume' },
  { to: '/roadmap', icon: Map, label: 'Roadmap' },
  { to: '/interview', icon: Mic, label: 'Mock Interview' },
  { to: '/technical', icon: Code2, label: 'Coding' },
  { to: '/aptitude', icon: Brain, label: 'Aptitude' },
  { to: '/companies', icon: Building2, label: 'Companies' },
  { to: '/profile', icon: User, label: 'Profile' },
]

export default function Sidebar({ open, onClose }) {
  const { user } = useAuth()
  const location = useLocation()

  return (
    <>
      {open && (
        <div className="fixed inset-0 bg-black/50 z-20 lg:hidden" onClick={onClose} />
      )}
      <aside
        className={`
          fixed lg:static inset-y-0 left-0 z-30
          w-64 bg-gray-900 border-r border-gray-800
          flex flex-col transition-transform duration-300
          ${open ? 'translate-x-0' : '-translate-x-full lg:translate-x-0 lg:w-0 lg:overflow-hidden'}
        `}
      >
        <div className="flex items-center justify-between p-4 border-b border-gray-800">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-lg bg-primary-600 flex items-center justify-center">
              <Zap size={16} className="text-white" />
            </div>
            <span className="font-bold text-white text-sm">PlacementAI</span>
          </div>
          <button onClick={onClose} className="lg:hidden text-gray-400 hover:text-white p-1">
            <X size={18} />
          </button>
        </div>

        {user && (
          <div className="p-4 border-b border-gray-800">
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-full bg-primary-600/30 border border-primary-600/50 flex items-center justify-center text-primary-400 font-bold text-sm">
                {user.name?.charAt(0)?.toUpperCase() || 'U'}
              </div>
              <div className="min-w-0">
                <p className="text-sm font-medium text-white truncate">{user.name}</p>
                <p className="text-xs text-gray-500">Lv.{user.level} · {getLevelTitle(user.level)}</p>
              </div>
            </div>
            <div className="mt-3 flex items-center justify-between text-xs">
              <span className="text-yellow-400">⚡ {user.xp?.toLocaleString()} XP</span>
              <span className="text-orange-400">🔥 {user.streak}d streak</span>
            </div>
          </div>
        )}

        <nav className="flex-1 overflow-y-auto p-3 space-y-1">
          {navItems.map(({ to, icon: Icon, label }) => (
            <NavLink
              key={to}
              to={to}
              className={({ isActive }) =>
                `flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors ${
                  isActive
                    ? 'bg-primary-600/20 text-primary-400 border border-primary-600/30'
                    : 'text-gray-400 hover:text-white hover:bg-gray-800'
                }`
              }
            >
              <Icon size={18} />
              {label}
            </NavLink>
          ))}
        </nav>

        <div className="p-4 border-t border-gray-800">
          <div className="text-xs text-gray-600 text-center">
            AI Placement Prep v1.0
          </div>
        </div>
      </aside>
    </>
  )
}
