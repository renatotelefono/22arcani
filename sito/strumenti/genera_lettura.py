# Zodiel – Short "La lettura di oggi": 3 carte (passato, presente, futuro) scelte da un algoritmo
# in base alla data, girate una alla volta, con parole chiave, una frase per carta e la sintesi
# (la stessa del sito, da sintesi.js). Niente lettrice: carte, movimento, testo e musica.
# Uso: python3 strumenti/genera_lettura.py 2026-11-01 [2026-11-02 ...]
import os, sys, re, json, math, random, subprocess, datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import genera_shorts3 as g3
try:
    import cielo_oggi as co          # il cielo del giorno (Luna, Mercurio retrogrado...)
except ImportError:
    co = None
from PIL import Image, ImageDraw, ImageFilter

BASE = g3.BASE; OUT = os.path.join(BASE, "youtube_grafica", "lettura")
W, H, FPS = 1080, 1920, 25
TURCH, BIANCO, GRIGIO = g3.TURCH, g3.BIANCO, g3.GRIGIO
CIN = lambda s, w=600: g3.font("Cinzel[wght].ttf", s, w)
POP = lambda s: g3.font("Poppins-Bold.ttf", s)
GIORNI = ["lunedì","martedì","mercoledì","giovedì","venerdì","sabato","domenica"]
MESI = ["gennaio","febbraio","marzo","aprile","maggio","giugno","luglio","agosto","settembre","ottobre","novembre","dicembre"]
POSIZ = [("Passato","IL PASSATO"), ("Presente","IL PRESENTE"), ("Futuro","IL FUTURO")]
IDS = sorted(n[:-5] for n in os.listdir(os.path.join(BASE, "asset", "img_it")) if n.endswith(".jpeg") and n[:2].isdigit())

# ---------------- scelta delle carte ----------------
def scegli(data):
    r = random.Random("zodiel-lettura-" + data)
    ids = r.sample(IDS, 3)
    return [(i, r.random() < 0.7) for i in ids]   # 70% dritte

JS = r"""
global.window={}; require(process.argv[2]+'/sintesi_dati.js'); require(process.argv[2]+'/sintesi.js');
const a=JSON.parse(process.argv[3]);
const s=window.creaSintesi({passato:{nome:a[0][0],dritta:a[0][1]},presente:{nome:a[1][0],dritta:a[1][1]},futuro:{nome:a[2][0],dritta:a[2][1]}});
console.log(JSON.stringify({s:s, d:window.ZODIEL_ARCANI}));
"""
def sintesi(carte):
    tmp = os.path.join(os.path.expanduser("~"), "_sint.js"); open(tmp, "w").write(JS)
    r = json.loads(subprocess.check_output(["node", tmp, BASE, json.dumps(carte)]).decode())
    pul = lambda h: re.sub(r"<[^>]+>", "", h)
    return [pul(p) for p in r["s"]["paragrafi"]], r["d"]

def prima_frase(fid, dritta, pos):
    f = os.path.join(BASE, "asset", "descrizione_it", "%s%s_%s.md" % (fid, "" if dritta else "_r", pos))
    t = re.sub(r"[*#_]", "", open(f, encoding="utf-8-sig").read()).replace("\n", " ").strip()
    m = re.match(r"(.+?[.!?])(\s|$)", t)
    return (m.group(1) if m else t).replace("’", "'")

# ---------------- grafica ----------------
def a_capo(d, testo, font, maxw):
    righe, cur = [], ""
    for p in testo.split():
        prova = (cur + " " + p).strip()
        if d.textlength(prova, font=font) <= maxw: cur = prova
        else: righe.append(cur); cur = p
    if cur: righe.append(cur)
    return righe

def testo_centrato(im, y, testo, font, col, maxw=940, interl=1.25):
    d = ImageDraw.Draw(im)
    for r in a_capo(d, testo, font, maxw):
        w = d.textlength(r, font=font); d.text(((W - w) / 2, y), r, font=font, fill=col)
        y += int(font.size * interl)
    return y

def sfondo():
    im = Image.new("RGBA", (W, H), (11, 11, 11, 255))
    g = Image.new("RGBA", (W, H), (0,0,0,0)); ImageDraw.Draw(g).ellipse([-250, 250, W+250, 1650], fill=(20, 70, 66, 255))
    im.alpha_composite(g.filter(ImageFilter.GaussianBlur(170)))
    d = ImageDraw.Draw(im); fz = CIN(44, 700)
    w = d.textlength("ZODIEL.CLOUD", font=fz); d.text(((W-w)/2, 1800), "ZODIEL.CLOUD", font=fz, fill=TURCH)
    g3.stella(d, (W-w)/2-34, 1826, 15, TURCH); g3.stella(d, (W+w)/2+34, 1826, 15, TURCH)
    return im

CH = 430                      # altezza carte nelle caselle
def carta(fid, dritta, h=CH):
    c = g3.carta_img(int(fid[:2]), not dritta, h); return c
def dorso(h=CH):
    c = Image.open(os.path.join(BASE, "asset", "dorso.jpeg")).convert("RGBA")
    c = c.resize((int(c.width * h / c.height), h), Image.LANCZOS)
    m = Image.new("L", c.size, 0); ImageDraw.Draw(m).rounded_rectangle([0,0,c.width-1,c.height-1], radius=int(h*0.04), fill=255)
    c.putalpha(m); return c

def ombra(c, r=26):
    s = Image.new("RGBA", (c.width + 2*r*2, c.height + 2*r*2), (0,0,0,0))
    s2 = Image.new("RGBA", c.size, TURCH + (190,)); s2.putalpha(c.split()[3])
    s.alpha_composite(s2, (2*r, 2*r)); return s.filter(ImageFilter.GaussianBlur(r)), 2*r

def incolla(im, c, cx, cy, alone=True):
    if alone:
        o, off = ombra(c); im.alpha_composite(o, (int(cx - c.width/2 - off), int(cy - c.height/2 - off)))
    im.alpha_composite(c, (int(cx - c.width/2), int(cy - c.height/2)))

SLOT_X = [W/2 - 330, W/2, W/2 + 330]; SLOT_Y = 520
ease = lambda x: 0.5 - 0.5 * math.cos(math.pi * max(0, min(1, x)))

# ---------------- voce (Piper, voce italiana "paola") ----------------
PIPER = os.path.expanduser("~/.local/bin/piper")
VOCE = os.path.expanduser("~/voci/vits-piper-it_IT-paola-medium/it_IT-paola-medium.onnx")
NUMERI = ["zero","uno","due","tre","quattro","cinque","sei","sette","otto","nove","dieci","undici","dodici","tredici",
          "quattordici","quindici","sedici","diciassette","diciotto","diciannove","venti","ventuno","ventidue","ventitré",
          "ventiquattro","venticinque","ventisei","ventisette","ventotto","ventinove","trenta","trentuno"]

CHIAVE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "chiave_tts.txt")
VOCE_GOOGLE = "it-IT-Chirp3-HD-Despina"

def parla(testo, path):
    """Voce Google Cloud TTS (Chirp 3 HD Despina); se manca la chiave usa Piper."""
    if os.path.exists(CHIAVE):
        import urllib.request, base64
        k = open(CHIAVE).read().strip()
        body = {"input": {"text": testo}, "voice": {"languageCode": "it-IT", "name": VOCE_GOOGLE},
                "audioConfig": {"audioEncoding": "LINEAR16", "sampleRateHertz": 24000}}
        req = urllib.request.Request("https://texttospeech.googleapis.com/v1/text:synthesize?key=" + k,
                                     data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
        a = json.load(urllib.request.urlopen(req, timeout=90))["audioContent"]
        open(path, "wb").write(base64.b64decode(a))
    else:
        t = testo.replace("22arcani.it", "Zodièl punto clàud")
        subprocess.run([PIPER, "-m", VOCE, "-f", path, "--sentence_silence", "0.25"], input=t.encode("utf-8"),
                       check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path]).decode())

def video(data):
    carte = scegli(data)
    par, D = sintesi(carte)
    dt = datetime.date.fromisoformat(data)
    data_txt = "%s %d %s" % (GIORNI[dt.weekday()], dt.day, MESI[dt.month-1])
    cielo = co.cielo(data) if co else {}
    cielo_parlato = co.frase_parlata(cielo) if co else ""
    cielo_riga = co.riga_video(cielo) if co else ""
    BACK = dorso(); FRONT = [carta(f, d) for f, d in carte]
    base = sfondo()
    # testi delle carte
    info = []
    for k, (fid, dritta) in enumerate(carte):
        d = D[fid]; i = 0 if dritta else 1
        nome = d["nome"] + ("" if dritta else " " + ({"p":"rovesciati","f":"rovesciata"}.get(d["genere"], "rovesciato")))
        info.append((POSIZ[k][1], nome, ", ".join(d["kw"][i][:3]), prima_frase(fid, dritta, POSIZ[k][0])))

    # testi parlati e loro durata
    tmpd = os.path.join(os.path.expanduser("~"), "_voce"); os.makedirs(tmpd, exist_ok=True)
    giorno_parlato = "%s %s %s" % (GIORNI[dt.weekday()], NUMERI[dt.day] if dt.day != 1 else "primo", MESI[dt.month-1])
    frasi = ["Ecco la lettura di oggi, %s. %sTre carte: passato, presente e futuro." % (giorno_parlato, cielo_parlato + " " if cielo_parlato else "")]
    for k in range(3):
        pos, nome, kw, frase = info[k]
        frasi.append("%s: %s. %s" % (pos.capitalize(), nome, frase))
    frasi.append("In sintesi. " + " ".join(par[1:4]))
    frasi.append("Questa è la lettura di oggi. La spiegazione completa è su 22arcani.it/oggi. E la tua? Scegli le tue tre carte, gratis: la sintesi segue il cielo del momento. Tocca il video collegato qui sotto.")
    wav = [os.path.join(tmpd, "v%d.wav" % i) for i in range(len(frasi))]
    dur = [parla(f, w) for f, w in zip(frasi, wav)]
    T_INT, T_DEAL = 3.0, max(2.0, dur[0] + 0.6 - 3.0)
    T_CK = [max(6.0, dur[1 + k] + 1.3) for k in range(3)]
    T_S = max(6.0, dur[4] + 1.0); T_F = max(5.0, dur[5] + 1.2)
    t_c0 = T_INT + T_DEAL
    CS = [t_c0 + sum(T_CK[:k]) for k in range(3)]
    t_s0 = t_c0 + sum(T_CK); t_f0 = t_s0 + T_S; TOT = t_f0 + T_F
    INIZI_VOCE = [0.3] + [CS[k] + 0.7 for k in range(3)] + [t_s0 + 0.4, t_f0 + 0.3]
    nfr = int(TOT * FPS)

    # pannelli statici
    def pannello_intro():
        im = base.copy()
        cx = lambda y, s, f, c: testo_centrato(im, y, s, f, c)
        cx(150, "LA LETTURA DI OGGI", CIN(74, 700), BIANCO)
        cx(250, data_txt, CIN(50, 500), GRIGIO)
        if cielo_riga: cx(330, cielo_riga, POP(38), TURCH)
        cx(1240, "3 carte scelte per oggi", CIN(52, 600), TURCH)
        cx(1320, "PASSATO · PRESENTE · FUTURO", CIN(42, 600), BIANCO)
        return im
    INTRO = pannello_intro()
    def testata(im):
        testo_centrato(im, 70, "LA LETTURA DI OGGI", CIN(54, 700), BIANCO)
        testo_centrato(im, 140, data_txt, CIN(38, 500), GRIGIO)
        d = ImageDraw.Draw(im); f = CIN(30, 700)
        for k in range(3):
            lab = POSIZ[k][0].upper(); w = d.textlength(lab, font=f)
            d.text((SLOT_X[k] - w/2, SLOT_Y + CH/2 + 22), lab, font=f, fill=TURCH)
    TAV = base.copy(); testata(TAV)
    def pannello_carta(k):
        im = Image.new("RGBA", (W, H), (0,0,0,0))
        pos, nome, kw, frase = info[k]
        y = 860
        y = testo_centrato(im, y, pos, CIN(46, 700), TURCH) + 10
        y = testo_centrato(im, y, nome.upper(), CIN(70, 700), BIANCO, 980) + 18
        y = testo_centrato(im, y, kw, POP(40), (150, 230, 222), 940) + 34
        testo_centrato(im, y, frase, POP(44), BIANCO, 940, 1.32)
        return im
    PAN = [pannello_carta(k) for k in range(3)]
    def pannello_sintesi():
        im = Image.new("RGBA", (W, H), (0,0,0,0))
        y = testo_centrato(im, 860, "LA SINTESI", CIN(50, 700), TURCH) + 24
        for p in par[1:4]:
            y = testo_centrato(im, y, p, POP(40), BIANCO, 960, 1.3) + 26
        return im
    SINT = pannello_sintesi()
    def pannello_finale():
        im = base.copy()
        c = lambda y, s, f, col: testo_centrato(im, y, s, f, col)
        c(260, "Questa è la lettura di oggi.", CIN(52, 600), BIANCO)
        c(400, "E LA TUA?", CIN(96, 700), TURCH)
        c(560, "Mescola il mazzo e scegli", CIN(50, 600), BIANCO)
        c(630, "le TUE 3 carte", CIN(50, 600), BIANCO)
        c(770, "SPIEGAZIONE COMPLETA SU", CIN(46, 700), BIANCO)
        testo_centrato(im, 860, "ZODIEL.CLOUD/OGGI", CIN(84, 700), TURCH, 1040)
        d = ImageDraw.Draw(im)
        d.rounded_rectangle([110, 1150, 970, 1340], radius=40, fill=(16, 52, 50, 255), outline=TURCH, width=5)
        c(1180, "Tocca il video collegato", CIN(50, 700), BIANCO); c(1255, "qui sotto", CIN(50, 700), BIANCO)
        d.line([(300, 1390), (200, 1590)], fill=TURCH, width=14); d.polygon([(165, 1530), (190, 1630), (262, 1560)], fill=TURCH)
        c(1680, "Domani una nuova lettura", CIN(40, 500), GRIGIO)
        return im
    FIN = pannello_finale()

    def alfa(im, a):
        if a >= 1: return im
        x = im.copy(); x.putalpha(x.split()[3].point(lambda v: int(v * max(0, a)))); return x

    def girata(k, p):          # p 0..1: rotazione della carta k
        if p <= 0: return BACK
        if p >= 1: return FRONT[k]
        s = abs(math.cos(math.pi * p)); src = BACK if p < 0.5 else FRONT[k]
        w = max(2, int(src.width * s)); return src.resize((w, src.height), Image.BILINEAR)

    os.makedirs(OUT, exist_ok=True)
    nome_file = os.path.join(OUT, "lettura_%s.mp4" % data)
    pad = os.path.join(os.path.expanduser("~"), "_pad.wav")
    # musica d'atmosfera bassa + campanelle quando le carte si girano + voce
    accordo = ("0.20*sin(2*PI*220*t)*(0.65+0.35*sin(2*PI*0.18*t))+0.16*sin(2*PI*277.2*t)*(0.65+0.35*sin(2*PI*0.13*t+1))"
               "+0.14*sin(2*PI*329.6*t)*(0.65+0.35*sin(2*PI*0.21*t+2))+0.08*sin(2*PI*440*t)*(0.6+0.4*sin(2*PI*0.11*t+3))")
    tocchi = [T_INT] + CS + [t_s0, t_f0]
    campane = "+".join("if(gte(t,%.2f),(0.35*sin(2*PI*880*t)+0.2*sin(2*PI*1320*t)+0.1*sin(2*PI*1760*t))*exp(-2.2*(t-%.2f)),0)" % (x, x) for x in tocchi)
    musica = os.path.join(tmpd, "musica.wav")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi", "-i",
        "aevalsrc='0.35*(%s)+0.6*(%s)':s=44100:d=%.2f" % (accordo, campane, TOT),
        "-af", "afade=t=in:d=1,afade=t=out:st=%.2f:d=1.5,aformat=channel_layouts=stereo" % (TOT - 1.5), musica], check=True)
    ins = ["-i", musica]; fc = []
    for i, (w, st) in enumerate(zip(wav, INIZI_VOCE)):
        ins += ["-i", w]; fc.append("[%d:a]aresample=44100,aformat=channel_layouts=stereo,adelay=%d|%d,volume=1.0[v%d]" % (i+1, st*1000, st*1000, i))
    fc.append("[0:a]volume=0.22[m]")
    fc.append("[m]" + "".join("[v%d]" % i for i in range(len(wav))) + "amix=inputs=%d:normalize=0:duration=first,loudnorm=I=-15:TP=-1.5:LRA=11,aresample=44100,aformat=sample_fmts=s16:channel_layouts=stereo[a]" % (len(wav)+1))
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error"] + ins + ["-filter_complex", ";".join(fc), "-map", "[a]", "-t", "%.2f" % TOT, pad], check=True)
    ff = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", "%dx%d" % (W, H),
        "-r", str(FPS), "-i", "-", "-i", pad, "-c:v", "libx264", "-preset", "veryfast", "-crf", "21", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "160k", "-shortest", "-movflags", "+faststart", nome_file], stdin=subprocess.PIPE)
    cache = {}
    for n in range(nfr):
        t = n / FPS
        if t < T_INT:
            im = INTRO.copy(); s = 1 + 0.03 * math.sin(t * 2)
            b = BACK.resize((int(BACK.width * 1.25 * s), int(BACK.height * 1.25 * s)))
            for j in range(3): incolla(im, b, W/2 + (j-1)*6, 760 + (j-1)*6, j == 2)
            if t < 0.4: im = Image.blend(Image.new("RGBA", (W,H), (0,0,0,255)), im, t/0.4)
        elif t < t_s0 + 0.0 or t < t_f0:
            if t < t_s0:
                key = None
            im = TAV.copy()
            for k in range(3):
                if t < t_c0:      # distribuzione
                    p = ease((t - T_INT - k * 0.35) / 1.0)
                    x = W/2 + (SLOT_X[k] - W/2) * p; y = 1100 + (SLOT_Y - 1100) * p
                    incolla(im, BACK, x, y)
                else:
                    tk = CS[k]
                    pg = 0 if t < tk else (t - tk) / 0.7
                    c = girata(k, pg)
                    attiva = t < t_s0 and tk <= t < tk + T_CK[k]
                    if attiva and pg >= 1:
                        c = c.resize((int(c.width * 1.08), int(c.height * 1.08)))
                    incolla(im, c, SLOT_X[k], SLOT_Y, attiva or t >= t_s0)
            if t_c0 <= t < t_s0:
                k = max(i for i in range(3) if CS[i] <= t); tl = t - CS[k]
                a = min(1, max(0, (tl - 0.6) / 0.4)) * min(1, max(0, (T_CK[k] - tl) / 0.3))
                if a > 0: im.alpha_composite(alfa(PAN[k], a))
            elif t >= t_s0:
                tl = t - t_s0; a = min(1, tl / 0.5) * min(1, max(0, (T_S - tl) / 0.4))
                im.alpha_composite(alfa(SINT, a))
        else:
            tl = t - t_f0; im = FIN.copy()
            if tl < 0.4: im = Image.blend(TAV, im, tl / 0.4)
        ff.stdin.write(im.convert("RGB").tobytes())
    ff.stdin.close(); ff.wait()
    print("fatto", data, [i for i in info], "->", os.path.basename(nome_file), "%.1fs" % TOT)

if __name__ == "__main__":
    for d in sys.argv[1:]: video(d)
