import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { ToastContainer } from 'react-toastify'
import 'react-toastify/dist/ReactToastify.css'
import { AuthProvider, useAuth } from './context/AuthContext'
import Layout from './components/Layout'

import Landing from './pages/Landing'
import Login from './pages/Login'
import Register from './pages/Register'
import Dashboard from './pages/Dashboard'
import Chat from './pages/Chat'
import Resume from './pages/Resume'
import ResumeAnalyze from './pages/ResumeAnalyze'
import ResumeCreate from './pages/ResumeCreate'
import Roadmap from './pages/Roadmap'
import RoadmapDetail from './pages/RoadmapDetail'
import Interview from './pages/Interview'
import InterviewSetup from './pages/InterviewSetup'
import InterviewSession from './pages/InterviewSession'
import InterviewResult from './pages/InterviewResult'
import Coding from './pages/Coding'
import ProblemDetail from './pages/ProblemDetail'
import Aptitude from './pages/Aptitude'
import Companies from './pages/Companies'
import CompanyDetail from './pages/CompanyDetail'
import Profile from './pages/Profile'

function PrivateRoute({ children }) {
  const { user, loading } = useAuth()
  if (loading) return <div className="flex items-center justify-center min-h-screen"><div className="animate-spin w-8 h-8 border-2 border-primary-500 border-t-transparent rounded-full" /></div>
  return user ? children : <Navigate to="/login" replace />
}

function PublicRoute({ children }) {
  const { user, loading } = useAuth()
  if (loading) return null
  return user ? <Navigate to="/dashboard" replace /> : children
}

function AppRoutes() {
  return (
    <Routes>
      <Route path="/" element={<PublicRoute><Landing /></PublicRoute>} />
      <Route path="/login" element={<PublicRoute><Login /></PublicRoute>} />
      <Route path="/register" element={<PublicRoute><Register /></PublicRoute>} />
      <Route element={<PrivateRoute><Layout /></PrivateRoute>}>
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/chat" element={<Chat />} />
        <Route path="/resume" element={<Resume />} />
        <Route path="/resume/analyze" element={<ResumeAnalyze />} />
        <Route path="/resume/create" element={<ResumeCreate />} />
        <Route path="/roadmap" element={<Roadmap />} />
        <Route path="/roadmap/:id" element={<RoadmapDetail />} />
        <Route path="/interview" element={<Interview />} />
        <Route path="/interview/setup" element={<InterviewSetup />} />
        <Route path="/interview/session/:id" element={<InterviewSession />} />
        <Route path="/interview/result/:id" element={<InterviewResult />} />
        <Route path="/technical" element={<Coding />} />
        <Route path="/technical/problems" element={<Coding />} />
        <Route path="/technical/problem/:slug" element={<ProblemDetail />} />
        <Route path="/aptitude" element={<Aptitude />} />
        <Route path="/companies" element={<Companies />} />
        <Route path="/companies/:slug" element={<CompanyDetail />} />
        <Route path="/profile" element={<Profile />} />
      </Route>
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  )
}

export default function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <AppRoutes />
        <ToastContainer position="top-right" autoClose={3000} theme="dark" />
      </AuthProvider>
    </BrowserRouter>
  )
}
