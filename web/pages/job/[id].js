import { useEffect, useState } from 'react'
import { useRouter } from 'next/router'

export default function JobPage() {
  const router = useRouter()
  const { id } = router.query
  const [status, setStatus] = useState(null)

  useEffect(() => {
    if (!id) return
    const timer = setInterval(async () => {
      const res = await fetch(`/api/jobs/${id}/status`)
      if (res.ok) {
        const data = await res.json()
        setStatus(data)
        if (data.hasDownload) clearInterval(timer)
      }
    }, 1000)
    return () => clearInterval(timer)
  }, [id])

  if (!status) return <p>Loading...</p>
  return (
    <div>
      <p>State: {status.state}</p>
      {status.hasDownload && <a href={`/api/jobs/${id}/download`}>Download ZIP</a>}
    </div>
  )
}
