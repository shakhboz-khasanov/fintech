import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { LogIn, AlertCircle } from 'lucide-react'
import { Button, Input } from '../components/ui/index'

export default function Login({ onLogin }) {
  const [form, setForm]     = useState({ username: '', password: '' })
  const [error, setError]   = useState('')
  const [loading, setLoading] = useState(false)
  const navigate = useNavigate()

  const handle = e => setForm(f => ({ ...f, [e.target.name]: e.target.value }))

  const submit = async e => {
    e.preventDefault()
    setError('')
    setLoading(true)
    try {
      await onLogin(form.username, form.password)
      navigate('/dashboard')
    } catch (err) {
      setError(err.response?.data?.detail || 'Kirish muvaffaqiyatsiz')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center px-4" style={{ backgroundColor: 'var(--bg)' }}>
      <div className="w-full max-w-sm animate-fade-in">
        {/* Logo */}
        <div className="text-center mb-8">
          <div className="w-12 h-12 rounded-2xl bg-brand-500 flex items-center justify-center mx-auto mb-4">
            <span className="text-white text-xl font-bold font-display">S</span>
          </div>
          <h1 className="page-title">Xush kelibsiz</h1>
          <p className="text-sm mt-1" style={{ color: 'var(--text-3)' }}>SarfAI hisobingizga kiring</p>
        </div>

        <div className="card-md p-6 space-y-4">
          {error && (
            <div className="flex items-center gap-2 p-3 rounded-xl bg-red-50 dark:bg-red-900/20 text-red-600 dark:text-red-400 text-sm">
              <AlertCircle size={15} className="flex-shrink-0" />
              {error}
            </div>
          )}

          <form onSubmit={submit} className="space-y-4">
            <Input
              label="Foydalanuvchi nomi"
              name="username"
              value={form.username}
              onChange={handle}
              placeholder="username"
              autoFocus
              required
            />
            <Input
              label="Parol"
              name="password"
              type="password"
              value={form.password}
              onChange={handle}
              placeholder="••••••••"
              required
            />
            <Button type="submit" className="w-full" disabled={loading}>
              {loading ? 'Kirish...' : <><LogIn size={15} /> Kirish</>}
            </Button>
          </form>
        </div>

        <p className="text-center text-sm mt-4" style={{ color: 'var(--text-3)' }}>
          Hisob yo'qmi?{' '}
          <Link to="/register" className="text-brand-600 dark:text-brand-400 font-medium hover:underline">
            Ro'yxatdan o'ting
          </Link>
        </p>
      </div>
    </div>
  )
}
