/* ==========================================================
   22 Arcani – pagina "Il cielo di oggi" (/cielo/)
   Descrive il cielo del momento (Luna, Sole, pianeti retrogradi, prossimi eventi)
   e le carte dei tarocchi in risonanza. Usata dal browser e da
   strumenti/genera_cielo_pagine.py (per scrivere la versione statica per Google).
   Richiede: cielo.js, momento_dati.js, sintesi_dati.js, motore_momento.js
   ========================================================== */
(function (g) {
  var GIORNI = ["domenica","lunedì","martedì","mercoledì","giovedì","venerdì","sabato"];
  var MESI = ["gennaio","febbraio","marzo","aprile","maggio","giugno","luglio","agosto","settembre","ottobre","novembre","dicembre"];
  var CARTA_PIANETA = { mercurio: "01_il_mago", luna: "02_la_papessa", venere: "03_l_imperatrice", giove: "10_la_ruota_della_fortuna",
                        marte: "16_la_torre", sole: "19_il_sole", saturno: "21_il_mondo" };
  var NOMI_EVENTI = { luna_nuova: "Luna nuova", primo_quarto: "Primo quarto di Luna", luna_piena: "Luna piena", ultimo_quarto: "Ultimo quarto di Luna",
    equinozio_primavera: "Equinozio di primavera", solstizio_estate: "Solstizio d'estate", equinozio_autunno: "Equinozio d'autunno", solstizio_inverno: "Solstizio d'inverno" };

  function esc(s) { return String(s).replace(/[&<>"]/g, function (m) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[m]; }); }
  function slug(id) { return id.replace(/^\d\d_/, "").replace(/_/g, "-"); }
  function maiusc(s) { return s.charAt(0).toUpperCase() + s.slice(1); }
  function due(n) { return (n < 10 ? "0" : "") + n; }
  function dataEstesa(d) { return GIORNI[d.getDay()] + " " + d.getDate() + " " + MESI[d.getMonth()] + " " + d.getFullYear(); }
  function cartaDelSegno(D, s) {
    for (var id in D.corrispondenze) { var c = D.corrispondenze[id]; if (c.tipo === "segno" && c.astro === s) return id; }
  }
  function cartaElemento(D, el) {
    for (var id in D.corrispondenze) { var c = D.corrispondenze[id]; if (c.tipo === "elemento" && c.astro === el) return id; }
  }

  // Prossimi eventi del cielo dopo la data indicata
  g.zodielProssimiEventi = function (data, quanti) {
    var C = g.ZODIEL_CIELO, D = g.ZODIEL_MOMENTO, p = C.inizio.split("-");
    var t0 = Date.UTC(+p[0], +p[1] - 1, +p[2]), ora = data.getTime(), out = [];
    for (var i = 0; i < C.eventi.length && out.length < quanti; i++) {
      var e = C.eventi[i], t = t0 + e[0] * 60000;
      if (t < ora) continue;
      var nome;
      if (NOMI_EVENTI[e[1]]) nome = NOMI_EVENTI[e[1]];
      else if (e[1] === "sole_ingresso") nome = "Il Sole entra in " + D.segni[e[2]];
      else if (e[1] === "stazione_retrograda") nome = D.pianeti[C.pianeti[e[2]]] + " diventa " + (C.pianeti[e[2]] === "venere" ? "retrograda" : "retrogrado");
      else if (e[1] === "stazione_diretta") nome = D.pianeti[C.pianeti[e[2]]] + (C.pianeti[e[2]] === "venere" ? " torna diretta" : " torna diretto");
      var dt = new Date(t);
      if (/luna_|quarto/.test(e[1])) {
        var c = g.zodielCielo(dt);
        if (c.disponibile) nome += " in " + D.segni[c.segnoLuna];
      }
      out.push({ data: dt, nome: nome, tipo: e[1] });
    }
    return out;
  };

  g.zodielPaginaCielo = function (data) {
    var D = g.ZODIEL_MOMENTO, A = g.ZODIEL_ARCANI, c = g.zodielCielo(data);
    if (!c.disponibile) return "<p>I dati del cielo per questa data non sono ancora disponibili.</p>";
    var segnoL = D.segni[c.segnoLuna], segnoS = D.segni[c.segnoSole];
    var faseTesto = D.fasi[c.fase][0].replace(/\{segno_luna\}/g, segnoL);
    var h = [];

    // 1. La Luna e il Sole
    h.push('<section class="cielo-blocco"><h2>🌙 La Luna oggi</h2>' +
      '<p class="cielo-grande">' + esc(maiusc(D.fasiNomi[c.fase])) + " in " + esc(segnoL) + '</p>' +
      '<p class="cielo-dettaglio">Illuminata al ' + c.illuminazione + "% · segno " + esc(D.elementoDi[D.elementoSegno[c.segnoLuna]]) + "</p>" +
      "<p>" + esc(faseTesto) + "</p></section>");
    h.push('<section class="cielo-blocco"><h2>☀️ Il Sole</h2><p class="cielo-grande">Sole in ' + esc(segnoS) + "</p>" +
      '<p>È la stagione ' + esc(D.segniDel[c.segnoSole]) + ': un buon periodo per meditare sulla sua carta, ' +
      '<a href="/arcani/' + slug(cartaDelSegno(D, c.segnoSole)) + '">' + esc(A[cartaDelSegno(D, c.segnoSole)].nome) + "</a>.</p></section>");

    // 2. Pianeti retrogradi
    var r = c.retrogradi.map(function (n) { return D.pianeti[n] + (n === "venere" ? " retrograda" : " retrogrado"); });
    h.push('<section class="cielo-blocco"><h2>🪐 Pianeti retrogradi</h2><p>' +
      (r.length ? esc(r.join(", ")) + "." : "Oggi nessun pianeta è retrogrado.") +
      (c.retrogradi.indexOf("mercurio") >= 0 ? ' <a href="/mercurio-retrogrado-2027/">Tutte le date di Mercurio retrogrado →</a>' : "") + "</p></section>");

    // 3. Le carte in risonanza con il cielo di oggi
    var carte = [], visti = {};
    function aggiungi(id, motivo, verso) { if (id && !visti[id]) { visti[id] = 1; carte.push({ id: id, motivo: motivo, verso: verso || 0 }); } }
    function verbo(id) { return A[id].genere === "p" ? "sono" : "è"; }
    var idL = cartaDelSegno(D, c.segnoLuna), idS = cartaDelSegno(D, c.segnoSole);
    if (c.fase === 0 || c.fase === 4) aggiungi("02_la_papessa", "Con la " + D.fasiNomi[c.fase] + " si accende la carta della Luna.");
    aggiungi(idL, "La Luna è in " + segnoL + ": " + A[idL].nome + " " + verbo(idL) + " la carta " + D.segniDel[c.segnoLuna] + ".");
    aggiungi(idS, "Il Sole è in " + segnoS + ": " + A[idS].nome + " " + verbo(idS) + " la carta " + D.segniDel[c.segnoSole] + ".");
    c.retrogradi.forEach(function (n) {
      if (n === "giove" || n === "saturno") return; // retrogradi per mesi: li citiamo solo sopra
      aggiungi(CARTA_PIANETA[n], D.pianeti[n] + " è " + (n === "venere" ? "retrograda" : "retrogrado") + ": " + A[CARTA_PIANETA[n]].nome + " è la sua carta, e oggi parla con la voce della carta rovesciata.", 1);
    });
    var pg = c.pianetaGiorno;
    aggiungi(CARTA_PIANETA[pg], "Oggi è " + GIORNI[c.giornoSett] + ", giorno " + D.pianetiDi[pg] + ": " + A[CARTA_PIANETA[pg]].nome + " è la sua carta.");
    var el = D.elementoSegno[c.segnoLuna];
    aggiungi(cartaElemento(D, el), "La Luna è in un segno " + D.elementoDi[el] + ", l'elemento " + (function (id) { return id ? A[id].nome.replace(/^Il /, "del ").replace(/^L'/, "dell'") : ""; })(cartaElemento(D, el)) + ".");
    h.push('<section class="cielo-blocco"><h2>🃏 Le carte in risonanza oggi</h2>' +
      "<p>Secondo le corrispondenze tradizionali tra tarocchi e astri, queste carte oggi parlano con più forza:</p>" +
      carte.map(function (x) {
        return '<article class="cielo-carta"><img src="/asset/img_web/' + x.id + '_240.webp" alt="' + esc(A[x.id].nome) + '" width="120" height="201" loading="lazy">' +
          '<div><h3><a href="/arcani/' + slug(x.id) + '">' + esc(A[x.id].nome) + "</a></h3>" +
          '<p class="cielo-motivo">' + esc(x.motivo) + "</p><p>" + esc(D.carte[x.id][x.verso]) + "</p></div></article>";
      }).join("") + "</section>");

    // 4. Prossimi eventi
    var ev = g.zodielProssimiEventi(data, 6);
    h.push('<section class="cielo-blocco"><h2>📅 I prossimi appuntamenti del cielo</h2><ul class="cielo-eventi">' +
      ev.map(function (e) {
        return "<li><strong>" + esc(e.nome) + "</strong> – " + dataEstesa(e.data) + ", ore " + due(e.data.getHours()) + ":" + due(e.data.getMinutes()) + "</li>";
      }).join("") + '</ul><p><a href="/calendario-lunare-2027/">Il calendario lunare completo del 2027 →</a></p></section>');

    return h.join("");
  };
  g.zodielDataEstesa = dataEstesa;
})(typeof window !== "undefined" ? window : globalThis);
