/* ==========================================================
   Zodiel – Sintesi finale della lettura
   Collega le tre carte (passato, presente, futuro) in un breve testo.
   Usa i dati di sintesi_dati.js (generato da strumenti/genera_arcani.py).
   ========================================================== */
(function () {
  function nomeInFrase(nome) {
    // "Il Matto" -> "il Matto", "L'Eremita" -> "l'Eremita"
    return nome.charAt(0).toLowerCase() + nome.slice(1);
  }
  function accorda(genere, parola) {
    var radice = parola.slice(0, -1);
    if (genere === "p") return radice + "i";
    if (genere === "f") return radice + "a";
    return parola;
  }
  function elenco(parole) {
    var p = parole.slice(0, 3);
    if (p.length === 1) return p[0];
    return p.slice(0, -1).join(", ") + " e " + p[p.length - 1];
  }
  function verbo(genere, singolare, plurale) {
    return genere === "p" ? plurale : singolare;
  }

  function info(carta) {
    var d = (window.ZODIEL_ARCANI || {})[carta.nome];
    if (!d) return null;
    var i = carta.dritta ? 0 : 1;
    return {
      nome: d.nome,
      genere: d.genere,
      dritta: carta.dritta,
      etichetta: nomeInFrase(d.nome) + (carta.dritta ? "" : " " + accorda(d.genere, "rovesciato")),
      kw: d.kw[i],
      consiglio: d.consiglio[i],
      id: carta.nome
    };
  }

  /* Restituisce { titolo, paragrafi: [stringhe HTML] } oppure null */
  window.creaSintesi = function (lettura) {
    if (!lettura || !window.ZODIEL_ARCANI) return null;
    var pa = info(lettura.passato), pr = info(lettura.presente), fu = info(lettura.futuro);
    if (!pa || !pr || !fu) return null;
    var par = [];

    // 1. Il racconto delle tre carte
    par.push(
      "Nel <strong>passato</strong>, " + pa.etichetta + " " + verbo(pa.genere, "parla", "parlano") + " di " + elenco(pa.kw) + ". " +
      "Nel <strong>presente</strong>, " + pr.etichetta + " " + verbo(pr.genere, "indica", "indicano") + " " + elenco(pr.kw) + ". " +
      "Nel <strong>futuro</strong>, " + fu.etichetta + " " + verbo(fu.genere, "annuncia", "annunciano") + " " + elenco(fu.kw) + "."
    );

    // 2. Il tono generale, dalle carte rovesciate
    var rov = [pa, pr, fu].filter(function (c) { return !c.dritta; });
    var tono;
    if (rov.length === 0) {
      tono = "Tutte e tre le carte sono dritte: le energie della tua lettura scorrono in armonia e il momento è favorevole per agire.";
    } else if (rov.length === 1) {
      tono = "Una sola carta è rovesciata, " + rov[0].etichetta + ": è il punto della tua storia a cui dedicare più attenzione.";
    } else if (rov.length === 2) {
      tono = "Due carte su tre sono rovesciate: la lettura ti invita a rallentare e a sciogliere qualche nodo prima di andare avanti.";
    } else {
      tono = "Tutte e tre le carte sono rovesciate: è il momento di fermarti, riflettere e ritrovare il tuo centro prima di prendere decisioni.";
    }
    par.push(tono);

    // 3. Il filo che unisce passato e futuro
    par.push("Il filo che lega le tue carte va da <em>" + pa.kw[0] + "</em> a <em>" + fu.kw[0] +
             "</em>: è il percorso che la lettura ti invita a compiere.");

    // 4. Rassicurazione per le carte più temute nel futuro
    var temute = { "13_la_morte": 1, "16_la_torre": 1, "15_il_diavolo": 1 };
    if (temute[fu.id]) {
      par.push(fu.nome + " nel futuro non va temut" + (fu.genere === "f" ? "a" : "o") +
               ": parla di una trasformazione, non di una sventura.");
    }

    // 5. I consigli
    par.push("<strong>Il consiglio per oggi:</strong> " + pr.consiglio + ".");
    par.push("<strong>Guardando avanti:</strong> " + fu.consiglio + ".");

    return { titolo: "La tua lettura in sintesi", paragrafi: par };
  };
})();
