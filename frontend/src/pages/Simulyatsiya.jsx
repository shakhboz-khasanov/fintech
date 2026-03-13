import { useState } from 'react'
import { TrendingUp, Calculator } from 'lucide-react'
import { Button, Input, Card, Alert, Badge } from '../components/ui/index'
import { CashflowChart } from '../components/charts/index'
import api from '../api/client'

function fmt(n) { return new Intl.NumberFormat('uz').format(Math.round(n)) }

export default function Simulyatsiya() {
  const [form, setForm] = useState({
    loan_amount_uzs: 10000000,
    annual_rate_pct: 26,
    term_months: 24,
    monthly_income_uzs: 5000000,
    monthly_expenses_uzs: 1500000,
    existing_debt_monthly_uzs: 0,
  })
  const [result, setResult]   = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError]     = useState('')
  const [showTable, setShowTable] = useState(false)

  const e = ev => setForm(f => ({ ...f, [ev.target.name]: Number(ev.target.value) }))

  const run = async () => {
    setLoading(true); setError('')
    try {
      const { data } = await api.post('/simulate', form)
      setResult(data)
    } catch (err) {
      setError(err.response?.data?.detail || 'Hisoblashda xatolik')
    } finally { setLoading(false) }
  }

  const dtiColor = result
    ? result.dti_ratio <= 0.4 ? 'success' : result.dti_ratio <= 0.5 ? 'warning' : 'danger'
    : 'default'

  return (
    <div className="max-w-3xl mx-auto px-4 py-8 animate-fade-in">
      <div className="mb-6">
        <h1 className="page-title">Kredit simulyatsiyasi</h1>
        <p className="text-sm mt-1" style={{ color: 'var(--text-3)' }}>Oylik to'lovlar va to'lov jadvalini hisoblash</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-5">
        {/* Input form */}
        <Card elevated className="space-y-4 h-fit">
          <h2 className="section-title flex items-center gap-2"><Calculator size={16} /> Parametrlar</h2>

          <Input label="Kredit miqdori (UZS)" name="loan_amount_uzs" type="number" min={500000}
            value={form.loan_amount_uzs} onChange={e} hint={`${fmt(form.loan_amount_uzs)} UZS`} />
          <Input label="Yillik stavka (%)" name="annual_rate_pct" type="number" min={1} max={60} step={0.1}
            value={form.annual_rate_pct} onChange={e} />
          <Input label="Muddat (oy)" name="term_months" type="number" min={1} max={240}
            value={form.term_months} onChange={e} />
          <div className="pt-2 border-t" style={{ borderColor: 'var(--border)' }}>
            <p className="text-xs font-semibold uppercase tracking-wide mb-3" style={{ color: 'var(--text-3)' }}>Moliyaviy holat</p>
            <div className="space-y-4">
              <Input label="Oylik daromad (UZS)" name="monthly_income_uzs" type="number" min={0}
                value={form.monthly_income_uzs} onChange={e} hint={`${fmt(form.monthly_income_uzs)} UZS`} />
              <Input label="Oylik xarajatlar (UZS)" name="monthly_expenses_uzs" type="number" min={0}
                value={form.monthly_expenses_uzs} onChange={e} />
              <Input label="Joriy qarz (oylik, UZS)" name="existing_debt_monthly_uzs" type="number" min={0}
                value={form.existing_debt_monthly_uzs} onChange={e} />
            </div>
          </div>

          <Button onClick={run} disabled={loading} className="w-full">
            {loading ? 'Hisoblanmoqda...' : <><TrendingUp size={15} /> Hisoblash</>}
          </Button>
        </Card>

        {/* Results */}
        <div className="space-y-4">
          {error && <Alert variant="danger">{error}</Alert>}

          {result && (
            <>
              {/* Key numbers */}
              <Card className="p-5 grid grid-cols-2 gap-4">
                {[
                  ['Oylik to\'lov',    `${fmt(result.monthly_payment)} UZS`],
                  ['Jami to\'lov',     `${fmt(result.total_payment)} UZS`],
                  ['Jami foiz',        `${fmt(result.total_interest)} UZS`],
                  ['DTI nisbati',      null],
                ].map(([k, v], i) => (
                  <div key={i} className={`${i === 3 ? 'col-span-2' : ''}`}>
                    <p className="text-xs font-medium uppercase tracking-wide mb-1" style={{ color: 'var(--text-3)' }}>{k}</p>
                    {v
                      ? <p className="text-xl font-semibold font-display" style={{ color: 'var(--text)' }}>{v}</p>
                      : <div className="flex items-center gap-2">
                          <p className="text-xl font-semibold font-display" style={{ color: 'var(--text)' }}>
                            {(result.dti_ratio * 100).toFixed(1)}%
                          </p>
                          <Badge variant={dtiColor}>
                            {result.dti_ratio <= 0.4 ? 'Yaxshi' : result.dti_ratio <= 0.5 ? 'Ehtiyot' : 'Yuqori'}
                          </Badge>
                        </div>
                    }
                  </div>
                ))}
              </Card>

              {result.dti_warning && (
                <Alert variant="warning">
                  DTI nisbati 40% dan oshdi. Ba'zi banklar qo'shimcha garov talab qilishi mumkin.
                </Alert>
              )}

              {/* Chart */}
              <Card className="p-5">
                <h3 className="section-title mb-4">To'lov tarkibi</h3>
                <CashflowChart schedule={result.schedule} />
              </Card>

              {/* Table toggle */}
              <Card className="p-5">
                <div className="flex items-center justify-between mb-3">
                  <h3 className="section-title">To'lov jadvali</h3>
                  <Button variant="ghost" onClick={() => setShowTable(s => !s)} className="text-xs">
                    {showTable ? 'Yashirish' : 'Ko\'rsatish'}
                  </Button>
                </div>
                {showTable && (
                  <div className="overflow-x-auto">
                    <table className="w-full text-xs">
                      <thead>
                        <tr style={{ color: 'var(--text-3)' }}>
                          {['Oy','To\'lov','Asosiy','Foiz','Qoldiq'].map(h => (
                            <th key={h} className="text-left py-2 pr-3 font-medium uppercase tracking-wide">{h}</th>
                          ))}
                        </tr>
                      </thead>
                      <tbody>
                        {result.schedule.map(row => (
                          <tr key={row.month} className="border-t" style={{ borderColor: 'var(--border)', color: 'var(--text-2)' }}>
                            <td className="py-2 pr-3">{row.month}</td>
                            <td className="py-2 pr-3">{fmt(row.payment)}</td>
                            <td className="py-2 pr-3 text-teal-600 dark:text-teal-400">{fmt(row.principal)}</td>
                            <td className="py-2 pr-3 text-amber-600 dark:text-amber-400">{fmt(row.interest)}</td>
                            <td className="py-2">{fmt(row.balance)}</td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                )}
              </Card>
            </>
          )}

          {!result && !loading && (
            <div className="flex flex-col items-center justify-center py-16 text-center" style={{ color: 'var(--text-3)' }}>
              <TrendingUp size={40} className="mb-3 opacity-30" />
              <p className="text-sm">Parametrlarni kiriting va hisoblang</p>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
