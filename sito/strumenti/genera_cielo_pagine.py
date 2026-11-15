# -*- coding: utf-8 -*-
"""
22 Arcani – pagine del cielo per Google e per gli utenti:
  /cielo/                       il cielo di oggi e le carte in risonanza (aggiornato dal browser)
  /calendario-lunare-2027/      lune nuove, piene e quarti del 2027 con la carta del segno
  /mercurio-retrogrado-2027/    date di Mercurio (e degli altri pianeti) retrogradi, con il Mago
  /segni/                       l'Arcano di ogni segno zodiacale

Uso (dalla cartella 22arcani/sito):  python strumenti/genera_cielo_pagine.py
Serve prima cielo.js (python strumenti/genera_cielo.py 2026 2027). Richiede Node (già usato dagli altri script).
Opzione:  --dest CARTELLA   scrive le pagine in un'altra cartella (per provarle senza toccare il sito)
"""
import os, sys, re, json, html, subprocess, datetime as dt
QUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, QUI)
import genera_cielo as gc

BASE = os.environ.get("ZODIEL_SITO") or os.path.dirname(QUI)
DEST = BASE
if "--dest" in sys.argv:
    DEST = os.path.abspath(sys.argv[sys.argv.index("--dest") + 1])
SITO = "https://22arcani.it"
OGGI = dt.date.today()

GIORNI = ["lunedì","martedì","mercoledì","giovedì","venerdì","sabato","domenica"]
MESI = ["gennaio","febbraio","marzo","aprile","maggio","giugno","luglio","agosto","settembre","ottobre","novembre","dicembre"]
esc = lambda s: html.escape(str(s), quote=True)
slug = lambda fid: re.sub(r"^\d\d_", "", fid).replace("_", "-")

def trova(nome):
    """Un file del sito: prima nella cartella di destinazione, poi nel sito."""
    for d in (DEST, BASE):
        p = os.path.join(d, nome)
        if os.path.exists(p): return p
    raise SystemExit("File mancante: " + nome)

# ---------- dati: arcani, frasi del momento, cielo ----------
JS = r"""
global.window = global; const f = JSON.parse(process.argv[2]);
for (const p of f) require(p);
const out = { A: ZODIEL_ARCANI, M: ZODIEL_MOMENTO, C: ZODIEL_CIELO };
if (typeof zodielPaginaCielo === "function") { const d = new Date(); out.cielo = zodielPaginaCielo(d); out.data = zodielDataEstesa(d); }
process.stdout.write(JSON.stringify(out));
"""
tmp = os.path.join(os.path.expanduser("~"), "_cielo_pagine.js")
open(tmp, "w", encoding="utf-8").write(JS)
file_js = [trova(n) for n in ("cielo.js", "momento_dati.js", "sintesi_dati.js", "motore_momento.js", os.path.join("cielo", "cielo_pagina.js"))]
dati = json.loads(subprocess.check_output(["node", tmp, json.dumps(file_js)]).decode("utf-8"))
A, M, C = dati["A"], dati["M"], dati["C"]
SEGNI, SEGNI_DEL = M["segni"], M["segniDel"]
CARTA_SEGNO = {v["astro"]: k for k, v in M["corrispondenze"].items() if v["tipo"] == "segno"}
CARTA_PIANETA = {v["astro"]: k for k, v in M["corrispondenze"].items() if v["tipo"] == "pianeta"}

# ---------- ora italiana (senza librerie: ora legale dall'ultima domenica di marzo a quella di ottobre) ----------
def ultima_domenica(anno, mese):
    d = dt.date(anno, mese + 1, 1) - dt.timedelta(days=1) if mese < 12 else dt.date(anno, 12, 31)
    return d - dt.timedelta(days=(d.weekday() + 1) % 7)
def roma(t):
    i = dt.datetime.combine(ultima_domenica(t.year, 3), dt.time(1)); f = dt.datetime.combine(ultima_domenica(t.year, 10), dt.time(1))
    return t + dt.timedelta(hours=2 if i <= t < f else 1)
def quando(t, anno=True):
    r = roma(t)
    return "%s %d %s%s, ore %02d:%02d" % (GIORNI[r.weekday()], r.day, MESI[r.month - 1], (" %d" % r.year) if anno else "", r.hour, r.minute)
def giorno(t):
    r = roma(t); return "%s %d %s %d" % (GIORNI[r.weekday()], r.day, MESI[r.month - 1], r.year)

INIZIO = dt.datetime.strptime(C["inizio"], "%Y-%m-%d")
EVENTI = [(INIZIO + dt.timedelta(minutes=m), tipo, x) for m, tipo, x in C["eventi"]]
segno_luna = lambda t: int(gc.luna(gc.gj(t)) // 30)
segno_pianeta = lambda p, t: int(gc.pianeta(p, gc.gj(t)) // 30)

def link_carta(fid, testo=None): return '<a href="/arcani/%s">%s</a>' % (slug(fid), esc(testo or A[fid]["nome"]))
def img_carta(fid, w=120):
    return '<img src="/asset/img_web/%s_240.webp" alt="%s" width="%d" height="%d" loading="lazy">' % (fid, esc(A[fid]["nome"]), w, round(w * 201 / 120))

# ---------- modello di pagina (stesso stile di /oggi/ e /arcani/) ----------
STILE = """
    .cielo-blocco { margin: 26px 0; padding: 18px 22px; border-radius: 12px; background: rgba(63,224,208,.07); }
    .cielo-blocco h2 { margin-top: 0; font-size: 22px; }
    .cielo-grande { font-size: 24px; color: #40E0D0; margin: 4px 0; }
    .cielo-dettaglio { opacity: .75; margin: 0 0 10px; font-size: 16px; }
    .cielo-carta, .scheda { display: flex; gap: 18px; align-items: flex-start; margin: 18px 0; padding-top: 14px; border-top: 1px solid rgba(255,255,255,.1); }
    .cielo-carta img, .scheda img { flex: none; border-radius: 6px; }
    .cielo-carta h3, .scheda h3 { margin: 0 0 4px; }
    .cielo-motivo { font-style: italic; opacity: .85; margin: 0 0 6px; }
    .cielo-eventi li, .lune li { margin-bottom: 6px; }
    .mese { margin-top: 26px; }
    .periodo { padding: 12px 16px; border-left: 3px solid #40E0D0; margin: 12px 0; background: rgba(63,224,208,.05); }
    .oggi-segno { padding: 12px 16px; border-radius: 10px; background: rgba(63,224,208,.12); text-align: center; }
    .avvertenza { font-size: 15px; opacity: .75; font-style: italic; }
    @media (max-width: 600px) { .cielo-carta, .scheda { flex-direction: column; align-items: center; text-align: center; } }
"""
def pagina(percorso, titolo, descrizione, h1, briciola, corpo, script="", faq=None, immagine="18_la_luna"):
    url = SITO + percorso
    ld = [{"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "22 Arcani", "item": SITO + "/"},
        {"@type": "ListItem", "position": 2, "name": briciola, "item": url}]}]
    if faq:
        ld.append({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"<[^>]+>", "", a)}} for q, a in faq]})
        corpo += '\n    <section class="faq">\n      <h2>Domande frequenti</h2>\n' + "".join(
            "      <h3>%s</h3>\n      <p>%s</p>\n" % (esc(q), a) for q, a in faq) + "    </section>"
    return """<!DOCTYPE html>
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
  <title>{titolo}</title>
  <meta name="description" content="{descrizione}">
  <link rel="canonical" href="{url}">
  <meta property="og:type" content="article">
  <meta property="og:title" content="{titolo}">
  <meta property="og:description" content="{descrizione}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{sito}/asset/img_it/{immagine}.jpeg">
  <link href="https://fonts.googleapis.com/css2?family=Cinzel+Decorative:wght@400;700&family=Playfair+Display:wght@400;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/arcani/arcani.css">
  <style>{stile}  </style>
{ld}
</head>
<body>
  <header class="testata">
    <a class="logo" href="/">22 Arcani</a>
    <nav><a href="/cielo/">Il cielo di oggi</a> <a href="/arcani/">Arcani Maggiori</a> <a class="pill" href="/master">Fai una lettura</a></nav>
  </header>

  <main class="arcano">
    <p class="briciole"><a href="/">Home</a> &rsaquo; {briciola}</p>
    <h1>{h1}</h1>
{corpo}

    <section class="finale">
      <h2>La tua lettura del momento</h2>
      <p>Mescola il mazzo e scegli tre carte: alla fine, la sintesi della tua lettura si collega al cielo di quel momento, con la fase della Luna, i segni e i pianeti. È gratuita e non serve registrarsi.</p>
      <a class="cta" href="/master">Inizia la lettura</a>
    </section>
    <p class="avvertenza">I collegamenti tra tarocchi e astri seguono la tradizione simbolica: sono uno spunto di riflessione, non una previsione. Le date e le posizioni dei pianeti sono invece calcolate con precisione astronomica (ora italiana).</p>
  </main>

  <footer class="piede"><a href="/">22arcani.it</a> · <a href="/cielo/">Il cielo di oggi</a> · <a href="/calendario-lunare-2027/">Calendario lunare 2027</a> · <a href="/mercurio-retrogrado-2027/">Mercurio retrogrado 2027</a> · <a href="/segni/">Arcani e segni</a> · <a href="/arcani/">Arcani Maggiori</a> · <a href="/privacy">Privacy e cookie</a></footer>
{script}
</body>
</html>
""".format(titolo=esc(titolo), descrizione=esc(descrizione), url=url, sito=SITO, immagine=immagine, stile=STILE,
           ld="\n".join('  <script type="application/ld+json">%s</script>' % json.dumps(x, ensure_ascii=False) for x in ld),
           briciola=esc(briciola), h1=esc(h1), corpo=corpo, script=script)

def scrivi(percorso, testo):
    p = os.path.join(DEST, percorso.strip("/"), "index.html")
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8", newline="\r\n") as f: f.write(testo)
    print("scritta", os.path.relpath(p, DEST))

SCRIPT_CIELO = """  <script src="/sintesi_dati.js"></script>
  <script src="/cielo.js"></script>
  <script src="/momento_dati.js"></script>
  <script src="/motore_momento.js"></script>
"""

# ============ 1. /cielo/ ============
corpo = """    <p class="data" style="text-align:center;opacity:.8" id="cielo-data">%s</p>
    <p>Ogni giorno il cielo cambia: la <strong>Luna</strong> attraversa un segno ogni due giorni e mezzo, il <strong>Sole</strong> uno ogni mese, e alcuni pianeti a volte sembrano tornare indietro (il <strong>moto retrogrado</strong>). Nella tradizione dei tarocchi ogni segno e ogni pianeta è legato a un <a href="/arcani/">Arcano Maggiore</a>: ecco il cielo di adesso e le carte che oggi parlano con più forza.</p>
    <div id="cielo-oggi">%s</div>
    <p>Vuoi sapere quale carta è legata al tuo segno? Leggi <a href="/segni/">gli Arcani dei 12 segni zodiacali</a>.</p>""" % (esc(dati["data"]), dati["cielo"])
script = SCRIPT_CIELO + """  <script src="/cielo/cielo_pagina.js"></script>
  <script>
  (function () {
    try {
      var d = new Date();
      document.getElementById("cielo-data").textContent = zodielDataEstesa(d);
      document.getElementById("cielo-oggi").innerHTML = zodielPaginaCielo(d);
      if (window.traccia) traccia("cielo_vista");
    } catch (e) {}
  })();
  </script>"""
scrivi("/cielo/", pagina("/cielo/", "Il cielo di oggi e i tarocchi: Luna, segni e pianeti retrogradi | 22 Arcani",
    "La fase della Luna di oggi, il segno di Luna e Sole, i pianeti retrogradi e le carte dei tarocchi in risonanza con il cielo. Aggiornato ogni giorno.",
    "Il cielo di oggi e i tarocchi", "Il cielo di oggi", corpo, script, immagine="17_la_stella"))

# ============ 2. /calendario-lunare-2027/ ============
FASI = {"luna_nuova": "Luna nuova", "primo_quarto": "Primo quarto", "luna_piena": "Luna piena", "ultimo_quarto": "Ultimo quarto"}
def riga_luna(t, tipo):
    s = segno_luna(t)
    return '        <li><strong>%s in %s</strong> – %s · carta: %s</li>\n' % (FASI[tipo], SEGNI[s], quando(t, False), link_carta(CARTA_SEGNO[s]))
lune = [(t, tipo) for t, tipo, x in EVENTI if tipo in FASI]
fine2026 = [(t, tipo) for t, tipo in lune if t.year == 2026 and roma(t).date() >= OGGI]
corpo = """    <p>Il calendario lunare 2027 con tutte le <strong>lune nuove</strong>, le <strong>lune piene</strong> e i <strong>quarti di Luna</strong>, giorno e ora italiana. Per ogni fase trovi il <strong>segno</strong> in cui si trova la Luna e l'<strong>Arcano Maggiore</strong> che la tradizione dei tarocchi lega a quel segno.</p>
    <section class="cielo-blocco">
      <h2>Le fasi della Luna nei tarocchi</h2>
      <p><strong>Luna nuova</strong>: il cielo è buio, è il momento delle intenzioni e dei nuovi inizi. <strong>Primo quarto</strong>: le prime prove, il tempo di agire. <strong>Luna piena</strong>: tutto viene alla luce, è il culmine delle emozioni. <strong>Ultimo quarto</strong>: il tempo di lasciare andare e fare ordine.</p>
      <p>La Luna, nei tarocchi, è legata alla %s, la carta dell'intuizione. Vuoi sapere com'è la Luna proprio adesso? Guarda <a href="/cielo/">il cielo di oggi</a>.</p>
    </section>
""" % link_carta("02_la_papessa", "Papessa")
if fine2026:
    corpo += '    <h2>Le ultime lune del 2026</h2>\n      <ul class="lune">\n' + "".join(riga_luna(t, x) for t, x in fine2026) + "      </ul>\n"
corpo += "    <h2>Calendario lunare 2027</h2>\n"
for m in range(1, 13):
    del_mese = [(t, x) for t, x in lune if roma(t).year == 2027 and roma(t).month == m]
    corpo += '    <section class="mese">\n      <h3>%s 2027</h3>\n      <ul class="lune">\n%s      </ul>\n    </section>\n' % (
        MESI[m - 1].capitalize(), "".join(riga_luna(t, x) for t, x in del_mese))
piene27 = [(t, x) for t, x in lune if x == "luna_piena" and roma(t).year == 2027]
nuove27 = [(t, x) for t, x in lune if x == "luna_nuova" and roma(t).year == 2027]
faq = [
    ("Quante lune piene ci sono nel 2027?", "Nel 2027 ci sono %d lune piene e %d lune nuove. La prima luna piena del 2027 è %s, in %s." % (
        len(piene27), len(nuove27), giorno(piene27[0][0]), SEGNI[segno_luna(piene27[0][0])])),
    ("Che carta dei tarocchi è legata alla Luna?", "Nella tradizione dei tarocchi la Luna come astro è legata alla Papessa, carta dell'intuizione e del mondo interiore. L'arcano chiamato La Luna è invece legato al segno dei Pesci."),
    ("Gli orari del calendario lunare sono in ora italiana?", "Sì: tutti gli orari sono in ora italiana e tengono conto dell'ora legale. Le fasi sono calcolate astronomicamente al minuto."),
]
scrivi("/calendario-lunare-2027/", pagina("/calendario-lunare-2027/", "Calendario lunare 2027: lune piene, lune nuove e tarocchi | 22 Arcani",
    "Calendario lunare 2027 con tutte le lune piene, le lune nuove e i quarti, giorno e ora italiana, con il segno della Luna e l'Arcano dei tarocchi collegato.",
    "Calendario lunare 2027 e tarocchi", "Calendario lunare 2027", corpo, faq=faq, immagine="18_la_luna"))

# ============ 3. /mercurio-retrogrado-2027/ ============
def periodi(pianeta):
    k = C["pianeti"].index(pianeta); ris = []; inizio = None
    for t, tipo, x in EVENTI:
        if x != k: continue
        if tipo == "stazione_retrograda": inizio = t
        elif tipo == "stazione_diretta": ris.append((inizio, t)); inizio = None
    if inizio: ris.append((inizio, None))
    return ris
def blocco_periodo(p, a, b):
    s1 = SEGNI[segno_pianeta(p, a)] if a else ""
    testo = "da <strong>%s</strong> (in %s)" % (quando(a), s1) if a else "già in corso"
    testo += " a <strong>%s</strong> (in %s)" % (quando(b), SEGNI[segno_pianeta(p, b)]) if b else ", fino a oltre la fine del calendario"
    return '      <p class="periodo">%s</p>\n' % testo
merc = periodi("mercurio")
merc27 = [(a, b) for a, b in merc if (a and roma(a).year == 2027) or (b and roma(b).year == 2027)]
merc_ora = [(a, b) for a, b in merc if b and roma(b).date() >= OGGI and roma(b).year == 2026]
mago = "01_il_mago"
corpo = """    <section class="intro">
      %s
      <div>
        <p>Tre o quattro volte l'anno, per circa tre settimane, <strong>Mercurio</strong> sembra fermarsi nel cielo e tornare indietro: è il <strong>moto retrogrado</strong>. In realtà il pianeta non inverte la sua corsa: è un effetto di prospettiva, dovuto al fatto che la Terra e Mercurio girano intorno al Sole a velocità diverse.</p>
        <p>Nella tradizione, Mercurio governa la <strong>comunicazione</strong>, i viaggi brevi, gli scambi e il pensiero. Nei tarocchi è il pianeta del %s.</p>
      </div>
    </section>
""" % (img_carta(mago), link_carta(mago, "Mago"))
if merc_ora:
    corpo += "    <h2>Mercurio retrogrado adesso</h2>\n" + "".join(blocco_periodo("mercurio", a, b) for a, b in merc_ora)
corpo += "    <h2>Mercurio retrogrado 2027: le date</h2>\n    <p>Nel 2027 Mercurio è retrogrado %d volte. Date e orari in ora italiana, con il segno in cui si trova il pianeta:</p>\n" % len(merc27)
corpo += "".join(blocco_periodo("mercurio", a, b) for a, b in merc27)
corpo += """    <h2>Mercurio retrogrado nei tarocchi: il Mago</h2>
    <p>Il Mago è la carta di Mercurio: parola, ingegno, capacità di trasformare le idee in azione. Quando Mercurio è retrogrado, il Mago parla con la voce della carta rovesciata: «%s»</p>
    <p>Nella tradizione, questi periodi sono considerati adatti a <strong>rileggere, chiarire e rivedere</strong>: riprendere un progetto lasciato a metà, risolvere un malinteso, ricontrollare i dettagli. Sono spunti simbolici: per contratti, viaggi e decisioni importanti contano i fatti, non il cielo.</p>
    <p>Durante la tua lettura, se esce il Mago mentre Mercurio è retrogrado, la sintesi lo segnala.</p>
""" % esc(M["carte"][mago][1])
altri = ""
for p, nome, carta, f in (("venere", "Venere", "03_l_imperatrice", "retrograda"), ("marte", "Marte", "16_la_torre", "retrogrado"),
                          ("giove", "Giove", "10_la_ruota_della_fortuna", "retrogrado"), ("saturno", "Saturno", "21_il_mondo", "retrogrado")):
    per = [(a, b) for a, b in periodi(p) if (a and roma(a).year == 2027) or (b and roma(b).year == 2027)]
    if per:
        altri += "    <h3>%s %s nel 2027 – %s</h3>\n" % (nome, f, link_carta(carta)) + "".join(blocco_periodo(p, a, b) for a, b in per)
    else:
        altri += "    <h3>%s nel 2027 – %s</h3>\n    <p>Nel 2027 %s non è mai %s.</p>\n" % (nome, link_carta(carta), nome, f)
corpo += "    <h2>Gli altri pianeti retrogradi nel 2027</h2>\n" + altri
faq = [("Quando è Mercurio retrogrado nel 2027?", "Nel 2027 Mercurio è retrogrado " + "; ".join(
            "da %s a %s" % (giorno(a), giorno(b)) for a, b in merc27 if a and b) + "."),
       ("Mercurio va davvero all'indietro?", "No. Il moto retrogrado è un effetto di prospettiva: visto dalla Terra, Mercurio sembra tornare indietro tra le stelle per alcune settimane, perché i due pianeti girano intorno al Sole a velocità diverse."),
       ("Che carta dei tarocchi è legata a Mercurio?", "Il Mago, Arcano Maggiore numero I, carta della parola, dell'ingegno e dell'iniziativa.")]
scrivi("/mercurio-retrogrado-2027/", pagina("/mercurio-retrogrado-2027/", "Mercurio retrogrado 2027: date, orari e significato nei tarocchi | 22 Arcani",
    "Tutte le date di Mercurio retrogrado nel 2027, in ora italiana, con il segno e il significato nei tarocchi: il Mago. In più Venere, Marte, Giove e Saturno retrogradi.",
    "Mercurio retrogrado 2027: date e significato nei tarocchi", "Mercurio retrogrado 2027", corpo, faq=faq, immagine=mago))

# ============ 4. /segni/ ============
DATE = ["21 marzo – 19 aprile","20 aprile – 20 maggio","21 maggio – 20 giugno","21 giugno – 22 luglio","23 luglio – 22 agosto","23 agosto – 22 settembre",
        "23 settembre – 22 ottobre","23 ottobre – 21 novembre","22 novembre – 21 dicembre","22 dicembre – 19 gennaio","20 gennaio – 18 febbraio","19 febbraio – 20 marzo"]
GOVERNO = ["marte","venere","mercurio","luna","sole","mercurio","venere","marte","giove","saturno","saturno","giove"]
TESTO_SEGNO = [
 "L'Imperatore riflette lo slancio dell'Ariete verso l'azione e il desiderio di guidare: forza di volontà, iniziativa, capacità di dare una direzione.",
 "Il Papa parla di valori solidi, tradizione e fiducia: come il Toro, cerca basi stabili e ciò che dura nel tempo.",
 "Gli Amanti raccontano la scelta e l'incontro: come i Gemelli, vivono di relazioni, dialogo e possibilità diverse.",
 "Il Carro unisce emozione e determinazione: come il Cancro, protegge ciò che ama e avanza guidato dal cuore.",
 "La Forza è il coraggio gentile: come il Leone, ha un cuore grande e vince le paure con la calma, non con la violenza.",
 "L'Eremita cerca la verità con pazienza e metodo: come la Vergine, osserva i dettagli e trova la propria luce nella riflessione.",
 "La Giustizia cerca equilibrio e onestà: come la Bilancia, pesa le scelte e desidera armonia nei rapporti.",
 "La Morte è la carta della trasformazione profonda: come lo Scorpione, non teme di chiudere un ciclo per rinascere.",
 "La Temperanza unisce gli opposti e cerca la misura: come il Sagittario, punta lontano e trova un senso più ampio nel viaggio.",
 "Il Diavolo parla di ambizione e di legami con la materia: come il Capricorno, invita a riconoscere ciò che trattiene per salire più in alto in libertà.",
 "La Stella è speranza e visione del futuro: come l'Acquario, guarda avanti e crede in un'idea più grande.",
 "La Luna è sogno, intuizione e sensibilità: come i Pesci, attraversa le emozioni profonde e il mondo invisibile."]
TESTO_PIANETA = {
 "marte": "è legato alla Torre: l'energia che rompe ciò che è rigido per fare spazio al nuovo.",
 "venere": "è legata all'Imperatrice: bellezza, piacere dei sensi e cura.",
 "mercurio": "è legato al Mago: parola, ingegno e capacità di trasformare le idee in azione.",
 "luna": "è legata alla Papessa: intuizione, mondo interiore e ascolto.",
 "sole": "è legato all'arcano del Sole: gioia, vitalità e voglia di risplendere.",
 "giove": "è legato alla Ruota della Fortuna: fiducia, espansione e occasioni.",
 "saturno": "è legato al Mondo: tempo, maturità e traguardi raggiunti con costanza."}
corpo = """    <p>Nella tradizione dei tarocchi più diffusa nei mazzi moderni, nata alla fine dell'Ottocento, ogni <strong>segno zodiacale</strong> è legato a un <strong>Arcano Maggiore</strong>, e ogni segno ha anche un <strong>pianeta</strong> che lo governa, con la sua carta. Ecco l'Arcano del tuo segno.</p>
    <p class="oggi-segno" id="segno-oggi"></p>
"""
for s in range(12):
    fid = CARTA_SEGNO[s]; p = GOVERNO[s]; pc = CARTA_PIANETA[p]
    trad = " (governatore tradizionale)" if s in (7, 10, 11) else ""
    corpo += """    <section class="scheda" id="%s">
      %s
      <div>
        <h3>%s · %s</h3>
        <p class="cielo-motivo">%s · segno %s</p>
        <p><strong>L'Arcano del segno:</strong> %s. %s</p>
        <p><strong>Il pianeta del segno:</strong> %s%s %s Carta: %s.</p>
      </div>
    </section>
""" % (SEGNI[s].lower(), img_carta(fid), esc(SEGNI[s]), esc(A[fid]["nome"]), DATE[s], M["elementoDi"][M["elementoSegno"][s]],
       link_carta(fid), esc(TESTO_SEGNO[s]), {"luna": "la Luna", "sole": "il Sole"}.get(p, M["pianeti"][p]), trad, TESTO_PIANETA[p], link_carta(pc))
corpo += """    <section class="cielo-blocco">
      <h2>Gli Arcani degli elementi</h2>
      <p>Tre carte sono legate agli elementi: %s all'<strong>aria</strong>, %s all'<strong>acqua</strong> e %s al <strong>fuoco</strong>. Quando la Luna passa in un segno del loro elemento, queste carte parlano con più forza: lo vedi ogni giorno nel <a href="/cielo/">cielo di oggi</a>.</p>
    </section>
""" % (link_carta("00_il_matto"), link_carta("12_l_appeso"), link_carta("20_il_giudizio"))
script = SCRIPT_CIELO + """  <script>
  (function () {
    try {
      var c = zodielCielo(new Date()), D = ZODIEL_MOMENTO;
      if (!c.disponibile) return;
      var s = D.segni[c.segnoSole], id = s.toLowerCase();
      document.getElementById("segno-oggi").innerHTML = "Oggi il Sole è in <a href='#" + id + "'>" + s + "</a> e la Luna in <a href='#" +
        D.segni[c.segnoLuna].toLowerCase() + "'>" + D.segni[c.segnoLuna] + "</a>.";
      var el = document.getElementById(id); if (el) el.style.background = "rgba(63,224,208,.10)";
    } catch (e) {}
  })();
  </script>"""
faq = [("Qual è la carta dei tarocchi del mio segno zodiacale?", "Ariete: l'Imperatore. Toro: il Papa. Gemelli: gli Amanti. Cancro: il Carro. Leone: la Forza. Vergine: l'Eremita. Bilancia: la Giustizia. Scorpione: la Morte. Sagittario: la Temperanza. Capricorno: il Diavolo. Acquario: la Stella. Pesci: la Luna."),
       ("Da dove vengono queste corrispondenze?", "Sono le corrispondenze della tradizione esoterica di fine Ottocento, poi riprese dal mazzo Rider-Waite e dalla maggior parte dei mazzi moderni. Sono simboliche: servono come spunto di riflessione.")]
scrivi("/segni/", pagina("/segni/", "La carta dei tarocchi del tuo segno zodiacale: gli Arcani dei 12 segni | 22 Arcani",
    "Qual è l'Arcano Maggiore del tuo segno zodiacale? Le corrispondenze tradizionali tra i 12 segni, i pianeti e le carte dei tarocchi, con il significato di ogni carta.",
    "La carta dei tarocchi del tuo segno zodiacale", "Arcani e segni", corpo, script, faq=faq, immagine="21_il_mondo"))

# ---------- sitemap.xml: aggiunge le pagine nuove o ne aggiorna la data ----------
PAGINE_SITEMAP = (("/cielo/", "daily", "0.8"), ("/calendario-lunare-2027/", "monthly", "0.8"),
                  ("/mercurio-retrogrado-2027/", "monthly", "0.8"), ("/segni/", "monthly", "0.8"))
if DEST == BASE:
    sm = os.path.join(BASE, "sitemap.xml")
    raw = open(sm, "rb").read(); crlf = b"\r\n" in raw
    x = raw.decode("utf-8").replace("\r\n", "\n")
    for p, f, pr in PAGINE_SITEMAP:
        loc = "<loc>%s%s</loc>" % (SITO, p)
        if loc in x:
            x = re.sub(r"(%s\s*<lastmod>)[^<]*(</lastmod>)" % re.escape(loc), r"\g<1>%s\g<2>" % OGGI.isoformat(), x)
        else:
            x = x.replace("</urlset>", "  <url>\n    %s\n    <lastmod>%s</lastmod>\n    <changefreq>%s</changefreq>\n    <priority>%s</priority>\n  </url>\n</urlset>" % (
                loc, OGGI.isoformat(), f, pr))
    if crlf: x = x.replace("\n", "\r\n")
    open(sm, "wb").write(x.encode("utf-8"))
    print("sitemap.xml aggiornata")
