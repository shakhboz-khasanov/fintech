// components/charts/index.jsx
import {
  AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip,
  ResponsiveContainer, LineChart, Line, Legend
} from 'recharts'

// ── DTI Gauge ─────────────────────────────────────────────────────────────────
export function DtiGauge({ value }) {
  const pct   = Math.min(value * 100, 100)
  const color = pct <= 40 ? '#14b8a6' : pct <= 50 ? '#f59e0b' : '#ef4444'
  const label = pct <= 40 ? 'Yaxshi' : pct <= 50 ? 'Ehtiyot boling' : 'Yuqori'

  // SVG arc gauge
  const radius = 52
  const cx = 70, cy = 70
  const startAngle = 210
  const endAngle   = startAngle + 120 * (pct / 100) * 1.0
  const totalArc   = 120
  const sweep      = totalArc * (pct / 100)
  const toRad = d => (d * Math.PI) / 180

  const arcPath = (start, end, r) => {
    const s = { x: cx + r * Math.cos(toRad(start)), y: cy + r * Math.sin(toRad(start)) }
    const e = { x: cx + r * Math.cos(toRad(end)),   y: cy + r * Math.sin(toRad(end)) }
    const large = end - start > 180 ? 1 : 0
    return `M ${s.x} ${s.y} A ${r} ${r} 0 ${large} 1 ${e.x} ${e.y}`
  }

  return (
    <div className="flex flex-col items-center">
      <svg width="140" height="90" viewBox="0 0 140 90">
        {/* Track */}
        <path d={arcPath(210, 330, radius)} fill="none" stroke="var(--border)" strokeWidth="10" strokeLinecap="round" />
        {/* Value */}
        <path d={arcPath(210, 210 + sweep * 1.2, radius)} fill="none" stroke={color} strokeWidth="10" strokeLinecap="round" />
        {/* Center text */}
        <text x={cx} y={cy + 8} textAnchor="middle" fontSize="18" fontWeight="700" fontFamily="Sora" fill={color}>
          {pct.toFixed(0)}%
        </text>
      </svg>
      <span className="text-xs font-semibold mt-1" style={{ color }}>{label}</span>
      <span className="text-xs mt-0.5" style={{ color: 'var(--text-3)' }}>Qarz yuki nisbati</span>
    </div>
  )
}

// ── Cashflow Chart ────────────────────────────────────────────────────────────
export function CashflowChart({ schedule }) {
  if (!schedule?.length) return null

  // Sample every Nth row for readability
  const step = Math.max(1, Math.floor(schedule.length / 24))
  const data = schedule.filter((_, i) => i % step === 0).map(r => ({
    month: r.month,
    Asosiy: Math.round(r.principal),
    Foiz:   Math.round(r.interest),
    Qoldiq: Math.round(r.balance / 1_000_000),
  }))

  return (
    <ResponsiveContainer width="100%" height={220}>
      <AreaChart data={data} margin={{ top: 4, right: 4, bottom: 0, left: 0 }}>
        <defs>
          <linearGradient id="gPrincipal" x1="0" y1="0" x2="0" y2="1">
            <stop offset="5%"  stopColor="#14b8a6" stopOpacity={0.25} />
            <stop offset="95%" stopColor="#14b8a6" stopOpacity={0} />
          </linearGradient>
          <linearGradient id="gInterest" x1="0" y1="0" x2="0" y2="1">
            <stop offset="5%"  stopColor="#f59e0b" stopOpacity={0.25} />
            <stop offset="95%" stopColor="#f59e0b" stopOpacity={0} />
          </linearGradient>
        </defs>
        <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" />
        <XAxis dataKey="month" tick={{ fontSize: 11, fill: 'var(--text-3)' }} tickLine={false} />
        <YAxis tick={{ fontSize: 11, fill: 'var(--text-3)' }} tickLine={false} axisLine={false} />
        <Tooltip
          contentStyle={{ background: 'var(--surface)', border: '1px solid var(--border)', borderRadius: 12, fontSize: 12 }}
          formatter={v => new Intl.NumberFormat('uz').format(v) + ' UZS'}
        />
        <Legend iconType="circle" iconSize={8} wrapperStyle={{ fontSize: 12 }} />
        <Area type="monotone" dataKey="Asosiy" stroke="#14b8a6" fill="url(#gPrincipal)" strokeWidth={2} dot={false} />
        <Area type="monotone" dataKey="Foiz"   stroke="#f59e0b" fill="url(#gInterest)"  strokeWidth={2} dot={false} />
      </AreaChart>
    </ResponsiveContainer>
  )
}

// ── Trend Chart ───────────────────────────────────────────────────────────────
export function TrendChart({ data }) {
  if (!data?.length) return <div className="text-sm" style={{ color: 'var(--text-3)' }}>Ma'lumot yo'q</div>

  const chartData = data.map(d => ({
    date: d.date.slice(5),
    Jami: d.total,
    Tasdiqlangan: d.approved,
    'Rad etilgan': d.total - d.approved,
  }))

  return (
    <ResponsiveContainer width="100%" height={220}>
      <LineChart data={chartData} margin={{ top: 4, right: 4, bottom: 0, left: 0 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="var(--border)" />
        <XAxis dataKey="date" tick={{ fontSize: 11, fill: 'var(--text-3)' }} tickLine={false} />
        <YAxis tick={{ fontSize: 11, fill: 'var(--text-3)' }} tickLine={false} axisLine={false} />
        <Tooltip
          contentStyle={{ background: 'var(--surface)', border: '1px solid var(--border)', borderRadius: 12, fontSize: 12 }}
        />
        <Legend iconType="circle" iconSize={8} wrapperStyle={{ fontSize: 12 }} />
        <Line type="monotone" dataKey="Jami"          stroke="#94a3b8" strokeWidth={2} dot={false} />
        <Line type="monotone" dataKey="Tasdiqlangan"  stroke="#14b8a6" strokeWidth={2} dot={false} />
        <Line type="monotone" dataKey="Rad etilgan"   stroke="#f87171" strokeWidth={2} dot={false} />
      </LineChart>
    </ResponsiveContainer>
  )
}
