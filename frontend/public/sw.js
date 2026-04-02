const CACHE = 'briefnote-v1'

self.addEventListener('install', () => {
  self.skipWaiting()
})

self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k)))
    )
  )
  self.clients.claim()
})

self.addEventListener('fetch', event => {
  if (event.request.method !== 'GET') return
  event.respondWith(
    caches.match(event.request).then(cached => {
      const fetched = fetch(event.request).then(resp => {
        if (resp && resp.status === 200) {
          const clone = resp.clone()
          caches.open(CACHE).then(cache => cache.put(event.request, clone))
        }
        return resp
      }).catch(() => cached)
      return cached || fetched
    })
  )
})
