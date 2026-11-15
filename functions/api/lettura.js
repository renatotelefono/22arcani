/* ==========================================================
   22 Arcani – POST /api/lettura
   Riceve le tre carte estratte e restituisce, in streaming,
   la sintesi scritta dal modello "tarocchi" su Ollama
   (PC Linux, raggiunto via Cloudflare Tunnel + Access).

   Il browser manda solo gli id delle carte e il verso:
   il testo della richiesta al modello lo costruisce questa
   funzione, così nessuno può usare Ollama per altri scopi.

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

function verso(genere, dritta) {
  const base = dritta ? "dritt" : "rovesciat";
  return base + (genere === "f" ? "a" : genere === "p" ? "i" : "o");
}

function creaPrompt(lettura, dati) {
  const righe = POSIZIONI.map(p => {
    const c = lettura[p];
    const d = dati[c.id];
    const kw = d.kw[c.dritta ? 0 : 1].join(", ");
    const pos = p.charAt(0).toUpperCase() + p.slice(1);
    return `- ${pos}: ${d.nome} (${verso(d.genere, c.dritta)}). Significato secondo Waite: ${kw}.`;
  });
  return "Carte:\n" + righe.join("\n") +
         "\nScrivi una lettura basandoti solo su questi significati.";
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

  let risposta;
  try {
    risposta = await fetch(OLLAMA_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "CF-Access-Client-Id": env.CF_ACCESS_CLIENT_ID,
        "CF-Access-Client-Secret": env.CF_ACCESS_CLIENT_SECRET
      },
      body: JSON.stringify({ model: MODELLO, prompt: creaPrompt(lettura, dati), stream: true })
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
