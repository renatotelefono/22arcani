# Zodiel – pagina "Tarocchi sì o no" (zodiel.cloud/si-o-no/).
# Uso: python3 strumenti/genera_si_no.py
import os, re, json, html
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
a = open(os.path.join(BASE, "sintesi_dati.js"), encoding="utf-8").read()
A = json.loads(a[a.index("{"):a.rindex("}") + 1])
# risposta tradizionale: (dritta, rovesciata)
R = {"00_il_matto": ("si", "no"), "01_il_mago": ("si", "no"), "02_la_papessa": ("forse", "no"),
     "03_l_imperatrice": ("si", "forse"), "04_l_imperatore": ("si", "no"), "05_il_papa": ("si", "no"),
     "06_gli_amanti": ("si", "no"), "07_il_carro": ("si", "no"), "08_la_forza": ("si", "forse"),
     "09_l_eremita": ("forse", "no"), "10_la_ruota_della_fortuna": ("si", "no"), "11_la_giustizia": ("si", "no"),
     "12_l_appeso": ("forse", "no"), "13_la_morte": ("no", "forse"), "14_la_temperanza": ("si", "forse"),
     "15_il_diavolo": ("no", "forse"), "16_la_torre": ("no", "no"), "17_la_stella": ("si", "forse"),
     "18_la_luna": ("forse", "no"), "19_il_sole": ("si", "si"), "20_il_giudizio": ("si", "no"), "21_il_mondo": ("si", "forse")}
ETI = {"si": "SÌ", "no": "NO", "forse": "FORSE"}
SPIEGA = {"si": "La carta è favorevole: l'energia va nella direzione che speri.",
          "no": "La carta invita alla prudenza: per ora la strada non è aperta.",
          "forse": "La risposta non è ancora definita: dipende da come ti muoverai."}
def rov(g): return {"p": "rovesciati", "f": "rovesciata"}.get(g, "rovesciato")
def slug(fid): return re.sub(r"^\d\d_", "", fid).replace("_", "-")
ids = sorted(A)
dati = {i: {"n": A[i]["nome"], "g": A[i]["genere"], "kw": [A[i]["kw"][0][:3], A[i]["kw"][1][:3]],
            "c": A[i]["consiglio"], "r": list(R[i]), "s": slug(i)} for i in ids}
righe = "\n".join(f'<tr><td><a href="/arcani/{slug(i)}">{html.escape(A[i]["nome"])}</a></td><td class="r-{R[i][0]}">{ETI[R[i][0]]}</td><td class="r-{R[i][1]}">{ETI[R[i][1]]}</td></tr>' for i in ids)
faq = [("Come funzionano i tarocchi sì o no?", "Scegli un argomento (amore, lavoro, soldi e fortuna, benessere, famiglia o crescita personale) e una delle domande proposte, poi concentrati e pesca una carta. Ogni Arcano Maggiore ha una risposta tradizionale, che cambia se la carta esce dritta o rovesciata: sì, no oppure forse."),
       ("I tarocchi sì o no sono gratis?", "Sì, su Zodiel la lettura sì o no è completamente gratuita e senza registrazione. Puoi fare tutte le domande che vuoi."),
       ("Quali carte dicono sì?", "Le carte più favorevoli sono il Sole, la Stella, il Mondo, il Mago, il Carro e la Ruota della Fortuna. Il Sole dice sì anche quando esce rovesciato."),
       ("Quali carte dicono no?", "La Torre dice no sia dritta sia rovesciata. Anche la Morte e il Diavolo dritti, e la maggior parte delle carte rovesciate, invitano ad aspettare."),
       ("Posso fare la stessa domanda più volte?", "Meglio di no: la prima risposta è quella che conta. Se la risposta è forse, prova a riformulare la domanda o fai una lettura completa a tre carte.")]
ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": r}} for q, r in faq]}
faqhtml = "\n".join(f"      <h3>{q}</h3>\n      <p>{r}</p>" for q, r in faq)


SEZIONI = [
 ("amore", "❤️ Amore", ["Questa persona prova qualcosa per me?", "La persona che amo tornerà da me?", "La nostra relazione durerà?", "Incontrerò presto una persona speciale?", "Devo fare io il primo passo?", "Chi ho amato pensa ancora a me?", "È la persona giusta per me?", "Dovrei dare un'altra possibilità a questa storia?"]),
 ("lavoro", "💼 Lavoro", ["Troverò presto un nuovo lavoro?", "È il momento giusto per cambiare lavoro?", "Otterrò la promozione che desidero?", "Il colloquio andrà bene?", "Devo accettare questa proposta di lavoro?", "Il mio progetto avrà successo?", "È il momento giusto per mettermi in proprio?", "Supererò l'esame o il concorso?"]),
 ("fortuna", "🍀 Soldi e fortuna", ["La mia situazione economica migliorerà presto?", "È il momento giusto per un investimento importante?", "Riceverò una buona notizia a breve?", "La fortuna è dalla mia parte in questo periodo?", "Riuscirò a risparmiare per ciò che desidero?", "Questo acquisto importante è una buona idea?", "Arriverà presto un'entrata inaspettata?", "Comprerò casa nei prossimi mesi?"]),
 ("benessere", "🌿 Salute e benessere", ["Ritroverò presto energia e vitalità?", "Riuscirò a cambiare un'abitudine che non mi fa bene?", "È il momento giusto per prendermi una pausa?", "Ritroverò la serenità interiore?", "Riuscirò a raggiungere il mio obiettivo di benessere?", "Questo periodo di stanchezza finirà presto?", "Riuscirò a dormire e a riposare meglio?", "È il momento di dedicare più tempo a me?"]),
 ("famiglia", "🏡 Famiglia e amicizie", ["Ritroverò l'armonia in famiglia?", "Riuscirò a chiarire con questa persona?", "Questa amicizia è sincera?", "È il momento giusto per un trasferimento?", "Devo perdonare questa persona?", "Riceverò l'aiuto di cui ho bisogno?", "Questa situazione in famiglia si risolverà?", "Farò nuove amicizie importanti?"]),
 ("io", "✨ Crescita personale", ["Sono sulla strada giusta?", "È il momento di prendere una decisione importante?", "Riuscirò a realizzare il mio sogno?", "Devo seguire il mio istinto in questa situazione?", "È il momento di lasciarmi il passato alle spalle?", "Un viaggio mi farà bene in questo periodo?", "Riuscirò a superare questa paura?", "Questo cambiamento sarà positivo per me?"]),
]

ELENCO = "".join("      <h3>%s</h3>\n      <ul class=\"elenco-dom\">%s</ul>\n" % (t, "".join("<li>%s</li>" % html.escape(q) for q in qs)) for k, t, qs in SEZIONI)
BOTTONI = "".join('<button type="button" data-s="%s">%s</button>' % (k, t) for k, t, _ in SEZIONI)
DOMJSON = json.dumps({k: qs for k, t, qs in SEZIONI}, ensure_ascii=False)
pagina = f'''<!DOCTYPE html>
<html lang="it">
<head>
  <meta charset="UTF-8">
  <link rel="icon" href="/favicon.svg" type="image/svg+xml">
  <link rel="icon" href="/favicon-48.png" sizes="48x48" type="image/png">
  <link rel="apple-touch-icon" href="/apple-touch-icon.png">
  <link rel="manifest" href="/manifest.webmanifest">
  <meta name="theme-color" content="#111111">
  <script src="/pwa.js" defer></script>
  <script src="/analytics.js"></script>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Tarocchi Sì o No Gratis: fai la tua domanda e pesca una carta | Zodiel</title>
  <meta name="description" content="Tarocchi sì o no gratis su amore, lavoro, fortuna e benessere: scegli la tua domanda, pesca una carta tra i 22 Arcani Maggiori e scopri subito se la risposta è sì, no o forse. Senza registrazione.">
  <link rel="canonical" href="https://zodiel.cloud/si-o-no/">
  <meta property="og:type" content="website">
  <meta property="og:title" content="Tarocchi Sì o No Gratis | Zodiel">
  <meta property="og:description" content="Fai una domanda e pesca una carta: sì, no o forse?">
  <meta property="og:url" content="https://zodiel.cloud/si-o-no/">
  <meta property="og:image" content="https://zodiel.cloud/asset/img_it/19_il_sole.jpeg">
  <link href="https://fonts.googleapis.com/css2?family=Cinzel+Decorative:wght@400;700&family=Playfair+Display:wght@400;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/arcani/arcani.css">
  <style>
    .sino h1 {{ margin-bottom: 8px; }}
    .gioco {{ text-align: center; margin: 24px 0 36px; padding: 24px 12px; border-radius: 16px; background: rgba(63,224,208,.06); }}
    .gioco textarea {{ width: 100%; max-width: 520px; box-sizing: border-box; min-height: 64px; padding: 12px; border-radius: 10px; border: 1px solid rgba(63,224,208,.5); background: #151515; color: #eee; font: inherit; font-size: 17px; }}
    .mazzo {{ display: flex; justify-content: center; flex-wrap: wrap; gap: 10px; margin: 22px auto 6px; max-width: 640px; }}
    .mazzo button {{ width: 72px; height: 121px; padding: 0; border: 0; border-radius: 7px; background: url(/asset/dorso.jpeg) center/cover; cursor: pointer; box-shadow: 0 0 0 1px rgba(63,224,208,.35); transition: transform .25s, box-shadow .25s; }}
    .mazzo button:hover {{ transform: translateY(-8px); box-shadow: 0 0 14px rgba(63,224,208,.7); }}
    .mazzo.scelto button {{ opacity: .25; pointer-events: none; }}
    .passo {{ margin: 18px 0 10px; }}
    .sezioni, .domande {{ display: flex; flex-wrap: wrap; justify-content: center; gap: 10px; max-width: 760px; margin: 0 auto; }}
    .sezioni button, .domande button {{ font: inherit; font-size: 16px; padding: 10px 16px; border-radius: 24px; border: 1px solid rgba(63,224,208,.6); background: #151515; color: #eee; cursor: pointer; }}
    .sezioni button:hover, .domande button:hover {{ background: rgba(63,224,208,.15); }}
    .sezioni button.attivo, .domande button.attivo {{ background: #3fe0d0; color: #111; font-weight: bold; }}
    .domande {{ flex-direction: column; align-items: stretch; max-width: 520px; }}
    .domande button {{ border-radius: 12px; text-align: left; }}
    .tua {{ font-size: 19px; color: #3fe0d0; font-style: italic; margin: 0 0 4px; }}
    ul.elenco-dom {{ columns: 2; column-gap: 30px; padding-left: 20px; }}
    @media (max-width: 600px) {{ ul.elenco-dom {{ columns: 1; }} }}
    .avviso {{ display: none; max-width: 520px; margin: 12px auto 0; padding: 10px 14px; border-radius: 10px; background: rgba(242,201,76,.12); color: #f2c94c; font-size: 16px; }}
    .gioco textarea.errore {{ border-color: #f2c94c; box-shadow: 0 0 10px rgba(242,201,76,.5); }}
    #risultato {{ display: none; margin-top: 18px; }}
    #risultato img {{ width: 170px; border-radius: 10px; box-shadow: 0 0 22px rgba(63,224,208,.5); }}
    #risultato img.giu {{ transform: rotate(180deg); }}
    .risposta {{ font-family: 'Cinzel Decorative', serif; font-size: 64px; margin: 10px 0 0; line-height: 1; }}
    .r-si {{ color: #3fe0a0; }} .r-no {{ color: #ff6b6b; }} .r-forse {{ color: #f2c94c; }}
    .nome-carta {{ font-size: 22px; margin: 8px 0; }}
    .gioco .piccolo {{ font-size: 15px; opacity: .75; }}
    .gioco .azioni a, .gioco .azioni button {{ margin: 8px 6px; }}
    .gioco .azioni button {{ font: inherit; }}
    table.sn {{ width: 100%; border-collapse: collapse; margin: 12px 0; }}
    table.sn td, table.sn th {{ padding: 8px; border-bottom: 1px solid rgba(255,255,255,.1); text-align: left; }}
    table.sn td:not(:first-child), table.sn th:not(:first-child) {{ text-align: center; font-weight: bold; }}
    @media (max-width: 600px) {{ .mazzo button {{ width: 58px; height: 97px; }} .risposta {{ font-size: 52px; }} }}
  </style>
  <script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
</head>
<body>
  <header class="testata">
    <a class="logo" href="/">Zodiel</a>
    <nav><a href="/oggi/">Lettura di oggi</a> <a href="/arcani/">Arcani Maggiori</a> <a class="pill" href="/master">Fai una lettura</a></nav>
  </header>

  <main class="arcano sino">
    <p class="briciole"><a href="/">Home</a> &rsaquo; Tarocchi sì o no</p>
    <h1>Tarocchi Sì o No gratis</h1>
    <p>Hai una domanda precisa e vuoi una risposta veloce? Con i <strong>tarocchi sì o no</strong> basta <strong>una carta</strong>: scegli l'argomento e la tua domanda, poi pesca una carta coperta tra gli Arcani Maggiori e scopri subito se la risposta è <strong>sì</strong>, <strong>no</strong> o <strong>forse</strong>. È gratis e senza registrazione.</p>

    <section class="gioco" id="gioco">
      <p class="passo"><strong>1.</strong> Scegli un argomento</p>
      <div class="sezioni" id="sezioni">{BOTTONI}</div>
      <div id="passo2" style="display:none">
        <p class="passo"><strong>2.</strong> Scegli la tua domanda</p>
        <div class="domande" id="domande"></div>
        <p class="piccolo" id="notaBen" style="display:none">Le carte non sostituiscono il parere di un medico: per la salute rivolgiti sempre a un professionista.</p>
      </div>
      <div id="passo3" style="display:none">
        <p class="passo"><strong>3.</strong> Respira, concentrati sulla domanda e scegli una carta</p>
        <p class="tua" id="tuaDomanda"></p>
        <div class="mazzo" id="mazzo"></div>
      </div>
      <div id="risultato" aria-live="polite">
        <img id="rImg" src="" alt="" width="240" height="403">
        <p class="nome-carta" id="rNome"></p>
        <p class="risposta" id="rRisp"></p>
        <p id="rTesto"></p>
        <div class="azioni">
          <button class="pill" type="button" id="ancora">🔄 Fai un'altra domanda</button>
          <a class="cta" href="/master" onclick="window.traccia && traccia('sino_vai_lettura')">✨ Vuoi più dettagli? Fai la lettura completa</a>
        </div>
        <p class="piccolo"><a id="rLink" href="#">Leggi il significato completo di questa carta →</a></p>
      </div>
    </section>


    <section>
      <h2>Come funzionano i tarocchi sì o no</h2>
      <p>Ogni Arcano Maggiore ha una sua energia. Le carte luminose, come il <strong>Sole</strong>, la <strong>Stella</strong> e il <strong>Mondo</strong>, rispondono sì; le carte di blocco o di crollo, come la <strong>Torre</strong>, rispondono no; le carte più misteriose, come la <strong>Luna</strong> o l'<strong>Eremita</strong>, rispondono forse. Quando una carta esce <strong>rovesciata</strong>, la sua energia è rallentata e la risposta di solito si fa più cauta.</p>
      <p>Per avere una risposta chiara fai una domanda <strong>semplice e precisa</strong>, che riguardi te e a cui si possa rispondere con sì o no. Per le situazioni più complesse è meglio la <a href="/master">lettura a tre carte</a>, che guarda passato, presente e futuro.</p>
      <p class="nota">I tarocchi sono uno strumento di riflessione personale: usali come spunto, non come una previsione certa.</p>
    </section>

    <section>
      <h2>Tutte le risposte sì o no dei 22 Arcani Maggiori</h2>
      <table class="sn">
        <tr><th>Carta</th><th>Dritta</th><th>Rovesciata</th></tr>
{righe}
      </table>
    </section>

    <section class="faq">
      <h2>Domande frequenti sui tarocchi sì o no</h2>
{faqhtml}
    </section>
    <p style="text-align:center;margin-top:30px">Ogni giorno c'è anche <a href="/oggi/">la lettura dei tarocchi di oggi</a>.</p>
  </main>

  <footer class="piede"><a href="/">zodiel.cloud</a> · <a href="/si-o-no/">Tarocchi sì o no</a> · <a href="/oggi/">La lettura di oggi</a> · <a href="/arcani/">Arcani Maggiori</a> · <a href="/privacy">Privacy e cookie</a></footer>

  <script>
  (function () {{
    var D = {json.dumps(dati, ensure_ascii=False)};
    var ETI = {json.dumps(ETI, ensure_ascii=False)}, SP = {json.dumps(SPIEGA, ensure_ascii=False)};
    var ids = Object.keys(D), mazzo = document.getElementById("mazzo");
    var esc = function (s) {{ return String(s).replace(/[&<>"]/g, function (m) {{ return {{"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}}[m]; }}); }};
    function rnd(n) {{ var a = new Uint32Array(1); (window.crypto || window.msCrypto).getRandomValues(a); return a[0] % n; }}
    var SEZ = {DOMJSON}, domanda = "", sezione = "";
    function $(id) {{ return document.getElementById(id); }}
    function mostra(id, si) {{ $(id).style.display = si ? "block" : "none"; }}
    function prepara() {{
      mazzo.innerHTML = ""; mazzo.className = "mazzo";
      for (var i = 0; i < 7; i++) {{
        var b = document.createElement("button"); b.type = "button"; b.setAttribute("aria-label", "Scegli la carta " + (i + 1));
        b.onclick = pesca; mazzo.appendChild(b);
      }}
    }}
    [].forEach.call(document.querySelectorAll("#sezioni button"), function (b) {{
      b.onclick = function () {{
        sezione = b.getAttribute("data-s");
        [].forEach.call(document.querySelectorAll("#sezioni button"), function (x) {{ x.classList.toggle("attivo", x === b); }});
        var box = $("domande"); box.innerHTML = "";
        SEZ[sezione].forEach(function (q) {{
          var d = document.createElement("button"); d.type = "button"; d.textContent = q;
          d.onclick = function () {{
            domanda = q;
            [].forEach.call(box.children, function (x) {{ x.classList.toggle("attivo", x === d); }});
            $("tuaDomanda").textContent = "«" + q + "»";
            prepara(); mostra("passo3", true); mostra("risultato", false);
            $("passo3").scrollIntoView({{ behavior: "smooth", block: "center" }});
          }};
          box.appendChild(d);
        }});
        mostra("notaBen", sezione === "benessere");
        mostra("passo2", true); mostra("passo3", false); mostra("risultato", false);
        $("passo2").scrollIntoView({{ behavior: "smooth", block: "start" }});
      }};
    }});
    function pesca() {{
      var id = ids[rnd(ids.length)], dritta = rnd(10) < 7, d = D[id], k = dritta ? 0 : 1, r = d.r[k];
      var nome = d.n + (dritta ? "" : " " + ({{p: "rovesciati", f: "rovesciata"}}[d.g] || "rovesciato"));
      mazzo.className = "mazzo scelto";
      var img = $("rImg"); img.src = "/asset/img_web/" + id + ".webp"; img.alt = nome; img.className = dritta ? "" : "giu";
      $("rNome").textContent = nome;
      var rr = $("rRisp"); rr.textContent = ETI[r]; rr.className = "risposta r-" + r;
      $("rTesto").innerHTML = SP[r] + " <strong>" + esc(nome) + "</strong> " + (d.g === "p" ? "parlano" : "parla") + " di " + esc(d.kw[k].join(", ")) + ". Il consiglio: " + esc(d.c[k]) + ".";
      $("rLink").href = "/arcani/" + d.s;
      mostra("risultato", true);
      $("risultato").scrollIntoView({{ behavior: "smooth", block: "center" }});
      window.traccia && traccia("sino_carta", {{ sezione: sezione, domanda: domanda, carta: d.n, orientamento: dritta ? "dritta" : "rovesciata", risposta: r }});
    }}
    $("ancora").onclick = function () {{
      mostra("passo3", false); mostra("risultato", false);
      [].forEach.call(document.querySelectorAll(".domande button"), function (x) {{ x.classList.remove("attivo"); }});
      $("passo2").scrollIntoView({{ behavior: "smooth", block: "start" }});
    }};
  }})();
  </script>
</body>
</html>
'''
os.makedirs(os.path.join(BASE, "si-o-no"), exist_ok=True)
open(os.path.join(BASE, "si-o-no", "index.html"), "w", encoding="utf-8").write(pagina)
print("ok")
