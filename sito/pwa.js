/* ==========================================================
   22 Arcani – App installabile (PWA)
   - registra il service worker
   - sul telefono mostra il pulsante "Installa 22 Arcani"
     · Android/Chrome: installazione con un tocco
     · iPhone/iPad: riquadro con i 3 passaggi
   - non disturba: compare dopo qualche secondo, mai sopra il banner
     dei cookie, e se chiuso non si rivede per 14 giorni
   ========================================================== */
(function () {
  var CHIAVE_NO = "zodiel_pwa_chiuso";
  var GIORNI_PAUSA = 14;

  function traccia(nome, p) { try { if (window.traccia) window.traccia(nome, p || {}); } catch (e) {} }

  // 1) service worker
  if ("serviceWorker" in navigator) {
    window.addEventListener("load", function () {
      navigator.serviceWorker.register("/sw.js").catch(function () {});
    });
  }

  var installata = window.matchMedia("(display-mode: standalone)").matches || window.navigator.standalone === true;
  if (installata) {
    try {
      if (!sessionStorage.getItem("zodiel_pwa_sessione")) {
        sessionStorage.setItem("zodiel_pwa_sessione", "1");
        traccia("pwa_aperta");
      }
    } catch (e) {}
    return; // già app: niente pulsante
  }

  var ua = navigator.userAgent || "";
  var iOS = /iphone|ipad|ipod/i.test(ua) || (navigator.platform === "MacIntel" && navigator.maxTouchPoints > 1);
  var telefono = window.matchMedia("(pointer: coarse)").matches && Math.min(screen.width, screen.height) < 900;
  if (!telefono) return;

  function inPausa() {
    try {
      var t = parseInt(localStorage.getItem(CHIAVE_NO) || "0", 10);
      return t && (Date.now() - t) < GIORNI_PAUSA * 864e5;
    } catch (e) { return false; }
  }
  if (inPausa()) return;

  var promptAndroid = null;
  var pulsante = null;

  function stile() {
    if (document.getElementById("pwa-stile")) return;
    var s = document.createElement("style");
    s.id = "pwa-stile";
    s.textContent =
      "#pwa-pulsante{position:fixed;left:50%;bottom:16px;transform:translateX(-50%);z-index:9998;display:flex;align-items:center;" +
      "gap:6px;background:#111;border:1.5px solid #40E0D0;border-radius:24px;padding:4px 4px 4px 16px;box-shadow:0 4px 18px rgba(0,0,0,.6);" +
      "font-family:'Playfair Display',Georgia,serif;animation:pwaEntra .5s ease-out}" +
      "#pwa-pulsante .pwa-installa{background:none;border:0;color:#40E0D0;font-size:16px;font-weight:bold;padding:8px 4px;cursor:pointer;font-family:inherit;white-space:nowrap}" +
      "#pwa-pulsante .pwa-x{background:none;border:0;color:#888;font-size:20px;line-height:1;padding:8px 12px;cursor:pointer}" +
      "@keyframes pwaEntra{from{opacity:0;transform:translate(-50%,20px)}to{opacity:1;transform:translate(-50%,0)}}" +
      "#pwa-ios{position:fixed;inset:0;z-index:10000;background:rgba(0,0,0,.75);display:flex;align-items:flex-end;justify-content:center}" +
      "#pwa-ios .pwa-box{background:#151515;border:1.5px solid #40E0D0;border-radius:18px 18px 0 0;padding:22px 22px 28px;max-width:420px;width:100%;" +
      "color:#e8e8e8;font-family:'Playfair Display',Georgia,serif;box-sizing:border-box;text-align:left}" +
      "#pwa-ios h3{color:#40E0D0;margin:0 0 16px;font-size:22px;text-align:center}" +
      "#pwa-ios ol{margin:0 0 20px;padding-left:24px;font-size:18px;line-height:1.6;text-align:left}" +
      "#pwa-ios li{margin-bottom:8px;text-align:left}" +
      "#pwa-ios .pwa-ico{display:inline-block;border:1px solid #40E0D0;border-radius:6px;padding:0 6px;color:#40E0D0;font-weight:bold}" +
      "#pwa-ios button{display:block;margin:0 auto;background:#40E0D0;color:#000;border:0;border-radius:16px;padding:10px 30px;font-size:16px;font-weight:bold}";
    document.head.appendChild(s);
  }

  function chiudi(ricorda) {
    if (pulsante) { pulsante.remove(); pulsante = null; }
    if (ricorda) { try { localStorage.setItem(CHIAVE_NO, String(Date.now())); } catch (e) {} }
  }

  function mostraIstruzioniIOS() {
    stile();
    var d = document.createElement("div");
    d.id = "pwa-ios";
    d.innerHTML =
      '<div class="pwa-box"><h3>Installa 22 Arcani sul tuo iPhone</h3><ol>' +
      '<li>Tocca <span class="pwa-ico">Condividi ⇪</span> (il quadrato con la freccia in su, in basso o in alto nello schermo)</li>' +
      '<li>Scorri e tocca <b>Aggiungi alla schermata Home</b></li>' +
      '<li>Tocca <b>Aggiungi</b></li></ol>' +
      '<button type="button">Ho capito</button></div>';
    d.addEventListener("click", function (e) { if (e.target === d || e.target.tagName === "BUTTON") d.remove(); });
    document.body.appendChild(d);
    traccia("pwa_istruzioni_ios");
  }

  function mostraPulsante() {
    if (pulsante || inPausa()) return;
    stile();
    pulsante = document.createElement("div");
    pulsante.id = "pwa-pulsante";
    pulsante.innerHTML = '<button type="button" class="pwa-installa">📲 Installa 22 Arcani</button>' +
                         '<button type="button" class="pwa-x" aria-label="Chiudi">×</button>';
    pulsante.querySelector(".pwa-x").addEventListener("click", function () { chiudi(true); traccia("pwa_pulsante_chiuso"); });
    pulsante.querySelector(".pwa-installa").addEventListener("click", function () {
      traccia("pwa_pulsante_toccato", { sistema: iOS ? "ios" : "android" });
      if (promptAndroid) {
        promptAndroid.prompt();
        promptAndroid.userChoice.then(function (r) {
          traccia("pwa_scelta", { esito: r.outcome });
          promptAndroid = null;
          chiudi(r.outcome !== "accepted");
        });
      } else if (iOS) {
        mostraIstruzioniIOS();
      }
    });
    document.body.appendChild(pulsante);
    traccia("pwa_pulsante_visto");
  }

  // aspetta qualche secondo e che non ci sia il banner dei cookie
  function quandoLibero(fn) {
    var tentativi = 0;
    (function prova() {
      if (!document.getElementById("banner-cookie")) return fn();
      if (++tentativi < 90) setTimeout(prova, 2000);
    })();
  }

  window.addEventListener("beforeinstallprompt", function (e) {
    e.preventDefault();
    promptAndroid = e;
    setTimeout(function () { quandoLibero(mostraPulsante); }, 5000);
  });

  window.addEventListener("appinstalled", function () {
    traccia("pwa_installata");
    chiudi(false);
  });

  if (iOS) {
    window.addEventListener("load", function () {
      setTimeout(function () { quandoLibero(mostraPulsante); }, 5000);
    });
  }
})();
