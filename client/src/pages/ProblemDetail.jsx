import { useState, useEffect, useRef } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { codingAPI } from '../services/api'
import { useToast } from '../hooks/useToast'
import { getDifficultyBg, LANGUAGES, LANGUAGE_STARTERS } from '../utils/helpers'
import Editor from '@monaco-editor/react'
import { Play, Send, ArrowLeft, ChevronDown, ChevronUp, Loader, CheckCircle, XCircle } from 'lucide-react'

export default function ProblemDetail() {
  const { slug } = useParams()
  const [problem, setProblem] = useState(null)
  const [lang, setLang] = useState('python')
  const [code, setCode] = useState(LANGUAGE_STARTERS.python)
  const [running, setRunning] = useState(false)
  const [submitting, setSubmitting] = useState(false)
  const [output, setOutput] = useState(null)
  const [showHints, setShowHints] = useState(false)
  const navigate = useNavigate()
  const toast = useToast()

  useEffect(() => {
    codingAPI.getProblem(slug)
      .then(r => setProblem(r.data.problem))
      .catch(() => toast.error('Problem not found'))
  }, [slug])

  const setLanguage = (l) => {
    setLang(l)
    setCode(LANGUAGE_STARTERS[l] || '')
  }

  const run = async () => {
    if (!code.trim()) return
    setRunning(true); setOutput(null)
    try {
      const { data } = await codingAPI.run({ problem_id: problem.id, language: lang, code })
      setOutput({ type: 'run', ...data })
    } catch { toast.error('Execution failed') }
    finally { setRunning(false) }
  }

  const submit = async () => {
    if (!code.trim()) return
    setSubmitting(true); setOutput(null)
    try {
      const { data } = await codingAPI.submit({ problem_id: problem.id, language: lang, code })
      setOutput({ type: 'submit', ...data })
      if (data.is_accepted) toast.success(`Accepted! +${data.xp_awarded} XP`)
      else toast.error('Wrong Answer')
    } catch { toast.error('Submission failed') }
    finally { setSubmitting(false) }
  }

  if (!problem) return (
    <div className="flex items-center justify-center h-64">
      <div className="animate-spin w-8 h-8 border-2 border-primary-500 border-t-transparent rounded-full" />
    </div>
  )

  return (
    <div className="flex flex-col h-[calc(100vh-8rem)] gap-0 animate-fade-in -m-6">
      <div className="flex items-center gap-3 px-6 py-3 border-b border-gray-800 bg-gray-900 shrink-0">
        <button onClick={() => navigate('/technical')} className="text-gray-400 hover:text-white p-1">
          <ArrowLeft size={18} />
        </button>
        <h1 className="font-semibold text-white">{problem.title}</h1>
        <span className={`badge border ${getDifficultyBg(problem.difficulty)}`}>{problem.difficulty}</span>
        <div className="ml-auto flex items-center gap-2">
          {LANGUAGES.map(l => (
            <button key={l.id} onClick={() => setLanguage(l.id)}
              className={`px-3 py-1.5 rounded text-xs border transition-colors ${lang === l.id ? 'bg-primary-600 border-primary-600 text-white' : 'border-gray-700 text-gray-400 hover:border-gray-600'}`}>
              {l.label}
            </button>
          ))}
        </div>
      </div>

      <div className="flex flex-1 overflow-hidden">
        {/* Left: Problem */}
        <div className="w-[45%] overflow-y-auto p-6 border-r border-gray-800 space-y-4">
          <div>
            <p className="text-gray-300 text-sm leading-relaxed">{problem.description}</p>
          </div>

          {problem.examples?.map((ex, i) => (
            <div key={i} className="bg-gray-800/50 rounded-lg p-4">
              <div className="text-xs text-gray-500 uppercase tracking-wider mb-2">Example {i + 1}</div>
              <div className="font-mono text-sm space-y-1">
                <div><span className="text-gray-400">Input: </span><span className="text-gray-200">{ex.input}</span></div>
                <div><span className="text-gray-400">Output: </span><span className="text-gray-200">{ex.output}</span></div>
                {ex.explanation && <div className="text-gray-500 text-xs mt-1">{ex.explanation}</div>}
              </div>
            </div>
          ))}

          {problem.constraints?.length > 0 && (
            <div>
              <h4 className="text-sm font-medium text-gray-400 mb-2">Constraints</h4>
              <ul className="space-y-1">
                {problem.constraints.map((c, i) => (
                  <li key={i} className="text-xs font-mono text-gray-400">• {c}</li>
                ))}
              </ul>
            </div>
          )}

          {problem.hints?.length > 0 && (
            <div>
              <button onClick={() => setShowHints(!showHints)}
                className="flex items-center gap-2 text-sm text-primary-400 hover:text-primary-300">
                {showHints ? <ChevronUp size={14} /> : <ChevronDown size={14} />} Hints ({problem.hints.length})
              </button>
              {showHints && (
                <div className="mt-2 space-y-2">
                  {problem.hints.map((h, i) => (
                    <div key={i} className="text-xs text-gray-400 p-2 bg-gray-800 rounded">💡 {h}</div>
                  ))}
                </div>
              )}
            </div>
          )}
        </div>

        {/* Right: Editor + Output */}
        <div className="flex-1 flex flex-col overflow-hidden">
          <div className="flex-1 overflow-hidden">
            <Editor
              height="100%"
              language={lang === 'cpp' ? 'cpp' : lang}
              value={code}
              onChange={v => setCode(v || '')}
              theme="vs-dark"
              options={{
                fontSize: 14,
                fontFamily: 'JetBrains Mono, monospace',
                minimap: { enabled: false },
                scrollBeyondLastLine: false,
                padding: { top: 16 },
                lineNumbers: 'on',
                wordWrap: 'on',
              }}
            />
          </div>

          {/* Controls */}
          <div className="border-t border-gray-800 p-3 flex items-center gap-3 bg-gray-900 shrink-0">
            <button onClick={run} disabled={running || submitting} className="btn-secondary flex items-center gap-2 text-sm">
              {running ? <Loader size={14} className="animate-spin" /> : <Play size={14} />}
              {running ? 'Running...' : 'Run'}
            </button>
            <button onClick={submit} disabled={running || submitting} className="btn-primary flex items-center gap-2 text-sm">
              {submitting ? <Loader size={14} className="animate-spin" /> : <Send size={14} />}
              {submitting ? 'Submitting...' : 'Submit'}
            </button>
            <div className="ml-auto text-xs text-gray-600">
              Ctrl+Enter to run
            </div>
          </div>

          {/* Output */}
          {output && (
            <div className="border-t border-gray-800 p-4 max-h-48 overflow-y-auto bg-gray-900 shrink-0">
              <div className="flex items-center gap-2 mb-2">
                {output.is_accepted || output.status === 'success'
                  ? <CheckCircle size={16} className="text-green-400" />
                  : <XCircle size={16} className="text-red-400" />}
                <span className={`text-sm font-medium ${output.is_accepted || output.status === 'success' ? 'text-green-400' : 'text-red-400'}`}>
                  {output.type === 'submit'
                    ? (output.is_accepted ? 'Accepted' : `${output.status?.replace(/_/g, ' ')}`)
                    : (output.status === 'success' ? 'Run Successful' : 'Error')}
                </span>
                {output.execution_time_ms && (
                  <span className="text-xs text-gray-500 ml-auto">{output.execution_time_ms}ms</span>
                )}
              </div>
              {output.stdout && <pre className="text-xs font-mono text-gray-300 whitespace-pre-wrap">{output.stdout}</pre>}
              {output.stderr && <pre className="text-xs font-mono text-red-400 whitespace-pre-wrap">{output.stderr}</pre>}
              {output.error && <pre className="text-xs font-mono text-red-400 whitespace-pre-wrap">{output.error}</pre>}
              {output.test_results?.length > 0 && (
                <div className="mt-2 space-y-1">
                  {output.test_results.slice(0, 3).map((t, i) => (
                    <div key={i} className="flex items-center gap-2 text-xs">
                      {t.passed ? <CheckCircle size={12} className="text-green-400" /> : <XCircle size={12} className="text-red-400" />}
                      <span className="text-gray-400">Case {i + 1}: {t.passed ? 'Passed' : `Expected ${t.expected}, Got ${t.actual}`}</span>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
