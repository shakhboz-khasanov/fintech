import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { CreditCard, TrendingUp, PiggyBank, User, ArrowRight, Zap } from 'lucide-react'
import { Card, Button, Badge, Spinner, StatCard } from '../components/ui/index'
import { DtiGauge } from '../components/charts/index'
import api from '../api/client'

function fmt(n) { return n ? new Intl.NumberFormat('uz').format(Math.round(n)) : '—' }

const QUICK_ACTIONS = [
  { to: '/kredit',       icon: CreditCard, label: 'Kredit tahlili',   desc: 'Mos banklarni ko\'ring',    color: 'brand' },
  { to: '/simulyatsiya', icon: TrendingUp, label: 'Simulyatsiya',      desc: 'To\'lov jadvalini hisoblang', color: 'info' },
  { to: '/depozit',      icon: PiggyBank,  label: 'Depozit',           desc: 'Jamg\'armangizni o\'stiring', color: 'success' },
  { to: '/profil',       icon: User,       label: 'Profilim',          desc: 'Ma\'lumotlarni yangilang',   color: 'warning' },
]

export default function Dashboard({ user }) {
  const [profile, setProfile]   = useState(null)
  const [lastPred, setLastPred] = useState(null)
  const [loading, setLoading]   = useState(true)
  const navigate = useNavigate()

  useEffect(() => {
    Promise.allSettled([
      api.get('/profile'),
      api.post('/predict', {}).catch(() => null),
    ]).then(([profRes]) => {
      if (profRes.status === 'fulfilled') setProfile(profRes.value.data)
      setLoading(false)
    })

    // Load last prediction from kredit if profile exists
    api.get('/profile').then(r => {
      api.post('/predict', r.data).then(p => setLastPred(p.data)).catch(() => {})
    }).catch(() => setLoading(false))
  }, [])

  const hour = new Date().getHours()
  const greeting = hour < 12 ? 'Xayrli tong' : hour < 17 ? 'Xayrli kun' : 'Xayrli kech'

  return (
    <div className="max-w-4xl mx-auto px-4 py-8 animate-fade-in">
      {/* Greeting */}
      <div className="mb-8">
        <h1 className="page-title">{greeting}, {user?.username} 👋</h1>
        <p className="text-sm mt-1" style={{ color: 'var(--text-3)' }}>
          SarfAI moliyaviy maslahatchi — kredit, depozit va rejalashtirish
        </p>
      </div>

      {loading ? (
        <div className="flex justify-center py-16"><Spinner size={28} /></div>
      ) : (
        <div className="space-y-6">
          {/* Profile missing prompt */}
          {!profile && (
            <div className="card-md p-6 flex items-center justify-between flex-wrap gap-4"
              style={{ background: 'linear-gradient(135deg, var(--brand) 0%, #0d9488 100%)' }}>
              <div>
                <p className="font-semibold text-white font-display">Profilingizni to'ldiring</p>
                <p className="text-sm text-white/80 mt-0.5">Kredit tahlili uchun moliyaviy ma'lumotlaringizni kiriting</p>
              </div>
              <button
                onClick={() => navigate('/profil')}
                className="flex items-center gap-2 bg-white text-teal-700 font-medium text-sm px-4 py-2 rounded-xl hover:bg-white/90 transition-all"
              >
                Boshlash <ArrowRight size={14} />
              </button>
            </div>
          )}

          {/* Last prediction summary */}
          {lastPred && (
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
              <Card className="sm:col-span-1 flex flex-col items-center justify-center p-5 text-center">
                <p className="text-xs font-medium uppercase tracking-wide mb-3" style={{ color: 'var(--text-3)' }}>
                  Kredit imkoniyati
                </p>
                <DtiGauge value={lastPred.dti_ratio} />
              </Card>

              <Card className="sm:col-span-2 p-5 space-y-3">
                <div className="flex items-center justify-between">
                  <p className="section-title">Oxirgi tahlil</p>
                  <Badge variant={lastPred.global_approval_probability >= 0.7 ? 'success' : lastPred.global_approval_probability >= 0.5 ? 'warning' : 'danger'}>
                    {Math.round(lastPred.global_approval_probability * 100)}% imkon
                  </Badge>
                </div>
                <div className="grid grid-cols-2 gap-3">
                  {[
                    ['Mos banklar',      `${lastPred.eligible_bank_count} ta`],
                    ['Maks kredit',      `${fmt(lastPred.max_affordable_loan_uzs)} UZS`],
                    ['Maxsus dasturlar', `${lastPred.special_programs?.length} ta`],
                    ['DTI nisbati',      `${(lastPred.dti_ratio * 100).toFixed(1)}%`],
                  ].map(([k, v]) => (
                    <div key={k} className="p-3 rounded-xl" style={{ backgroundColor: 'var(--surface2)' }}>
                      <p className="text-xs" style={{ color: 'var(--text-3)' }}>{k}</p>
                      <p className="font-semibold text-sm mt-0.5 font-display" style={{ color: 'var(--text)' }}>{v}</p>
                    </div>
                  ))}
                </div>
                <Button onClick={() => navigate('/kredit')} className="w-full">
                  <Zap size={14} /> Batafsil tahlil
                </Button>
              </Card>
            </div>
          )}

          {/* Quick actions */}
          <div>
            <p className="section-title mb-3">Tezkor harakatlar</p>
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
              {QUICK_ACTIONS.map(({ to, icon: Icon, label, desc, color }) => (
                <button
                  key={to}
                  onClick={() => navigate(to)}
                  className="card p-4 text-left hover:shadow-card-md transition-all group hover:border-brand-300 dark:hover:border-brand-700 active:scale-[0.98]"
                >
                  <div className={`w-9 h-9 rounded-xl mb-3 flex items-center justify-center ${
                    color === 'brand'   ? 'bg-teal-100 text-teal-600 dark:bg-teal-900/40 dark:text-teal-400' :
                    color === 'info'    ? 'bg-blue-100 text-blue-600 dark:bg-blue-900/40 dark:text-blue-400' :
                    color === 'success' ? 'bg-emerald-100 text-emerald-600 dark:bg-emerald-900/40 dark:text-emerald-400' :
                                         'bg-amber-100 text-amber-600 dark:bg-amber-900/40 dark:text-amber-400'
                  }`}>
                    <Icon size={16} />
                  </div>
                  <p className="font-semibold text-sm mb-0.5" style={{ color: 'var(--text)' }}>{label}</p>
                  <p className="text-xs leading-relaxed" style={{ color: 'var(--text-3)' }}>{desc}</p>
                </button>
              ))}
            </div>
          </div>

          {/* Profile snapshot */}
          {profile && (
            <Card className="p-5">
              <div className="flex items-center justify-between mb-4">
                <h3 className="section-title">Profil ma'lumotlari</h3>
                <button
                  onClick={() => navigate('/profil')}
                  className="text-xs flex items-center gap-1 hover:underline"
                  style={{ color: 'var(--brand)' }}
                >
                  Tahrirlash <ArrowRight size={12} />
                </button>
              </div>
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
                {[
                  ['Oylik daromad',   `${fmt(profile.monthly_income_uzs)} UZS`],
                  ['Joriy qarz',      `${fmt(profile.existing_debt_monthly_uzs)} UZS`],
                  ['Kredit tarixi',   profile.credit_history_status === 'good' ? 'Yaxshi' : profile.credit_history_status === 'bad' ? 'Yomon' : 'Yo\'q'],
                  ['Garov',          profile.has_collateral ? 'Bor' : 'Yo\'q'],
                ].map(([k, v]) => (
                  <div key={k} className="p-3 rounded-xl" style={{ backgroundColor: 'var(--surface2)' }}>
                    <p className="text-xs" style={{ color: 'var(--text-3)' }}>{k}</p>
                    <p className="font-semibold text-sm mt-0.5" style={{ color: 'var(--text)' }}>{v}</p>
                  </div>
                ))}
              </div>
            </Card>
          )}
        </div>
      )}
    </div>
  )
}
