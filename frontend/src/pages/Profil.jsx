import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { CheckCircle, ChevronRight, ChevronLeft, User, Briefcase, Wallet, Target } from 'lucide-react'
import { Button, Input, Select, Card, Alert } from '../components/ui/index'
import api from '../api/client'

const STEPS = [
  { label: 'Shaxsiy',    icon: User },
  { label: 'Ish',        icon: Briefcase },
  { label: 'Moliya',     icon: Wallet },
  { label: 'Kredit',     icon: Target },
]

const REGIONS = ['Toshkent shahri','Toshkent viloyati','Samarqand','Farg\'ona','Andijon','Namangan','Buxoro','Xorazm','Qashqadaryo','Surxondaryo','Jizzax','Sirdaryo','Navoiy','Qoraqalpog\'iston']
const BANKS   = ['none','kapitalbank','hamkorbank','xalq_banki','ipoteka_bank','nbu','ipak_yoli','asakabank','orient_finans','agrobank','mkbank','aloqabank','trastbank','turonbank','other']
const BANK_LABELS = { none:'Yo\'q', kapitalbank:'Kapitalbank', hamkorbank:'Hamkorbank', xalq_banki:'Xalq Banki', ipoteka_bank:'Ipoteka Bank', nbu:'NBU', ipak_yoli:'Ipak Yo\'li Bank', asakabank:'Asakabank', orient_finans:'Orient Finans', agrobank:'Agrobank', mkbank:'MKBank', aloqabank:'Aloqabank', trastbank:'Trastbank', turonbank:'Turonbank', other:'Boshqa' }

const EMPTY = {
  age:18, gender:'male', region:'Toshkent shahri', marital_status:'single', dependents_count:0, is_young_family:false,
  employment_type:'employed_state', profession_category:'education', profession_role:'teacher', salary_bank:'none', work_experience_months:0,
  monthly_income_uzs:3000000, has_additional_income:false, additional_income_uzs:0, income_proof_type:'official_certificate',
  existing_debt_monthly_uzs:0, credit_history_status:'none', has_collateral:false, collateral_type:'none', collateral_value_uzs:0, has_guarantor:false, savings_uzs:0,
  loan_purpose:'consumer', loan_amount_requested_uzs:5000000, loan_term_months:24, preferred_currency:'uzs',
  is_student:false, is_mahalla_low_income:false, is_women_entrepreneur:false, is_youth_entrepreneur:false, is_farmer:false,
  teacher_qualification_category:'none', teacher_experience_years:0,
}

function fmt(n) { return new Intl.NumberFormat('uz').format(n) }

export default function Profil() {
  const [step, setStep]   = useState(0)
  const [form, setForm]   = useState(EMPTY)
  const [loading, setLoading] = useState(false)
  const [saved, setSaved]     = useState(false)
  const [error, setError]     = useState('')
  const navigate = useNavigate()

  useEffect(() => {
    api.get('/profile').then(r => setForm(f => ({ ...f, ...r.data }))).catch(() => {})
  }, [])

  const set = (k, v) => setForm(f => ({ ...f, [k]: v }))
  const e   = e => set(e.target.name, e.target.type === 'checkbox' ? e.target.checked : e.target.type === 'number' ? Number(e.target.value) : e.target.value)

  const save = async () => {
    setLoading(true); setError('')
    try {
      await api.post('/profile', form).catch(() => api.put('/profile', form))
      setSaved(true)
      setTimeout(() => navigate('/kredit'), 1200)
    } catch (err) {
      setError(err.response?.data?.detail || 'Saqlashda xatolik')
    } finally { setLoading(false) }
  }

  if (saved) return (
    <div className="max-w-lg mx-auto px-4 py-16 text-center animate-fade-in">
      <CheckCircle size={56} className="mx-auto text-brand-500 mb-4" />
      <h2 className="page-title mb-2">Profil saqlandi!</h2>
      <p style={{ color: 'var(--text-3)' }}>Kredit tahlili sahifasiga o'tilmoqda...</p>
    </div>
  )

  return (
    <div className="max-w-2xl mx-auto px-4 py-8 animate-fade-in">
      <div className="mb-8">
        <h1 className="page-title">Moliyaviy profilim</h1>
        <p className="text-sm mt-1" style={{ color: 'var(--text-3)' }}>Kredit tahlili uchun ma'lumotlaringizni kiriting</p>
      </div>

      {/* Step indicators */}
      <div className="flex items-center gap-2 mb-8">
        {STEPS.map(({ label, icon: Icon }, i) => (
          <div key={i} className="flex items-center gap-2 flex-1">
            <button
              onClick={() => i <= step && setStep(i)}
              className={`flex items-center gap-2 px-3 py-2 rounded-xl text-xs font-medium transition-all flex-1 ${
                i === step    ? 'bg-brand-500 text-white shadow-card-md' :
                i < step      ? 'bg-brand-100 text-brand-700 dark:bg-brand-900/40 dark:text-brand-300' :
                                'text-[color:var(--text-3)]'
              }`}
              style={i > step ? { backgroundColor: 'var(--surface2)' } : {}}
            >
              <Icon size={13} />
              <span className="hidden sm:inline">{label}</span>
              <span className="sm:hidden">{i + 1}</span>
            </button>
            {i < STEPS.length - 1 && <ChevronRight size={14} style={{ color: 'var(--text-3)' }} className="flex-shrink-0" />}
          </div>
        ))}
      </div>

      {error && <Alert variant="danger" className="mb-4">{error}</Alert>}

      <Card elevated className="space-y-5">
        {/* Step 0 — Demographics */}
        {step === 0 && <>
          <h2 className="section-title">Shaxsiy ma'lumotlar</h2>
          <div className="grid grid-cols-2 gap-4">
            <Input label="Yosh" name="age" type="number" min={18} max={65} value={form.age} onChange={e} />
            <Select label="Jins" name="gender" value={form.gender} onChange={e}>
              <option value="male">Erkak</option>
              <option value="female">Ayol</option>
            </Select>
            <Select label="Viloyat" name="region" value={form.region} onChange={e} className="col-span-2">
              {REGIONS.map(r => <option key={r} value={r}>{r}</option>)}
            </Select>
            <Select label="Oilaviy holat" name="marital_status" value={form.marital_status} onChange={e}>
              <option value="single">Turmush qurmagan</option>
              <option value="married">Turmush qurgan</option>
              <option value="divorced">Ajrashgan</option>
              <option value="widowed">Beva</option>
            </Select>
            <Input label="Qaramog'idagilar soni" name="dependents_count" type="number" min={0} max={10} value={form.dependents_count} onChange={e} />
          </div>
          <label className="flex items-center gap-2 text-sm cursor-pointer" style={{ color: 'var(--text-2)' }}>
            <input type="checkbox" name="is_young_family" checked={form.is_young_family} onChange={e} className="rounded" />
            Yosh oila (35 yoshgacha)
          </label>
        </>}

        {/* Step 1 — Employment */}
        {step === 1 && <>
          <h2 className="section-title">Ish va daromad</h2>
          <div className="grid grid-cols-2 gap-4">
            <Select label="Ish turi" name="employment_type" value={form.employment_type} onChange={e} className="col-span-2">
              <option value="employed_state">Davlat xodimi</option>
              <option value="employed_private">Xususiy xodim</option>
              <option value="self_employed">Mustaqil ish</option>
              <option value="entrepreneur">Tadbirkor</option>
              <option value="farmer">Fermer</option>
              <option value="student">Talaba</option>
              <option value="pensioner">Pensioner</option>
              <option value="unemployed">Ishsiz</option>
            </Select>
            <Select label="Kasb toifasi" name="profession_category" value={form.profession_category} onChange={e}>
              <option value="education">Ta'lim</option>
              <option value="healthcare">Tibbiyot</option>
              <option value="security">Mudofaa/Xavfsizlik</option>
              <option value="agriculture">Qishloq xo'jaligi</option>
              <option value="it_tech">IT/Texnologiya</option>
              <option value="finance">Moliya</option>
              <option value="legal">Huquq</option>
              <option value="civil_service">Davlat xizmati</option>
              <option value="business_owner">Biznes egasi</option>
              <option value="other">Boshqa</option>
            </Select>
            <Input label="Ish tajribasi (oy)" name="work_experience_months" type="number" min={0} value={form.work_experience_months} onChange={e} />
            <Input label="Oylik daromad (UZS)" name="monthly_income_uzs" type="number" min={0} value={form.monthly_income_uzs} onChange={e}
              hint={`${fmt(form.monthly_income_uzs)} UZS`} />
            <Select label="Maosh banki" name="salary_bank" value={form.salary_bank} onChange={e}>
              {BANKS.map(b => <option key={b} value={b}>{BANK_LABELS[b]}</option>)}
            </Select>
            <Select label="Daromad tasdiq" name="income_proof_type" value={form.income_proof_type} onChange={e}>
              <option value="official_certificate">Rasmiy ma'lumotnoma</option>
              <option value="bank_statement">Bank ko'chirma</option>
              <option value="tax_declaration">Soliq deklaratsiyasi</option>
              <option value="none">Yo'q</option>
            </Select>
          </div>
          <label className="flex items-center gap-2 text-sm cursor-pointer" style={{ color: 'var(--text-2)' }}>
            <input type="checkbox" name="has_additional_income" checked={form.has_additional_income} onChange={e} className="rounded" />
            Qo'shimcha daromad bor
          </label>
          {form.has_additional_income && (
            <Input label="Qo'shimcha daromad (UZS)" name="additional_income_uzs" type="number" min={0} value={form.additional_income_uzs} onChange={e} />
          )}
          {form.profession_category === 'education' && (
            <div className="grid grid-cols-2 gap-4 p-4 rounded-xl" style={{ backgroundColor: 'var(--surface2)' }}>
              <Select label="O'qituvchi toifasi" name="teacher_qualification_category" value={form.teacher_qualification_category} onChange={e}>
                <option value="none">Toifasiz</option>
                <option value="standard">Standart</option>
                <option value="top_category">Oliy toifa</option>
              </Select>
              <Input label="Pedagogik tajriba (yil)" name="teacher_experience_years" type="number" min={0} max={40} value={form.teacher_experience_years} onChange={e} />
            </div>
          )}
        </>}

        {/* Step 2 — Financial */}
        {step === 2 && <>
          <h2 className="section-title">Moliyaviy holat</h2>
          <div className="grid grid-cols-2 gap-4">
            <Input label="Joriy qarz (oylik, UZS)" name="existing_debt_monthly_uzs" type="number" min={0} value={form.existing_debt_monthly_uzs} onChange={e}
              hint={`${fmt(form.existing_debt_monthly_uzs)} UZS`} />
            <Input label="Jamg'arma (UZS)" name="savings_uzs" type="number" min={0} value={form.savings_uzs} onChange={e} />
            <Select label="Kredit tarixi" name="credit_history_status" value={form.credit_history_status} onChange={e} className="col-span-2">
              <option value="none">Yo'q (birinchi kredit)</option>
              <option value="good">Yaxshi</option>
              <option value="bad">Yomon</option>
              <option value="overdue">Muddati o'tgan</option>
            </Select>
          </div>
          <label className="flex items-center gap-2 text-sm cursor-pointer" style={{ color: 'var(--text-2)' }}>
            <input type="checkbox" name="has_collateral" checked={form.has_collateral} onChange={e} className="rounded" />
            Garov mulki bor
          </label>
          {form.has_collateral && (
            <div className="grid grid-cols-2 gap-4">
              <Select label="Garov turi" name="collateral_type" value={form.collateral_type} onChange={e}>
                <option value="real_estate">Ko'chmas mulk</option>
                <option value="vehicle">Transport</option>
                <option value="both">Ikkalasi ham</option>
              </Select>
              <Input label="Garov qiymati (UZS)" name="collateral_value_uzs" type="number" min={0} value={form.collateral_value_uzs} onChange={e} />
            </div>
          )}
          <label className="flex items-center gap-2 text-sm cursor-pointer" style={{ color: 'var(--text-2)' }}>
            <input type="checkbox" name="has_guarantor" checked={form.has_guarantor} onChange={e} className="rounded" />
            Kafil bor
          </label>
          <div className="pt-2 border-t" style={{ borderColor: 'var(--border)' }}>
            <p className="text-xs font-medium mb-3" style={{ color: 'var(--text-3)' }}>MAXSUS DASTURLAR</p>
            <div className="space-y-2">
              {[
                ['is_student',           'Talabaman'],
                ['is_mahalla_low_income','Mahalla ro\'yxatidagi kam ta\'minlangan oila'],
                ['is_women_entrepreneur','Ayol tadbirkor'],
                ['is_youth_entrepreneur','Yosh tadbirkor (35 yoshgacha)'],
                ['is_farmer',            'Fermer'],
              ].map(([key, label]) => (
                <label key={key} className="flex items-center gap-2 text-sm cursor-pointer" style={{ color: 'var(--text-2)' }}>
                  <input type="checkbox" name={key} checked={form[key]} onChange={e} className="rounded" />
                  {label}
                </label>
              ))}
            </div>
          </div>
        </>}

        {/* Step 3 — Loan request */}
        {step === 3 && <>
          <h2 className="section-title">Kredit so'rovi</h2>
          <div className="grid grid-cols-2 gap-4">
            <Select label="Kredit maqsadi" name="loan_purpose" value={form.loan_purpose} onChange={e} className="col-span-2">
              <option value="consumer">Iste'mol krediti</option>
              <option value="mortgage">Ipoteka</option>
              <option value="auto">Avtokredit</option>
              <option value="education">Ta'lim</option>
              <option value="business">Biznes</option>
              <option value="green_energy">Yashil energiya</option>
              <option value="computer_equipment">Kompyuter jihozi</option>
            </Select>
            <Input label="Kredit miqdori (UZS)" name="loan_amount_requested_uzs" type="number" min={500000} value={form.loan_amount_requested_uzs} onChange={e}
              hint={`${fmt(form.loan_amount_requested_uzs)} UZS`} className="col-span-2" />
            <Input label="Muddat (oy)" name="loan_term_months" type="number" min={3} max={240} value={form.loan_term_months} onChange={e} />
            <Select label="Valyuta" name="preferred_currency" value={form.preferred_currency} onChange={e}>
              <option value="uzs">UZS</option>
              <option value="usd">USD</option>
            </Select>
          </div>
          {/* Summary */}
          <div className="p-4 rounded-xl space-y-2" style={{ backgroundColor: 'var(--surface2)' }}>
            <p className="text-xs font-semibold uppercase tracking-wide" style={{ color: 'var(--text-3)' }}>Qisqacha ma'lumot</p>
            {[
              ['Oylik daromad', `${fmt(form.monthly_income_uzs)} UZS`],
              ['Joriy qarz',    `${fmt(form.existing_debt_monthly_uzs)} UZS / oy`],
              ['Kredit miqdori',`${fmt(form.loan_amount_requested_uzs)} UZS`],
              ['Muddat',        `${form.loan_term_months} oy`],
            ].map(([k, v]) => (
              <div key={k} className="flex justify-between text-sm">
                <span style={{ color: 'var(--text-2)' }}>{k}</span>
                <span className="font-medium" style={{ color: 'var(--text)' }}>{v}</span>
              </div>
            ))}
          </div>
        </>}

        {/* Navigation */}
        <div className="flex items-center justify-between pt-2 border-t" style={{ borderColor: 'var(--border)' }}>
          <Button variant="secondary" onClick={() => setStep(s => s - 1)} disabled={step === 0}>
            <ChevronLeft size={15} /> Ortga
          </Button>
          {step < STEPS.length - 1
            ? <Button onClick={() => setStep(s => s + 1)}>Keyingi <ChevronRight size={15} /></Button>
            : <Button onClick={save} disabled={loading}>{loading ? 'Saqlanmoqda...' : <><CheckCircle size={15} /> Saqlash</>}</Button>
          }
        </div>
      </Card>
    </div>
  )
}
