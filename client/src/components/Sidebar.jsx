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

  return (
    <>
      {open && (
        <div className="fixed inset-0 bg-black/60 z-20 lg:hidden backdrop-blur-sm" onClick={onClose} />
      )}
      <aside
        className={`
          fixed lg:static inset-y-0 left-0 z-30
          w-64 flex flex-col transition-transform duration-300
          ${open ? 'translate-x-0' : '-translate-x-full lg:translate-x-0 lg:w-0 lg:overflow-hidden'}
        `}
        style={{
          background: 'linear-gradient(180deg, #0a0f2e 0%, #080c22 40%, #060919 100%)',
          borderRight: '1px solid rgba(139, 92, 246, 0.15)',
        }}
      >
        {/* Logo */}
        <div className="flex items-center justify-between p-4" style={{ borderBottom: '1px solid rgba(139,92,246,0.12)' }}>
          <div className="flex items-center gap-2.5">
            <div className="w-8 h-8 rounded-lg flex items-center justify-center"
              style={{ background: 'linear-gradient(135deg, #7c3aed, #6366f1)', boxShadow: '0 0 16px rgba(124,58,237,0.5)' }}>
              <Zap size={16} className="text-white" />
            </div>
            <div>
              <span className="font-bold text-white text-sm tracking-tight">PlacementAI</span>
              <div className="w-full h-px mt-0.5" style={{ background: 'linear-gradient(90deg, rgba(139,92,246,0.6), transparent)' }} />
            </div>
          </div>
          <button onClick={onClose} className="lg:hidden text-gray-500 hover:text-white p-1 rounded transition-colors">
            <X size={18} />
          </button>
        </div>

        {/* User info */}
        {user && (
          <div className="p-4 mx-3 mt-3 rounded-xl" style={{ background: 'rgba(139,92,246,0.08)', border: '1px solid rgba(139,92,246,0.15)' }}>
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-full flex items-center justify-center text-sm font-bold shrink-0"
                style={{
                  background: 'linear-gradient(135deg, rgba(139,92,246,0.3), rgba(99,102,241,0.2))',
                  border: '2px solid rgba(139,92,246,0.4)',
                  color: '#c4b5fd',
                }}>
                {user.name?.charAt(0)?.toUpperCase() || 'U'}
              </div>
              <div className="min-w-0">
                <p className="text-sm font-semibold text-white truncate">{user.name}</p>
                <p className="text-xs text-purple-400">Lv.{user.level} · {getLevelTitle(user.level)}</p>
              </div>
            </div>
            <div className="mt-3 flex items-center justify-between text-xs">
              <span className="flex items-center gap-1" style={{ color: '#fde68a' }}>⚡ {user.xp?.toLocaleString()} XP</span>
              <span className="flex items-center gap-1" style={{ color: '#fb923c' }}>🔥 {user.streak}d</span>
            </div>
          </div>
        )}

        {/* Nav */}
        <nav className="flex-1 overflow-y-auto p-3 space-y-0.5 mt-2">
          {navItems.map(({ to, icon: Icon, label }) => (
            <NavLink
              key={to}
              to={to}
              className={({ isActive }) =>
                `flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-all duration-200 ${
                  isActive ? 'nav-link-active' : 'text-gray-500 hover:text-gray-200 hover:bg-white/5'
                }`
              }
            >
              {({ isActive }) => (
                <>
                  <Icon size={17} className={isActive ? 'text-purple-400' : ''} />
                  {label}
                </>
              )}
            </NavLink>
          ))}
        </nav>

        <div className="p-4" style={{ borderTop: '1px solid rgba(139,92,246,0.1)' }}>
          <div className="text-xs text-center" style={{ color: 'rgba(139,92,246,0.4)' }}>
            AI Placement Prep v1.0
          </div>
        </div>
      </aside>
    </>
  )
}
