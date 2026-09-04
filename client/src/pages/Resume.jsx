import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { resumeAPI } from '../services/api'
import { useToast } from '../hooks/useToast'
import { formatDate, getScoreColor, getScoreBg } from '../utils/helpers'
import { Upload, FileText, Plus, Trash2, ChevronRight, Star, AlertCircle, CheckCircle } from 'lucide-react'
import { useDropzone } from 'react-dropzone'

export default function Resume() {
  const [resumes, setResumes] = useState([])
  const [uploading, setUploading] = useState(false)
  const [loading, setLoading] = useState(true)
  const toast = useToast()

  useEffect(() => {
    resumeAPI.getAll().then(r => setResumes(r.data.resumes || [])).catch(console.error).finally(() => setLoading(false))
  }, [])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    accept: { 'application/pdf': ['.pdf'], 'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'] },
    maxFiles: 1,
    onDrop: async (files) => {
      if (!files[0]) return
      const formData = new FormData()
      formData.append('file', files[0])
      setUploading(true)
      try {
        const { data } = await resumeAPI.upload(formData)
        setResumes(prev => [data.resume, ...prev])
        toast.success('Resume uploaded and analyzed!')
      } catch (err) {
        toast.error(err.response?.data?.detail || 'Upload failed')
      } finally { setUploading(false) }
    },
  })

  const deleteResume = async (id) => {
    try {
      await resumeAPI.delete(id)
      setResumes(prev => prev.filter(r => r.id !== id))
      toast.success('Deleted')
    } catch { toast.error('Failed to delete') }
  }

  if (loading) return <div className="flex justify-center py-20"><div className="animate-spin w-8 h-8 border-2 border-primary-500 border-t-transparent rounded-full" /></div>

  return (
    <div className="space-y-6 animate-fade-in">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-white">Resume</h1>
          <p className="text-gray-400 mt-1">Upload, analyze, and improve your resume</p>
        </div>
        <Link to="/resume/create" className="btn-primary flex items-center gap-2">
          <Plus size={16} /> Create Resume
        </Link>
      </div>

      <div
        {...getRootProps()}
        className={`border-2 border-dashed rounded-xl p-10 text-center cursor-pointer transition-colors ${
          isDragActive ? 'border-primary-500 bg-primary-600/10' : 'border-gray-700 hover:border-gray-600'
        } ${uploading ? 'pointer-events-none opacity-60' : ''}`}
      >
        <input {...getInputProps()} />
        <Upload size={32} className="mx-auto mb-3 text-gray-500" />
        <p className="text-gray-300 font-medium mb-1">
          {uploading ? 'Uploading and analyzing...' : isDragActive ? 'Drop your resume here' : 'Drop your resume or click to upload'}
        </p>
        <p className="text-sm text-gray-500">PDF or DOCX, max 10MB</p>
      </div>

      {resumes.length === 0 ? (
        <div className="card text-center py-12">
          <FileText size={40} className="mx-auto mb-3 text-gray-600" />
          <p className="text-gray-400">No resumes yet. Upload one above or create from scratch.</p>
        </div>
      ) : (
        <div className="space-y-3">
          {resumes.map(resume => (
            <div key={resume.id} className="card flex items-start gap-4 hover:border-gray-700 transition-colors">
              <div className="w-10 h-10 rounded-lg bg-blue-900/30 border border-blue-800 flex items-center justify-center shrink-0">
                <FileText size={18} className="text-blue-400" />
              </div>
              <div className="flex-1 min-w-0">
                <div className="flex items-start justify-between gap-4">
                  <div>
                    <h3 className="font-semibold text-white">{resume.personal_info?.name || 'Resume'}</h3>
                    <p className="text-sm text-gray-500 mt-0.5">{formatDate(resume.created_at)}</p>
                  </div>
                  <div className="flex items-center gap-2 shrink-0">
                    <Link to={`/resume/analyze`} state={{ resumeId: resume.id }}
                      className="text-primary-400 hover:text-primary-300 text-sm flex items-center gap-1">
                      Analyze <ChevronRight size={14} />
                    </Link>
                    <button onClick={() => deleteResume(resume.id)} className="text-gray-600 hover:text-red-400 p-1">
                      <Trash2 size={15} />
                    </button>
                  </div>
                </div>
                <div className="flex flex-wrap gap-2 mt-3">
                  {resume.skills?.technical?.slice(0, 5).map(s => (
                    <span key={s} className="badge badge-blue">{s}</span>
                  ))}
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-4">
        <div className="card border-primary-600/30">
          <Star size={20} className="text-primary-400 mb-3" />
          <h3 className="font-semibold text-white mb-1">ATS Score</h3>
          <p className="text-sm text-gray-400">Check how well your resume passes Applicant Tracking Systems</p>
          <Link to="/resume/analyze" className="text-primary-400 text-sm hover:underline mt-3 block">Analyze now →</Link>
        </div>
        <div className="card border-green-600/30">
          <CheckCircle size={20} className="text-green-400 mb-3" />
          <h3 className="font-semibold text-white mb-1">JD Matching</h3>
          <p className="text-sm text-gray-400">Paste a job description to see how your resume matches</p>
          <Link to="/resume/analyze" className="text-primary-400 text-sm hover:underline mt-3 block">Match now →</Link>
        </div>
        <div className="card border-yellow-600/30">
          <AlertCircle size={20} className="text-yellow-400 mb-3" />
          <h3 className="font-semibold text-white mb-1">AI Suggestions</h3>
          <p className="text-sm text-gray-400">Get AI-powered tips to improve every section of your resume</p>
          <Link to="/resume/analyze" className="text-primary-400 text-sm hover:underline mt-3 block">Get tips →</Link>
        </div>
      </div>
    </div>
  )
}
