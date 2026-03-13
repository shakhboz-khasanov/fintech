import { useState } from 'react'
import { PiggyBank, CheckCircle, TrendingUp } from 'lucide-react'
import { Button, Input, Select, Card, Alert, Badge } from '../components/ui/index'
import api from '../api/client'

function fmt(n) { return n ? new Intl.NumberFormat('uz').format(Math.round(n)) : '—' }

function DepositCard({ match, highlight }) {
  return (
    <div className={`card p-4 transition-all hover:shadow-card-md ${highlight ? 'ring-2 ring-brand-400 dark:ring-brand-500' : ''}`}>
      <div className="flex items-start justify-between gap-3">
        <div className="flex-1">
          <div className="flex items-center gap-2 flex-wrap">
            <span className="font-semibold text-sm" style={{ color: 'var(--text)' }}>{match.bank_name}</span>
            {highlight && <Badge variant="brand"><CheckCircle size={10} /> Eng yaxshi</Badge>}
            <Badge variant={match.currency === 'uzs' ? 'success' : 'info'}>
              {match.currency.toUpperCase()}
            </Badge>
          </div>
          <p className="text-xs mt-0.5" style={{ color: 'var(--text-3)' }}>{match.product_name}</p>
          <div className="flex items-center gap-4 mt-2 flex-wrap text-xs" style={{ color: 'var(--text-2)' }}>
            <span>Muddat: <strong>{match.term_months} oy</strong></span>
            {match.min_amount && (
              <span>Min: <strong>{fmt(match.min_amount)} {match.currency.toUpperCase()}</strong></span>
            )}
          </div>
          {match.notes && <p className="text-xs mt-1 italic" style={{ color: 'var(--text-3)' }}>{match.notes}</p>}
        </div>

        <div className="flex flex-col items-center flex-shrink-0">
          <span className="text-2xl font-bold font-display text-brand-500 dark:text-brand-400">
            {match.rate_pct}%
          </span>
          <span className="text-xs" style={{ color: 'var(--text-3)' }}>yillik</span>
          {match.projected_return && (
            <span className="text-xs mt-1 text-emerald-600 dark:text-emerald-400 font-medium">
              +{fmt(match.projected_return)}
            </span>
          )}
        </div>
      </div>
    </div>
  )
}

export default function Depozit() {
  const [form, setForm] = useState({
    amount_uzs: 5000000,
    preferred_currency: 'uzs',
    preferred_term_months: 12,
    needs_early_withdrawal: false,
  })
  const [result, setResult]   = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError]     = useState('')
  const [filter, setFilter]   = useState('all')

  const e = ev => setForm(f => ({
    ...f,
    [ev.target.name]: ev.target.type === 'checkbox'
      ? ev.target.checked
      : ev.target.type === 'number'
        ? Number(ev.target.value)
        : ev.target.value
  }))

  const run = async () => {
    setLoading(true); setError('')
    try {
      const payload = { ...form }
      if (form.preferred_currency === 'usd') {
        payload.amount_usd = Math.round(form.amount_uzs / 12700)
        payload.amount_uzs = undefined
      }
      const { data } = await api.post('/deposit/match', payload)
      setResult(data)
    } catch (err) {
      setError(err.response?.data?.detail || 'Hisoblashda xatolik')
    } finally { setLoading(false) }
  }

  const filtered = result?.matches?.filter(m => {
    if (filter === 'uzs') return m.currency === 'uzs'
    if (filter === 'usd') return m.currency === 'usd'
    return true
  }) ?? []

  return (
    <div className="max-w-3xl mx-auto px-4 py-8 animate-fade-in">
      <div className="mb-6">
        <h1 className="page-title">Depozit maslahatchisi</h1>
        <p className="text-sm mt-1" style={{ color: 'var(--text-3)' }}>Jamg'armangizga eng mos depozit mahsulotlarini toping</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-5">
        {/* Form */}
        <Card elevated className="lg:col-span-1 space-y-4 h-fit">
          <h2 className="section-title flex items-center gap-2"><PiggyBank size={16} /> Parametrlar</h2>

          <Input
            label="Jamg'arma miqdori (UZS)"
            name="amount_uzs"
            type="number"
            min={0}
            value={form.amount_uzs}
            onChange={e}
            hint={`${fmt(form.amount_uzs)} UZS`}
          />
          <Select label="Valyuta" name="preferred_currency" value={form.preferred_currency} onChange={e}>
            <option value="uzs">UZS</option>
            <option value="usd">USD</option>
            <option value="both">Ikkalasi</option>
          </Select>
          <Input
            label="Afzal muddat (oy)"
            name="preferred_term_months"
            type="number"
            min={1}
            max={36}
            value={form.preferred_term_months}
            onChange={e}
          />
          <label className="flex items-center gap-2 text-sm cursor-pointer" style={{ color: 'var(--text-2)' }}>
            <input
              type="checkbox"
              name="needs_early_withdrawal"
              checked={form.needs_early_withdrawal}
              onChange={e}
              className="rounded"
            />
            Muddatidan oldin yechish kerak
          </label>

          <Button onClick={run} disabled={loading} className="w-full">
            {loading ? 'Qidirilmoqda...' : <><TrendingUp size={15} /> Topish</>}
          </Button>
        </Card>

        {/* Results */}
        <div className="lg:col-span-2 space-y-4">
          {error && <Alert variant="danger">{error}</Alert>}

          {result && (
            <>
              {/* Best picks */}
              {(result.best_uzs || result.best_usd) && (
                <Card className="p-5">
                  <h3 className="section-title mb-3">Eng yaxshi takliflar</h3>
                  <div className="space-y-3">
                    {result.best_uzs && <DepositCard match={result.best_uzs} highlight />}
                    {result.best_usd && result.best_usd.bank_slug !== result.best_uzs?.bank_slug && (
                      <DepositCard match={result.best_usd} highlight />
                    )}
                  </div>
                </Card>
              )}

              {/* Tips */}
              {result.tips?.length > 0 && (
                <div className="space-y-2">
                  {result.tips.map((tip, i) => (
                    <div key={i} className="p-3 rounded-xl text-sm" style={{ backgroundColor: 'var(--surface2)', color: 'var(--text-2)' }}>
                      {tip}
                    </div>
                  ))}
                </div>
              )}

              {/* All matches */}
              <div>
                <div className="flex items-center justify-between mb-3 flex-wrap gap-2">
                  <h3 className="section-title">Barcha takliflar ({filtered.length})</h3>
                  <div className="flex gap-1">
                    {[['all','Hammasi'],['uzs','UZS'],['usd','USD']].map(([v, l]) => (
                      <button
                        key={v}
                        onClick={() => setFilter(v)}
                        className="px-3 py-1.5 rounded-lg text-xs font-medium transition-all"
                        style={{
                          backgroundColor: filter === v ? 'var(--brand)' : 'var(--surface2)',
                          color: filter === v ? '#fff' : 'var(--text-2)',
                        }}
                      >
                        {l}
                      </button>
                    ))}
                  </div>
                </div>
                <div className="space-y-3">
                  {filtered.map((m, i) => (
                    <DepositCard
                      key={i}
                      match={m}
                      highlight={
                        (m.currency === 'uzs' && m.bank_slug === result.best_uzs?.bank_slug && m.product_name === result.best_uzs?.product_name) ||
                        (m.currency === 'usd' && m.bank_slug === result.best_usd?.bank_slug && m.product_name === result.best_usd?.product_name)
                      }
                    />
                  ))}
                  {filtered.length === 0 && (
                    <p className="text-center py-8 text-sm" style={{ color: 'var(--text-3)' }}>
                      Bu filtr bo'yicha natija topilmadi
                    </p>
                  )}
                </div>
              </div>
            </>
          )}

          {!result && !loading && (
            <div className="flex flex-col items-center justify-center py-20 text-center" style={{ color: 'var(--text-3)' }}>
              <PiggyBank size={48} className="mb-3 opacity-20" />
              <p className="text-sm">Parametrlarni kiriting va eng yaxshi depozitni toping</p>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
