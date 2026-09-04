import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { companiesAPI } from '../services/api'
import { ArrowLeft, MapPin, Users, DollarSign, ChevronDown, ChevronUp } from 'lucide-react'

const TIER_COLORS = { 'tier-1': 'badge-yellow', 'tier-2': 'badge-blue', 'tier-3': 'badge-purple', 'mnc': 'badge-green', 'startup': 'badge-red' }

function Section({ title, children, defaultOpen = false }) {
  const [open, setOpen] = useState(defaultOpen)
  return (
    <div className="card p-0 overflow-hidden">
      <button onClick={() => setOpen(!open)} className="w-full flex items-center justify-between p-4 hover:bg-gray-800/50 transition-colors">
        <h3 className="font-semibold text-white">{title}</h3>
        {open ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
      </button>
      {open && <div className="border-t border-gray-800 p-4">{children}</div>}
    </div>
  )
}

export default function CompanyDetail() {
  const { slug } = useParams()
  const [company, setCompany] = useState(null)
  const navigate = useNavigate()

  useEffect(() => {
    companiesAPI.getOne(slug).then(r => setCompany(r.data.company)).catch(() => navigate('/companies'))
  }, [slug])

  if (!company) return <div className="flex justify-center py-20"><div className="animate-spin w-8 h-8 border-2 border-primary-500 border-t-transparent rounded-full" /></div>

  return (
    <div className="space-y-6 animate-fade-in max-w-3xl">
      <div className="flex items-center gap-3">
        <button onClick={() => navigate('/companies')} className="btn-ghost p-2"><ArrowLeft size={18} /></button>
      </div>

      <div className="card">
        <div className="flex items-start gap-4">
          <div className="w-16 h-16 rounded-xl bg-gray-800 border border-gray-700 flex items-center justify-center text-3xl shrink-0">
            {company.logo || company.name.charAt(0)}
          </div>
          <div className="flex-1">
            <div className="flex items-center gap-2 mb-1">
              <h1 className="text-2xl font-bold text-white">{company.name}</h1>
              <span className={`badge ${TIER_COLORS[company.tier] || 'badge-blue'}`}>{company.tier}</span>
            </div>
            <p className="text-gray-400">{company.industry}</p>
            <div className="flex items-center gap-4 mt-2 text-sm text-gray-500">
              {company.headquarters && <span className="flex items-center gap-1"><MapPin size={12} />{company.headquarters}</span>}
              {company.size && <span className="flex items-center gap-1"><Users size={12} />{company.size}</span>}
              {company.salary_range && <span className="flex items-center gap-1"><DollarSign size={12} />{typeof company.salary_range === 'string' ? company.salary_range : `${company.salary_range.min || ''} – ${company.salary_range.max || ''}`}</span>}
            </div>
          </div>
        </div>
        <p className="text-gray-300 mt-4 text-sm">{company.description}</p>
      </div>

      {company.eligibility && (
        <Section title="Eligibility Criteria" defaultOpen>
          <div className="grid grid-cols-2 gap-3">
            {Object.entries(company.eligibility).map(([k, v]) => (
              <div key={k} className="bg-gray-800/50 rounded-lg p-3">
                <div className="text-xs text-gray-500 capitalize mb-1">{k.replace(/_/g, ' ')}</div>
                <div className="text-white font-medium text-sm">{String(v)}</div>
              </div>
            ))}
          </div>
        </Section>
      )}

      {company.recruitment_process?.length > 0 && (
        <Section title="Recruitment Process" defaultOpen>
          <div className="space-y-3">
            {company.recruitment_process.map((stage, i) => (
              <div key={i} className="flex gap-3">
                <div className="w-6 h-6 rounded-full bg-primary-600/20 border border-primary-600/40 flex items-center justify-center text-primary-400 text-xs font-bold shrink-0 mt-0.5">
                  {i + 1}
                </div>
                <div>
                  <p className="font-medium text-white text-sm">{stage.stage}</p>
                  <p className="text-xs text-gray-400 mt-0.5">{stage.description}</p>
                  <p className="text-xs text-gray-600 mt-0.5">{stage.duration}</p>
                </div>
              </div>
            ))}
          </div>
        </Section>
      )}

      {company.aptitude_pattern && (
        <Section title="Aptitude Test Pattern">
          <div className="grid grid-cols-2 gap-3 text-sm">
            {Object.entries(company.aptitude_pattern).map(([k, v]) => (
              <div key={k} className="flex justify-between">
                <span className="text-gray-400 capitalize">{k.replace(/_/g, ' ')}</span>
                <span className="text-white font-medium">{String(v)}</span>
              </div>
            ))}
          </div>
        </Section>
      )}

      {company.technical_topics?.length > 0 && (
        <Section title="Technical Topics to Prepare">
          <div className="flex flex-wrap gap-2">
            {company.technical_topics.map(t => (
              <span key={t} className="badge badge-blue">{t}</span>
            ))}
          </div>
        </Section>
      )}

      {company.coding_pattern && (
        <Section title="Coding Round Pattern">
          <div className="grid grid-cols-2 gap-3 text-sm">
            {Object.entries(company.coding_pattern).map(([k, v]) => (
              <div key={k} className="flex justify-between">
                <span className="text-gray-400 capitalize">{k.replace(/_/g, ' ')}</span>
                <span className="text-white font-medium">{String(v)}</span>
              </div>
            ))}
          </div>
        </Section>
      )}

      {company.hr_topics?.length > 0 && (
        <Section title="Common HR Topics">
          <ul className="space-y-1.5">
            {company.hr_topics.map(t => (
              <li key={t} className="text-sm text-gray-300">• {t}</li>
            ))}
          </ul>
        </Section>
      )}

      {company.roles?.length > 0 && (
        <Section title="Open Roles">
          <div className="space-y-2">
            {company.roles.map((r, i) => (
              <div key={i} className="flex items-start gap-2">
                <span className="badge badge-green shrink-0">{typeof r === 'string' ? r : r.title}</span>
                {r.description && <span className="text-xs text-gray-400 mt-0.5">{r.description}</span>}
              </div>
            ))}
          </div>
        </Section>
      )}
    </div>
  )
}
