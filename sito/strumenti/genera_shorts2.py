# 22 Arcani – secondo blocco di Shorts: gancio iniziale + cornice + finale con invito al sito
# Uso: python3 strumenti/genera_shorts2.py [codice ...]   (es. 06_gli_amanti_r_Presente)
import os, sys, subprocess
from PIL import Image, ImageDraw, ImageFont, ImageFilter

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "youtube_grafica", "shorts2")
FONTS = os.path.expanduser("~/fonts")
W, H = 1080, 1920
TURCH = (64, 224, 208)
BIANCO = (238, 238, 238)
GRIGIO = (170, 170, 170)
NERO = (11, 11, 11)

# numero: (nome, genere m/f/p)
CARTE = {
 0:("Il Matto","m"),1:("Il Mago","m"),2:("La Papessa","f"),3:("L'Imperatrice","f"),
 4:("L'Imperatore","m"),5:("Il Papa","m"),6:("Gli Amanti","p"),7:("Il Carro","m"),
 8:("La Forza","f"),9:("L'Eremita","m"),10:("La Ruota della Fortuna","f"),11:("La Giustizia","f"),
 12:("L'Appeso","m"),13:("La Morte","f"),14:("La Temperanza","f"),15:("Il Diavolo","m"),
 16:("La Torre","f"),17:("La Stella","f"),18:("La Luna","f"),19:("Il Sole","m"),
 20:("Il Giudizio","m"),21:("Il Mondo","m")}
ROV = {"m":"rovesciato","f":"rovesciata","p":"rovesciati"}
USCITA = {"m":"Ti è uscito","f":"Ti è uscita","p":"Ti sono usciti"}
POS = {"Passato":"nel passato","Presente":"nel presente","Futuro":"nel futuro"}

def font(nome, size, wght=None):
    f = ImageFont.truetype(os.path.join(FONTS, nome), size)
    if wght:
        try: f.set_variation_by_axes([wght])
        except Exception: pass
    return f

def stella(d, cx, cy, r, col):
    import math
    pts=[]
    for i in range(8):
        a=math.pi/4*i - math.pi/2; rr = r if i%2==0 else r*0.28
        pts.append((cx+rr*math.cos(a), cy+rr*math.sin(a)))
    d.polygon(pts, fill=col)

def testo_centrato(d, y, txt, f, col, glow=False, img=None):
    w = d.textlength(txt, font=f); x = (W - w) / 2
    if glow and img is not None:
        g = Image.new("RGBA", img.size, (0,0,0,0)); gd = ImageDraw.Draw(g)
        gd.text((x, y), txt, font=f, fill=TURCH + (200,))
        g = g.filter(ImageFilter.GaussianBlur(14)); img.alpha_composite(g)
        d = ImageDraw.Draw(img)
    d.text((x, y), txt, font=f, fill=col)
    return d

def adatta(d, txt, nome, size, maxw, wght=None):
    while size > 30:
        f = font(nome, size, wght)
        if d.textlength(txt, font=f) <= maxw: return f
        size -= 4
    return font(nome, size, wght)

def carta_img(num, rov, altezza):
    nomi = sorted(os.listdir(os.path.join(BASE, "asset", "img_it")))
    fn = [n for n in nomi if n.startswith("%02d_" % num)][0]
    c = Image.open(os.path.join(BASE, "asset", "img_it", fn)).convert("RGBA")
    c = c.resize((int(c.width * altezza / c.height), altezza), Image.LANCZOS)
    if rov: c = c.rotate(180)
    m = Image.new("L", c.size, 0); ImageDraw.Draw(m).rounded_rectangle([0,0,c.width-1,c.height-1], radius=int(altezza*0.03), fill=255)
    c.putalpha(m)
    return c

def con_alone(base, img, xy, raggio=28):
    g = Image.new("RGBA", base.size, (0,0,0,0))
    sag = Image.new("RGBA", img.size, TURCH + (255,)); sag.putalpha(img.split()[3])
    g.alpha_composite(sag, xy); g = g.filter(ImageFilter.GaussianBlur(raggio))
    base.alpha_composite(g); base.alpha_composite(img, xy)

def sfondo():
    im = Image.new("RGBA", (W, H), NERO + (255,))
    g = Image.new("RGBA", (W, H), (0,0,0,0)); ImageDraw.Draw(g).ellipse([-200, 300, W+200, 1500], fill=(20, 70, 66, 255))
    im.alpha_composite(g.filter(ImageFilter.GaussianBlur(160)))
    return im

def cornice(num, rov, pos, path):
    nome, gen = CARTE[num]
    im = Image.new("RGBA", (W, H), (0,0,0,0)); d = ImageDraw.Draw(im)
    d.rectangle([0,0,W,438], fill=NERO+(255,)); d.rectangle([0,1672,W,H], fill=NERO+(255,))
    g = Image.new("RGBA", (W, H), (0,0,0,0)); ImageDraw.Draw(g).ellipse([-300,-500,900,300], fill=(20,60,58,255))
    g = g.filter(ImageFilter.GaussianBlur(120)); m = Image.new("L",(W,H),0); ImageDraw.Draw(m).rectangle([0,0,W,438], fill=255)
    im.paste(g, (0,0), Image.composite(g.split()[3], m, m))
    d = ImageDraw.Draw(im)
    for y in (438, 1670): d.rectangle([0,y,W,y+2], fill=TURCH+(255,))
    c = carta_img(num, rov, 338); con_alone(im, c, (60, 50), 14)
    d = ImageDraw.Draw(im)
    ft = adatta(d, nome.upper(), "CinzelDecorative-Bold.ttf", 92, 740)
    d.text((300, 92), nome.upper(), font=ft, fill=TURCH)
    sub = (ROV[gen].upper() + " · " if rov else "") + POS[pos].upper()
    d.text((300, 215), sub, font=adatta(d, sub, "Cinzel[wght].ttf", 50, 740, 500), fill=BIANCO)
    d.text((300, 292), "cosa significa?", font=font("PlayfairDisplay[wght].ttf", 40), fill=GRIGIO)
    testo_centrato(d, 1722, "Qual è la TUA carta? Scoprilo gratis", font("PlayfairDisplay[wght].ttf", 40), BIANCO)
    fz = font("Cinzel[wght].ttf", 66, 700)
    d = testo_centrato(d, 1790, "22ARCANI.IT/YT", fz, TURCH, glow=True, img=im)
    wz = d.textlength("22ARCANI.IT/YT", font=fz)
    stella(d, (W-wz)/2 - 45, 1828, 24, TURCH); stella(d, (W+wz)/2 + 45, 1828, 24, TURCH)
    im.save(path)

def gancio(num, rov, pos, path):
    nome, gen = CARTE[num]
    im = sfondo(); d = ImageDraw.Draw(im)
    domanda = USCITA[gen] + (" " + ROV[gen] if rov else "")
    testo_centrato(d, 170, domanda, font("PlayfairDisplay-Italic[wght].ttf", 70), BIANCO)
    if len(nome) > 16:
        parole = nome.upper().split(" "); a = " ".join(parole[:2]); b = " ".join(parole[2:])
        fn = font("CinzelDecorative-Bold.ttf", 110)
        d = testo_centrato(d, 265, a, fn, TURCH, glow=True, img=im)
        d = testo_centrato(d, 380, b, fn, TURCH, glow=True, img=im)
        testo_centrato(d, 515, POS[pos] + "?", font("PlayfairDisplay-Italic[wght].ttf", 64), BIANCO)
        c = carta_img(num, rov, 960); con_alone(im, c, ((W - c.width)//2, 650), 40)
    else:
        d = testo_centrato(d, 270, nome.upper(), adatta(d, nome.upper(), "CinzelDecorative-Bold.ttf", 120, 980), TURCH, glow=True, img=im)
        testo_centrato(d, 410, POS[pos] + "?", font("PlayfairDisplay-Italic[wght].ttf", 64), BIANCO)
        c = carta_img(num, rov, 1060); con_alone(im, c, ((W - c.width)//2, 560), 40)
    d = ImageDraw.Draw(im)
    testo_centrato(d, 1700, "Ascolta cosa ti dice", font("PlayfairDisplay[wght].ttf", 48), GRIGIO)
    d.polygon([(W/2-22,1790),(W/2+22,1790),(W/2,1818)], fill=TURCH)
    im.convert("RGB").save(path)

def finale(path):
    im = sfondo(); d = ImageDraw.Draw(im)
    testo_centrato(d, 380, "E la TUA carta,", font("PlayfairDisplay-Italic[wght].ttf", 84), BIANCO)
    testo_centrato(d, 490, "qual è?", font("PlayfairDisplay-Italic[wght].ttf", 84), BIANCO)
    testo_centrato(d, 700, "Scegli 3 carte e scopri", font("PlayfairDisplay[wght].ttf", 56), GRIGIO)
    testo_centrato(d, 775, "passato, presente e futuro", font("PlayfairDisplay[wght].ttf", 56), GRIGIO)
    d = testo_centrato(d, 960, "LETTURA GRATIS", font("Cinzel[wght].ttf", 80, 700), BIANCO)
    d = testo_centrato(d, 1080, "22ARCANI.IT", font("CinzelDecorative-Bold.ttf", 118), TURCH, glow=True, img=im)
    d.rounded_rectangle([190, 1330, 890, 1450], radius=60, outline=TURCH, width=4)
    testo_centrato(d, 1360, "Link nel commento in alto", font("PlayfairDisplay[wght].ttf", 46), BIANCO)
    stella(d, W/2, 1600, 50, TURCH)
    im.convert("RGB").save(path)

def video(codice):
    p = codice.split("_"); num = int(p[0]); pos = p[-1]; rov = "_r_" in codice
    src = os.path.join(BASE, "asset", "video_it", codice + ".mp4")
    cpng = os.path.join(OUT, "cornice_" + codice + ".png"); gpng = os.path.join(OUT, "gancio_" + codice + ".jpg")
    fpng = os.path.join(OUT, "finale.jpg"); out = os.path.join(OUT, "short2_" + codice + ".mp4")
    cornice(num, rov, pos, cpng); gancio(num, rov, pos, gpng)
    finale(fpng)
    dur = float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","default=nw=1:nk=1",src]).decode())
    G, F = 2.2, 3.5
    flt = (
      "[0:v]scale=-2:1230,crop=1080:1230:(iw-1080)/2+60:0,pad=1080:1920:0:440:color=0x0b0b0b,setsar=1,fps=25[v];"
      "[v][1:v]overlay=0:0[vc];"
      "[2:v]scale=1080:1920,setsar=1,format=rgba,fade=t=out:st=%.2f:d=0.4:alpha=1[g];" % (G-0.4) +
      "[vc][g]overlay=0:0:enable='lte(t,%.2f)',format=yuv420p[main];" % G +
      "[3:v]scale=1080:1920,setsar=1,fps=25,fade=t=in:st=0:d=0.4,format=yuv420p[fin];"
      "[0:a]aresample=44100,afade=t=out:st=%.2f:d=0.8[a0];" % (dur-0.8) +
      "anullsrc=r=44100:cl=stereo,atrim=0:%.2f[a1];" % F +
      "[main][a0][fin][a1]concat=n=2:v=1:a=1[ov][oa]")
    cmd = ["ffmpeg","-v","error","-y","-i",src,"-i",cpng,"-loop","1","-t","%.2f" % (G+0.1),"-i",gpng,"-loop","1","-t","%.2f" % F,"-i",fpng,
           "-filter_complex",flt,"-map","[ov]","-map","[oa]","-c:v","libx264","-preset","veryfast","-crf","21","-c:a","aac","-b:a","160k","-movflags","+faststart",out+".tmp.mp4"]
    subprocess.check_call(cmd); os.replace(out+".tmp.mp4", out)
    print("fatto", out)

if __name__ == "__main__":
    for c in sys.argv[1:]: video(c)
