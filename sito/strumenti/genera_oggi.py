# Zodiel – pagina "La lettura di oggi" (zodiel.cloud/oggi).
# Scrive oggi/calendario.js (carte di ogni giorno, stesso algoritmo del video) e oggi/index.html
# (già compilata con la lettura del giorno di generazione, per Google; il JS la aggiorna al giorno corrente).
# Uso: python3 strumenti/genera_oggi.py            (calendario da 7 giorni fa a +400 giorni)
import os, sys, re, json, html, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import genera_lettura as gl

BASE = gl.BASE; DIR = os.path.join(BASE, "oggi"); os.makedirs(DIR, exist_ok=True)
oggi = datetime.date.today()
giorni = [oggi + datetime.timedelta(days=i) for i in range(-7, 401)]
cal = {d.isoformat(): [[i, dr] for i, dr in gl.scegli(d.isoformat())] for d in giorni}
open(os.path.join(DIR, "calendario.js"), "w", encoding="utf-8").write(
    "// Generato da strumenti/genera_oggi.py: non modificare a mano.\nwindow.ZODIEL_OGGI = " +
    json.dumps(cal, separators=(",", ":")) + ";\n")

def slug(fid): return re.sub(r"^\d\d_", "", fid).replace("_", "-")
def testo_md(fid, dritta, pos):
    f = os.path.join(BASE, "asset", "descrizione_it", "%s%s_%s.md" % (fid, "" if dritta else "_r", pos))
    t = re.sub(r"[*#_]", "", open(f, encoding="utf-8-sig").read())
    return [p.strip() for p in re.split(r"\n\s*\n|\s{2,}\n", t) if p.strip()]

carte = gl.scegli(oggi.isoformat())
par, D = gl.sintesi(carte)
data_txt = "%s %d %s %d" % (gl.GIORNI[oggi.weekday()], oggi.day, gl.MESI[oggi.month-1], oggi.year)
blocchi = []
for k, (fid, dr) in enumerate(carte):
    d = D[fid]; pos = gl.POSIZ[k][0]
    nome = d["nome"] + ("" if dr else " " + {"p": "rovesciati", "f": "rovesciata"}.get(d["genere"], "rovesciato"))
    kw = ", ".join(d["kw"][0 if dr else 1][:3])
    ps = "".join("<p>%s</p>" % html.escape(p) for p in testo_md(fid, dr, pos))
    blocchi.append(f'''<article class="carta-oggi">
        <img src="/asset/img_web/{fid}.webp" alt="{html.escape(nome)}" width="240" height="403"{'' if dr else ' class="giu"'}>
        <div><p class="pos">{pos}</p><h2>{html.escape(nome)}</h2><p class="kw">{html.escape(kw)}</p>{ps}
        <a href="/arcani/{slug(fid)}">Leggi tutto su questa carta →</a></div></article>''')
sint = "".join("<p>%s</p>" % html.escape(p) for p in par)
nomi = ", ".join(re.sub(r"<[^>]+>", "", D[f]["nome"]) for f, _ in carte)

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
  <title>La lettura dei tarocchi di oggi: passato, presente e futuro | Zodiel</title>
  <meta name="description" content="Ogni giorno una nuova lettura dei tarocchi gratis: tre Arcani Maggiori per passato, presente e futuro, con il significato di ogni carta e la sintesi. Poi scegli le tue carte.">
  <link rel="canonical" href="https://zodiel.cloud/oggi/">
  <meta property="og:type" content="article">
  <meta property="og:title" content="La lettura dei tarocchi di oggi | Zodiel">
  <meta property="og:description" content="Tre carte per passato, presente e futuro: la lettura del giorno, gratis.">
  <meta property="og:url" content="https://zodiel.cloud/oggi/">
  <meta property="og:image" content="https://zodiel.cloud/asset/img_it/{carte[1][0]}.jpeg">
  <link href="https://fonts.googleapis.com/css2?family=Cinzel+Decorative:wght@400;700&family=Playfair+Display:wght@400;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/arcani/arcani.css">
  <style>
    .oggi h1 {{ margin-bottom: 4px; }}
    .oggi .data {{ text-align: center; opacity: .8; margin: 0 0 24px; text-transform: capitalize; }}
    .carta-oggi {{ display: flex; gap: 24px; align-items: flex-start; margin: 28px 0; padding-top: 20px; border-top: 1px solid rgba(255,255,255,.12); }}
    .carta-oggi img {{ width: 150px; height: auto; flex: none; border-radius: 8px; }}
    .carta-oggi img.giu {{ transform: rotate(180deg); }}
    .carta-oggi h2 {{ margin: 0 0 4px; }}
    .carta-oggi .pos {{ margin: 0; text-transform: uppercase; letter-spacing: 2px; font-size: 14px; color: #3fe0d0; }}
    .carta-oggi .kw {{ margin: 0 0 10px; font-style: italic; opacity: .85; }}
    .sintesi-oggi {{ margin-top: 30px; padding: 20px; border-radius: 12px; background: rgba(63,224,208,.08); }}
    .chiama {{ text-align: center; margin: 36px 0 10px; }}
    .chiama .cta {{ font-size: 20px; }}
    @media (max-width: 600px) {{ .carta-oggi {{ flex-direction: column; align-items: center; }} .carta-oggi img {{ width: 130px; }} }}
  </style>
  <script type="application/ld+json">{{"@context":"https://schema.org","@type":"WebPage","name":"La lettura dei tarocchi di oggi","url":"https://zodiel.cloud/oggi/","description":"Ogni giorno tre Arcani Maggiori per passato, presente e futuro, con significato e sintesi.","isPartOf":{{"@type":"WebSite","name":"Zodiel","url":"https://zodiel.cloud/"}}}}</script>
</head>
<body>
  <header class="testata">
    <a class="logo" href="/">Zodiel</a>
    <nav><a href="/si-o-no/">Sì o no</a> <a href="/arcani/">Arcani Maggiori</a> <a class="pill" href="/master">Fai una lettura</a></nav>
  </header>

  <main class="arcano oggi">
    <p class="briciole"><a href="/">Home</a> &rsaquo; La lettura di oggi</p>
    <h1>La lettura dei tarocchi di oggi</h1>
    <p class="data" id="data">{data_txt}</p>
    <p>Ogni giorno Zodiel estrae <strong>tre Arcani Maggiori</strong>: uno per il <strong>passato</strong>, uno per il <strong>presente</strong> e uno per il <strong>futuro</strong>. È la stessa lettura del video quotidiano sul nostro canale YouTube. Oggi sono uscite: <strong id="nomi">{html.escape(nomi)}</strong>.</p>

    <div id="carte">{"".join(blocchi)}</div>

    <section class="sintesi-oggi">
      <h2>La sintesi della lettura</h2>
      <div id="sintesi">{sint}</div>
    </section>

    <div class="chiama">
      <p><strong>Questa è la lettura di oggi. E la tua?</strong><br>Scegli tu le tue tre carte e scopri cosa dicono a te.</p>
      <a class="cta" href="/master">✨ Ora fai la tua lettura gratis</a>
      <p style="margin-top:18px"><a href="https://www.youtube.com/@zodiel-tarocchi" rel="noopener">▶ Guarda la lettura di oggi su YouTube</a></p>
    </div>
  </main>

  <footer class="piede"><a href="/">zodiel.cloud</a> · <a href="/oggi/">La lettura di oggi</a> · <a href="/arcani/">Arcani Maggiori</a> · <a href="/privacy">Privacy e cookie</a></footer>

  <script src="/sintesi_dati.js"></script>
  <script src="/sintesi.js"></script>
  <script src="/oggi/calendario.js"></script>
  <script>
  (function () {{
    var PRIMA = "{oggi.isoformat()}";
    var GIORNI = ["domenica","lunedì","martedì","mercoledì","giovedì","venerdì","sabato"];
    var MESI = {json.dumps(gl.MESI)};
    var POS = ["Passato","Presente","Futuro"];
    var oggi = new Intl.DateTimeFormat("en-CA", {{ timeZone: "Europe/Rome" }}).format(new Date());
    if (oggi === PRIMA || !window.ZODIEL_OGGI || !window.ZODIEL_OGGI[oggi] || !window.ZODIEL_ARCANI) return;
    var c = window.ZODIEL_OGGI[oggi], A = window.ZODIEL_ARCANI;
    var p = oggi.split("-"), dt = new Date(+p[0], +p[1] - 1, +p[2]);
    document.getElementById("data").textContent = GIORNI[dt.getDay()] + " " + (+p[2]) + " " + MESI[+p[1] - 1] + " " + p[0];
    var esc = function (s) {{ return String(s).replace(/[&<>"]/g, function (m) {{ return {{"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}}[m]; }}); }};
    var rov = function (g) {{ return g === "p" ? "rovesciati" : g === "f" ? "rovesciata" : "rovesciato"; }};
    document.getElementById("nomi").textContent = c.map(function (x) {{ return A[x[0]].nome; }}).join(", ");
    var cont = document.getElementById("carte"); cont.innerHTML = "";
    c.forEach(function (x, k) {{
      var d = A[x[0]], dr = x[1], nome = d.nome + (dr ? "" : " " + rov(d.genere));
      var slug = x[0].replace(/^\\d\\d_/, "").replace(/_/g, "-");
      var art = document.createElement("article"); art.className = "carta-oggi";
      art.innerHTML = '<img src="/asset/img_web/' + x[0] + '.webp" alt="' + esc(nome) + '" width="240" height="403"' + (dr ? "" : ' class="giu"') + '>' +
        '<div><p class="pos">' + POS[k] + '</p><h2>' + esc(nome) + '</h2><p class="kw">' + esc(d.kw[dr ? 0 : 1].slice(0, 3).join(", ")) + '</p>' +
        '<div class="testo"></div><a href="/arcani/' + slug + '">Leggi tutto su questa carta →</a></div>';
      cont.appendChild(art);
      fetch("/asset/descrizione_it/" + x[0] + (dr ? "" : "_r") + "_" + POS[k] + ".md").then(function (r) {{ return r.text(); }}).then(function (t) {{
        art.querySelector(".testo").innerHTML = t.replace(/[*#_]/g, "").split(/\\n\\s*\\n|\\s{{2,}}\\n/).filter(function (s) {{ return s.trim(); }})
          .map(function (s) {{ return "<p>" + esc(s.trim()) + "</p>"; }}).join("");
      }});
    }});
    var s = window.creaSintesi && window.creaSintesi({{ passato: {{nome: c[0][0], dritta: c[0][1]}}, presente: {{nome: c[1][0], dritta: c[1][1]}}, futuro: {{nome: c[2][0], dritta: c[2][1]}} }});
    if (s) document.getElementById("sintesi").innerHTML = s.paragrafi.map(function (q) {{ return "<p>" + q + "</p>"; }}).join("");
  }})();
  </script>
</body>
</html>
'''
open(os.path.join(DIR, "index.html"), "w", encoding="utf-8").write(pagina)
print("ok", oggi, nomi, len(cal), "giorni")
