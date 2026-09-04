import { toast } from 'react-toastify'

export const useToast = () => ({
  success: (msg) => toast.success(msg, { theme: 'dark' }),
  error: (msg) => toast.error(msg, { theme: 'dark' }),
  info: (msg) => toast.info(msg, { theme: 'dark' }),
  warn: (msg) => toast.warn(msg, { theme: 'dark' }),
})
