import { useState, useCallback } from 'react'
import api from '../api/client'

const TOKEN_KEY = 'sarfai-token'
const USER_KEY  = 'sarfai-user'

export function useAuth() {
  const [user, setUser] = useState(() => {
    try { return JSON.parse(localStorage.getItem(USER_KEY)) } catch { return null }
  })

  const login = useCallback(async (username, password) => {
    const { data } = await api.post('/auth/login', { username, password })
    localStorage.setItem(TOKEN_KEY, data.token)
    localStorage.setItem(USER_KEY, JSON.stringify({ username: data.username, is_admin: data.is_admin }))
    setUser({ username: data.username, is_admin: data.is_admin })
    return data
  }, [])

  const register = useCallback(async (username, password) => {
    const { data } = await api.post('/auth/register', { username, password })
    localStorage.setItem(TOKEN_KEY, data.token)
    localStorage.setItem(USER_KEY, JSON.stringify({ username: data.username, is_admin: data.is_admin }))
    setUser({ username: data.username, is_admin: data.is_admin })
    return data
  }, [])

  const logout = useCallback(() => {
    localStorage.removeItem(TOKEN_KEY)
    localStorage.removeItem(USER_KEY)
    setUser(null)
  }, [])

  return { user, login, register, logout, isAdmin: user?.is_admin === true }
}

export function getToken() {
  return localStorage.getItem(TOKEN_KEY)
}
