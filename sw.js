// Service Worker — Hallel PWA
// Mantém o app instalável e funcionando offline. Os dados continuam
// 100% locais no aparelho (localStorage / IndexedDB) — nada é enviado.

const CACHE = 'hallel-v5';
const CORE = [
  './',
  './index.html',
  './logo.png',
  './manifest.json',
  './icon-192.png',
  './icon-512.png',
  './icon-maskable-512.png',
  './apple-touch-icon.png'
];

self.addEventListener('install', e => {
  e.waitUntil(
    caches.open(CACHE).then(c => c.addAll(CORE)).then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys()
      .then(keys => Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

// Clique numa notificação → foca/abre o app
self.addEventListener('notificationclick', e => {
  e.notification.close();
  e.waitUntil(
    clients.matchAll({ type: 'window', includeUncontrolled: true }).then(list => {
      for (const c of list) { if ('focus' in c) return c.focus(); }
      if (clients.openWindow) return clients.openWindow('./');
    })
  );
});

self.addEventListener('fetch', e => {
  const req = e.request;
  if (req.method !== 'GET') return;

  const url = new URL(req.url);
  // Terceiros (CDN, YouTube, Spotify, Deezer…) passam direto pela rede
  if (url.origin !== self.location.origin) return;

  // Mídia pesada (stems do mixer, áudio, vídeo, PDF grande) NÃO entra no cache —
  // passa direto pela rede pra manter o app instalado leve
  if (/\.(mp3|wav|m4a|ogg|aac|mp4|webm|mov)$/i.test(url.pathname)) return;

  // HTML / navegação → network-first: sempre pega a versão mais nova quando online,
  // e cai pro cache quando offline (assim suas atualizações chegam automaticamente)
  if (req.mode === 'navigate' || url.pathname.endsWith('/') || url.pathname.endsWith('index.html')) {
    e.respondWith(
      fetch(req)
        .then(res => {
          const copy = res.clone();
          caches.open(CACHE).then(c => c.put(req, copy));
          return res;
        })
        .catch(() => caches.match(req).then(r => r || caches.match('./index.html')))
    );
    return;
  }

  // Estáticos do próprio app → cache-first
  e.respondWith(
    caches.match(req).then(cached => cached || fetch(req).then(res => {
      const copy = res.clone();
      caches.open(CACHE).then(c => c.put(req, copy));
      return res;
    }))
  );
});
