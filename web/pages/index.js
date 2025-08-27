import { useState } from 'react'
import { useRouter } from 'next/router'

export default function Home() {
  const [url, setUrl] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [agree, setAgree] = useState(false)
  const router = useRouter()

  const submit = async (e) => {
    e.preventDefault()
    if (!agree) return
    const res = await fetch('/api/jobs', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ url, email, password })
    })
    const data = await res.json()
    router.push(`/job/${data.jobId}`)
  }

  return (
    <form onSubmit={submit}>
      <input placeholder="Substack URL" value={url} onChange={e => setUrl(e.target.value)} />
      <input placeholder="Email" value={email} onChange={e => setEmail(e.target.value)} />
      <input placeholder="Password" type="password" value={password} onChange={e => setPassword(e.target.value)} />
      <label>
        <input type="checkbox" checked={agree} onChange={e => setAgree(e.target.checked)} /> I confirm I have rights
      </label>
      <button type="submit">Submit</button>
    </form>
  )
}
