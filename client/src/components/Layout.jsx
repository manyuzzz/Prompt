import { Outlet } from 'react-router-dom'
import Sidebar from './Sidebar'
import TopNav from './TopNav'
import { useState } from 'react'

export default function Layout() {
  const [sidebarOpen, setSidebarOpen] = useState(true)

  return (
    <div className="flex h-screen overflow-hidden" style={{ background: 'linear-gradient(135deg, #05071a 0%, #080c22 60%, #05071a 100%)' }}>
      {/* Decorative orbs */}
      <div className="pointer-events-none fixed top-0 left-64 w-96 h-96 rounded-full opacity-10"
        style={{ background: 'radial-gradient(circle, rgba(139,92,246,0.6) 0%, transparent 70%)', filter: 'blur(60px)' }} />
      <div className="pointer-events-none fixed bottom-0 right-0 w-80 h-80 rounded-full opacity-8"
        style={{ background: 'radial-gradient(circle, rgba(6,182,212,0.4) 0%, transparent 70%)', filter: 'blur(80px)' }} />

      <Sidebar open={sidebarOpen} onClose={() => setSidebarOpen(false)} />
      <div className="flex-1 flex flex-col min-w-0 overflow-hidden">
        <TopNav onMenuClick={() => setSidebarOpen(!sidebarOpen)} />
        <main className="flex-1 overflow-y-auto p-6">
          <div className="max-w-7xl mx-auto">
            <Outlet />
          </div>
        </main>
      </div>
    </div>
  )
}
