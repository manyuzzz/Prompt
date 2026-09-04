import { useState, useEffect, useRef } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { interviewAPI } from '../services/api'
import { useToast } from '../hooks/useToast'
import { Send, Square, Mic, MicOff, Loader, ChevronRight } from 'lucide-react'

export default function InterviewSession() {
  const { id } = useParams()
  const [interview, setInterview] = useState(null)
  const [currentQ, setCurrentQ] = useState(null)
  const [answer, setAnswer] = useState('')
  const [submitting, setSubmitting] = useState(false)
  const [ending, setEnding] = useState(false)
  const [questionNum, setQuestionNum] = useState(1)
  const [feedback, setFeedback] = useState(null)
  const [listening, setListening] = useState(false)
  const recognitionRef = useRef(null)
  const navigate = useNavigate()
  const toast = useToast()

  useEffect(() => {
    interviewAPI.getOne(id).then(r => {
      const inv = r.data.interview
      setInterview(inv)
      if ((inv.status === 'ongoing' || inv.status === 'in_progress') && inv.questions?.length) {
        setCurrentQ(inv.questions[0])
      } else if (inv.status === 'completed') {
        navigate(`/interview/result/${id}`, { replace: true })
      }
    }).catch(() => toast.error('Failed to load interview'))
  }, [id])

  const startListening = () => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition
    if (!SpeechRecognition) { toast.warn('Speech recognition not supported in this browser'); return }
    const rec = new SpeechRecognition()
    rec.continuous = true; rec.interimResults = true; rec.lang = 'en-US'
    rec.onresult = e => {
      const transcript = Array.from(e.results).map(r => r[0].transcript).join('')
      setAnswer(transcript)
    }
    rec.onerror = () => setListening(false)
    rec.onend = () => setListening(false)
    recognitionRef.current = rec
    rec.start()
    setListening(true)
  }

  const stopListening = () => {
    recognitionRef.current?.stop()
    setListening(false)
  }

  const submitAnswer = async () => {
    if (!answer.trim()) { toast.warn('Please provide an answer'); return }
    setSubmitting(true)
    try {
      const { data } = await interviewAPI.respond(id, {
        question_id: currentQ.id,
        answer: answer.trim(),
      })
      setFeedback(data.evaluation)
      if (data.next_question) {
        setTimeout(() => {
          setCurrentQ(data.next_question)
          setAnswer('')
          setFeedback(null)
          setQuestionNum(n => n + 1)
        }, 3000)
      } else {
        setTimeout(() => endInterview(), 3000)
      }
    } catch { toast.error('Failed to submit answer') }
    finally { setSubmitting(false) }
  }

  const endInterview = async () => {
    setEnding(true)
    try {
      await interviewAPI.end(id)
      navigate(`/interview/result/${id}`)
    } catch { toast.error('Failed to end interview') }
    finally { setEnding(false) }
  }

  if (!interview || !currentQ) return (
    <div className="flex items-center justify-center h-64">
      <div className="animate-spin w-8 h-8 border-2 border-primary-500 border-t-transparent rounded-full" />
    </div>
  )

  return (
    <div className="max-w-3xl mx-auto space-y-6 animate-fade-in">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-xl font-bold text-white capitalize">{interview.type?.replace('_', ' ')} Interview</h1>
          <p className="text-gray-400 text-sm">Question {questionNum} of {interview.questions?.length || '?'}</p>
        </div>
        <button onClick={endInterview} disabled={ending} className="btn-secondary text-sm flex items-center gap-2 text-red-400 border-red-800 hover:bg-red-900/20">
          <Square size={14} /> {ending ? 'Ending...' : 'End Interview'}
        </button>
      </div>

      {/* Progress */}
      <div className="progress-bar">
        <div className="progress-fill bg-primary-500"
          style={{ width: `${((questionNum - 1) / (interview.questions?.length || 1)) * 100}%` }} />
      </div>

      {/* Question */}
      <div className="card border-primary-600/30">
        <div className="flex items-start gap-3">
          <div className="w-8 h-8 rounded-full bg-primary-600/20 border border-primary-600/40 flex items-center justify-center text-primary-400 text-sm font-bold shrink-0">
            Q
          </div>
          <div>
            <p className="text-gray-200 leading-relaxed">{currentQ.question}</p>
            {currentQ.hint && (
              <p className="text-xs text-gray-500 mt-3 p-2 bg-gray-800 rounded italic">💡 Hint: {currentQ.hint}</p>
            )}
          </div>
        </div>
      </div>

      {/* Feedback (after submission) */}
      {feedback && (
        <div className="card border-green-600/30 bg-green-900/10">
          <h4 className="font-semibold text-green-400 mb-2">Evaluation</h4>
          <p className="text-sm text-gray-300 mb-3">{feedback.feedback}</p>
          <div className="grid grid-cols-3 gap-3 text-center text-xs">
            {Object.entries(feedback.scores || {}).slice(0, 3).map(([k, v]) => (
              <div key={k} className="bg-gray-800 rounded p-2">
                <div className="text-white font-bold">{Math.round(v)}</div>
                <div className="text-gray-500 capitalize">{k.replace(/_/g, ' ')}</div>
              </div>
            ))}
          </div>
          {feedback.follow_up && (
            <p className="mt-3 text-sm text-primary-400 flex items-center gap-1">
              <ChevronRight size={14} /> Follow-up: {feedback.follow_up}
            </p>
          )}
        </div>
      )}

      {/* Answer Input */}
      {!feedback && (
        <div className="space-y-3">
          <div className="relative">
            <textarea
              value={answer}
              onChange={e => setAnswer(e.target.value)}
              placeholder="Type your answer here or use the microphone..."
              className="input h-40 resize-none pr-12"
            />
            <button
              onClick={listening ? stopListening : startListening}
              className={`absolute right-3 top-3 p-2 rounded-lg transition-colors ${listening ? 'bg-red-600 text-white' : 'bg-gray-700 text-gray-400 hover:text-white'}`}
            >
              {listening ? <MicOff size={16} /> : <Mic size={16} />}
            </button>
          </div>
          {listening && (
            <div className="flex items-center gap-2 text-sm text-red-400">
              <div className="w-2 h-2 bg-red-500 rounded-full animate-pulse" />
              Listening... speak your answer
            </div>
          )}
          <div className="flex gap-3">
            <button onClick={submitAnswer} disabled={submitting || !answer.trim()} className="btn-primary flex items-center gap-2 flex-1 justify-center py-3">
              {submitting ? <><Loader size={16} className="animate-spin" /> Evaluating...</> : <><Send size={16} /> Submit Answer</>}
            </button>
          </div>
        </div>
      )}
    </div>
  )
}
