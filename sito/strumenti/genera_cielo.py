# -*- coding: utf-8 -*-
"""
Zodiel – Calcolo del cielo (senza librerie esterne).
Crea cielo.js con, per ogni giorno: longitudine di Sole e Luna, pianeti retrogradi
ed eventi (fasi lunari esatte, equinozi/solstizi, ingressi del Sole, stazioni dei pianeti).

Uso (dalla cartella zodiel_cloud):   python strumenti/genera_cielo.py 2026 2027
Scrive cielo.js nella cartella principale del sito.
Precisione: Sole ~0,01°, Luna ~0,1°, pianeti qualche minuto d'arco: più che sufficiente
per segni zodiacali, fasi e moto retrogrado (verificato con la libreria "ephem").
"""
import os, sys, math, json, datetime as dt

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

RAD = math.pi / 180

def gj(t):  # giorno giuliano da datetime UTC
    a = (14 - t.month) // 12
    y = t.year + 4800 - a
    m = t.month + 12 * a - 3
    jdn = t.day + (153 * m + 2) // 5 + 365 * y + y // 4 - y // 100 + y // 400 - 32045
    return jdn - 0.5 + (t.hour + t.minute / 60 + t.second / 3600) / 24

def norm(x): return x % 360

# ---------- Sole (Meeus, cap. 25, bassa precisione) ----------
def sole(jd):
    T = (jd - 2451545.0) / 36525
    L0 = norm(280.46646 + 36000.76983 * T + 0.0003032 * T * T)
    M = norm(357.52911 + 35999.05029 * T - 0.0001537 * T * T)
    C = ((1.914602 - 0.004817 * T) * math.sin(M * RAD) + (0.019993 - 0.000101 * T) * math.sin(2 * M * RAD)
         + 0.000289 * math.sin(3 * M * RAD))
    om = 125.04 - 1934.136 * T
    return norm(L0 + C - 0.00569 - 0.00478 * math.sin(om * RAD))

# ---------- Luna (Meeus, cap. 47, termini principali) ----------
TERMINI_LUNA = [  # D, M, M', F, coefficiente (1e-6 gradi)
 (0,0,1,0,6288774),(2,0,-1,0,1274027),(2,0,0,0,658314),(0,0,2,0,213618),(0,1,0,0,-185116),
 (0,0,0,2,-114332),(2,0,-2,0,58793),(2,-1,-1,0,57066),(2,0,1,0,53322),(2,-1,0,0,45758),
 (0,1,-1,0,-40923),(1,0,0,0,-34720),(0,1,1,0,-30383),(2,0,0,-2,15327),(0,0,1,2,-12528),
 (0,0,1,-2,10980),(4,0,-1,0,10675),(0,0,3,0,10034),(4,0,-2,0,8548),(2,1,-1,0,-7888),
 (2,1,0,0,-6766),(1,0,-1,0,-5163),(1,1,0,0,4987),(2,-1,1,0,4036),(2,0,2,0,3994),
 (4,0,0,0,3861),(2,0,-3,0,3665),(0,1,-2,0,-2689),(2,0,-1,2,-2602),(2,-1,-2,0,2390),
 (1,0,1,0,-2348),(2,-2,0,0,2236),(0,1,2,0,-2120),(0,2,0,0,-2069),(2,-2,-1,0,2048),
 (2,0,1,-2,-1773),(2,0,0,2,-1595),(4,-1,-1,0,1215),(0,0,2,2,-1110),(3,0,-1,0,-892),
 (2,1,1,0,-810),(4,-1,-2,0,759),(0,2,-1,0,-713),(2,2,-1,0,-700),(2,1,-2,0,691),
 (2,-1,0,-2,596),(4,0,1,0,549),(0,0,4,0,537),(4,-1,0,0,520),(1,0,-2,0,-487),
]
def luna(jd):
    T = (jd - 2451545.0) / 36525
    Lp = norm(218.3164477 + 481267.88123421 * T - 0.0015786 * T * T)
    D = norm(297.8501921 + 445267.1114034 * T - 0.0018819 * T * T)
    M = norm(357.5291092 + 35999.0502909 * T - 0.0001536 * T * T)
    Mp = norm(134.9633964 + 477198.8675055 * T + 0.0087414 * T * T)
    F = norm(93.2720950 + 483202.0175233 * T - 0.0036539 * T * T)
    E = 1 - 0.002516 * T - 0.0000074 * T * T
    A1 = norm(119.75 + 131.849 * T); A2 = norm(53.09 + 479264.290 * T)
    s = 0
    for d, m, mp, f, c in TERMINI_LUNA:
        k = c * (E ** abs(m))
        s += k * math.sin((d * D + m * M + mp * Mp + f * F) * RAD)
    s += 3958 * math.sin(A1 * RAD) + 1962 * math.sin((Lp - F) * RAD) + 318 * math.sin(A2 * RAD)
    om = 125.04 - 1934.136 * T
    return norm(Lp + s / 1e6 - 0.00478 * math.sin(om * RAD))

# ---------- Pianeti (elementi kepleriani JPL, validi 1800-2050) ----------
EL = {  # a, e, I, L, long.peri, long.nodo  + variazioni per secolo
 "mercurio": ((0.38709927, 0.20563593, 7.00497902, 252.25032350, 77.45779628, 48.33076593),
              (0.00000037, 0.00001906, -0.00594749, 149472.67411175, 0.16047689, -0.12534081)),
 "venere":   ((0.72333566, 0.00677672, 3.39467605, 181.97909950, 131.60246718, 76.67984255),
              (0.00000390, -0.00004107, -0.00078890, 58517.81538729, 0.00268329, -0.27769418)),
 "terra":    ((1.00000261, 0.01671123, -0.00001531, 100.46457166, 102.93768193, 0.0),
              (0.00000562, -0.00004392, -0.01294668, 35999.37244981, 0.32327364, 0.0)),
 "marte":    ((1.52371034, 0.09339410, 1.84969142, -4.55343205, -23.94362959, 49.55953891),
              (0.00001847, 0.00007882, -0.00813131, 19140.30268499, 0.44441088, -0.29257343)),
 "giove":    ((5.20288700, 0.04838624, 1.30439695, 34.39644051, 14.72847983, 100.47390909),
              (-0.00011607, -0.00013253, -0.00183714, 3034.74612775, 0.21252668, 0.20469106)),
 "saturno":  ((9.53667594, 0.05386179, 2.48599187, 49.95424423, 92.59887831, 113.66242448),
              (-0.00125060, -0.00050991, 0.00193609, 1222.49362201, -0.41897216, -0.28867794)),
}
def eliocentrico(nome, T):
    e0, de = EL[nome]
    a, e, I, L, wb, Om = [x + y * T for x, y in zip(e0, de)]
    w = wb - Om
    M = norm(L - wb + 180) - 180
    Er = M * RAD; ee = e
    En = Er + ee * math.sin(Er)
    for _ in range(8):
        En = En - (En - ee * math.sin(En) - Er) / (1 - ee * math.cos(En))
    xp = a * (math.cos(En) - e); yp = a * math.sqrt(1 - e * e) * math.sin(En)
    w, Om, I = w * RAD, Om * RAD, I * RAD
    x = (math.cos(w) * math.cos(Om) - math.sin(w) * math.sin(Om) * math.cos(I)) * xp + \
        (-math.sin(w) * math.cos(Om) - math.cos(w) * math.sin(Om) * math.cos(I)) * yp
    y = (math.cos(w) * math.sin(Om) + math.sin(w) * math.cos(Om) * math.cos(I)) * xp + \
        (-math.sin(w) * math.sin(Om) + math.cos(w) * math.cos(Om) * math.cos(I)) * yp
    return x, y

def pianeta(nome, jd):
    T = (jd - 2451545.0) / 36525
    xp, yp = eliocentrico(nome, T)
    xt, yt = eliocentrico("terra", T)
    lon = math.atan2(yp - yt, xp - xt) / RAD
    # precessione: elementi J2000 -> equinozio della data
    return norm(lon + 1.396971 * T)

PIANETI = ["mercurio", "venere", "marte", "giove", "saturno"]

def diff(a, b):  # differenza angolare b-a in (-180, 180]
    return (b - a + 180) % 360 - 180

def cerca(f, t0, t1, prec=1 / 1440):
    """Bisezione: istante (giorno giuliano) in cui f cambia segno tra t0 e t1."""
    f0 = f(t0)
    while t1 - t0 > prec:
        tm = (t0 + t1) / 2
        fm = f(tm)
        if (fm > 0) == (f0 > 0): t0, f0 = tm, fm
        else: t1 = tm
    return (t0 + t1) / 2

def main(anno1, anno2):
    inizio = dt.datetime(anno1, 1, 1)
    fine = dt.datetime(anno2 + 1, 1, 2)
    giorni = (fine - inizio).days
    jd0 = gj(inizio)
    sol, lun, retro = [], [], []
    eventi = []
    for i in range(giorni):
        jd = jd0 + i
        s, l = sole(jd), luna(jd)
        sol.append(round(s, 2)); lun.append(round(l, 2))
        bit = 0
        for k, p in enumerate(PIANETI):
            if diff(pianeta(p, jd - 0.5), pianeta(p, jd + 0.5)) < 0: bit |= 1 << k
        retro.append(bit)
    # eventi tra un giorno e il successivo
    FASI = {0: "luna_nuova", 90: "primo_quarto", 180: "luna_piena", 270: "ultimo_quarto"}
    STAG = {0: "equinozio_primavera", 90: "solstizio_estate", 180: "equinozio_autunno", 270: "solstizio_inverno"}
    for i in range(giorni - 1):
        a, b = jd0 + i, jd0 + i + 1
        for ang, nome in FASI.items():
            f = lambda t, ang=ang: diff(ang, norm(luna(t) - sole(t)))
            if f(a) < 0 <= f(b): eventi.append([cerca(f, a, b), nome, None])
        for k in range(12):
            f = lambda t, k=k: diff(k * 30, sole(t))
            if f(a) < 0 <= f(b):
                eventi.append([cerca(f, a, b), STAG.get(k * 30, "sole_ingresso"), k])
        for k, p in enumerate(PIANETI):
            r0, r1 = retro[i] >> k & 1, retro[i + 1] >> k & 1
            if r0 != r1:
                g = lambda t, p=p: diff(pianeta(p, t - 0.5), pianeta(p, t + 0.5))
                eventi.append([cerca(g, a, b), "stazione_retrograda" if r1 else "stazione_diretta", k])
    # istante in minuti dall'inizio (UTC)
    ev = [[round((t - jd0) * 1440), n, x] for t, n, x in sorted(eventi)]
    dati = {"inizio": inizio.strftime("%Y-%m-%d"), "giorni": giorni,
            "pianeti": PIANETI, "sole": sol, "luna": lun, "retro": retro, "eventi": ev}
    with open(os.path.join(BASE, "cielo.js"), "w", encoding="utf-8") as fh:
        fh.write("// Generato da strumenti/genera_cielo.py: non modificare a mano.\n")
        fh.write("// Longitudini alle 00:00 UTC di ogni giorno; eventi in minuti dall'inizio (UTC).\n")
        fh.write("window.ZODIEL_CIELO = " + json.dumps(dati, separators=(",", ":")) + ";\n")
    print(f"OK: {giorni} giorni, {len(ev)} eventi -> cielo.js")

if __name__ == "__main__":
    a1 = int(sys.argv[1]) if len(sys.argv) > 1 else dt.date.today().year
    a2 = int(sys.argv[2]) if len(sys.argv) > 2 else a1 + 1
    main(a1, a2)
