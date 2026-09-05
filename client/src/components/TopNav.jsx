import { Menu, Bell, LogOut, Settings } from 'lucide-react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

export default function TopNav({ onMenuClick }) {
  const { user, logout } = useAuth()
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  return (
    <header
      className="h-14 flex items-center justify-between px-4 shrink-0"
      style={{
        background: 'linear-gradient(90deg, rgba(8,12,34,0.95) 0%, rgba(5,7,26,0.98) 100%)',
        borderBottom: '1px solid rgba(139, 92, 246, 0.12)',
        backdropFilter: 'blur(12px)',
      }}
    >
      <div className="flex items-center gap-3">
        <button onClick={onMenuClick} className="text-gray-500 hover:text-purple-300 p-1.5 rounded-lg hover:bg-white/5 transition-all">
          <Menu size={20} />
        </button>
        {user && (
          <div className="hidden sm:flex items-center gap-2 text-xs text-gray-500">
            <span className="text-purple-400 font-medium">{user.name}</span>
            <span>·</span>
            <span className="text-yellow-400">⚡ {user.xp?.toLocaleString()} XP</span>
          </div>
        )}
      </div>

      <div className="flex items-center gap-1">
        <button className="text-gray-500 hover:text-purple-300 p-2 rounded-lg hover:bg-white/5 transition-all">
          <Bell size={17} />
        </button>
        <button
          onClick={() => navigate('/profile')}
          className="text-gray-500 hover:text-purple-300 p-2 rounded-lg hover:bg-white/5 transition-all"
        >
          <Settings size={17} />
        </button>
        <div className="w-px h-5 mx-1" style={{ background: 'rgba(139,92,246,0.2)' }} />
        <button
          onClick={handleLogout}
          className="text-gray-500 hover:text-red-400 p-2 rounded-lg hover:bg-red-500/5 flex items-center gap-2 text-sm transition-all"
        >
          <LogOut size={16} />
          <span className="hidden sm:inline">Logout</span>
        </button>
      </div>
    </header>
  )
}
