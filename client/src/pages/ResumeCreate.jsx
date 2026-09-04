import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { resumeAPI } from '../services/api'
import { useToast } from '../hooks/useToast'
import { Plus, Trash2, Save } from 'lucide-react'

const TEMPLATES = ['modern', 'classic', 'minimal', 'technical']

export default function ResumeCreate() {
  const [saving, setSaving] = useState(false)
  const [template, setTemplate] = useState('modern')
  const [form, setForm] = useState({
    personal_info: { name: '', email: '', phone: '', location: '', linkedin: '', github: '', portfolio: '' },
    education: [{ institution: '', degree: '', branch: '', cgpa: '', year_of_passing: '' }],
    experience: [],
    projects: [{ name: '', description: '', tech_stack: [], link: '' }],
    skills: { technical: [], soft: [], tools: [] },
    certifications: [],
    achievements: [],
    coding_profiles: { leetcode: '', hackerrank: '', codechef: '', codeforces: '' },
  })
  const toast = useToast()
  const navigate = useNavigate()

  const setField = (path, value) => {
    setForm(prev => {
      const parts = path.split('.')
      const updated = { ...prev }
      let cur = updated
      for (let i = 0; i < parts.length - 1; i++) {
        cur[parts[i]] = Array.isArray(cur[parts[i]]) ? [...cur[parts[i]]] : { ...cur[parts[i]] }
        cur = cur[parts[i]]
      }
      cur[parts[parts.length - 1]] = value
      return updated
    })
  }

  const addItem = (key, template) => setForm(prev => ({ ...prev, [key]: [...prev[key], template] }))
  const removeItem = (key, idx) => setForm(prev => ({ ...prev, [key]: prev[key].filter((_, i) => i !== idx) }))

  const handleSave = async () => {
    if (!form.personal_info.name || !form.personal_info.email) {
      toast.warn('Name and email are required'); return
    }
    setSaving(true)
    try {
      const payload = { ...form, template, skills: { ...form.skills, technical: form.skills.technical.filter(Boolean) } }
      await resumeAPI.create(payload)
      toast.success('Resume saved!')
      navigate('/resume')
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Failed to save')
    } finally { setSaving(false) }
  }

  const skillsList = (key) => ({
    value: form.skills[key].join(', '),
    onChange: (e) => setField(`skills.${key}`, e.target.value.split(',').map(s => s.trim())),
  })

  return (
    <div className="space-y-6 animate-fade-in">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white">Create Resume</h1>
          <p className="text-gray-400 mt-1">Build your resume from scratch</p>
        </div>
        <button onClick={handleSave} disabled={saving} className="btn-primary flex items-center gap-2">
          <Save size={16} /> {saving ? 'Saving...' : 'Save Resume'}
        </button>
      </div>

      {/* Template */}
      <div className="card">
        <h3 className="font-semibold text-white mb-3">Template</h3>
        <div className="flex gap-3 flex-wrap">
          {TEMPLATES.map(t => (
            <button key={t} onClick={() => setTemplate(t)}
              className={`px-4 py-2 rounded-lg text-sm capitalize border transition-colors ${template === t ? 'bg-primary-600 border-primary-600 text-white' : 'border-gray-700 text-gray-400 hover:border-gray-600'}`}>
              {t}
            </button>
          ))}
        </div>
      </div>

      {/* Personal Info */}
      <div className="card space-y-4">
        <h3 className="font-semibold text-white">Personal Information</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {[
            ['name', 'Full Name', 'text'],
            ['email', 'Email', 'email'],
            ['phone', 'Phone', 'tel'],
            ['location', 'Location', 'text'],
            ['linkedin', 'LinkedIn URL', 'url'],
            ['github', 'GitHub URL', 'url'],
          ].map(([k, label, type]) => (
            <div key={k}>
              <label className="label">{label}</label>
              <input type={type} className="input" value={form.personal_info[k] || ''}
                onChange={e => setField(`personal_info.${k}`, e.target.value)} />
            </div>
          ))}
        </div>
      </div>

      {/* Education */}
      <div className="card space-y-4">
        <div className="flex items-center justify-between">
          <h3 className="font-semibold text-white">Education</h3>
          <button onClick={() => addItem('education', { institution: '', degree: '', branch: '', cgpa: '', year_of_passing: '' })} className="btn-ghost text-xs flex items-center gap-1">
            <Plus size={14} /> Add
          </button>
        </div>
        {form.education.map((edu, i) => (
          <div key={i} className="p-4 bg-gray-800/50 rounded-lg space-y-3">
            <div className="flex justify-between">
              <span className="text-xs text-gray-500 uppercase tracking-wider">Education {i + 1}</span>
              <button onClick={() => removeItem('education', i)} className="text-gray-600 hover:text-red-400"><Trash2 size={14} /></button>
            </div>
            <div className="grid grid-cols-2 gap-3">
              {[
                ['institution', 'Institution'],
                ['degree', 'Degree'],
                ['branch', 'Branch/Field'],
                ['cgpa', 'CGPA'],
                ['year_of_passing', 'Year of Passing'],
              ].map(([k, label]) => (
                <div key={k}>
                  <label className="label">{label}</label>
                  <input className="input" value={edu[k] || ''}
                    onChange={e => {
                      const updated = [...form.education]
                      updated[i] = { ...updated[i], [k]: e.target.value }
                      setField('education', updated)
                    }} />
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>

      {/* Projects */}
      <div className="card space-y-4">
        <div className="flex items-center justify-between">
          <h3 className="font-semibold text-white">Projects</h3>
          <button onClick={() => addItem('projects', { name: '', description: '', tech_stack: [], link: '' })} className="btn-ghost text-xs flex items-center gap-1">
            <Plus size={14} /> Add
          </button>
        </div>
        {form.projects.map((proj, i) => (
          <div key={i} className="p-4 bg-gray-800/50 rounded-lg space-y-3">
            <div className="flex justify-between">
              <span className="text-xs text-gray-500 uppercase tracking-wider">Project {i + 1}</span>
              <button onClick={() => removeItem('projects', i)} className="text-gray-600 hover:text-red-400"><Trash2 size={14} /></button>
            </div>
            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="label">Project Name</label>
                <input className="input" value={proj.name}
                  onChange={e => { const u = [...form.projects]; u[i] = { ...u[i], name: e.target.value }; setField('projects', u) }} />
              </div>
              <div>
                <label className="label">Tech Stack (comma-separated)</label>
                <input className="input" value={proj.tech_stack?.join(', ')}
                  onChange={e => { const u = [...form.projects]; u[i] = { ...u[i], tech_stack: e.target.value.split(',').map(s => s.trim()) }; setField('projects', u) }} />
              </div>
              <div className="col-span-2">
                <label className="label">Description</label>
                <textarea className="input h-20 resize-none" value={proj.description}
                  onChange={e => { const u = [...form.projects]; u[i] = { ...u[i], description: e.target.value }; setField('projects', u) }} />
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Skills */}
      <div className="card space-y-4">
        <h3 className="font-semibold text-white">Skills</h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div>
            <label className="label">Technical Skills</label>
            <input className="input" placeholder="Python, Java, React, ..." {...skillsList('technical')} />
          </div>
          <div>
            <label className="label">Soft Skills</label>
            <input className="input" placeholder="Leadership, Communication, ..." {...skillsList('soft')} />
          </div>
          <div>
            <label className="label">Tools & Technologies</label>
            <input className="input" placeholder="Git, Docker, AWS, ..." {...skillsList('tools')} />
          </div>
        </div>
      </div>

      {/* Coding Profiles */}
      <div className="card space-y-4">
        <h3 className="font-semibold text-white">Coding Profiles</h3>
        <div className="grid grid-cols-2 gap-4">
          {['leetcode', 'hackerrank', 'codechef', 'codeforces'].map(k => (
            <div key={k}>
              <label className="label capitalize">{k}</label>
              <input className="input" placeholder={`${k}.com/username`}
                value={form.coding_profiles[k] || ''}
                onChange={e => setField(`coding_profiles.${k}`, e.target.value)} />
            </div>
          ))}
        </div>
      </div>

      <div className="flex justify-end">
        <button onClick={handleSave} disabled={saving} className="btn-primary flex items-center gap-2 px-8 py-3">
          <Save size={16} /> {saving ? 'Saving...' : 'Save Resume'}
        </button>
      </div>
    </div>
  )
}
