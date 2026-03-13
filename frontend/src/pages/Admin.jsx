import { useState, useEffect, useCallback } from 'react'
import { BarChart2, Users, Building2, Activity, RefreshCw, ToggleLeft, ToggleRight } from 'lucide-react'
import { Card, Badge, Spinner, StatCard, Button, Input, Alert } from '../components/ui/index'
import { TrendChart } from '../components/charts/index'
import api from '../api/client'

function fmt(n) { return n ? new Intl.NumberFormat('uz').format(Math.round(n)) : '—' }

const TABS = [
  { id: 'stats',    label: 'Statistika', icon: BarChart2 },
  { id: 'trends',   label: 'Tendensiya', icon: Activity },
  { id: 'users',    label: 'Foydalanuvchilar', icon: Users },
  { id: 'banks',    label: 'Banklar', icon: Building2 },
]

// ── Stats tab ─────────────────────────────────────────────────────────────────
function StatsTab() {
  const [data, setData]       = useState(null)
  const [purposes, setPurposes] = useState([])
  const [programs, setPrograms] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    Promise.all([
      api.get('/admin/stats'),
      api.get('/admin/purposes'),
      api.get('/admin/programs'),
    ]).then(([s, p, pr]) => {
      setData(s.data); setPurposes(p.data); setPrograms(pr.data)
    }).finally(() => setLoading(false))
  }, [])

  if (loading) return <div className="flex justify-center py-16"><Spinner size={28} /></div>
  if (!data)   return <Alert variant="danger">Ma'lumot yuklanmadi</Alert>

  return (
    <div className="space-y-5">
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
        <StatCard label="Foydalanuvchilar" value={data.total_users}       icon={Users}    color="brand" />
        <StatCard label="Tahlillar"        value={data.total_predictions}  icon={BarChart2} color="info" />
        <StatCard label="Tasdiqlangan"     value={data.approved_count}     icon={Activity} color="success"
          sub={`${(data.approval_rate * 100).toFixed(1)}% ulush`} />
        <StatCard label="Rad etilgan"      value={data.rejected_count}     icon={Activity} color="danger" />
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <Card className="p-5">
          <p className="label mb-3">O'rtacha ko'rsatkichlar</p>
          {[
            ['DTI nisbati', `${(data.avg_dti * 100).toFixed(1)}%`],
            ['Oylik daromad', `${fmt(data.avg_income_uzs)} UZS`],
            ['Kredit miqdori', `${fmt(data.avg_loan_amount_uzs)} UZS`],
          ].map(([k, v]) => (
            <div key={k} className="flex justify-between py-2 border-b text-sm" style={{ borderColor: 'var(--border)' }}>
              <span style={{ color: 'var(--text-2)' }}>{k}</span>
              <span className="font-semibold" style={{ color: 'var(--text)' }}>{v}</span>
            </div>
          ))}
        </Card>

        <Card className="p-5">
          <p className="label mb-3">Kredit maqsadlari</p>
          {purposes.slice(0, 6).map(p => (
            <div key={p.loan_purpose} className="flex items-center justify-between py-1.5 text-sm">
              <span style={{ color: 'var(--text-2)' }}>{p.loan_purpose}</span>
              <span className="font-medium" style={{ color: 'var(--text)' }}>{p.count} ({p.pct}%)</span>
            </div>
          ))}
        </Card>

        <Card className="p-5">
          <p className="label mb-3">Faol dasturlar</p>
          {programs.length === 0
            ? <p className="text-sm" style={{ color: 'var(--text-3)' }}>Hali dastur ishlatilmagan</p>
            : programs.slice(0, 6).map(p => (
              <div key={p.program_id} className="flex items-center justify-between py-1.5 text-sm">
                <span style={{ color: 'var(--text-2)' }}>{p.program_id}</span>
                <span className="font-medium" style={{ color: 'var(--text)' }}>{p.count} ({p.pct}%)</span>
              </div>
            ))
          }
        </Card>
      </div>
    </div>
  )
}

// ── Trends tab ────────────────────────────────────────────────────────────────
function TrendsTab() {
  const [data, setData]   = useState([])
  const [days, setDays]   = useState(30)
  const [loading, setLoading] = useState(true)

  const load = useCallback(() => {
    setLoading(true)
    api.get(`/admin/trends?days=${days}`)
      .then(r => setData(r.data))
      .finally(() => setLoading(false))
  }, [days])

  useEffect(() => { load() }, [load])

  return (
    <div className="space-y-4">
      <div className="flex items-center gap-2 flex-wrap">
        {[7, 14, 30, 60, 90].map(d => (
          <button
            key={d}
            onClick={() => setDays(d)}
            className="px-3 py-1.5 rounded-lg text-xs font-medium transition-all"
            style={{
              backgroundColor: days === d ? 'var(--brand)' : 'var(--surface2)',
              color: days === d ? '#fff' : 'var(--text-2)',
            }}
          >
            {d} kun
          </button>
        ))}
        <button onClick={load} className="btn-ghost ml-auto text-xs flex items-center gap-1">
          <RefreshCw size={12} /> Yangilash
        </button>
      </div>
      <Card className="p-5">
        <p className="section-title mb-4">Tahlil tendensiyasi</p>
        {loading
          ? <div className="flex justify-center py-8"><Spinner /></div>
          : <TrendChart data={data} />
        }
      </Card>
    </div>
  )
}

// ── Users tab ─────────────────────────────────────────────────────────────────
function UsersTab() {
  const [users, setUsers]   = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    api.get('/admin/users').then(r => setUsers(r.data)).finally(() => setLoading(false))
  }, [])

  if (loading) return <div className="flex justify-center py-16"><Spinner size={28} /></div>

  return (
    <Card className="p-5">
      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr style={{ color: 'var(--text-3)' }}>
              {['#', 'Foydalanuvchi', 'Rol', 'Ro\'yxat sanasi', 'So\'nggi faollik', 'Tahlillar'].map(h => (
                <th key={h} className="text-left py-2 pr-4 font-medium uppercase tracking-wide text-xs">{h}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {users.map(u => (
              <tr key={u.id} className="border-t" style={{ borderColor: 'var(--border)' }}>
                <td className="py-3 pr-4" style={{ color: 'var(--text-3)' }}>{u.id}</td>
                <td className="py-3 pr-4 font-medium" style={{ color: 'var(--text)' }}>{u.username}</td>
                <td className="py-3 pr-4">
                  <Badge variant={u.is_admin ? 'warning' : 'default'}>
                    {u.is_admin ? 'Admin' : 'Foydalanuvchi'}
                  </Badge>
                </td>
                <td className="py-3 pr-4" style={{ color: 'var(--text-2)' }}>
                  {new Date(u.created_at).toLocaleDateString('uz')}
                </td>
                <td className="py-3 pr-4" style={{ color: 'var(--text-2)' }}>
                  {new Date(u.last_active_at).toLocaleDateString('uz')}
                </td>
                <td className="py-3" style={{ color: 'var(--text)' }}>{u.prediction_count}</td>
              </tr>
            ))}
          </tbody>
        </table>
        {users.length === 0 && (
          <p className="text-center py-8 text-sm" style={{ color: 'var(--text-3)' }}>Foydalanuvchilar yo'q</p>
        )}
      </div>
    </Card>
  )
}

// ── Banks tab ─────────────────────────────────────────────────────────────────
function BanksTab() {
  const [banks, setBanks]   = useState([])
  const [loading, setLoading] = useState(true)
  const [editing, setEditing] = useState(null)
  const [saving, setSaving]   = useState(false)
  const [error, setError]     = useState('')

  useEffect(() => {
    api.get('/admin/banks').then(r => setBanks(r.data)).finally(() => setLoading(false))
  }, [])

  const toggleActive = async (bank) => {
    try {
      const { data } = await api.put(`/admin/banks/${bank.id}`, { is_active: !bank.is_active })
      setBanks(bs => bs.map(b => b.id === bank.id ? data : b))
    } catch { setError('O\'zgartirishda xatolik') }
  }

  const saveEdit = async () => {
    if (!editing) return
    setSaving(true)
    try {
      const { data } = await api.put(`/admin/banks/${editing.id}`, {
        rate_min: editing.rate_min,
        rate_max: editing.rate_max,
        max_loan_uzs: editing.max_loan_uzs,
        notes: editing.notes,
      })
      setBanks(bs => bs.map(b => b.id === data.id ? data : b))
      setEditing(null)
    } catch { setError('Saqlashda xatolik') } finally { setSaving(false) }
  }

  if (loading) return <div className="flex justify-center py-16"><Spinner size={28} /></div>

  return (
    <div className="space-y-4">
      {error && <Alert variant="danger">{error}</Alert>}

      {/* Edit modal */}
      {editing && (
        <Card elevated className="p-5 space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="section-title">Tahrirlash: {editing.bank_name}</h3>
            <button onClick={() => setEditing(null)} className="btn-ghost text-xs">Bekor</button>
          </div>
          <div className="grid grid-cols-2 gap-4">
            <Input label="Min stavka (%)" type="number" step={0.1} value={editing.rate_min}
              onChange={e => setEditing(v => ({ ...v, rate_min: Number(e.target.value) }))} />
            <Input label="Maks stavka (%)" type="number" step={0.1} value={editing.rate_max}
              onChange={e => setEditing(v => ({ ...v, rate_max: Number(e.target.value) }))} />
            <Input label="Maks kredit (UZS)" type="number" value={editing.max_loan_uzs} className="col-span-2"
              onChange={e => setEditing(v => ({ ...v, max_loan_uzs: Number(e.target.value) }))} />
            <Input label="Izoh" value={editing.notes} className="col-span-2"
              onChange={e => setEditing(v => ({ ...v, notes: e.target.value }))} />
          </div>
          <Button onClick={saveEdit} disabled={saving}>{saving ? 'Saqlanmoqda...' : 'Saqlash'}</Button>
        </Card>
      )}

      <Card className="p-5">
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr style={{ color: 'var(--text-3)' }}>
                {['Bank', 'Mahsulot', 'Stavka', 'Maks kredit', 'Holat', ''].map(h => (
                  <th key={h} className="text-left py-2 pr-4 font-medium uppercase tracking-wide text-xs">{h}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {banks.map(b => (
                <tr key={b.id} className="border-t" style={{ borderColor: 'var(--border)' }}>
                  <td className="py-3 pr-4 font-medium" style={{ color: 'var(--text)' }}>{b.bank_name}</td>
                  <td className="py-3 pr-4 text-xs max-w-[160px] truncate" style={{ color: 'var(--text-2)' }}>{b.product_name}</td>
                  <td className="py-3 pr-4" style={{ color: 'var(--text-2)' }}>{b.rate_min}–{b.rate_max}%</td>
                  <td className="py-3 pr-4" style={{ color: 'var(--text-2)' }}>{fmt(b.max_loan_uzs)}</td>
                  <td className="py-3 pr-4">
                    <button onClick={() => toggleActive(b)} className="flex items-center gap-1 text-xs">
                      {b.is_active
                        ? <><ToggleRight size={16} className="text-brand-500" /> <span className="text-brand-600 dark:text-brand-400">Faol</span></>
                        : <><ToggleLeft size={16} style={{ color: 'var(--text-3)' }} /> <span style={{ color: 'var(--text-3)' }}>Nofaol</span></>
                      }
                    </button>
                  </td>
                  <td className="py-3">
                    <button
                      onClick={() => setEditing(b)}
                      className="text-xs hover:underline"
                      style={{ color: 'var(--brand)' }}
                    >
                      Tahrirlash
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </Card>
    </div>
  )
}

// ── Main Admin page ───────────────────────────────────────────────────────────
export default function Admin() {
  const [tab, setTab] = useState('stats')

  return (
    <div className="max-w-5xl mx-auto px-4 py-8 animate-fade-in">
      <div className="mb-6">
        <h1 className="page-title">Admin panel</h1>
        <p className="text-sm mt-1" style={{ color: 'var(--text-3)' }}>Platforma boshqaruvi va statistikasi</p>
      </div>

      {/* Tabs */}
      <div className="flex gap-1 mb-6 p-1 rounded-xl w-fit" style={{ backgroundColor: 'var(--surface2)' }}>
        {TABS.map(({ id, label, icon: Icon }) => (
          <button
            key={id}
            onClick={() => setTab(id)}
            className={`flex items-center gap-1.5 px-4 py-2 rounded-lg text-sm font-medium transition-all ${
              tab === id ? 'shadow-card' : ''
            }`}
            style={{
              backgroundColor: tab === id ? 'var(--surface)' : 'transparent',
              color: tab === id ? 'var(--text)' : 'var(--text-3)',
            }}
          >
            <Icon size={14} />
            <span className="hidden sm:inline">{label}</span>
          </button>
        ))}
      </div>

      {tab === 'stats'  && <StatsTab />}
      {tab === 'trends' && <TrendsTab />}
      {tab === 'users'  && <UsersTab />}
      {tab === 'banks'  && <BanksTab />}
    </div>
  )
}
