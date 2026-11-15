/* ==========================================================
   22 Arcani – Carta del giorno
   Stessa carta per tutti nello stesso giorno (ora italiana).
   Le 44 combinazioni (22 carte x dritta/rovesciata) seguono un ordine
   mescolato fisso: nessuna ripetizione per 44 giorni.
   Usa i dati di sintesi_dati.js.
   ========================================================== */
(function () {
  var INIZIO = Date.UTC(2026, 0, 1); // giorno 0 del ciclo

  // generatore pseudo-casuale con seme fisso (stesso ordine per tutti)
  function mulberry32(a) {
    return function () {
      a |= 0; a = a + 0x6D2B79F5 | 0;
      var t = Math.imul(a ^ a >>> 15, 1 | a);
      t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t;
      return ((t ^ t >>> 14) >>> 0) / 4294967296;
    };
  }

  function ordine() {
    var ids = Object.keys(window.ZODIEL_ARCANI || {}).sort();
    var combo = [];
    ids.forEach(function (id) { combo.push([id, true]); combo.push([id, false]); });
    var rnd = mulberry32(20261004);
    for (var i = combo.length - 1; i > 0; i--) {
      var j = Math.floor(rnd() * (i + 1));
      var t = combo[i]; combo[i] = combo[j]; combo[j] = t;
    }
    // evita la stessa carta in due giorni consecutivi (anche a cavallo del ciclo)
    for (var k = 0; k < combo.length; k++) {
      var prev = combo[(k - 1 + combo.length) % combo.length];
      if (combo[k][0] === prev[0]) {
        for (var m = 0; m < combo.length; m++) {
          var cand = combo[m], pm = combo[(m - 1 + combo.length) % combo.length], nm = combo[(m + 1) % combo.length];
          var nk = combo[(k + 1) % combo.length];
          if (m !== k && cand[0] !== prev[0] && cand[0] !== nk[0] &&
              combo[k][0] !== pm[0] && combo[k][0] !== nm[0]) {
            combo[m] = combo[k]; combo[k] = cand; break;
          }
        }
      }
    }
    return combo;
  }

  // data di oggi in Italia, come "AAAA-MM-GG"
  function oggiItalia() {
    return new Intl.DateTimeFormat("en-CA", { timeZone: "Europe/Rome" }).format(new Date());
  }

  function accorda(genere, parola) {
    var r = parola.slice(0, -1);
    return genere === "p" ? r + "i" : genere === "f" ? r + "a" : parola;
  }

  /* data facoltativa "AAAA-MM-GG" (per le prove); restituisce i dati della carta */
  window.cartaDelGiorno = function (data) {
    var d = data || oggiItalia();
    var p = d.split("-").map(Number);
    var giorno = Math.floor((Date.UTC(p[0], p[1] - 1, p[2]) - INIZIO) / 86400000);
    var lista = ordine();
    if (!lista.length) return null;
    var scelta = lista[((giorno % lista.length) + lista.length) % lista.length];
    var info = window.ZODIEL_ARCANI[scelta[0]];
    var i = scelta[1] ? 0 : 1;
    var dataLeggibile = new Date(Date.UTC(p[0], p[1] - 1, p[2], 12)).toLocaleDateString("it-IT",
      { weekday: "long", day: "numeric", month: "long", year: "numeric", timeZone: "Europe/Rome" });
    return {
      data: d,
      dataLeggibile: dataLeggibile,
      id: scelta[0],
      dritta: scelta[1],
      nome: info.nome,
      nomeCompleto: info.nome + (scelta[1] ? "" : " " + accorda(info.genere, "rovesciato")),
      parole: info.kw[i],
      messaggio: (info.giorno || [])[i] || "",
      consiglio: info.consiglio[i],
      img: "/asset/img_web/" + scelta[0] + ".webp",
      paginaArcano: "/arcani/" + scelta[0].slice(3).replace(/_/g, "-")
    };
  };
})();
