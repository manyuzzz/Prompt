import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { roadmapAPI } from '../services/api'
import { useToast } from '../hooks/useToast'
import { CheckCircle, Circle, Clock, ChevronDown, ChevronRight, ArrowLeft, Zap } from 'lucide-react'

const TYPE_COLORS = {
  coding: 'badge-green',
  aptitude: 'badge-purple',
  interview: 'badge-yellow',
  reading: 'badge-blue',
  revision: 'badge-red',
}

export default function RoadmapDetail() {
  const { id } = useParams()
  const [roadmap, setRoadmap] = useState(null)
  const [loading, setLoading] = useState(true)
  const [openPhase, setOpenPhase] = useState(0)
  const [completing, setCompleting] = useState(null)
  const toast = useToast()
  const navigate = useNavigate()

  useEffect(() => {
    roadmapAPI.getOne(id)
      .then(r => { setRoadmap(r.data.roadmap); })
      .catch(() => toast.error('Failed to load'))
      .finally(() => setLoading(false))
  }, [id])

  const completeTask = async (taskId) => {
    if (completing) return
    setCompleting(taskId)
    try {
      const { data } = await roadmapAPI.completeTask(id, taskId)
      setRoadmap(data.roadmap)
      toast.success(`+${data.xp_awarded} XP earned!`)
    } catch { toast.error('Failed to mark complete') }
    finally { setCompleting(null) }
  }

  if (loading) return <div className="flex justify-center py-20"><div className="animate-spin w-8 h-8 border-2 border-primary-500 border-t-transparent rounded-full" /></div>
  if (!roadmap) return null

  return (
    <div className="space-y-6 animate-fade-in max-w-4xl">
      <div className="flex items-center gap-3">
        <button onClick={() => navigate('/roadmap')} className="btn-ghost p-2"><ArrowLeft size={18} /></button>
        <div>
          <h1 className="text-2xl font-bold text-white">{roadmap.title}</h1>
          <p className="text-gray-400">{roadmap.target_company || 'General'} · {roadmap.target_role}</p>
        </div>
      </div>

      <div className="grid grid-cols-3 gap-4">
        <div className="card text-center">
          <div className="text-2xl font-bold text-primary-400">{Math.round(roadmap.completion_percentage || 0)}%</div>
          <div className="text-xs text-gray-500 mt-1">Complete</div>
        </div>
        <div className="card text-center">
          <div className="text-2xl font-bold text-green-400">{roadmap.total_tasks || 0}</div>
          <div className="text-xs text-gray-500 mt-1">Total Tasks</div>
        </div>
        <div className="card text-center">
          <div className="text-2xl font-bold text-yellow-400">{roadmap.completed_tasks || 0}</div>
          <div className="text-xs text-gray-500 mt-1">Completed</div>
        </div>
      </div>

      <div className="progress-bar h-3">
        <div className="progress-fill bg-primary-500 h-full" style={{ width: `${roadmap.completion_percentage || 0}%` }} />
      </div>

      {(roadmap.phases || []).map((phase, pi) => (
        <div key={pi} className="card p-0 overflow-hidden">
          <button
            onClick={() => setOpenPhase(openPhase === pi ? -1 : pi)}
            className="w-full flex items-center justify-between p-4 hover:bg-gray-800/50 transition-colors"
          >
            <div className="flex items-center gap-3">
              <div className="w-8 h-8 rounded-full bg-primary-600/20 border border-primary-600/40 flex items-center justify-center text-primary-400 text-sm font-bold">
                {pi + 1}
              </div>
              <div className="text-left">
                <div className="font-semibold text-white">{phase.title}</div>
                <div className="text-xs text-gray-500">{phase.duration} · {phase.focus}</div>
              </div>
            </div>
            {openPhase === pi ? <ChevronDown size={16} /> : <ChevronRight size={16} />}
          </button>

          {openPhase === pi && (
            <div className="border-t border-gray-800">
              {(phase.weeks || []).map((week, wi) => (
                <div key={wi} className="border-b border-gray-800 last:border-0">
                  <div className="px-4 py-2 bg-gray-800/30">
                    <span className="text-sm font-medium text-gray-300">{week.title}</span>
                    <span className="text-xs text-gray-600 ml-2">Week {week.week_number}</span>
                  </div>
                  <div className="divide-y divide-gray-800/50">
                    {(week.tasks || []).map(task => (
                      <div key={task.id} className="flex items-start gap-3 px-4 py-3">
                        <button
                          onClick={() => !task.completed && completeTask(task.id)}
                          disabled={task.completed || completing === task.id}
                          className="mt-0.5 shrink-0"
                        >
                          {task.completed
                            ? <CheckCircle size={18} className="text-green-400" />
                            : completing === task.id
                              ? <div className="w-4.5 h-4.5 border-2 border-primary-500 border-t-transparent rounded-full animate-spin" />
                              : <Circle size={18} className="text-gray-600 hover:text-primary-400 transition-colors" />
                          }
                        </button>
                        <div className="flex-1 min-w-0">
                          <p className={`text-sm font-medium ${task.completed ? 'text-gray-500 line-through' : 'text-white'}`}>
                            {task.title}
                          </p>
                          {task.description && <p className="text-xs text-gray-500 mt-0.5">{task.description}</p>}
                          <div className="flex items-center gap-2 mt-1.5">
                            <span className={`badge ${TYPE_COLORS[task.type] || 'badge-blue'}`}>{task.type}</span>
                            <span className="text-xs text-gray-600 flex items-center gap-1"><Clock size={10} />{task.estimated_time}</span>
                            <span className="text-xs text-yellow-500 flex items-center gap-1"><Zap size={10} />+{task.xp_reward}</span>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      ))}
    </div>
  )
}
