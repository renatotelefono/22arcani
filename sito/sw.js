/* ==========================================================
   22 Arcani – Service worker (PWA)
   Le pagine vengono SEMPRE prese dal sito (nessun contenuto vecchio).
   Se manca la connessione, mostra offline.html.
   I video e le immagini non vengono salvati sul telefono.
   ========================================================== */
var VERSIONE = "zodiel-v1";
var DA_SALVARE = ["/offline.html", "/icon-192.png", "/favicon.svg"];

self.addEventListener("install", function (e) {
  e.waitUntil(caches.open(VERSIONE).then(function (c) { return c.addAll(DA_SALVARE); }));
  self.skipWaiting();
});

self.addEventListener("activate", function (e) {
  e.waitUntil(
    caches.keys().then(function (nomi) {
      return Promise.all(nomi.filter(function (n) { return n !== VERSIONE; })
                             .map(function (n) { return caches.delete(n); }));
    }).then(function () { return self.clients.claim(); })
  );
});

self.addEventListener("fetch", function (e) {
  if (e.request.mode !== "navigate") return; // tutto il resto: normale, dal sito
  e.respondWith(
    fetch(e.request).catch(function () { return caches.match("/offline.html"); })
  );
});
