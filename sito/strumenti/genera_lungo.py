# 22 Arcani – video lungo "Scegli una carta" (16:9) con i video della lettrice.
# Uso: python3 strumenti/genera_lungo.py <nome> <titolo_riga2> <codice1> <codice2> <codice3>
# es.: python3 strumenti/genera_lungo.py futuro_01 "Cosa ti riserva il futuro?" 19_il_sole_Futuro 10_la_ruota_della_fortuna_Futuro 17_la_stella_Futuro
import os, sys, re, subprocess, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import genera_shorts3 as g3
from PIL import Image, ImageDraw, ImageFilter

BASE = g3.BASE; FPS = 25; W, H = 1920, 1080
TURCH, BIANCO, GRIGIO, NERO = g3.TURCH, g3.BIANCO, g3.GRIGIO, g3.NERO
nome, riga2, codici = sys.argv[1], sys.argv[2], sys.argv[3:6]
OUT = os.path.join(BASE, "youtube_grafica", "lunghi"); TMP = os.path.join(OUT, "_tmp_" + nome)
os.makedirs(TMP, exist_ok=True)
F = lambda n, s, w=None: g3.font(n, s, w)

def sfondo():
    im = Image.new("RGBA", (W, H), NERO + (255,))
    gl = Image.new("RGBA", (W, H), (0,0,0,0)); ImageDraw.Draw(gl).ellipse([200, 100, W-200, H+300], fill=(20, 70, 66, 255))
    im.alpha_composite(gl.filter(ImageFilter.GaussianBlur(220))); return im

def cx(im, y, txt, f, col, glow=False, x0=0, w=W):
    d = ImageDraw.Draw(im); tw = d.textlength(txt, font=f); x = x0 + (w - tw) / 2
    if glow:
        gl = Image.new("RGBA", im.size, (0,0,0,0)); ImageDraw.Draw(gl).text((x, y), txt, font=f, fill=TURCH + (200,))
        im.alpha_composite(gl.filter(ImageFilter.GaussianBlur(16)))
    ImageDraw.Draw(im).text((x, y), txt, font=f, fill=col)

def carta(path_or_num, h, rov=False):
    if isinstance(path_or_num, int):
        f = [x for x in os.listdir(os.path.join(BASE, "asset", "img_it")) if x.startswith("%02d_" % path_or_num)][0]
        c = Image.open(os.path.join(BASE, "asset", "img_it", f)).convert("RGBA")
    else:
        c = Image.open(path_or_num).convert("RGBA")
    c = c.resize((int(c.width * h / c.height), h), Image.LANCZOS)
    m = Image.new("L", c.size, 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, c.width-1, c.height-1], radius=int(h*0.04), fill=255)
    c.putalpha(m)
    return c.rotate(180) if rov else c

def alone(im, c, xy, r=40):
    sh = Image.new("RGBA", im.size, (0,0,0,0))
    sh.paste(Image.new("RGBA", c.size, TURCH + (170,)), xy, c)
    im.alpha_composite(sh.filter(ImageFilter.GaussianBlur(r))); im.alpha_composite(c, xy)

DORSO = os.path.join(BASE, "asset", "dorso.jpeg")
def tre_dorsi(im, y, h, numeri=True, evid=None):
    c = carta(DORSO, h); gap = 120; tot = 3 * c.width + 2 * gap; x = (W - tot) // 2
    for i in range(3):
        xi = x + i * (c.width + gap)
        alone(im, c, (xi, y), 50 if evid == i else 28)
        if numeri: cx(im, y + h + 18, str(i + 1), F("Cinzel[wght].ttf", 72, 600), TURCH, True, xi, c.width)

def intro(path):
    im = sfondo()
    cx(im, 40, "SCEGLI UNA CARTA", F("Cinzel[wght].ttf", 96, 600), TURCH, True)
    cx(im, 165, riga2, F("Cinzel[wght].ttf", 60, 600), BIANCO)
    tre_dorsi(im, 270, 560)
    cx(im, 975, "Respira, pensa alla tua domanda… e scegli 1, 2 o 3", F("Cinzel[wght].ttf", 46, 600), GRIGIO)
    im.convert("RGB").save(path)

def conta(path, n):
    im = sfondo()
    cx(im, 60, "Hai scelto?", F("Cinzel[wght].ttf", 70, 600), BIANCO)
    tre_dorsi(im, 230, 440, numeri=True)
    cx(im, 760, str(n), F("Cinzel[wght].ttf", 230, 600), TURCH, True)
    im.convert("RGB").save(path)

def info(cod):
    p = cod.split("_"); num = int(p[0]); pos = p[-1]; rov = "_r_" in cod
    nomec, gen = g3.CARTE[num]
    sotto = (g3.ROV[gen] + " · " if rov else "") + g3.POS[pos]
    return num, rov, nomec, sotto

def rivela(path, i, cod, dorso=False):
    num, rov, nomec, sotto = info(cod)
    im = sfondo()
    cx(im, 40, "CARTA %d" % (i + 1), F("Cinzel[wght].ttf", 64, 700), BIANCO)
    c = carta(DORSO, 760) if dorso else carta(num, 760, rov)
    alone(im, c, ((W - c.width) // 2, 140), 50)
    if not dorso:
        cx(im, 930, nomec.upper() + "  ·  " + sotto, F("Cinzel[wght].ttf", 56, 700), TURCH, True)
    im.convert("RGB").save(path)

def cornice(path, i, cod):
    num, rov, nomec, sotto = info(cod)
    im = Image.new("RGBA", (W, H), (0,0,0,0))
    bg = sfondo(); bg.paste((0,0,0,0), (60, 150, 60 + 1344, 150 + 756)); im = bg
    d = ImageDraw.Draw(im); d.rectangle([56, 146, 60 + 1344 + 3, 150 + 756 + 3], outline=TURCH, width=3)
    d.text((60, 45), "CARTA %d  ·  %s" % (i + 1, nomec.upper()), font=F("Cinzel[wght].ttf", 64, 600), fill=TURCH)
    c = carta(num, 620, rov); alone(im, c, (1404 + (516 - c.width) // 2, 180), 36)
    cx(im, 830, nomec.upper(), g3.adatta(ImageDraw.Draw(im), nomec.upper(), "Cinzel[wght].ttf", 40, 480, 700), BIANCO, False, 1404, 516)
    cx(im, 885, sotto, F("Cinzel[wght].ttf", 32, 500), GRIGIO, False, 1404, 516)
    cx(im, 932, "Lettura completa gratis:  22ARCANI.IT", F("Cinzel[wght].ttf", 38, 700), TURCH)
    im.save(path)

def finale(path):
    im = sfondo()
    cx(im, 110, "E se le carte fossero le TUE?", F("Cinzel[wght].ttf", 76, 600), BIANCO)
    cx(im, 230, "Passato · Presente · Futuro: la tua lettura con 3 carte", F("Cinzel[wght].ttf", 48, 600), GRIGIO)
    cx(im, 380, "GRATIS SU", F("Cinzel[wght].ttf", 70, 700), BIANCO)
    cx(im, 470, "22ARCANI.IT", F("Cinzel[wght].ttf", 150, 600), TURCH, True)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([560, 720, 1360, 830], radius=40, fill=(16, 52, 50, 255), outline=TURCH, width=4)
    cx(im, 742, "Il link è nella descrizione", F("Cinzel[wght].ttf", 46, 700), BIANCO)
    d.polygon([(935, 850), (985, 850), (960, 885)], fill=TURCH)
    cx(im, 900, "Iscriviti: ogni settimana una nuova lettura", F("Cinzel[wght].ttf", 44, 600), GRIGIO)
    im.convert("RGB").save(path)

def miniatura(path):
    im = sfondo()
    c = carta(DORSO, 520); gap = 50; x = (W - (3 * c.width + 2 * gap)) // 2
    for i in range(3): alone(im, c, (x + i * (c.width + gap), 470), 40)
    cx(im, 40, "SCEGLI", F("Cinzel[wght].ttf", 190, 600), TURCH, True)
    cx(im, 250, "UNA CARTA", F("Cinzel[wght].ttf", 150, 600), BIANCO, True)
    im.convert("RGB").resize((1280, 720), Image.LANCZOS).save(path, quality=92)

# --- audio di sottofondo sintetico (tenue) per le parti senza voce ---
def pad(dur, path):
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi", "-i",
        "aevalsrc='0.05*sin(2*PI*110*t)*(0.6+0.4*sin(2*PI*0.2*t))+0.035*sin(2*PI*164.8*t)*(0.6+0.4*sin(2*PI*0.13*t+1))+0.025*sin(2*PI*220*t)*(0.6+0.4*sin(2*PI*0.17*t+2))+0.015*sin(2*PI*329.6*t)':s=44100:d=%.2f" % dur,
        "-af", ("lowpass=f=900,afade=t=in:d=1,afade=t=out:st=%.2f:d=1,aformat=channel_layouts=stereo" % (dur - 1)) if dur > 3 else "lowpass=f=900,aformat=channel_layouts=stereo", path], check=True)

def seg_img(img, dur, out, zoom=True, audio=True):
    a = os.path.join(TMP, os.path.basename(out) + ".wav"); pad(dur, a)
    z = "zoompan=z='1+0.04*on/%d':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=%dx%d:fps=%d" % (int(dur*FPS), W, H, FPS) if zoom else "fps=%d" % FPS
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-loop", "1", "-framerate", str(FPS), "-t", "%.2f" % dur, "-i", img, "-i", a,
        "-filter_complex", "[0:v]scale=%d:%d,%s,format=yuv420p%s[v]" % (W*1.1 if zoom else W, H*1.1 if zoom else H, z, (",fade=t=in:d=0.4,fade=t=out:st=%.2f:d=0.4" % (dur - 0.4)) if zoom else ""),
        "-map", "[v]", "-map", "1:a", "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-c:a", "aac", "-b:a", "160k", "-shortest", out], check=True)

def seg_rivela(i, cod, out):
    d1, d2 = os.path.join(TMP, "riv_d%d.png" % i), os.path.join(TMP, "riv_f%d.png" % i)
    rivela(d1, i, cod, dorso=True); rivela(d2, i, cod)
    dur = 4.0; a = os.path.join(TMP, "riv%d.wav" % i); pad(dur, a)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-loop", "1", "-framerate", str(FPS), "-t", "%.2f" % dur, "-i", d1,
        "-loop", "1", "-framerate", str(FPS), "-t", "%.2f" % dur, "-i", d2, "-i", a,
        "-filter_complex", "[0:v][1:v]xfade=transition=fade:duration=0.7:offset=1.2,format=yuv420p,fade=t=in:d=0.3[v]",
        "-map", "[v]", "-map", "2:a", "-t", "%.2f" % dur, "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-c:a", "aac", "-b:a", "160k", out], check=True)
    return dur

def seg_lettrice(i, cod, out):
    src = os.path.join(BASE, "asset", "video_it", cod + ".mp4")
    testo = re.sub(r"[*#_]", "", open(os.path.join(BASE, "asset", "descrizione_it", cod + ".md"), encoding="utf-8").read()).replace("\n", " ").strip()
    dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", src]).decode())
    bl = g3.blocchi(g3.tempi_parole(testo, g3.silenzi(src, dur)), 5)
    ass = os.path.join(TMP, "sub%d.ass" % i)
    with open(ass, "w", encoding="utf-8") as f:
        f.write("[Script Info]\nScriptType: v4.00+\nPlayResX: 1920\nPlayResY: 1080\n\n[V4+ Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n"
                "Style: Sub,Poppins,62,&H00FFFFFF,&H00FFFFFF,&H00000000,&H96000000,1,0,0,0,100,100,0,0,1,5,2,2,60,576,200,1\n\n[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n")
        for k, (t, a, b) in enumerate(bl):
            nb = bl[k+1][1] if k + 1 < len(bl) else b + 0.3
            f.write("Dialogue: 0,%s,%s,Sub,,0,0,0,,%s\n" % (g3.ts(a), g3.ts(max(b, min(nb, b + 0.4))), t.replace("’", "'")))
    cj = os.path.join(TMP, "cornice%d.png" % i); cornice(cj, i, cod)
    fc = ("[0:v]scale=1344:756,setsar=1,fps=%d[lv];[1:v]fps=%d[cf];[cf][lv]overlay=60:150:shortest=1[a];"
          "[a]subtitles=%s:fontsdir=%s,format=yuv420p,fade=t=in:d=0.4,fade=t=out:st=%.2f:d=0.4[v];"
          "[0:a]aresample=44100,aformat=channel_layouts=stereo,afade=t=out:st=%.2f:d=0.5[au]") % (FPS, FPS, ass.replace(":", "\\:"), g3.FONTS.replace(":", "\\:"), dur - 0.4, dur - 0.5)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", src, "-loop", "1", "-framerate", str(FPS), "-t", "%.2f" % dur, "-i", cj,
        "-filter_complex", fc, "-map", "[v]", "-map", "[au]", "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-c:a", "aac", "-b:a", "160k", out], check=True)
    return dur

if __name__ == "__main__":
    import json
    def dur(o): return float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",o]).decode())
    def fatto(o): return os.path.exists(o) and os.path.getsize(o) > 10000
    durf = os.path.join(TMP, "durate.json"); dd = json.load(open(durf)) if os.path.exists(durf) else {}
    def salva(): json.dump(dd, open(durf, "w"))
    parti, capitoli, t = [], [], 0.0
    ij = os.path.join(TMP, "intro.jpg"); o = os.path.join(TMP, "p00.mp4")
    if not fatto(o): intro(ij); seg_img(ij, 12, o)
    parti.append(o); capitoli.append((0, "Scegli la tua carta")); t += dur(o)
    for n in (5, 4, 3, 2, 1):
        cj = os.path.join(TMP, "c%d.jpg" % n); o = os.path.join(TMP, "p0c%d.mp4" % n)
        if not fatto(o): conta(cj, n); seg_img(cj, 1.0, o, zoom=False)
        parti.append(o); t += dur(o)
    for i, cod in enumerate(codici):
        num, rov, nomec, sotto = info(cod)
        capitoli.append((t, "Carta %d – %s" % (i + 1, nomec)))
        o = os.path.join(TMP, "p%d1.mp4" % (i + 1))
        if not fatto(o): dd[o] = seg_rivela(i, cod, o); salva()
        t += dur(o); parti.append(o)
        o = os.path.join(TMP, "p%d2.mp4" % (i + 1))
        if not fatto(o): dd[o] = seg_lettrice(i, cod, o); salva(); print("parte", o); sys.exit(0)
        t += dur(o); parti.append(o)
    capitoli.append((t, "La tua lettura gratis"))
    fj = os.path.join(TMP, "finale.jpg"); o = os.path.join(TMP, "p9.mp4")
    if not fatto(o): finale(fj); seg_img(fj, 10, o)
    parti.append(o)
    lst = os.path.join(TMP, "lista.txt")
    with open(lst, "w") as f: f.writelines("file '%s'\n" % p for p in parti)
    out = os.path.join(OUT, "lungo_%s.mp4" % nome)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst,
                    "-c", "copy", "-movflags", "+faststart", out], check=True)
    miniatura(os.path.join(OUT, "miniatura_%s.jpg" % nome))
    with open(os.path.join(OUT, "capitoli_%s.txt" % nome), "w", encoding="utf-8") as f:
        for s, txt in capitoli: f.write("%d:%02d %s\n" % (int(s) // 60, int(s) % 60, txt))
    print("fatto", out)
