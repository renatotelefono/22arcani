# Prototipo "La lettura del momento"

Lettura che cambia con il cielo reale (fase e segno della Luna, Sole, pianeti retrogradi,
equinozi e solstizi) e con il momento (ora del giorno, giorno della settimana).
Usa le corrispondenze tradizionali carta-astro. **Nessuna IA online, nessun costo, nessun dato degli utenti.**
La cartella è esclusa da git: non va online con il push.

## Provalo subito
Fai doppio clic su **prova_momento.html** (si apre nel browser, non serve internet).
- Scegli le carte, poi usa **+3 ore** e **+1 giorno** per vedere come cambia la lettura.
- In fondo c'è la tua sintesi a regole attuale, per confronto.
- La riga "Carte in risonanza" (in piccolo) serve solo a te per capire perché è uscita una frase.

## I file
| File | Cosa fa | Lo modifichi? |
|---|---|---|
| `momento_dati.js` | Tutte le frasi (circa 150) e le corrispondenze carta-astro | **Sì: è la bozza da rivedere** |
| `motore_momento.js` | Compone la lettura | No |
| `cielo.js` | Posizioni di Sole, Luna e pianeti 2026-2027 | No (si rigenera) |
| `genera_cielo.py` | Calcola `cielo.js` (Python puro, senza librerie) | No |
| `test_momento.js` | Controlli automatici | No |

## Come rivedere le frasi
Apri `momento_dati.js` con un editor di testo (anche Blocco note).
- Cambia liberamente il testo tra virgolette, ma lascia intatti i segnaposto tra `{graffe}`.
- Resta neutro: niente "sei pronto/a", "ti senti solo/a" e simili.
- Dopo le modifiche, ricarica `prova_momento.html` e lancia il test: in PowerShell, nella cartella,
  scrivi `node test_momento.js` e controlla che dica "0 falliti".

## Rigenerare il cielo (una volta all'anno)
In PowerShell, nella cartella: `python genera_cielo.py 2027 2028`
(Python è già sul tuo PC, non serve installare niente.)

## Verifiche fatte
- Calcoli astronomici confrontati con la libreria professionale "ephem" su 2 anni:
  errore massimo Luna 0,014°, nessun segno lunare sbagliato, lune piene entro 2 minuti.
- 3.000 letture casuali: 2.998 testi diversi, nessuna forma di genere riferita a chi legge,
  nessun errore di grammatica negli accordi ("del Mago", "Venere retrograda", "gli Amanti sono").
- Stessa stesa in 35 momenti della stessa settimana: 35 testi diversi.

## Limiti da sapere
- Equinozi e solstizi seguono l'emisfero nord (Italia).
- L'ora è quella del dispositivo di chi legge.
- Se la data è fuori dal 2026-2027 la lettura usa solo ora e giorno (senza cielo).
