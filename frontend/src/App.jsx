import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { useTheme } from './hooks/useTheme'
import { useAuth } from './hooks/useAuth'
import Navbar from './components/layout/Navbar'

import Login        from './pages/Login'
import Register     from './pages/Register'
import Dashboard    from './pages/Dashboard'
import Profil       from './pages/Profil'
import Kredit       from './pages/Kredit'
import Simulyatsiya from './pages/Simulyatsiya'
import Depozit      from './pages/Depozit'
import Admin        from './pages/Admin'

function PrivateRoute({ children, adminOnly = false, user }) {
  if (!user) return <Navigate to="/login" replace />
  if (adminOnly && !user.is_admin) return <Navigate to="/dashboard" replace />
  return children
}

function AuthLayout({ user, logout, dark, toggleTheme, children }) {
  return (
    <div className="min-h-screen" style={{ backgroundColor: 'var(--bg)' }}>
      <Navbar user={user} onLogout={logout} dark={dark} onThemeToggle={toggleTheme} />
      <main>{children}</main>
    </div>
  )
}

export default function App() {
  const { dark, toggle } = useTheme()
  const { user, login, register, logout } = useAuth()

  return (
    <BrowserRouter>
      <Routes>
        {/* Public routes */}
        <Route path="/login"    element={user ? <Navigate to="/dashboard" replace /> : <Login    onLogin={login} />} />
        <Route path="/register" element={user ? <Navigate to="/dashboard" replace /> : <Register onRegister={register} />} />

        {/* Protected routes */}
        <Route path="/dashboard" element={
          <PrivateRoute user={user}>
            <AuthLayout user={user} logout={logout} dark={dark} toggleTheme={toggle}>
              <Dashboard user={user} />
            </AuthLayout>
          </PrivateRoute>
        } />
        <Route path="/profil" element={
          <PrivateRoute user={user}>
            <AuthLayout user={user} logout={logout} dark={dark} toggleTheme={toggle}>
              <Profil />
            </AuthLayout>
          </PrivateRoute>
        } />
        <Route path="/kredit" element={
          <PrivateRoute user={user}>
            <AuthLayout user={user} logout={logout} dark={dark} toggleTheme={toggle}>
              <Kredit />
            </AuthLayout>
          </PrivateRoute>
        } />
        <Route path="/simulyatsiya" element={
          <PrivateRoute user={user}>
            <AuthLayout user={user} logout={logout} dark={dark} toggleTheme={toggle}>
              <Simulyatsiya />
            </AuthLayout>
          </PrivateRoute>
        } />
        <Route path="/depozit" element={
          <PrivateRoute user={user}>
            <AuthLayout user={user} logout={logout} dark={dark} toggleTheme={toggle}>
              <Depozit />
            </AuthLayout>
          </PrivateRoute>
        } />
        <Route path="/admin" element={
          <PrivateRoute user={user} adminOnly>
            <AuthLayout user={user} logout={logout} dark={dark} toggleTheme={toggle}>
              <Admin />
            </AuthLayout>
          </PrivateRoute>
        } />

        {/* Fallback */}
        <Route path="*" element={<Navigate to={user ? "/dashboard" : "/login"} replace />} />
      </Routes>
    </BrowserRouter>
  )
}
