import axios from 'axios'

const BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: BASE_URL,
  headers: { 'Content-Type': 'application/json' },
  withCredentials: false,
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

api.interceptors.response.use(
  (res) => res,
  (err) => {
    if (err.response?.status === 401) {
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      window.location.href = '/login'
    }
    return Promise.reject(err)
  }
)

export const authAPI = {
  register: (data) => api.post('/api/auth/register', data),
  login: (data) => api.post('/api/auth/login', data),
  me: () => api.get('/api/auth/me'),
  updateProfile: (data) => api.put('/api/auth/profile', data),
  resetProgress: () => api.post('/api/auth/reset'),
}

export const chatAPI = {
  getConversations: () => api.get('/api/chat/conversations'),
  getConversation: (id) => api.get(`/api/chat/conversations/${id}`),
  send: (data) => api.post('/api/chat/send', data),
  deleteConversation: (id) => api.delete(`/api/chat/conversations/${id}`),
  getSuggestions: () => api.get('/api/chat/suggestions'),
}

export const resumeAPI = {
  getAll: () => api.get('/api/resumes'),
  getOne: (id) => api.get(`/api/resumes/${id}`),
  upload: (formData) =>
    api.post('/api/resumes/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    }),
  analyze: (id) => api.post(`/api/resumes/analyze/${id}`),
  create: (data) => api.post('/api/resumes/create', data),
  update: (id, data) => api.put(`/api/resumes/${id}`, data),
  delete: (id) => api.delete(`/api/resumes/${id}`),
  getLatestAnalysis: () => api.get('/api/resumes/analyses/latest'),
}

export const roadmapAPI = {
  getAll: () => api.get('/api/roadmaps'),
  getActive: () => api.get('/api/roadmaps/active'),
  getOne: (id) => api.get(`/api/roadmaps/${id}`),
  generate: (data) => api.post('/api/roadmaps/generate', data),
  completeTask: (roadmapId, taskId) =>
    api.patch(`/api/roadmaps/${roadmapId}/tasks/${taskId}`),
}

export const interviewAPI = {
  getAll: () => api.get('/api/interviews'),
  start: (data) => api.post('/api/interviews/start', data),
  respond: (interviewId, data) =>
    api.post('/api/interviews/respond', { interview_id: interviewId, ...data }),
  end: (interviewId) => api.post('/api/interviews/end', { interview_id: interviewId }),
  getOne: (id) => api.get(`/api/interviews/${id}`),
}

export const codingAPI = {
  getProblems: (params) => api.get('/api/coding/problems', { params }),
  getTopics: () => api.get('/api/coding/problems/topics'),
  getProblem: (slug) => api.get(`/api/coding/problems/${slug}`),
  run: (data) => api.post('/api/coding/run', data),
  submit: (data) => api.post('/api/coding/submit', data),
  getSubmissions: (params) => api.get('/api/coding/submissions', { params }),
}

export const aptitudeAPI = {
  getQuestions: (params) => api.get('/api/aptitude/questions', { params }),
  getCategories: () => api.get('/api/aptitude/categories'),
  submit: (data) => api.post('/api/aptitude/submit', data),
  submitBatch: (data) => api.post('/api/aptitude/submit-batch', data),
  getStats: () => api.get('/api/aptitude/stats'),
}

export const companiesAPI = {
  getAll: (params) => api.get('/api/companies', { params }),
  getOne: (slug) => api.get(`/api/companies/${slug}`),
}

export const progressAPI = {
  get: () => api.get('/api/progress'),
  getDashboard: () => api.get('/api/progress/dashboard'),
}

export default api
