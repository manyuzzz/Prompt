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
    <header className="h-14 bg-gray-900 border-b border-gray-800 flex items-center justify-between px-4 shrink-0">
      <button onClick={onMenuClick} className="text-gray-400 hover:text-white p-1 rounded">
        <Menu size={20} />
      </button>

      <div className="flex items-center gap-2">
        <button className="text-gray-400 hover:text-white p-2 rounded-lg hover:bg-gray-800">
          <Bell size={18} />
        </button>
        <button
          onClick={() => navigate('/profile')}
          className="text-gray-400 hover:text-white p-2 rounded-lg hover:bg-gray-800"
        >
          <Settings size={18} />
        </button>
        <div className="w-px h-6 bg-gray-700 mx-1" />
        <button
          onClick={handleLogout}
          className="text-gray-400 hover:text-red-400 p-2 rounded-lg hover:bg-gray-800 flex items-center gap-2 text-sm"
        >
          <LogOut size={16} />
          <span className="hidden sm:inline">Logout</span>
        </button>
      </div>
    </header>
  )
}
