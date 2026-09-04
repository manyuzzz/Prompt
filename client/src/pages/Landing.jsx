import { Link } from 'react-router-dom'
import { Zap, Brain, Code2, Mic, FileText, Map, ArrowRight, Star, Users, Trophy } from 'lucide-react'

const features = [
  { icon: Brain, title: 'AI Chatbot', desc: 'Ask anything about placements — get instant expert answers on DSA, HR, system design, and more.' },
  { icon: FileText, title: 'Resume Analyzer', desc: 'Upload your resume and get ATS score, JD matching, and AI-powered improvement suggestions.' },
  { icon: Map, title: 'Personalized Roadmap', desc: 'Get a 12-week placement roadmap tailored to your target company, role, and skill level.' },
  { icon: Mic, title: 'AI Mock Interview', desc: 'Practice HR, Technical, and Behavioral interviews with AI feedback on every answer.' },
  { icon: Code2, title: 'Coding Platform', desc: 'Solve 150+ curated problems across topics with multi-language code execution.' },
  { icon: Trophy, title: 'Aptitude Training', desc: 'Practice Quantitative, Logical, and Verbal with company-specific question patterns.' },
]

const stats = [
  { value: '50+', label: 'Coding Problems' },
  { value: '100+', label: 'Aptitude Questions' },
  { value: '10+', label: 'Top Companies' },
  { value: '95%', label: 'Placement Rate' },
]

export default function Landing() {
  return (
    <div className="min-h-screen bg-gray-950 text-white">
      <nav className="border-b border-gray-800 px-6 py-4 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 rounded-lg bg-primary-600 flex items-center justify-center">
            <Zap size={16} className="text-white" />
          </div>
          <span className="font-bold text-lg">PlacementAI</span>
        </div>
        <div className="flex items-center gap-3">
          <Link to="/login" className="btn-ghost text-sm">Sign in</Link>
          <Link to="/register" className="btn-primary text-sm">Get Started</Link>
        </div>
      </nav>

      <section className="px-6 py-24 text-center max-w-4xl mx-auto">
        <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-primary-600/10 border border-primary-600/30 text-primary-400 text-sm mb-6">
          <Zap size={14} />
          <span>AI-Powered Placement Preparation</span>
        </div>
        <h1 className="text-5xl md:text-6xl font-bold mb-6 leading-tight">
          Land Your Dream Job with{' '}
          <span className="text-gradient">AI-Powered</span>{' '}
          Placement Prep
        </h1>
        <p className="text-xl text-gray-400 mb-10 max-w-2xl mx-auto">
          Complete placement preparation platform with AI chatbot, resume analyzer, mock interviews, coding practice, and personalized roadmaps — everything you need in one place.
        </p>
        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <Link to="/register" className="btn-primary flex items-center gap-2 text-base py-3 px-8">
            Start Free <ArrowRight size={18} />
          </Link>
          <Link to="/login" className="btn-secondary flex items-center gap-2 text-base py-3 px-8">
            Sign In
          </Link>
        </div>

        <div className="grid grid-cols-2 md:grid-cols-4 gap-6 mt-20">
          {stats.map(({ value, label }) => (
            <div key={label} className="text-center">
              <div className="text-3xl font-bold text-primary-400">{value}</div>
              <div className="text-sm text-gray-500 mt-1">{label}</div>
            </div>
          ))}
        </div>
      </section>

      <section className="px-6 py-16 max-w-6xl mx-auto">
        <h2 className="text-3xl font-bold text-center mb-4">Everything for Placement Success</h2>
        <p className="text-gray-400 text-center mb-12">Six integrated modules that work together to maximize your placement readiness</p>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {features.map(({ icon: Icon, title, desc }) => (
            <div key={title} className="card hover:border-primary-600/50 transition-colors group">
              <div className="w-10 h-10 rounded-lg bg-primary-600/10 border border-primary-600/30 flex items-center justify-center mb-4 group-hover:bg-primary-600/20 transition-colors">
                <Icon size={20} className="text-primary-400" />
              </div>
              <h3 className="font-semibold text-white mb-2">{title}</h3>
              <p className="text-sm text-gray-400">{desc}</p>
            </div>
          ))}
        </div>
      </section>

      <section className="px-6 py-16 text-center">
        <div className="card max-w-2xl mx-auto border-primary-600/30">
          <Users size={40} className="text-primary-400 mx-auto mb-4" />
          <h2 className="text-2xl font-bold mb-3">Ready to Ace Your Placements?</h2>
          <p className="text-gray-400 mb-6">Join thousands of students who improved their placement readiness with PlacementAI</p>
          <Link to="/register" className="btn-primary inline-flex items-center gap-2">
            Create Free Account <ArrowRight size={16} />
          </Link>
        </div>
      </section>

      <footer className="border-t border-gray-800 px-6 py-8 text-center text-gray-600 text-sm">
        © 2024 PlacementAI. Built for engineering students.
      </footer>
    </div>
  )
}
