# 22 Arcani – Shorts "stile 3": gancio con zoom, lettrice con zoom lento, stacchi sulla carta,
# sottotitoli grandi, finale "Tocca il video collegato".
# Uso: python3 strumenti/genera_shorts3.py 00_il_matto_Presente [altri codici...]
import os, re, sys, subprocess, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "youtube_grafica", "shorts3")
FONTS = os.environ.get("ZODIEL_FONTS", os.path.expanduser("~/fonts"))
if not os.path.isdir(FONTS): FONTS = os.path.join(BASE, "fonts")  # font salvati nella cartella 22arcani/sito
W, H = 1080, 1920
TURCH = (64, 224, 208); BIANCO = (238, 238, 238); GRIGIO = (170, 170, 170); NERO = (11, 11, 11)
FPS = 25
G = 1.8      # durata gancio
F = 3.5      # durata finale
VY, VH = 300, 1300   # zona video lettrice

CARTE = {
 0:("Il Matto","m"),1:("Il Mago","m"),2:("La Papessa","f"),3:("L'Imperatrice","f"),
 4:("L'Imperatore","m"),5:("Il Papa","m"),6:("Gli Amanti","p"),7:("Il Carro","m"),
 8:("La Forza","f"),9:("L'Eremita","m"),10:("La Ruota della Fortuna","f"),11:("La Giustizia","f"),
 12:("L'Appeso","m"),13:("La Morte","f"),14:("La Temperanza","f"),15:("Il Diavolo","m"),
 16:("La Torre","f"),17:("La Stella","f"),18:("La Luna","f"),19:("Il Sole","m"),
 20:("Il Giudizio","m"),21:("Il Mondo","m")}
ROV = {"m":"rovesciato","f":"rovesciata","p":"rovesciati"}
SE = {"m":"Se ti è uscito","f":"Se ti è uscita","p":"Se ti sono usciti"}
POS = {"Passato":"nel passato","Presente":"nel presente","Futuro":"nel futuro"}

def font(nome, size, wght=None):
    f = ImageFont.truetype(os.path.join(FONTS, nome), size)
    if wght:
        try: f.set_variation_by_axes([wght])
        except Exception: pass
    return f

def adatta(d, txt, nome, size, maxw, wght=None):
    while size > 30:
        f = font(nome, size, wght)
        if d.textlength(txt, font=f) <= maxw: return f
        size -= 4
    return font(nome, size, wght)

def centrato(img, y, txt, f, col, glow=False):
    d = ImageDraw.Draw(img); w = d.textlength(txt, font=f); x = (W - w) / 2
    if glow:
        g = Image.new("RGBA", img.size, (0,0,0,0)); ImageDraw.Draw(g).text((x, y), txt, font=f, fill=TURCH + (210,))
        img.alpha_composite(g.filter(ImageFilter.GaussianBlur(14)))
    ImageDraw.Draw(img).text((x, y), txt, font=f, fill=col)

def stella(d, cx, cy, r, col):
    pts = []
    for i in range(8):
        a = math.pi/4*i - math.pi/2; rr = r if i % 2 == 0 else r*0.28
        pts.append((cx+rr*math.cos(a), cy+rr*math.sin(a)))
    d.polygon(pts, fill=col)

def sfondo():
    im = Image.new("RGBA", (W, H), NERO + (255,))
    g = Image.new("RGBA", (W, H), (0,0,0,0)); ImageDraw.Draw(g).ellipse([-200, 300, W+200, 1500], fill=(20, 70, 66, 255))
    im.alpha_composite(g.filter(ImageFilter.GaussianBlur(160)))
    return im

def carta_img(num, rov, altezza):
    d = os.path.join(BASE, "asset", "img_it")
    fn = [n for n in sorted(os.listdir(d)) if n.startswith("%02d_" % num)][0]
    c = Image.open(os.path.join(d, fn)).convert("RGBA")
    c = c.resize((int(c.width * altezza / c.height), altezza), Image.LANCZOS)
    if rov: c = c.rotate(180)
    m = Image.new("L", c.size, 0); ImageDraw.Draw(m).rounded_rectangle([0,0,c.width-1,c.height-1], radius=int(altezza*0.03), fill=255)
    c.putalpha(m); return c

def con_alone(base, img, xy, raggio=30):
    g = Image.new("RGBA", base.size, (0,0,0,0))
    s = Image.new("RGBA", img.size, TURCH + (255,)); s.putalpha(img.split()[3])
    g.alpha_composite(s, xy); base.alpha_composite(g.filter(ImageFilter.GaussianBlur(raggio))); base.alpha_composite(img, xy)

# ---------- grafiche ----------
def gancio(num, rov, pos, path):
    nome, gen = CARTE[num]; im = sfondo()
    centrato(im, 150, SE[gen] + (" " + ROV[gen] if rov else ""), font("PlayfairDisplay-Italic[wght].ttf", 66), BIANCO)
    d = ImageDraw.Draw(im)
    if len(nome) > 16:
        p = nome.upper().split(" "); fn = font("CinzelDecorative-Bold.ttf", 108)
        centrato(im, 245, " ".join(p[:2]), fn, TURCH, glow=True); centrato(im, 360, " ".join(p[2:]), fn, TURCH, glow=True); y2 = 495
    else:
        centrato(im, 250, nome.upper(), adatta(d, nome.upper(), "CinzelDecorative-Bold.ttf", 124, 980), TURCH, glow=True); y2 = 400
    centrato(im, y2, POS[pos] + "…", font("PlayfairDisplay-Italic[wght].ttf", 64), BIANCO)
    c = carta_img(num, rov, 1080); con_alone(im, c, ((W - c.width)//2, y2 + 130), 44)
    im2 = Image.new("RGBA", im.size); im2.alpha_composite(im)
    centrato(im2, 1740, "ascolta cosa ti dice", font("PlayfairDisplay-Italic[wght].ttf", 54), BIANCO)
    im2.convert("RGB").save(path)

def cornice(num, rov, pos, path):
    nome, gen = CARTE[num]
    im = Image.new("RGBA", (W, H), (0,0,0,0)); d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W, VY], fill=NERO + (255,)); d.rectangle([0, VY+VH, W, H], fill=NERO + (255,))
    for y in (VY - 3, VY + VH): d.rectangle([0, y, W, y+3], fill=TURCH + (255,))
    t = nome.upper(); centrato(im, 95, t, adatta(d, t, "CinzelDecorative-Bold.ttf", 96, 1000), TURCH, glow=True)
    sub = (ROV[gen].upper() + " · " if rov else "") + POS[pos].upper()
    centrato(im, 210, sub, font("Cinzel[wght].ttf", 46, 600), BIANCO)
    fz = font("Cinzel[wght].ttf", 50, 700); d = ImageDraw.Draw(im)
    centrato(im, 1650, "22ARCANI.IT", fz, TURCH)
    w = d.textlength("22ARCANI.IT", font=fz); stella(d, (W-w)/2-38, 1680, 18, TURCH); stella(d, (W+w)/2+38, 1680, 18, TURCH)
    im.save(path)

def stacco(num, rov, path):
    im = Image.new("RGBA", (W, VH), (11, 11, 11, 235))
    g = Image.new("RGBA", (W, VH), (0,0,0,0)); ImageDraw.Draw(g).ellipse([100, 150, W-100, VH-150], fill=(20, 90, 84, 255))
    im.alpha_composite(g.filter(ImageFilter.GaussianBlur(120)))
    c = carta_img(num, rov, 1140); con_alone(im, c, ((W - c.width)//2, (VH - c.height)//2), 40)
    im.save(path)

def finale(path):
    im = sfondo()
    centrato(im, 300, "E le TUE 3 carte?", font("PlayfairDisplay-Italic[wght].ttf", 86), BIANCO)
    centrato(im, 430, "Insieme raccontano", font("PlayfairDisplay[wght].ttf", 56), GRIGIO)
    centrato(im, 505, "molto di più", font("PlayfairDisplay[wght].ttf", 56), GRIGIO)
    centrato(im, 680, "LETTURA GRATIS", font("Cinzel[wght].ttf", 80, 700), BIANCO)
    centrato(im, 790, "22ARCANI.IT", font("CinzelDecorative-Bold.ttf", 116), TURCH, glow=True)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([110, 1060, 970, 1250], radius=40, fill=(16, 52, 50, 255), outline=TURCH, width=5)
    centrato(im, 1090, "Tocca il video collegato", font("PlayfairDisplay[wght].ttf", 58, 700), BIANCO)
    centrato(im, 1165, "qui sotto", font("PlayfairDisplay[wght].ttf", 58, 700), BIANCO)
    # freccia verso il basso a sinistra (dove YouTube mostra il video collegato)
    d.line([(300, 1300), (200, 1500)], fill=TURCH, width=14)
    d.polygon([(165, 1440), (190, 1540), (262, 1470)], fill=TURCH)
    stella(d, W/2, 1420, 34, TURCH)
    im.convert("RGB").save(path)

# ---------- tempi delle parole (senza riconoscimento vocale) ----------
def silenzi(src, dur):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", src, "-af", "silencedetect=n=-35dB:d=0.18", "-f", "null", "-"],
                       capture_output=True, text=True).stderr
    s = [float(x) for x in re.findall(r"silence_start: ([0-9.]+)", r)]
    e = [float(x) for x in re.findall(r"silence_end: ([0-9.]+)", r)]
    if len(e) < len(s): e.append(dur)
    parl, t = [], 0.0
    for a, b in zip(s, e):
        if a > t + 0.05: parl.append((t, a))
        t = b
    if t < dur - 0.05: parl.append((t, dur))
    return parl

def tempi_parole(testo, parl):
    parole = testo.split()
    peso = [len(p) + 1.5 + (2.5 if p[-1] in ".,:;!?" else 0) for p in parole]
    tot_p, tot_t = sum(peso), sum(b - a for a, b in parl)
    out, acc = [], 0.0
    def mappa(x):  # tempo "di sola voce" -> tempo reale
        for a, b in parl:
            if x <= b - a: return a + x
            x -= b - a
        return parl[-1][1]
    for p, w in zip(parole, peso):
        t0 = acc / tot_p * tot_t; acc += w; t1 = acc / tot_p * tot_t
        out.append((p, mappa(t0 + 0.001), mappa(t1)))
    return out

def blocchi(parole, maxp=3):
    res, cur = [], []
    for p in parole:
        cur.append(p)
        if len(cur) >= maxp or p[0][-1] in ".,:;!?":
            res.append(cur); cur = []
    if cur: res.append(cur)
    return [(" ".join(x[0] for x in b), b[0][1], b[-1][2]) for b in res]

def ts(t):
    h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60
    return "%d:%02d:%05.2f" % (h, m, s)

def scrivi_ass(path, blocchi_, dopo):
    head = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Sub,Poppins,150,&H00FFFFFF,&H00FFFFFF,&H00000000,&H96000000,1,0,0,0,100,100,0,0,1,9,4,2,50,50,560,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    with open(path, "w", encoding="utf-8") as f:
        f.write(head)
        for i, (txt, a, b) in enumerate(blocchi_):
            if b < dopo: continue
            a = max(a, dopo)
            nb = blocchi_[i+1][1] if i + 1 < len(blocchi_) else b + 0.3
            f.write("Dialogue: 0,%s,%s,Sub,,0,0,0,,{\\fad(60,0)}%s\n" % (ts(a), ts(max(b, min(nb, b + 0.4))), txt.replace("’", "'")))

# ---------- montaggio ----------
def video(codice):
    p = codice.split("_"); num = int(p[0]); pos = p[-1]; rov = "_r_" in codice
    src = os.path.join(BASE, "asset", "video_it", codice + ".mp4")
    testo = open(os.path.join(BASE, "asset", "descrizione_it", codice + ".md"), encoding="utf-8").read()
    testo = re.sub(r"[*#_]", "", testo).replace("\n", " ").strip()
    os.makedirs(OUT, exist_ok=True); tmp = os.path.join(OUT, "_tmp"); os.makedirs(tmp, exist_ok=True)
    dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", src]).decode())
    parl = silenzi(src, dur)
    parole = tempi_parole(testo, parl)
    ass = os.path.join(tmp, codice + ".ass"); scrivi_ass(ass, blocchi(parole), G)
    # stacchi sulla carta: ai silenzi più vicini a 9 s, 20 s, 31 s… (durata 1.6 s)
    sil_fine = [parl[i][1] for i in range(len(parl) - 1)]
    st = []
    t = 9.0
    while t < dur - 6:
        if sil_fine:
            c = min(sil_fine, key=lambda x: abs(x - t))
            if abs(c - t) < 4 and (not st or c - st[-1] > 6): st.append(c)
        t += 11
    gj, cj, sj, fj = [os.path.join(tmp, n) for n in ("gancio_%s.jpg" % codice, "cornice_%s.png" % codice, "stacco_%s.png" % codice, "finale3.jpg")]
    gancio(num, rov, pos, gj); cornice(num, rov, pos, cj); stacco(num, rov, sj); finale(fj)
    out = os.path.join(OUT, "short3_%s.mp4" % codice)
    nfr = int(dur * FPS) + 5
    fc = []
    fc.append("[0:v]scale=-2:%d,crop=1080:%d:(iw-1080)/2+60:0,setsar=1,fps=%d,"
              "zoompan=z='min(1+0.0009*on,1.10)':x='iw/2-(iw/zoom/2)':y='ih/3-(ih/zoom/3)':d=1:s=1080x%d:fps=%d[lv]" % (VH, VH, FPS, VH, FPS))
    fc.append("color=c=0x0b0b0b:s=%dx%d:r=%d:d=%.2f[bg]" % (W, H, FPS, dur))
    fc.append("[bg][lv]overlay=0:%d:shortest=1[a1]" % VY)
    cur = "a1"
    for i, t0 in enumerate(st):
        fc.append("[3:v]format=rgba,fade=t=in:st=%.2f:d=0.2:alpha=1,fade=t=out:st=%.2f:d=0.2:alpha=1[s%d]" % (t0, t0 + 1.4, i))
        fc.append("[%s][s%d]overlay=0:%d:enable='between(t,%.2f,%.2f)'[c%d]" % (cur, i, VY, t0, t0 + 1.6, i)); cur = "c%d" % i
    fc.append("[%s][2:v]overlay=0:0[fr]" % cur)
    fc.append("[fr]subtitles=%s:fontsdir=%s[sb]" % (ass.replace(":", "\\:"), FONTS.replace(":", "\\:")))
    fc.append("[1:v]scale=1188:2112,zoompan=z='1+0.07*on/%d':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=%dx%d:fps=%d,"
              "format=rgba,fade=t=out:st=%.2f:d=0.3:alpha=1[gk]" % (int(G*FPS), W, H, FPS, G - 0.3))
    fc.append("[sb][gk]overlay=0:0:enable='lte(t,%.2f)'[vm]" % G)
    fc.append("[4:v]scale=%d:%d,setsar=1,fps=%d,fade=t=in:st=0:d=0.3[fin]" % (W, H, FPS))
    fc.append("anullsrc=r=44100:cl=stereo,atrim=0:%.2f[sil]" % F)
    fc.append("[0:a]aresample=44100,aformat=channel_layouts=stereo,afade=t=out:st=%.2f:d=0.6[au]" % (dur - 0.6))
    fc.append("[vm][au][fin][sil]concat=n=2:v=1:a=1[v][a]")
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-i", src, "-loop", "1", "-framerate", str(FPS), "-t", "%.2f" % (G + 0.2), "-i", gj,
           "-loop", "1", "-t", "%.2f" % dur, "-i", cj, "-loop", "1", "-t", "%.2f" % dur, "-i", sj,
           "-loop", "1", "-t", "%.2f" % F, "-i", fj,
           "-filter_complex", ";".join(fc), "-map", "[v]", "-map", "[a]",
           "-c:v", "libx264", "-preset", "veryfast", "-crf", "21", "-pix_fmt", "yuv420p",
           "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", out]
    subprocess.run(cmd, check=True)
    print("fatto", out, "stacchi:", ["%.1f" % x for x in st])

if __name__ == "__main__":
    for c in sys.argv[1:]: video(c)
