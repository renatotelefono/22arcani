# 22 Arcani (Zodiel 2.0)

Sito di tarocchi di Marsiglia in italiano: 22arcani.it

## Struttura

- `sito/` — il sito pubblicato da Cloudflare Pages (cartella di output)
- `strumenti/` — script di supporto (es. generatore delle pagine degli Arcani)
- `materiali/` — testi, scansioni e appunti di lavoro (i video NON vanno nel repository)

## Pubblicazione

Ogni push sul ramo `main` viene pubblicato in automatico da Cloudflare Pages.

- Build command: nessuno
- Output directory: `sito`

## Note

- Progetto separato da Zodiel 1 (zodiel.cloud): nessun file in comune.
- Fase iniziale: lettura a tre carte con mazzo ridotto (3 carte, 18 spezzoni "solo mani").
- La sintesi finale della lettura è scritta dal modello `tarocchi` (Qwen 1.5B addestrato con LoRA). Se il modello non risponde, la pagina mostra la sintesi classica di `sito/sintesi.js`.

## Sintesi con il modello (Ollama)

Percorso di una richiesta:

1. `sito/interpretazione.html` chiama `POST /api/lettura` con gli id delle tre carte e il verso.
2. `functions/api/lettura.js` (Pages Function) costruisce il prompt con i significati di `sito/sintesi_dati.js` e chiama `https://api.22arcani.it/api/generate`.
3. Cloudflare Access (applicazione `api`, policy `solo sito`, Service Auth) lascia passare solo le richieste con il service token `22arcani-sito`.
4. Cloudflare Tunnel `22arcani-linux` porta la richiesta a Ollama (`localhost:11434`) sul PC Linux.

Variabili del progetto Pages: `CF_ACCESS_CLIENT_ID`, `CF_ACCESS_CLIENT_SECRET`.
Le chiavi non vanno mai nel repository (vedi `.gitignore`).
