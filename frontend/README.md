# SarfAI Frontend V2

React + Vite + Tailwind — Uzbek-language fintech UI.

## Quick Start

```bash
cd frontend
npm install
cp .env.example .env     # optional — defaults to /api proxy
npm run dev              # http://localhost:5173
```

## Environment

```
VITE_API_URL=/api        # proxied to http://localhost:8000 via vite.config.js
```

For production pointing directly at the backend:
```
VITE_API_URL=https://your-api-domain.com
```

## Pages

| Route | Page | Auth |
|---|---|---|
| `/login` | Login | Public |
| `/register` | Register | Public |
| `/dashboard` | Overview + quick actions | ✅ |
| `/profil` | 4-step financial profile form | ✅ |
| `/kredit` | ML prediction + bank results | ✅ |
| `/simulyatsiya` | Cashflow simulation + chart | ✅ |
| `/depozit` | Deposit advisor | ✅ |
| `/admin` | Admin panel (stats/trends/users/banks) | ✅ Admin only |

## Features

- 🌙 Day/Night mode — persisted in `localStorage`, respects OS preference on first load
- 📱 Fully responsive — mobile-first, single column → sidebar on desktop
- 🔒 Auth guard — unauthenticated users redirected to `/login`
- 🔑 Admin guard — non-admins redirected from `/admin`
- ⚡ Auto token injection via Axios interceptor
- 🔄 Auto logout on 401
