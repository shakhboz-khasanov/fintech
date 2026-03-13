import { useState, useEffect } from 'react'

export function useTheme() {
  const [dark, setDark] = useState(() =>
    document.documentElement.classList.contains('dark')
  )

  useEffect(() => {
    if (dark) {
      document.documentElement.classList.add('dark')
      localStorage.setItem('sarfai-theme', 'dark')
    } else {
      document.documentElement.classList.remove('dark')
      localStorage.setItem('sarfai-theme', 'light')
    }
  }, [dark])

  return { dark, toggle: () => setDark(d => !d) }
}
