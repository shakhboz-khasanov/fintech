import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { Zap, ChevronDown, ChevronUp, CheckCircle, XCircle, Star, AlertTriangle, TrendingUp, Lightbulb, ArrowRight } from 'lucide-react'
import { Button, Badge, Card, Spinner, Alert } from '../components/ui/index'
import { DtiGauge } from '../components/charts/index'
import api from '../api/client'

function fmt(n) { return n ? new Intl.NumberFormat('uz').format(Math.round(n)) : '—' }
function pct(n) { return (n * 100).toFixed(0) + '%' }

const PROGRAM_LABELS = {
  hamrokh:              'HAMROKH',
  teacher_mortgage:     'O\'qituvchi ipotekasi',
  youth_entrepreneur:   'Yoshlar tadbirkorligi',
  mahalla_low_income:   'Mahalla arzon ipoteka',
  agriculture:          'Qishloq xo\'jaligi',
  rural_mortgage:       'Qishloq ipotekasi',
  budget_salary_project:'Maosh loyihasi',
  education_loan:       'Ta\'lim krediti',
  green_energy:         'Yashil energiya',
  women_ifc:            'IFC Ayol tadbirkorlar',
}

function BankCard({ bank, programs }) {
  const [open, setOpen] = useState(false)
  const scorePct = Math.round(bank.score * 100)
  const color = scorePct >= 70 ? '#14b8a6' : scorePct >= 50 ? '#f59e0b' : '#ef4444'

  return (
    <div
      className={`card p-4 transition-all ${bank.eligible ? 'hover:shadow-card-md' : 'opacity-70'}`}
    >
      <div className="flex items-start justify-between gap-3">
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 flex-wrap">
            <span className="font-semibold text-sm" style={{ color: 'var(--text)' }}>{bank.bank_name}</span>
            {bank.eligible
              ? <Badge variant="success"><CheckCircle size={10} /> Mos</Badge>
              : <Badge variant="danger"><XCircle size={10} /> Mos emas</Badge>
            }
            {bank.matched_programs.map(p => (
              <Badge key={p} variant="brand">{PROGRAM_LABELS[p] || p}</Badge>
            ))}
          </div>
          <p className="text-xs mt-0.5" style={{ color: 'var(--text-3)' }}>{bank.product_name}</p>
          <div className="flex items-center gap-4 mt-2 flex-wrap">
            <span className="text-xs" style={{ color: 'var(--text-2)' }}>
              Stavka: <strong>{bank.rate_min}–{bank.rate_max}%</strong>
            </span>
            <span className="text-xs" style={{ color: 'var(--text-2)' }}>
              Maks: <strong>{fmt(bank.max_loan_uzs)} UZS</strong>
            </span>
            {bank.collateral_required && (
              <span className="text-xs text-amber-600 dark:text-amber-400">Garov talab</span>
            )}
          </div>
        </div>

        {/* Score circle */}
        <div className="flex flex-col items-center flex-shrink-0">
          <div
            className="w-14 h-14 rounded-full flex items-center justify-center border-2 font-bold font-display text-lg"
            style={{ borderColor: color, color }}
          >
            {scorePct}
          </div>
          <span className="text-xs mt-1" style={{ color: 'var(--text-3)' }}>ball</span>
        </div>
      </div>

      {/* Ineligibility reasons */}
      {!bank.eligible && bank.ineligible_reasons?.length > 0 && (
        <button
          onClick={() => setOpen(o => !o)}
          className="flex items-center gap-1 text-xs mt-2 hover:underline"
          style={{ color: 'var(--text-3)' }}
        >
          {open ? <ChevronUp size={12} /> : <ChevronDown size={12} />}
          Mos emasligi sabablari ({bank.ineligible_reasons.length})
        </button>
      )}
      {open && (
        <ul className="mt-2 space-y-1">
          {bank.ineligible_reasons.map((r, i) => (
            <li key={i} className="flex items-start gap-1.5 text-xs" style={{ color: 'var(--text-3)' }}>
              <XCircle size={11} className="text-red-400 mt-0.5 flex-shrink-0" />
              {r}
            </li>
          ))}
        </ul>
      )}

      {bank.notes && (
        <p className="text-xs mt-2 italic" style={{ color: 'var(--text-3)' }}>{bank.notes}</p>
      )}
    </div>
  )
}

export default function Kredit() {
  const [result, setResult]   = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError]     = useState('')
  const [filter, setFilter]   = useState('all') // all | eligible | programs
  const navigate = useNavigate()

  const run = async () => {
    setLoading(true); setError('')
    try {
      const profile = await api.get('/profile').then(r => r.data)
      const { data } = await api.post('/predict', profile)
      setResult(data)
    } catch (err) {
      if (err.response?.status === 404) {
        setError('Profil topilmadi. Avval profilingizni to\'ldiring.')
      } else {
        setError(err.response?.data?.detail || 'Tahlil qilishda xatolik')
      }
    } finally { setLoading(false) }
  }

  useEffect(() => { run() }, [])

  const filteredBanks = result?.per_bank_scores?.filter(b => {
    if (filter === 'eligible')  return b.eligible
    if (filter === 'programs')  return b.matched_programs?.length > 0
    return true
  }) ?? []

  const globalPct = result ? Math.round(result.global_approval_probability * 100) : 0

  return (
    <div className="max-w-3xl mx-auto px-4 py-8 animate-fade-in">
      <div className="flex items-center justify-between mb-6 flex-wrap gap-3">
        <div>
          <h1 className="page-title">Kredit tahlili</h1>
          <p className="text-sm mt-1" style={{ color: 'var(--text-3)' }}>Sizning profilingizga mos bank mahsulotlari</p>
        </div>
        <Button onClick={run} disabled={loading} variant="secondary">
          {loading ? <Spinner size={16} /> : <Zap size={15} />}
          Qayta hisoblash
        </Button>
      </div>

      {error && (
        <Alert variant="danger" className="mb-4">
          {error}
          {error.includes('Profil') && (
            <button onClick={() => navigate('/profil')} className="ml-2 underline text-sm">Profil to'ldirish</button>
          )}
        </Alert>
      )}

      {loading && !result && (
        <div className="flex flex-col items-center py-20 gap-4">
          <Spinner size={32} />
          <p style={{ color: 'var(--text-3)' }}>Tahlil qilinmoqda...</p>
        </div>
      )}

      {result && (
        <div className="space-y-5">
          {/* Summary row */}
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            {/* Global score */}
            <Card className="flex flex-col items-center text-center p-5">
              <p className="text-xs font-medium uppercase tracking-wide mb-3" style={{ color: 'var(--text-3)' }}>Umumiy ball</p>
              <div
                className="w-20 h-20 rounded-full border-4 flex items-center justify-center font-bold font-display text-2xl mb-2"
                style={{
                  borderColor: globalPct >= 70 ? '#14b8a6' : globalPct >= 50 ? '#f59e0b' : '#ef4444',
                  color:       globalPct >= 70 ? '#14b8a6' : globalPct >= 50 ? '#f59e0b' : '#ef4444',
                }}
              >
                {globalPct}%
              </div>
              <Badge variant={globalPct >= 70 ? 'success' : globalPct >= 50 ? 'warning' : 'danger'}>
                {globalPct >= 70 ? 'Yuqori' : globalPct >= 50 ? 'O\'rta' : 'Past'}
              </Badge>
            </Card>

            {/* DTI gauge */}
            <Card className="flex flex-col items-center p-5">
              <p className="text-xs font-medium uppercase tracking-wide mb-2" style={{ color: 'var(--text-3)' }}>Qarz yuki</p>
              <DtiGauge value={result.dti_ratio} />
            </Card>

            {/* Quick stats */}
            <Card className="p-5 space-y-3">
              <p className="text-xs font-medium uppercase tracking-wide" style={{ color: 'var(--text-3)' }}>Qisqa ko'rsatkichlar</p>
              {[
                ['Mos banklar',        `${result.eligible_bank_count} ta`],
                ['Maks kredit',        `${fmt(result.max_affordable_loan_uzs)} UZS`],
                ['Maxsus dasturlar',   `${result.special_programs?.length} ta`],
              ].map(([k, v]) => (
                <div key={k} className="flex justify-between text-sm">
                  <span style={{ color: 'var(--text-2)' }}>{k}</span>
                  <span className="font-semibold" style={{ color: 'var(--text)' }}>{v}</span>
                </div>
              ))}
            </Card>
          </div>

          {/* Special programs */}
          {result.special_programs?.length > 0 && (
            <Card className="p-5">
              <div className="flex items-center gap-2 mb-3">
                <Star size={16} className="text-amber-500" />
                <h3 className="section-title">Maxsus dasturlar</h3>
              </div>
              <div className="space-y-3">
                {result.special_programs.map(p => (
                  <div key={p.program_id} className="p-3 rounded-xl" style={{ backgroundColor: 'var(--surface2)' }}>
                    <div className="flex items-center gap-2 mb-1">
                      <Badge variant="brand">{p.program_name}</Badge>
                      {p.rate_discount_pct > 0 && <Badge variant="success">-{p.rate_discount_pct}% stavka</Badge>}
                    </div>
                    <p className="text-sm" style={{ color: 'var(--text-2)' }}>{p.benefit}</p>
                    <p className="text-xs mt-1" style={{ color: 'var(--text-3)' }}>
                      Banklar: {p.applicable_banks.join(', ')}
                    </p>
                  </div>
                ))}
              </div>
            </Card>
          )}

          {/* Tips */}
          {result.profile_tips?.length > 0 && (
            <Card className="p-5">
              <div className="flex items-center gap-2 mb-3">
                <Lightbulb size={16} className="text-brand-500" />
                <h3 className="section-title">Maslahatlar</h3>
              </div>
              <ul className="space-y-2">
                {result.profile_tips.map((tip, i) => (
                  <li key={i} className="text-sm" style={{ color: 'var(--text-2)' }}>{tip}</li>
                ))}
              </ul>
            </Card>
          )}

          {/* Bank list */}
          <div>
            <div className="flex items-center justify-between mb-3 flex-wrap gap-2">
              <h3 className="section-title">Bank mahsulotlari</h3>
              <div className="flex gap-1">
                {[['all','Hammasi'],['eligible','Mos'],['programs','Dasturlar']].map(([v, l]) => (
                  <button
                    key={v}
                    onClick={() => setFilter(v)}
                    className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-all ${
                      filter === v
                        ? 'bg-brand-500 text-white'
                        : 'hover:bg-slate-100 dark:hover:bg-slate-800'
                    }`}
                    style={{ color: filter === v ? undefined : 'var(--text-2)', backgroundColor: filter === v ? undefined : 'var(--surface2)' }}
                  >
                    {l}
                  </button>
                ))}
              </div>
            </div>
            <div className="space-y-3">
              {filteredBanks.map(b => (
                <BankCard key={b.bank_id} bank={b} programs={result.special_programs} />
              ))}
              {filteredBanks.length === 0 && (
                <p className="text-center py-8 text-sm" style={{ color: 'var(--text-3)' }}>
                  Bu filtr bo'yicha natija topilmadi
                </p>
              )}
            </div>
          </div>

          {/* Actions */}
          <div className="flex gap-3 flex-wrap">
            <Button onClick={() => navigate('/simulyatsiya')} variant="secondary">
              <TrendingUp size={15} /> Simulyatsiya
            </Button>
            <Button onClick={() => navigate('/profil')}>
              Profilni yangilash <ArrowRight size={15} />
            </Button>
          </div>
        </div>
      )}
    </div>
  )
}
