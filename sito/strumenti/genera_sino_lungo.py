# Zodiel – video lungo 16:9 "Tarocchi sì o no: scegli una carta" con la voce di Google (Despina).
# Riprendibile: ogni chiamata crea i pezzi mancanti (max ~150 s di lavoro) e alla fine li unisce.
# Uso: python3 strumenti/genera_sino_lungo.py      (ripetere finché stampa "FINITO")
import os, sys, json, time, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import genera_shorts3 as g3
import genera_lettura as gl
from PIL import Image, ImageDraw, ImageFilter

BASE = g3.BASE; W, H = 1920, 1080
TURCH, BIANCO, GRIGIO, NERO = g3.TURCH, g3.BIANCO, g3.GRIGIO, g3.NERO
VERDE, ROSSO, GIALLO = (63, 224, 160), (255, 107, 107), (242, 201, 76)
CIN = lambda s, w=600: g3.font("Cinzel[wght].ttf", s, w)
POP = lambda s: g3.font("Poppins-Bold.ttf", s)
OUT = os.path.join(BASE, "youtube_grafica", "lunghi"); TMP = os.path.join(OUT, "_tmp_sino_02")
os.makedirs(TMP, exist_ok=True)
T0 = time.time()
A = (lambda a: json.loads(a[a.index("{"):a.rindex("}") + 1]))(open(os.path.join(BASE, "sintesi_dati.js"), encoding="utf-8").read())
R = {"00_il_matto": ("si", "no"), "01_il_mago": ("si", "no"), "02_la_papessa": ("forse", "no"),
     "03_l_imperatrice": ("si", "forse"), "04_l_imperatore": ("si", "no"), "05_il_papa": ("si", "no"),
     "06_gli_amanti": ("si", "no"), "07_il_carro": ("si", "no"), "08_la_forza": ("si", "forse"),
     "09_l_eremita": ("forse", "no"), "10_la_ruota_della_fortuna": ("si", "no"), "11_la_giustizia": ("si", "no"),
     "12_l_appeso": ("forse", "no"), "13_la_morte": ("no", "forse"), "14_la_temperanza": ("si", "forse"),
     "15_il_diavolo": ("no", "forse"), "16_la_torre": ("no", "no"), "17_la_stella": ("si", "forse"),
     "18_la_luna": ("forse", "no"), "19_il_sole": ("si", "si"), "20_il_giudizio": ("si", "no"), "21_il_mondo": ("si", "forse")}
ETI = {"si": "SÌ", "no": "NO", "forse": "FORSE"}; COL = {"si": VERDE, "no": ROSSO, "forse": GIALLO}
PAROLA = {"si": "sì", "no": "no", "forse": "forse"}
SCELTE = ["19_il_sole", "16_la_torre", "18_la_luna"]
TESTI_CARTE = [
 "Hai scelto la carta numero uno? È il Sole, e la risposta è un sì luminoso. Il Sole è una delle carte più positive di tutto il mazzo: parla di gioia, successo e vitalità. Se la tua domanda riguarda l'amore, indica un sentimento sincero e un periodo sereno. Se riguarda il lavoro o un progetto, annuncia risultati concreti e riconoscimenti. Le situazioni si chiariscono e i dubbi si dissolvono. Il Sole è così positivo che dice sì perfino quando esce rovesciato: in quel caso il successo arriva, ma con un po' di ritardo. Il consiglio della carta: goditi questo momento e condividi la tua gioia con chi ami.",
 "Hai scelto la carta numero due? È la Torre, e la risposta, per ora, è no. La Torre rappresenta un cambiamento improvviso, qualcosa che crolla per lasciare spazio al nuovo. Non è una carta da temere: dice che la strada che immagini non è quella giusta, o che non è ancora il momento. Se la tua domanda riguarda una relazione, forse qualcosa deve essere chiarito prima di andare avanti. Se riguarda il lavoro, potrebbe arrivare una svolta inattesa, diversa da quella che speri. Il messaggio della Torre è che a volte un no apre la porta a qualcosa di più autentico. Il consiglio: non aggrapparti a ciò che sta cambiando, e lascia andare ciò che non regge più.",
 "Hai scelto la carta numero tre? È la Luna, e la risposta è: forse. La Luna è la carta del mistero, dell'intuizione e delle cose non ancora chiare. Dice che mancano delle informazioni, o che la situazione è ancora in movimento. Se la tua domanda riguarda una persona, potrebbe esserci qualcosa che non conosci ancora. Se riguarda una scelta, è meglio aspettare prima di decidere. La Luna ti invita ad ascoltare il tuo istinto, ma anche a non lasciarti guidare dalle paure. Tra qualche giorno prova a rifare la domanda: la risposta potrebbe diventare più chiara. Il consiglio: osserva, ascolta, e non avere fretta."]
IDS = sorted(A)
def riga_voce(i):
    d, (a, b) = A[i]["nome"], R[i]
    return "%s: dritta %s, rovesciata %s." % (d, PAROLA[a], PAROLA[b]) if A[i]["genere"] == "f" else \
           ("%s: dritti %s, rovesciati %s." % (d, PAROLA[a], PAROLA[b]) if A[i]["genere"] == "p" else "%s: dritto %s, rovesciato %s." % (d, PAROLA[a], PAROLA[b]))
SEG = [
 ("intro", "Ciao, qui è Zodiel. Hai una domanda e cerchi una risposta semplice: sì o no? In questo video sono le carte dei tarocchi a risponderti. Pensa a una domanda chiara, che riguardi te e a cui si possa rispondere con un sì o con un no. Per esempio: questa persona tornerà da me? Troverò un nuovo lavoro? È il momento giusto per cambiare casa?", 0),
 ("scelta", "Ora chiudi gli occhi per un momento, respira profondamente e concentrati sulla tua domanda. Davanti a te ci sono tre carte coperte. Scegli quella che ti attira di più: la uno, la due o la tre. Scrivi nei commenti il numero che hai scelto. Poi vai al capitolo della tua carta, oppure continua a guardare per scoprirle tutte.", 6),
 ("carta1", TESTI_CARTE[0], 0), ("carta2", TESTI_CARTE[1], 0), ("carta3", TESTI_CARTE[2], 0),
 ("tabella1", "Ecco ora le risposte di tutti i ventidue Arcani Maggiori, così potrai usarle anche con il tuo mazzo. " + " ".join(riga_voce(i) for i in IDS[:11]), 0),
 ("tabella2", "Continuiamo. " + " ".join(riga_voce(i) for i in IDS[11:]), 0),
 ("finale", "Vuoi fare la tua domanda con una carta tutta per te? Sul sito 22arcani.it, nella pagina sì o no, scegli l'argomento: amore, lavoro, fortuna o benessere. Poi scegli la tua domanda e pesca la tua carta. È gratis. Se questo video ti è stato utile, iscriviti al canale: ogni giorno alle dodici c'è una nuova lettura dei tarocchi. Ricorda che i tarocchi sono uno spunto di riflessione, non una previsione certa. A presto!", 0)]

# ---------------- grafica ----------------
def sfondo(piede=True):
    im = Image.new("RGBA", (W, H), NERO + (255,))
    g = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(g).ellipse([200, 100, W - 200, H + 300], fill=(20, 70, 66, 255))
    im.alpha_composite(g.filter(ImageFilter.GaussianBlur(220)))
    if piede:
        d = ImageDraw.Draw(im); f = CIN(30, 600); t = "·  ZODIEL.CLOUD  ·"
        d.text(((W - d.textlength(t, font=f)) / 2, H - 60), t, font=f, fill=TURCH)
    return im
def cx(im, y, t, f, col, x0=0, w=W, glow=False):
    d = ImageDraw.Draw(im); x = x0 + (w - d.textlength(t, font=f)) / 2
    if glow:
        g = Image.new("RGBA", im.size, (0, 0, 0, 0)); ImageDraw.Draw(g).text((x, y), t, font=f, fill=col + (220,))
        im.alpha_composite(g.filter(ImageFilter.GaussianBlur(18)))
    ImageDraw.Draw(im).text((x, y), t, font=f, fill=col)
def carta(fid, h, rov=False):
    p = os.path.join(BASE, "asset", "dorso.jpeg") if fid == "dorso" else os.path.join(BASE, "asset", "img_it", fid + ".jpeg")
    c = Image.open(p).convert("RGBA"); c = c.resize((int(c.width * h / c.height), h), Image.LANCZOS)
    m = Image.new("L", c.size, 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, c.width - 1, c.height - 1], radius=int(h * .04), fill=255); c.putalpha(m)
    return c.rotate(180) if rov else c
def incolla(im, c, x, y, alone=True):
    if alone:
        s = Image.new("RGBA", im.size, (0, 0, 0, 0)); ImageDraw.Draw(s).rounded_rectangle([x - 6, y - 6, x + c.width + 6, y + c.height + 6], radius=30, fill=TURCH + (160,))
        im.alpha_composite(s.filter(ImageFilter.GaussianBlur(28)))
    im.alpha_composite(c, (x, y))
def tre_dorsi(im, y, h):
    c = carta("dorso", h); gap = 90; tot = 3 * c.width + 2 * gap; x0 = (W - tot) // 2
    for k in range(3):
        x = x0 + k * (c.width + gap); incolla(im, c, x, y); cx(im, y + h + 20, str(k + 1), CIN(80, 700), TURCH, x, c.width)
def img_intro():
    im = sfondo(); cx(im, 110, "TAROCCHI", CIN(120, 700), BIANCO, glow=False)
    cx(im, 250, "SÌ o NO?", CIN(200, 800), TURCH, glow=True)
    cx(im, 520, "Pensa alla tua domanda e scegli una carta", CIN(54, 500), BIANCO)
    tre_dorsi_piccoli = carta("dorso", 300); gap = 60; x0 = (W - (3 * tre_dorsi_piccoli.width + 2 * gap)) // 2
    for k in range(3): incolla(im, tre_dorsi_piccoli, x0 + k * (tre_dorsi_piccoli.width + gap), 630)
    return im
def img_scelta():
    im = sfondo(); cx(im, 60, "Scegli una carta", CIN(90, 700), BIANCO); tre_dorsi(im, 210, 620)
    cx(im, 960, "Scrivi il tuo numero nei commenti", CIN(40, 500), GRIGIO); return im
def img_carta(k):
    fid = SCELTE[k]; r = R[fid][0]; im = sfondo(); c = carta(fid, 860); incolla(im, c, 220, 90)
    x0, w = 220 + c.width + 80, W - (220 + c.width + 80) - 120
    cx(im, 120, "CARTA %d" % (k + 1), CIN(56, 600), GRIGIO, x0, w)
    cx(im, 210, A[fid]["nome"].upper(), CIN(96, 700), BIANCO, x0, w)
    cx(im, 360, ETI[r], CIN(260, 800), COL[r], x0, w, glow=True)
    cx(im, 700, ", ".join(A[fid]["kw"][0][:3]), CIN(46, 700), TURCH, x0, w)
    righe = gl.a_capo(ImageDraw.Draw(im), "Il consiglio: " + A[fid]["consiglio"][0], CIN(42, 500), w)
    y = 800
    for rr in righe: cx(im, y, rr, CIN(42, 500), BIANCO, x0, w); y += 56
    return im
def img_tabella(parte):
    ids = IDS[:11] if parte == 0 else IDS[11:]; im = sfondo(False)
    cx(im, 30, "Le risposte dei 22 Arcani Maggiori", CIN(64, 700), BIANCO)
    d = ImageDraw.Draw(im); f, fb = CIN(48, 600), CIN(48, 800); y = 135
    d.text((330, y), "CARTA", font=CIN(34, 700), fill=GRIGIO); d.text((1130, y), "DRITTA", font=CIN(34, 700), fill=GRIGIO); d.text((1440, y), "ROVESCIATA", font=CIN(34, 700), fill=GRIGIO)
    y += 60
    for i in ids:
        a, b = R[i]; c = carta(i, 70); im.alpha_composite(c, (250, y - 8)); d = ImageDraw.Draw(im)
        d.text((330, y), A[i]["nome"], font=f, fill=BIANCO); d.text((1130, y), ETI[a], font=fb, fill=COL[a]); d.text((1440, y), ETI[b], font=fb, fill=COL[b])
        y += 78
    return im
def img_finale():
    im = sfondo(); cx(im, 120, "Fai la TUA domanda", CIN(90, 700), BIANCO)
    cx(im, 260, "amore · lavoro · fortuna · benessere", CIN(52, 500), GRIGIO)
    cx(im, 400, "ZODIEL.CLOUD/SI-O-NO", CIN(120, 700), TURCH, glow=True)
    cx(im, 570, "Gratis, senza registrazione", CIN(50, 500), BIANCO)
    d = ImageDraw.Draw(im); d.rounded_rectangle([260, 720, 1660, 860], radius=40, fill=(16, 52, 50, 255), outline=TURCH, width=5)
    cx(im, 762, "Iscriviti: ogni giorno alle 12 una nuova lettura", CIN(46, 600), BIANCO, 260, 1400); return im
IMG = {"intro": img_intro, "scelta": img_scelta, "carta1": lambda: img_carta(0), "carta2": lambda: img_carta(1), "carta3": lambda: img_carta(2),
       "tabella1": lambda: img_tabella(0), "tabella2": lambda: img_tabella(1), "finale": img_finale}

def dur(p): return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p]).decode())
ACC = ("0.20*sin(2*PI*220*t)*(0.65+0.35*sin(2*PI*0.18*t))+0.16*sin(2*PI*277.2*t)*(0.65+0.35*sin(2*PI*0.13*t+1))"
       "+0.14*sin(2*PI*329.6*t)*(0.65+0.35*sin(2*PI*0.21*t+2))+0.08*sin(2*PI*440*t)*(0.6+0.4*sin(2*PI*0.11*t+3))")
def segmento(k, nome, testo, pausa):
    out = os.path.join(TMP, "%02d_%s.mp4" % (k, nome))
    if os.path.exists(out): return out
    png = os.path.join(TMP, "%02d_%s.png" % (k, nome)); IMG[nome]().convert("RGB").save(png)
    wav = os.path.join(TMP, "%02d_%s.wav" % (k, nome)); dv = gl.parla(testo, wav)
    D = dv + 1.0 + 1.2 + pausa
    camp = "if(gte(t,0.3),(0.35*sin(2*PI*880*t)+0.2*sin(2*PI*1320*t))*exp(-2.2*(t-0.3)),0)"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-loop", "1", "-framerate", "25", "-i", png, "-i", wav, "-f", "lavfi", "-i",
        "aevalsrc='0.35*(%s)+0.5*(%s)':s=44100:d=%.2f" % (ACC, camp, D),
        "-filter_complex", "[1:a]aresample=44100,aformat=channel_layouts=stereo,adelay=1000|1000[v];[2:a]aformat=channel_layouts=stereo,volume=0.22[m];"
        "[m][v]amix=inputs=2:normalize=0:duration=first,loudnorm=I=-15:TP=-1.5:LRA=11,aresample=44100,aformat=sample_fmts=s16:channel_layouts=stereo[a];"
        "[0:v]fade=t=in:st=0:d=0.5,fade=t=out:st=%.2f:d=0.5,format=yuv420p[vv]" % (D - 0.5),
        "-map", "[vv]", "-map", "[a]", "-t", "%.2f" % D, "-c:v", "libx264", "-preset", "veryfast", "-tune", "stillimage", "-r", "25",
        "-c:a", "aac", "-b:a", "160k", out + ".tmp.mp4"], check=True)
    os.replace(out + ".tmp.mp4", out); print("pezzo", nome, "%.1fs" % D); return out

pezzi = []
for k, (nome, testo, pausa) in enumerate(SEG):
    if not os.path.exists(os.path.join(TMP, "%02d_%s.mp4" % (k, nome))) and time.time() - T0 > 100:
        print("CONTINUA: rilancia il comando"); sys.exit(0)
    pezzi.append(segmento(k, nome, testo, pausa))
lista = os.path.join(TMP, "lista.txt"); open(lista, "w").write("".join("file '%s'\n" % p for p in pezzi))
finale = os.path.join(OUT, "lungo_sino_01.mp4")
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lista, "-c", "copy", "-movflags", "+faststart", finale], check=True)
# capitoli
t, cap = 0.0, []
NOMI = {"intro": "Introduzione: come funziona", "scelta": "Scegli una carta: 1, 2 o 3", "carta1": "Carta 1", "carta2": "Carta 2", "carta3": "Carta 3",
        "tabella1": "Le risposte sì o no dei 22 Arcani (1ª parte)", "tabella2": "Le risposte sì o no dei 22 Arcani (2ª parte)", "finale": "Fai la tua domanda su 22arcani.it"}
for p, (nome, _, _) in zip(pezzi, SEG):
    cap.append("%d:%02d %s" % (int(t) // 60, int(t) % 60, NOMI[nome])); t += dur(p)
open(os.path.join(OUT, "capitoli_sino_01.txt"), "w", encoding="utf-8").write("\n".join(cap) + "\n")
# miniatura 1280x720
m = sfondo(); cx(m, 40, "TAROCCHI", CIN(110, 700), BIANCO); cx(m, 170, "SÌ o NO?", CIN(230, 800), TURCH, glow=True)
c = carta("dorso", 400); g = 70; x0 = (W - (3 * c.width + 2 * g)) // 2
for k in range(3): incolla(m, c, x0 + k * (c.width + g), 520); cx(m, 520 + 150, str(k + 1), CIN(110, 800), BIANCO, x0 + k * (c.width + g), c.width)
m.convert("RGB").resize((1280, 720), Image.LANCZOS).save(os.path.join(OUT, "miniatura_sino_01.jpg"), quality=92)
print("FINITO", finale, "%.0fs" % dur(finale)); print("\n".join(cap))
