# -*- coding: utf-8 -*-
"""
22 Arcani – il cielo di un giorno, per i video quotidiani.
Usa gli stessi dati del sito (cielo.js, momento_dati.js, motore_momento.js) tramite Node.
  import cielo_oggi as co
  c = co.cielo("2026-11-09")        -> dati del cielo alle 9:00 di quel giorno (ora italiana)
  co.frase_parlata(c)               -> "Il cielo di oggi: Luna nuova in Scorpione, con Mercurio retrogrado."
  co.riga_video(c)                  -> "Luna nuova in Scorpione · Mercurio retrogrado"
Prova veloce:  python strumenti/cielo_oggi.py 2026-11-24
"""
import os, sys, json, subprocess

BASE = os.environ.get("ZODIEL_SITO") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JS = r"""
global.window = global; const B = process.argv[2];
for (const f of ["cielo.js", "momento_dati.js", "motore_momento.js"]) require(B + "/" + f);
const [y, m, d] = process.argv[3].split("-").map(Number);
const c = zodielCielo(new Date(y, m - 1, d, 9, 0)), D = ZODIEL_MOMENTO;
const out = { disponibile: !!c.disponibile };
if (c.disponibile) Object.assign(out, { fase: D.fasiNomi[c.fase], segno_luna: D.segni[c.segnoLuna], segno_sole: D.segni[c.segnoSole],
  retrogradi: c.retrogradi, eventi: c.eventi.map(e => ({ tipo: e.tipo, pianeta: e.pianeta ? D.pianeti[e.pianeta] : null })) });
// segno della Luna nel momento esatto di una Luna nuova o piena di quel giorno
const C = ZODIEL_CIELO, p = C.inizio.split("-"), t0 = Date.UTC(+p[0], +p[1] - 1, +p[2]);
const g0 = new Date(y, m - 1, d).getTime();
for (const e of C.eventi) {
  const t = t0 + e[0] * 60000;
  if (t >= g0 && t < g0 + 864e5 && (e[1] === "luna_piena" || e[1] === "luna_nuova")) out.segno_evento = D.segni[zodielCielo(new Date(t)).segnoLuna];
}
process.stdout.write(JSON.stringify(out));
"""
STAGIONI = {"equinozio_primavera": "l'equinozio di primavera", "solstizio_estate": "il solstizio d'estate",
            "equinozio_autunno": "l'equinozio d'autunno", "solstizio_inverno": "il solstizio d'inverno"}

def cielo(data_iso):
    tmp = os.path.join(os.path.expanduser("~"), "_cielo_oggi.js")
    with open(tmp, "w", encoding="utf-8") as f: f.write(JS)
    try:
        return json.loads(subprocess.check_output(["node", tmp, BASE, data_iso]).decode("utf-8"))
    except Exception:
        return {"disponibile": False}   # se manca qualcosa, il video si fa lo stesso, senza cielo

def frase_parlata(c):
    if not c.get("disponibile"): return ""
    tipi = [e["tipo"] for e in c["eventi"]]
    fase = c["fase"][0].upper() + c["fase"][1:]
    stagione = next((STAGIONI[t] for t in tipi if t in STAGIONI), None)
    if stagione:
        f = "Oggi è %s, con la %s in %s." % (stagione, c["fase"], c["segno_luna"])
    elif "luna_piena" in tipi or "luna_nuova" in tipi:
        f = "Oggi è %s in %s." % (fase, c.get("segno_evento") or c["segno_luna"])
    else:
        f = "Il cielo di oggi: %s in %s." % (c["fase"], c["segno_luna"])
    stazione = next((e for e in c["eventi"] if e["pianeta"] == "Mercurio"), None)
    if stazione:
        f += " E proprio oggi Mercurio %s." % ("diventa retrogrado" if stazione["tipo"] == "stazione_retrograda" else "torna diretto")
    elif "mercurio" in c["retrogradi"]:
        f = f[:-1] + ", con Mercurio retrogrado."
    return f

def riga_video(c):
    if not c.get("disponibile"): return ""
    r = "%s in %s" % (c["fase"][0].upper() + c["fase"][1:], c.get("segno_evento") or c["segno_luna"])
    stazione = next((e for e in c["eventi"] if e["pianeta"] == "Mercurio"), None)
    if stazione: r += " · Mercurio %s oggi" % ("diventa retrogrado" if stazione["tipo"] == "stazione_retrograda" else "torna diretto")
    elif "mercurio" in c["retrogradi"]: r += " · Mercurio retrogrado"
    return r

if __name__ == "__main__":
    for d in sys.argv[1:] or ["2026-11-09"]:
        c = cielo(d); print(d, "|", riga_video(c), "|", frase_parlata(c))
