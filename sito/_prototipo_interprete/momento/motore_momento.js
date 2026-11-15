/* ==========================================================
   22 Arcani – "La lettura del momento"
   Collega le 3 carte al cielo reale (Luna, Sole, pianeti) e all'ora del giorno.
   Usa: cielo.js (genera_cielo.py), momento_dati.js, sintesi_dati.js.
   Stesse carte + stesso momento = stesso testo; momento diverso = testo diverso.
   ========================================================== */
(function (g) {
  var GIORNO = 86400000;

  // ---------- strumenti ----------
  function hash(s) { var h = 2166136261; for (var i = 0; i < s.length; i++) { h ^= s.charCodeAt(i); h = Math.imul(h, 16777619); } return h >>> 0; }
  function generatore(seme) { // mulberry32
    var a = seme;
    return function () { a |= 0; a = a + 0x6D2B79F5 | 0; var t = Math.imul(a ^ a >>> 15, 1 | a);
      t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; };
  }
  function scegli(rnd, lista) { return lista[Math.floor(rnd() * lista.length)]; }
  function maiuscola(s) { return s.charAt(0).toUpperCase() + s.slice(1); }
  function riempi(testo, v) {
    var r = testo.replace(/\{([^}]+)\}/g, function (m, k) { return v[k] !== undefined ? v[k] : m; });
    return maiuscola(r);
  }
  function minuscola(nome) { return nome.charAt(0).toLowerCase() + nome.slice(1); }
  function genitivo(nomeMin) { // "il Carro" -> "del Carro"
    return nomeMin.replace(/^il /, "del ").replace(/^la /, "della ").replace(/^l'/, "dell'")
                  .replace(/^gli /, "degli ").replace(/^lo /, "dello ").replace(/^i /, "dei ");
  }
  function dativo(nomeMin) { // "il Mago" -> "al Mago"
    return nomeMin.replace(/^il /, "al ").replace(/^la /, "alla ").replace(/^l'/, "all'")
                  .replace(/^gli /, "agli ").replace(/^lo /, "allo ").replace(/^i /, "ai ");
  }
  function fascia(ora) {
    if (ora >= 5 && ora < 8) return "alba";
    if (ora >= 8 && ora < 12) return "mattino";
    if (ora >= 12 && ora < 17) return "pomeriggio";
    if (ora >= 17 && ora < 21) return "sera";
    return "notte";
  }
  function dataLocale(d) { return d.getFullYear() + "-" + (d.getMonth() + 1) + "-" + d.getDate(); }

  // ---------- il cielo in un istante ----------
  g.zodielCielo = function (data) {
    var C = g.ZODIEL_CIELO, D = g.ZODIEL_MOMENTO;
    var ris = { fascia: fascia(data.getHours()), giornoSett: data.getDay() };
    ris.pianetaGiorno = D.pianetaGiorno[ris.giornoSett];
    if (!C) return ris;
    var p = C.inizio.split("-");
    var t0 = Date.UTC(+p[0], +p[1] - 1, +p[2]);
    var x = (data.getTime() - t0) / GIORNO, i = Math.floor(x), f = x - i;
    if (i < 0 || i >= C.giorni - 1) return ris; // fuori dal periodo calcolato
    function interp(arr) { var a = arr[i], b = arr[i + 1]; var d = ((b - a) % 360 + 360) % 360; return (a + d * f) % 360; }
    var sole = interp(C.sole), luna = interp(C.luna);
    var elong = ((luna - sole) % 360 + 360) % 360;
    ris.disponibile = true;
    ris.segnoSole = Math.floor(sole / 30);
    ris.segnoLuna = Math.floor(luna / 30);
    ris.fase = Math.round(elong / 45) % 8;
    ris.illuminazione = Math.round((1 - Math.cos(elong * Math.PI / 180)) / 2 * 100);
    ris.retrogradi = C.pianeti.filter(function (n, k) { return C.retro[i] >> k & 1; });
    // eventi nel giorno locale di chi legge
    var inizioGiorno = new Date(data.getFullYear(), data.getMonth(), data.getDate()).getTime();
    ris.eventi = C.eventi.filter(function (e) { var t = t0 + e[0] * 60000; return t >= inizioGiorno && t < inizioGiorno + GIORNO; })
      .map(function (e) { return { tipo: e[1], pianeta: e[1].indexOf("stazione") === 0 ? C.pianeti[e[2]] : null }; });
    var FASE_EVENTO = { luna_nuova: 0, primo_quarto: 2, luna_piena: 4, ultimo_quarto: 6 };
    ris.eventi.forEach(function (e) { if (FASE_EVENTO[e.tipo] !== undefined) ris.fase = FASE_EVENTO[e.tipo]; });
    return ris;
  };

  // ---------- perché una carta "risuona" con il cielo ----------
  function risonanza(id, cielo) {
    var D = g.ZODIEL_MOMENTO, c = D.corrispondenze[id];
    if (!c || !cielo.disponibile) return null;
    var cand = [];
    if (c.tipo === "segno") {
      if (cielo.segnoSole === c.astro) cand.push({ causa: "sole_nel_segno", peso: 5 });
      if (cielo.segnoLuna === c.astro) cand.push({ causa: "luna_nel_segno", peso: 4 });
    } else if (c.tipo === "pianeta") {
      if (c.astro === "luna" && (cielo.fase === 0 || cielo.fase === 4)) cand.push({ causa: "fase", peso: 5 });
      if (c.astro === "sole" && cielo.eventi.some(function (e) { return /equinozio|solstizio/.test(e.tipo); })) cand.push({ causa: "evento_sole", peso: 6 });
      if (cielo.eventi.some(function (e) { return e.pianeta === c.astro; })) cand.push({ causa: "stazione", peso: 7 });
      else if (cielo.retrogradi.indexOf(c.astro) >= 0) cand.push({ causa: "retrogrado", peso: 5 });
      if (cielo.pianetaGiorno === c.astro) cand.push({ causa: "giorno", peso: 3 });
    } else if (c.tipo === "elemento") {
      if (D.elementoSegno[cielo.segnoLuna] === c.astro) cand.push({ causa: "luna_elemento", peso: 2 });
    }
    cand.sort(function (a, b) { return b.peso - a.peso; });
    return cand[0] || null;
  }

  // ---------- la lettura ----------
  // lettura = { passato: {nome: "00_il_matto", dritta: true}, presente: {...}, futuro: {...} }
  g.creaLetturaMomento = function (lettura, data) {
    var D = g.ZODIEL_MOMENTO, A = g.ZODIEL_ARCANI || {};
    data = data || new Date();
    var cielo = g.zodielCielo(data);
    var carte = [lettura.passato, lettura.presente, lettura.futuro];
    var chiave = carte.map(function (c) { return c.nome + (c.dritta ? "+" : "-"); }).join("|") + "|" + dataLocale(data) + "|" + cielo.fascia;
    var rnd = generatore(hash(chiave));

    var v = { giorno: D.giorni[cielo.giornoSett] };
    if (cielo.disponibile) {
      v.segno_luna = D.segni[cielo.segnoLuna];
      v.segno_sole = D.segni[cielo.segnoSole];
      v.di_el = D.elementoDi[D.elementoSegno[cielo.segnoLuna]];
      v.fase_nome = D.fasiNomi[cielo.fase];
    }
    var paragrafi = [];

    // 1. Il cielo di adesso
    var p1 = [riempi(scegli(rnd, D.fasce[cielo.fascia]), v)];
    if (cielo.disponibile) {
      p1.push(riempi(scegli(rnd, D.fasi[cielo.fase]), v));
      var ev = cielo.eventi.filter(function (e) { return D.eventi[e.tipo]; })[0];
      if (ev) p1.push(riempi(scegli(rnd, D.eventi[ev.tipo]), Object.assign({}, v, { pianeta: ev.pianeta ? D.pianeti[ev.pianeta] : "" })));
    }
    paragrafi.push(p1.join(" "));

    // 2. Le carte in risonanza con il cielo (al massimo 2)
    var ris = [];
    carte.forEach(function (c, k) { var r = risonanza(c.nome, cielo); if (r) ris.push({ carta: c, r: r, ordine: k }); });
    ris.sort(function (a, b) { return b.r.peso - a.r.peso || a.ordine - b.ordine; });
    ris = ris.slice(0, 2);
    var pianetiCitati = {};
    var p2 = ris.map(function (x) {
      var id = x.carta.nome, corr = D.corrispondenze[id], a = A[id] || { nome: id, genere: "m" };
      var nomeMin = minuscola(a.nome), pl = a.genere === "p";
      var legame = "la carta " + (corr.tipo === "segno" ? D.segniDel[corr.astro] :
                    corr.tipo === "pianeta" ? D.pianetiDi[corr.astro] : "dell'elemento " + corr.astro);
      if (corr.tipo === "pianeta") pianetiCitati[corr.astro] = 1;
      var w = Object.assign({}, v, {
        Carta: a.nome, carta: nomeMin, legame: legame, "è": pl ? "sono" : "è", sia: pl ? "siano" : "sia",
        rappresenta: pl ? "rappresentano" : "rappresenta", o: a.genere === "f" ? "a" : pl ? "i" : "o",
        di_carta: genitivo(nomeMin), a_carta: dativo(nomeMin),
        segno_carta: corr.tipo === "segno" ? D.segni[corr.astro] : "",
        segno_carta_art: corr.tipo === "segno" ? D.segniArt[corr.astro] : "",
        pianeta: corr.tipo === "pianeta" ? D.pianeti[corr.astro] : "",
        retrogrado: corr.astro === "venere" ? "retrograda" : "retrogrado",
        pianeta_a: D.pianetiA[cielo.pianetaGiorno], pianeta_di: D.pianetiDi[cielo.pianetaGiorno]
      });
      return riempi(scegli(rnd, D.cause[x.r.causa]), w) + " " + D.carte[id][x.carta.dritta ? 0 : 1];
    });
    // un pianeta retrogrado "importante" non già citato
    if (cielo.disponibile) {
      var stazioneOggi = cielo.eventi.some(function (e) { return e.pianeta; });
      var retro = ["mercurio", "venere", "marte"].filter(function (n) { return cielo.retrogradi.indexOf(n) >= 0 && !pianetiCitati[n]; })[0];
      if (retro && !stazioneOggi) p2.push(scegli(rnd, D.retrogradi[retro]));
    }
    if (p2.length) paragrafi.push(p2.join(" "));

    // 3. Gli elementi della stesa
    var conta = {};
    carte.forEach(function (c) { var e = (D.corrispondenze[c.nome] || {}).elemento; if (e) conta[e] = (conta[e] || 0) + 1; });
    var dom = Object.keys(conta).filter(function (e) { return conta[e] >= 2; })[0];
    var p3 = dom ? (conta[dom] === 3 ? scegli(rnd, D.elementi.tutte[dom]) : scegli(rnd, D.elementi.prevale[dom])) : scegli(rnd, D.elementi.diverse);
    if (dom && cielo.disponibile && D.elementoSegno[cielo.segnoLuna] === dom) p3 += " " + riempi(scegli(rnd, D.elementi.rinforzo), v);
    paragrafi.push(p3);

    // 4. Chiusura: il giorno e una domanda
    paragrafi.push(scegli(rnd, D.chiusureGiorno[cielo.pianetaGiorno]) + " " + scegli(rnd, D.domande));

    // Scheda del cielo (riga breve da mostrare sopra la lettura)
    var mesi = ["gennaio","febbraio","marzo","aprile","maggio","giugno","luglio","agosto","settembre","ottobre","novembre","dicembre"];
    var scheda = [maiuscola(D.giorni[cielo.giornoSett]) + " " + data.getDate() + " " + mesi[data.getMonth()] + ", " + D.fasceNomi[cielo.fascia]];
    if (cielo.disponibile) {
      scheda.push(maiuscola(D.fasiNomi[cielo.fase]) + " in " + D.segni[cielo.segnoLuna]);
      scheda.push("Sole in " + D.segni[cielo.segnoSole]);
      if (cielo.retrogradi.length) {
        var nomi = cielo.retrogradi.map(function (n) { return D.pianeti[n]; });
        scheda.push((nomi.length > 1 ? nomi.slice(0, -1).join(", ") + " e " + nomi[nomi.length - 1] + " retrogradi" : nomi[0] + " retrogrado"));
      }
    }
    return { titolo: "La lettura del momento", scheda: scheda.join(" · "), paragrafi: paragrafi,
             risonanze: ris.map(function (x) { return x.carta.nome + ": " + x.r.causa; }), cielo: cielo, avvertenza: D.avvertenza };
  };
})(typeof window !== "undefined" ? window : globalThis);
