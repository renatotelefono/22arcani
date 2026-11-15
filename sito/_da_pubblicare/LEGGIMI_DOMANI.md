# Lancio "lettura del momento" – tutto pronto per domani

Questa cartella è esclusa da git: niente di quello che c'è qui va online finché non lo copiamo nel sito.
**Nessun file del sito è stato modificato stanotte.**

## Cosa c'è di pronto
| Cosa | File qui | Dove andrà nel sito |
|---|---|---|
| Pagina "Il cielo di oggi" | `cielo/index.html`, `cielo/cielo_pagina.js` | `/cielo/` |
| Calendario lunare 2027 | `calendario-lunare-2027/index.html` | `/calendario-lunare-2027/` |
| Mercurio retrogrado 2027 | `mercurio-retrogrado-2027/index.html` | `/mercurio-retrogrado-2027/` |
| La carta del tuo segno | `segni/index.html` | `/segni/` |
| Riquadro "Novità" + paragrafo con i link | `index.html` (home modificata) | `index.html` |
| Script che genera le 4 pagine | `strumenti/genera_cielo_pagine.py` | `strumenti/` |
| Cielo del giorno nel video quotidiano | `strumenti/cielo_oggi.py` + `strumenti/genera_lettura.py` (modificato) | `strumenti/` |
| Righe per la sitemap | `sitemap_righe_nuove.txt` | dentro `sitemap.xml` |
| Testi per YouTube | `TESTI_YOUTUBE.md` | (li usi tu) |

(`strumenti/genera_cielo.py` qui è solo una copia identica di quella che hai già: non serve copiarla.)

## Controlli già fatti
- Le 5 pagine sono HTML valido; tutti i link interni e le immagini esistono.
- Date e orari verificati con una libreria astronomica professionale (ora italiana, con ora legale).
- Gli script delle pagine funzionano (simulati come nel browser) e se qualcosa manca la pagina resta leggibile.
- Testi neutri, niente previsioni: su date e contratti la pagina di Mercurio dice che "contano i fatti, non il cielo".

## Domani, in ordine
1. **Rivedi** (15 minuti): apri le pagine e i testi; dimmi se cambiare qualcosa.
2. **Io copio tutto nel sito**: rigenero le pagine con la data di domani, aggiungo le righe alla sitemap
   e controllo che `index.html` non sia cambiato nel frattempo.
3. **Tu provi in locale**: in PowerShell, nella cartella `22arcani/sito`, `python -m http.server 8000`, poi apri
   http://localhost:8000/cielo/ , /segni/ , /calendario-lunare-2027/ , /mercurio-retrogrado-2027/ e la home.
4. **Tu pubblichi** con i comandi che ti preparo (solo i file nuovi e modificati).
5. **Google Search Console**: invii di nuovo `https://22arcani.it/sitemap.xml` (ti guido se serve).
6. **YouTube**: post della community, commento fissato, e lo Short di venerdì 13 (Mercurio torna diretto).
7. **Video quotidiano**: il primo video generato con il nuovo script avrà il cielo del giorno nell'intro;
   controlla che la riga sotto la data non si sovrapponga a nulla.

## Ogni tanto
- Le pagine si aggiornano da sole nel browser; rigenerarle (`python strumenti/genera_cielo_pagine.py`) serve
  solo per la versione che legge Google, per esempio una volta al mese.
- A fine 2027: `python strumenti/genera_cielo.py 2028 2029`, poi creiamo le pagine 2028.
