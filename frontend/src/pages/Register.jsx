import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { UserPlus, AlertCircle } from 'lucide-react'
import { Button, Input } from '../components/ui/index'

export default function Register({ onRegister }) {
  const [form, setForm]       = useState({ username: '', password: '', confirm: '' })
  const [error, setError]     = useState('')
  const [loading, setLoading] = useState(false)
  const navigate = useNavigate()

  const handle = e => setForm(f => ({ ...f, [e.target.name]: e.target.value }))

  const submit = async e => {
    e.preventDefault()
    setError('')
    if (form.password !== form.confirm) { setError('Parollar mos emas'); return }
    if (form.password.length < 6)      { setError('Parol kamida 6 ta belgi bo\'lishi kerak'); return }
    setLoading(true)
    try {
      await onRegister(form.username, form.password)
      navigate('/profil')
    } catch (err) {
      setError(err.response?.data?.detail || 'Ro\'yxatdan o\'tish muvaffaqiyatsiz')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center px-4" style={{ backgroundColor: 'var(--bg)' }}>
      <div className="w-full max-w-sm animate-fade-in">
        <div className="text-center mb-8">
          <div className="w-12 h-12 rounded-2xl bg-brand-500 flex items-center justify-center mx-auto mb-4">
            <span className="text-white text-xl font-bold font-display">S</span>
          </div>
          <h1 className="page-title">Hisob yaratish</h1>
          <p className="text-sm mt-1" style={{ color: 'var(--text-3)' }}>SarfAI bilan moliyaviy rejalashtiring</p>
        </div>

        <div className="card-md p-6 space-y-4">
          {error && (
            <div className="flex items-center gap-2 p-3 rounded-xl bg-red-50 dark:bg-red-900/20 text-red-600 dark:text-red-400 text-sm">
              <AlertCircle size={15} className="flex-shrink-0" />
              {error}
            </div>
          )}

          <form onSubmit={submit} className="space-y-4">
            <Input label="Foydalanuvchi nomi" name="username" value={form.username} onChange={handle}
              placeholder="kamol_1990" hint="Kamida 3 ta belgi" required autoFocus />
            <Input label="Parol" name="password" type="password" value={form.password} onChange={handle}
              placeholder="••••••••" hint="Kamida 6 ta belgi" required />
            <Input label="Parolni tasdiqlang" name="confirm" type="password" value={form.confirm} onChange={handle}
              placeholder="••••••••" required />
            <Button type="submit" className="w-full" disabled={loading}>
              {loading ? 'Yaratilmoqda...' : <><UserPlus size={15} /> Ro'yxatdan o'tish</>}
            </Button>
          </form>
        </div>

        <p className="text-center text-sm mt-4" style={{ color: 'var(--text-3)' }}>
          Hisobingiz bormi?{' '}
          <Link to="/login" className="text-brand-600 dark:text-brand-400 font-medium hover:underline">
            Kiring
          </Link>
        </p>
      </div>
    </div>
  )
}
