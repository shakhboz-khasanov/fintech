// components/ui/index.jsx — all small UI primitives in one file

import { Sun, Moon } from 'lucide-react'

// ── Button ────────────────────────────────────────────────────────────────────
export function Button({ children, variant = 'primary', className = '', ...props }) {
  const base = {
    primary:   'btn-primary',
    secondary: 'btn-secondary',
    ghost:     'btn-ghost',
  }[variant]
  return (
    <button className={`${base} ${className} flex items-center justify-center gap-2`} {...props}>
      {children}
    </button>
  )
}

// ── Card ──────────────────────────────────────────────────────────────────────
export function Card({ children, className = '', elevated = false, ...props }) {
  return (
    <div className={`${elevated ? 'card-md' : 'card'} p-5 ${className}`} {...props}>
      {children}
    </div>
  )
}

// ── Input ─────────────────────────────────────────────────────────────────────
export function Input({ label, error, hint, className = '', ...props }) {
  return (
    <div className="space-y-1">
      {label && <label className="label">{label}</label>}
      <input className={`input-base ${error ? 'border-red-400 focus:border-red-400 focus:ring-red-300/40' : ''} ${className}`} {...props} />
      {error  && <p className="text-xs text-red-500 mt-1">{error}</p>}
      {hint && !error && <p className="text-xs" style={{ color: 'var(--text-3)' }}>{hint}</p>}
    </div>
  )
}

// ── Select ────────────────────────────────────────────────────────────────────
export function Select({ label, error, children, className = '', ...props }) {
  return (
    <div className="space-y-1">
      {label && <label className="label">{label}</label>}
      <select
        className={`input-base ${error ? 'border-red-400' : ''} ${className}`}
        {...props}
      >
        {children}
      </select>
      {error && <p className="text-xs text-red-500 mt-1">{error}</p>}
    </div>
  )
}

// ── Badge ─────────────────────────────────────────────────────────────────────
export function Badge({ children, variant = 'default', className = '' }) {
  const variants = {
    default:  'bg-slate-100 text-slate-600 dark:bg-slate-700 dark:text-slate-300',
    success:  'bg-emerald-100 text-emerald-700 dark:bg-emerald-900/40 dark:text-emerald-400',
    warning:  'bg-amber-100 text-amber-700 dark:bg-amber-900/40 dark:text-amber-400',
    danger:   'bg-red-100 text-red-700 dark:bg-red-900/40 dark:text-red-400',
    brand:    'bg-teal-100 text-teal-700 dark:bg-teal-900/40 dark:text-teal-400',
    info:     'bg-blue-100 text-blue-700 dark:bg-blue-900/40 dark:text-blue-400',
  }
  return (
    <span className={`inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-medium ${variants[variant]} ${className}`}>
      {children}
    </span>
  )
}

// ── Spinner ───────────────────────────────────────────────────────────────────
export function Spinner({ size = 20 }) {
  return (
    <svg
      className="animate-spin"
      style={{ width: size, height: size, color: 'var(--brand)' }}
      xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"
    >
      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z" />
    </svg>
  )
}

// ── ThemeToggle ───────────────────────────────────────────────────────────────
export function ThemeToggle({ dark, onToggle }) {
  return (
    <button
      onClick={onToggle}
      className="w-9 h-9 flex items-center justify-center rounded-xl border transition-all hover:scale-105 active:scale-95"
      style={{ borderColor: 'var(--border)', backgroundColor: 'var(--surface2)', color: 'var(--text-2)' }}
      title={dark ? 'Kunduzgi rejim' : 'Tungi rejim'}
    >
      {dark ? <Sun size={16} /> : <Moon size={16} />}
    </button>
  )
}

// ── Divider ───────────────────────────────────────────────────────────────────
export function Divider({ label }) {
  return (
    <div className="flex items-center gap-3 my-4">
      <div className="flex-1 h-px" style={{ backgroundColor: 'var(--border)' }} />
      {label && <span className="text-xs" style={{ color: 'var(--text-3)' }}>{label}</span>}
      <div className="flex-1 h-px" style={{ backgroundColor: 'var(--border)' }} />
    </div>
  )
}

// ── Alert ─────────────────────────────────────────────────────────────────────
export function Alert({ children, variant = 'info' }) {
  const styles = {
    info:    'bg-blue-50  border-blue-200  text-blue-800  dark:bg-blue-900/20  dark:border-blue-800  dark:text-blue-300',
    warning: 'bg-amber-50 border-amber-200 text-amber-800 dark:bg-amber-900/20 dark:border-amber-800 dark:text-amber-300',
    danger:  'bg-red-50   border-red-200   text-red-800   dark:bg-red-900/20   dark:border-red-800   dark:text-red-300',
    success: 'bg-green-50 border-green-200 text-green-800 dark:bg-green-900/20 dark:border-green-800 dark:text-green-300',
  }
  return (
    <div className={`border rounded-xl p-4 text-sm ${styles[variant]}`}>
      {children}
    </div>
  )
}

// ── StatCard ──────────────────────────────────────────────────────────────────
export function StatCard({ label, value, sub, icon: Icon, color = 'brand' }) {
  const colorMap = {
    brand:   'text-teal-500  bg-teal-50  dark:bg-teal-900/30',
    success: 'text-emerald-500 bg-emerald-50 dark:bg-emerald-900/30',
    warning: 'text-amber-500 bg-amber-50 dark:bg-amber-900/30',
    danger:  'text-red-500   bg-red-50   dark:bg-red-900/30',
    info:    'text-blue-500  bg-blue-50  dark:bg-blue-900/30',
  }
  return (
    <div className="card p-5 flex items-start gap-4">
      {Icon && (
        <div className={`w-10 h-10 rounded-xl flex items-center justify-center flex-shrink-0 ${colorMap[color]}`}>
          <Icon size={18} />
        </div>
      )}
      <div className="min-w-0">
        <p className="text-xs font-medium uppercase tracking-wide" style={{ color: 'var(--text-3)' }}>{label}</p>
        <p className="text-2xl font-semibold mt-0.5 font-display" style={{ color: 'var(--text)' }}>{value}</p>
        {sub && <p className="text-xs mt-0.5" style={{ color: 'var(--text-3)' }}>{sub}</p>}
      </div>
    </div>
  )
}
