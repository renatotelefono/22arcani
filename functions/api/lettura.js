/* ==========================================================
   22 Arcani – POST /api/lettura
   Riceve le tre carte estratte e restituisce, in streaming,
   la sintesi scritta dal modello "tarocchi" su Ollama
   (PC Linux, raggiunto via Cloudflare Tunnel + Access).

   Il browser manda solo gli id delle carte e il verso:
   il testo della richiesta al modello lo costruisce questa
   funzione, così nessuno può usare Ollama per altri scopi.

   La richiesta usa ESATTAMENTE il formato degli esempi di
   addestramento (llm_local/data/*.jsonl):
     PASSATO: <Nome> (carta dritta|rovesciata)
     <testo di asset/descrizione_it/<id>[_r]_Passato.md>
     (riga vuota, poi PRESENTE e FUTURO allo stesso modo)
   Le descrizioni sono le stesse che il visitatore legge
   nelle tre fasi della pagina interpretazione.

   Variabili richieste (Pages > Settings > Variables and secrets):
     CF_ACCESS_CLIENT_ID, CF_ACCESS_CLIENT_SECRET
   ========================================================== */

const OLLAMA_URL = "https://api.22arcani.it/api/generate";
const MODELLO = "tarocchi";
const POSIZIONI = ["passato", "presente", "futuro"];

let arcani = null; // dati delle carte, letti una volta da /sintesi_dati.js

async function caricaArcani(env, request) {
  if (arcani) return arcani;
  const r = await env.ASSETS.fetch(new URL("/sintesi_dati.js", request.url));
  const t = await r.text();
  arcani = JSON.parse(t.slice(t.indexOf("{"), t.lastIndexOf("}") + 1));
  return arcani;
}

function errore(messaggio, stato) {
  return new Response(JSON.stringify({ errore: messaggio }), {
    status: stato,
    headers: { "Content-Type": "application/json; charset=utf-8" }
  });
}

// Come negli esempi di addestramento: spazi a fine riga tolti
// e apostrofi tipografici convertiti in apostrofi semplici.
function pulisci(testo) {
  return testo.replace(/^\uFEFF/, "").replace(/[\u2018\u2019]/g, "'")
    .replace(/\r\n/g, "\n").split("\n").map(r => r.trim()).join("\n").trim();
}

async function descrizione(env, request, id, dritta, posizione) {
  const file = `/asset/descrizione_it/${id}${dritta ? "" : "_r"}_${posizione}.md`;
  const r = await env.ASSETS.fetch(new URL(file, request.url));
  if (!r.ok) throw new Error("descrizione mancante: " + file);
  return pulisci(await r.text());
}

async function creaPrompt(env, request, lettura, dati) {
  const blocchi = [];
  for (const p of POSIZIONI) {
    const c = lettura[p];
    const pos = p.charAt(0).toUpperCase() + p.slice(1);   // "Passato"
    const testo = await descrizione(env, request, c.id, c.dritta, pos);
    blocchi.push(`${p.toUpperCase()}: ${dati[c.id].nome} (carta ${c.dritta ? "dritta" : "rovesciata"})\n${testo}`);
  }
  return blocchi.join("\n\n");
}

export async function onRequestPost({ request, env }) {
  if (!env.CF_ACCESS_CLIENT_ID || !env.CF_ACCESS_CLIENT_SECRET) {
    return errore("configurazione mancante", 500);
  }

  let corpo;
  try { corpo = await request.json(); } catch (e) { return errore("richiesta non valida", 400); }

  let dati;
  try { dati = await caricaArcani(env, request); } catch (e) { return errore("dati carte non disponibili", 500); }

  // Accetta solo id di carte esistenti e il verso (dritta sì/no)
  const lettura = {};
  for (const p of POSIZIONI) {
    const c = corpo && corpo[p];
    const id = c && typeof c.id === "string" ? c.id.replace(/^(\d{2})_\1_/, "$1_") : "";
    if (!dati[id] || typeof c.dritta !== "boolean") return errore("carte non valide", 400);
    lettura[p] = { id, dritta: c.dritta };
  }

  let prompt;
  try { prompt = await creaPrompt(env, request, lettura, dati); } catch (e) { return errore("descrizioni non disponibili", 500); }

  let risposta;
  try {
    risposta = await fetch(OLLAMA_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "CF-Access-Client-Id": env.CF_ACCESS_CLIENT_ID,
        "CF-Access-Client-Secret": env.CF_ACCESS_CLIENT_SECRET
      },
      body: JSON.stringify({ model: MODELLO, prompt, stream: true })
    });
  } catch (e) {
    return errore("modello non raggiungibile", 502);
  }
  if (!risposta.ok || !risposta.body) return errore("modello non disponibile", 502);

  // Ollama risponde con una riga JSON per pezzo di testo:
  // la trasformiamo in testo semplice che il browser mostra man mano.
  const decoder = new TextDecoder();
  const encoder = new TextEncoder();
  let resto = "";
  const trasforma = new TransformStream({
    transform(pezzo, controller) {
      resto += decoder.decode(pezzo, { stream: true });
      const righe = resto.split("\n");
      resto = righe.pop();
      for (const riga of righe) {
        if (!riga.trim()) continue;
        try {
          const j = JSON.parse(riga);
          if (j.response) controller.enqueue(encoder.encode(j.response));
        } catch (e) { /* riga incompleta o non valida: la saltiamo */ }
      }
    },
    flush(controller) {
      try {
        const j = JSON.parse(resto);
        if (j.response) controller.enqueue(encoder.encode(j.response));
      } catch (e) {}
    }
  });

  return new Response(risposta.body.pipeThrough(trasforma), {
    headers: {
      "Content-Type": "text/plain; charset=utf-8",
      "Cache-Control": "no-store"
    }
  });
}
