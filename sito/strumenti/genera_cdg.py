# Zodiel – Short "Carta del giorno": stessa carta che il sito mostra in home quel giorno
# (algoritmo di carta_giorno.js), spiegata dalla lettrice (video "Presente").
# Uso: python3 strumenti/genera_cdg.py 2026-11-01 [2026-11-02 ...]
# Richiede node (per calcolare la carta del giorno da carta_giorno.js).
import os, sys, json, subprocess, shutil
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import genera_shorts3 as g3
from PIL import Image, ImageDraw

BASE = g3.BASE
OUT = os.path.join(BASE, "youtube_grafica", "cdg")
W, H, TURCH, BIANCO, GRIGIO = g3.W, g3.H, g3.TURCH, g3.BIANCO, g3.GRIGIO
F = g3.font; C = g3.centrato
INFO = {}

JS = r"""
global.window = {};
require(process.argv[2] + '/sintesi_dati.js');
require(process.argv[2] + '/carta_giorno.js');
const out = {};
for (const d of process.argv.slice(3)) { const c = window.cartaDelGiorno(d); out[d] = [c.id, c.dritta, c.dataLeggibile, c.nomeCompleto]; }
console.log(JSON.stringify(out));
"""

def carte(date):
    tmp = os.path.join(os.path.expanduser("~"), "_cdg_calc.js")
    open(tmp, "w").write(JS)
    return json.loads(subprocess.check_output(["node", tmp, BASE] + date).decode())

def gancio(num, rov, pos, path):
    nome, gen = g3.CARTE[num]; im = g3.sfondo(); d = ImageDraw.Draw(im)
    C(im, 120, "LA CARTA DI OGGI", F("Cinzel[wght].ttf", 70, 700), BIANCO)
    C(im, 215, INFO["data"], F("Cinzel[wght].ttf", 60, 600), GRIGIO)
    t = nome.upper()
    C(im, 300, t, g3.adatta(d, t, "Cinzel[wght].ttf", 120, 980, 700), TURCH, glow=True)
    y2 = 440
    if rov: C(im, y2, g3.ROV[gen], F("Cinzel[wght].ttf", 64, 600), BIANCO); y2 += 80
    c = g3.carta_img(num, rov, 1060 if not rov else 990); g3.con_alone(im, c, ((W - c.width)//2, y2 + 40), 44)
    C(im, 1760, "ascolta cosa ti dice", F("Cinzel[wght].ttf", 54, 600), BIANCO)
    im.convert("RGB").save(path)

def cornice(num, rov, pos, path):
    nome, gen = g3.CARTE[num]
    im = Image.new("RGBA", (W, H), (0,0,0,0)); d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W, g3.VY], fill=g3.NERO + (255,)); d.rectangle([0, g3.VY+g3.VH, W, H], fill=g3.NERO + (255,))
    for y in (g3.VY - 3, g3.VY + g3.VH): d.rectangle([0, y, W, y+3], fill=TURCH + (255,))
    C(im, 40, "CARTA DEL GIORNO · " + INFO["data_breve"].upper(), F("Cinzel[wght].ttf", 40, 600), BIANCO)
    t = nome.upper(); C(im, 110, t, g3.adatta(d, t, "Cinzel[wght].ttf", 96, 1000, 700), TURCH, glow=True)
    if rov: C(im, 222, g3.ROV[gen].upper(), F("Cinzel[wght].ttf", 44, 600), BIANCO)
    fz = F("Cinzel[wght].ttf", 50, 700); d = ImageDraw.Draw(im)
    C(im, 1650, "ZODIEL.CLOUD", fz, TURCH)
    w = d.textlength("ZODIEL.CLOUD", font=fz); g3.stella(d, (W-w)/2-38, 1680, 18, TURCH); g3.stella(d, (W+w)/2+38, 1680, 18, TURCH)
    im.save(path)

def finale(path):
    im = g3.sfondo(); d = ImageDraw.Draw(im)
    C(im, 230, "Questa è la carta di oggi", F("Cinzel[wght].ttf", 66, 600), BIANCO)
    C(im, 315, "per tutti.", F("Cinzel[wght].ttf", 66, 600), BIANCO)
    C(im, 470, "E le TUE 3 carte?", F("Cinzel[wght].ttf", 80, 700), BIANCO)
    C(im, 650, "SCOPRILE GRATIS", F("Cinzel[wght].ttf", 74, 700), BIANCO)
    C(im, 760, "ZODIEL.CLOUD", F("Cinzel[wght].ttf", 116, 700), TURCH, glow=True)
    d.rounded_rectangle([110, 1020, 970, 1210], radius=40, fill=(16, 52, 50, 255), outline=TURCH, width=5)
    C(im, 1050, "Tocca il video collegato", F("Cinzel[wght].ttf", 52, 700), BIANCO)
    C(im, 1125, "qui sotto", F("Cinzel[wght].ttf", 52, 700), BIANCO)
    d.line([(300, 1260), (200, 1460)], fill=TURCH, width=14)
    d.polygon([(165, 1400), (190, 1500), (262, 1430)], fill=TURCH)
    C(im, 1600, "Domani una nuova carta:", F("Cinzel[wght].ttf", 54, 600), GRIGIO)
    C(im, 1675, "iscriviti per non perderla", F("Cinzel[wght].ttf", 54, 600), GRIGIO)
    im.convert("RGB").save(path)

g3.gancio, g3.cornice, g3.finale, g3.OUT = gancio, cornice, finale, OUT

if __name__ == "__main__":
    date = sys.argv[1:]
    dati = carte(date)
    os.makedirs(OUT, exist_ok=True)
    for dt in date:
        fid, dritta, leggibile, nome_completo = dati[dt]
        codice = fid + ("" if dritta else "_r") + "_Presente"
        parti = leggibile.split(" ")              # es. "domenica 1 novembre 2026"
        INFO["data"] = " ".join(parti[:3])
        INFO["data_breve"] = " ".join(parti[1:3])
        uscita = os.path.join(OUT, "cdg_%s_%s.mp4" % (dt, fid[3:] + ("" if dritta else "_r")))
        if os.path.exists(uscita): print("esiste", uscita); continue
        g3.video(codice)
        shutil.move(os.path.join(OUT, "short3_%s.mp4" % codice), uscita)
        print("fatto", dt, nome_completo, "->", os.path.basename(uscita))
