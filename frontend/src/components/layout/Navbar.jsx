import { useState } from 'react'
import { Link, useLocation, useNavigate } from 'react-router-dom'
import { LayoutDashboard, User, CreditCard, TrendingUp, PiggyBank, ShieldCheck, Menu, X, LogOut } from 'lucide-react'
import { ThemeToggle } from '../ui/index'

const NAV_ITEMS = [
  { to: '/dashboard',    label: 'Bosh sahifa',   icon: LayoutDashboard },
  { to: '/profil',       label: 'Profilim',       icon: User },
  { to: '/kredit',       label: 'Kredit',         icon: CreditCard },
  { to: '/simulyatsiya', label: 'Simulyatsiya',   icon: TrendingUp },
  { to: '/depozit',      label: 'Depozit',        icon: PiggyBank },
]

export default function Navbar({ user, onLogout, dark, onThemeToggle }) {
  const location = useLocation()
  const navigate = useNavigate()
  const [menuOpen, setMenuOpen] = useState(false)

  const handleLogout = () => {
    onLogout()
    navigate('/login')
  }

  return (
    <header
      className="sticky top-0 z-40 border-b"
      style={{ backgroundColor: 'var(--surface)', borderColor: 'var(--border)' }}
    >
      <div className="max-w-6xl mx-auto px-4 sm:px-6 h-14 flex items-center justify-between gap-4">
        {/* Logo */}
        <Link to="/dashboard" className="flex items-center gap-2 flex-shrink-0">
          <div className="w-7 h-7 rounded-lg bg-brand-500 flex items-center justify-center">
            <span className="text-white text-xs font-bold font-display">S</span>
          </div>
          <span className="font-display font-semibold text-base" style={{ color: 'var(--text)' }}>
            SarfAI
          </span>
        </Link>

        {/* Desktop nav */}
        <nav className="hidden md:flex items-center gap-1 flex-1 justify-center">
          {NAV_ITEMS.map(({ to, label, icon: Icon }) => {
            const active = location.pathname === to
            return (
              <Link
                key={to}
                to={to}
                className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-sm font-medium transition-all ${
                  active
                    ? 'bg-brand-50 text-brand-700 dark:bg-brand-900/30 dark:text-brand-300'
                    : 'hover:bg-slate-100 dark:hover:bg-slate-800'
                }`}
                style={{ color: active ? undefined : 'var(--text-2)' }}
              >
                <Icon size={15} />
                {label}
              </Link>
            )
          })}
          {user?.is_admin && (
            <Link
              to="/admin"
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-sm font-medium transition-all ${
                location.pathname === '/admin'
                  ? 'bg-amber-50 text-amber-700 dark:bg-amber-900/30 dark:text-amber-300'
                  : 'hover:bg-slate-100 dark:hover:bg-slate-800'
              }`}
              style={{ color: location.pathname === '/admin' ? undefined : 'var(--text-2)' }}
            >
              <ShieldCheck size={15} />
              Admin
            </Link>
          )}
        </nav>

        {/* Right actions */}
        <div className="flex items-center gap-2 flex-shrink-0">
          <ThemeToggle dark={dark} onToggle={onThemeToggle} />

          {/* Username */}
          <span
            className="hidden sm:block text-sm font-medium px-3 py-1.5 rounded-lg"
            style={{ color: 'var(--text-2)', backgroundColor: 'var(--surface2)' }}
          >
            {user?.username}
          </span>

          <button
            onClick={handleLogout}
            className="hidden sm:flex items-center gap-1.5 btn-ghost text-sm"
            title="Chiqish"
          >
            <LogOut size={15} />
          </button>

          {/* Mobile hamburger */}
          <button
            className="md:hidden w-9 h-9 flex items-center justify-center rounded-xl"
            style={{ color: 'var(--text-2)' }}
            onClick={() => setMenuOpen(o => !o)}
          >
            {menuOpen ? <X size={18} /> : <Menu size={18} />}
          </button>
        </div>
      </div>

      {/* Mobile menu */}
      {menuOpen && (
        <div
          className="md:hidden border-t px-4 py-3 space-y-1 animate-slide-down"
          style={{ backgroundColor: 'var(--surface)', borderColor: 'var(--border)' }}
        >
          {NAV_ITEMS.map(({ to, label, icon: Icon }) => (
            <Link
              key={to}
              to={to}
              onClick={() => setMenuOpen(false)}
              className={`flex items-center gap-2.5 px-3 py-2.5 rounded-xl text-sm font-medium w-full ${
                location.pathname === to
                  ? 'bg-brand-50 text-brand-700 dark:bg-brand-900/30 dark:text-brand-300'
                  : ''
              }`}
              style={{ color: location.pathname === to ? undefined : 'var(--text-2)' }}
            >
              <Icon size={16} /> {label}
            </Link>
          ))}
          {user?.is_admin && (
            <Link to="/admin" onClick={() => setMenuOpen(false)}
              className="flex items-center gap-2.5 px-3 py-2.5 rounded-xl text-sm font-medium w-full"
              style={{ color: 'var(--text-2)' }}
            >
              <ShieldCheck size={16} /> Admin
            </Link>
          )}
          <button
            onClick={handleLogout}
            className="flex items-center gap-2.5 px-3 py-2.5 rounded-xl text-sm font-medium w-full text-red-500"
          >
            <LogOut size={16} /> Chiqish
          </button>
        </div>
      )}
    </header>
  )
}
