import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { companiesAPI } from '../services/api'
import { Building2, Search, ChevronRight } from 'lucide-react'

const TIERS = ['all', 'tier-1', 'tier-2', 'tier-3', 'mnc', 'startup']
const TIER_COLORS = {
  'tier-1': 'badge-yellow',
  'tier-2': 'badge-blue',
  'tier-3': 'badge-purple',
  'mnc': 'badge-green',
  'startup': 'badge-red',
}

export default function Companies() {
  const [companies, setCompanies] = useState([])
  const [loading, setLoading] = useState(true)
  const [search, setSearch] = useState('')
  const [tier, setTier] = useState('all')
  const navigate = useNavigate()

  useEffect(() => {
    companiesAPI.getAll({ limit: 50 })
      .then(r => setCompanies(r.data.companies || []))
      .catch(console.error)
      .finally(() => setLoading(false))
  }, [])

  const filtered = companies.filter(c => {
    const matchSearch = !search || c.name.toLowerCase().includes(search.toLowerCase())
    const matchTier = tier === 'all' || c.tier === tier
    return matchSearch && matchTier
  })

  if (loading) return <div className="flex justify-center py-20"><div className="animate-spin w-8 h-8 border-2 border-primary-500 border-t-transparent rounded-full" /></div>

  return (
    <div className="space-y-6 animate-fade-in">
      <div>
        <h1 className="text-2xl font-bold text-white">Company Preparation</h1>
        <p className="text-gray-400 mt-1">Company-specific preparation guides, interview patterns, and tips</p>
      </div>

      <div className="flex flex-wrap gap-3">
        <div className="relative flex-1 min-w-48">
          <Search size={15} className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-500" />
          <input className="input pl-9" placeholder="Search companies..."
            value={search} onChange={e => setSearch(e.target.value)} />
        </div>
        <div className="flex gap-2 flex-wrap">
          {TIERS.map(t => (
            <button key={t} onClick={() => setTier(t)}
              className={`px-3 py-2 rounded-lg text-sm capitalize border transition-colors ${tier === t ? 'bg-primary-600 border-primary-600 text-white' : 'border-gray-700 text-gray-400 hover:border-gray-600'}`}>
              {t}
            </button>
          ))}
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {filtered.map(company => (
          <div key={company.id}
            onClick={() => navigate(`/companies/${company.slug}`)}
            className="card cursor-pointer hover:border-gray-700 transition-colors group flex items-start gap-4">
            <div className="w-12 h-12 rounded-xl bg-gray-800 border border-gray-700 flex items-center justify-center text-2xl shrink-0">
              {company.logo || company.name.charAt(0)}
            </div>
            <div className="flex-1 min-w-0">
              <div className="flex items-center gap-2 mb-1">
                <h3 className="font-semibold text-white group-hover:text-primary-400 transition-colors">{company.name}</h3>
                <span className={`badge ${TIER_COLORS[company.tier] || 'badge-blue'}`}>{company.tier}</span>
              </div>
              <p className="text-sm text-gray-400">{company.industry} · {company.size}</p>
              <p className="text-xs text-gray-500 mt-1 truncate">{company.description}</p>
            </div>
            <ChevronRight size={16} className="text-gray-600 group-hover:text-gray-400 mt-1 shrink-0" />
          </div>
        ))}
        {filtered.length === 0 && (
          <div className="col-span-2 card text-center py-12">
            <Building2 size={40} className="mx-auto mb-3 text-gray-600" />
            <p className="text-gray-400">No companies found</p>
          </div>
        )}
      </div>
    </div>
  )
}
