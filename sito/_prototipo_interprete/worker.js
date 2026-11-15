// 22 Arcani – Interprete (prototipo). Cloudflare Worker.
// - POST /api/interpreta  -> lettura personalizzata
// - GET  /                -> pagina di prova (solo se MODALITA_PROVA = "si")
// Il testo scritto dagli utenti NON viene salvato né scritto nei log.
import { CARTE } from "./testi_carte.js";
import {
  validaRichiesta, controllaTemi, costruisciMessaggi, controllaNeutro,
  estraiTesto, pulisciUscita, ARGOMENTI
} from "./logica.js";
import { PAGINA_PROVA } from "./pagina_prova.js";

const MODELLI_CLOUDFLARE = [
  "@cf/mistralai/mistral-small-3.1-24b-instruct",
  "@cf/google/gemma-4-26b-a4b-it",
  "@cf/meta/llama-3.3-70b-instruct-fp8-fast"
];

function json(dati, stato, cors) {
  return new Response(JSON.stringify(dati), {
    status: stato || 200,
    headers: { "content-type": "application/json; charset=utf-8", "cache-control": "no-store", ...cors }
  });
}

function intestazioniCors(req, env) {
  const origine = req.headers.get("origin") || "";
  const consentite = (env.ORIGINI_CONSENTITE || "").split(",").map(s => s.trim()).filter(Boolean);
  const ok = consentite.includes(origine) || /^http:\/\/(localhost|127\.0\.0\.1)(:\d+)?$/.test(origine);
  return ok ? { "access-control-allow-origin": origine, "access-control-allow-methods": "POST, OPTIONS",
                "access-control-allow-headers": "content-type", "vary": "origin" } : {};
}

async function chiamaModello(env, modello, messaggi) {
  if (modello === "claude") {
    if (!env.ANTHROPIC_API_KEY) throw new Error("Chiave Claude non configurata");
    const r = await fetch("https://api.anthropic.com/v1/messages", {
      method: "POST",
      headers: { "x-api-key": env.ANTHROPIC_API_KEY, "anthropic-version": "2023-06-01", "content-type": "application/json" },
      body: JSON.stringify({
        model: env.MODELLO_CLAUDE || "claude-haiku-5-5",
        max_tokens: 700,
        system: messaggi[0].content,
        messages: messaggi.slice(1)
      })
    });
    if (!r.ok) throw new Error("Claude ha risposto " + r.status);
    const d = await r.json();
    return (d.content || []).map(b => b.text || "").join("");
  }
  const r = await env.AI.run(modello, { messages: messaggi, max_tokens: 700, temperature: 0.7 });
  return estraiTesto(r);
}

async function verificaTurnstile(env, token, ip) {
  if (!env.TURNSTILE_SECRET) return true; // nel prototipo è spento
  const form = new FormData();
  form.append("secret", env.TURNSTILE_SECRET);
  form.append("response", token || "");
  if (ip) form.append("remoteip", ip);
  const r = await fetch("https://challenges.cloudflare.com/turnstile/v0/siteverify", { method: "POST", body: form });
  const d = await r.json();
  return !!d.success;
}

export async function interpreta(dati, env) {
  const v = validaRichiesta(dati);
  if (!v.ok) return { stato: 400, corpo: { errore: v.errore } };

  const temi = controllaTemi(v.situazione);
  if (temi.blocca) return { stato: 200, corpo: { testo: temi.risposta, note: [], fonte: "messaggio-fisso", tipo: temi.tipo } };

  const prova = env.MODALITA_PROVA === "si";
  let modello = env.MODELLO || MODELLI_CLOUDFLARE[0];
  if (prova && dati.modello && (MODELLI_CLOUDFLARE.includes(dati.modello) || dati.modello === "claude")) modello = dati.modello;

  const messaggi = costruisciMessaggi(v);
  try {
    let testo = pulisciUscita(await chiamaModello(env, modello, messaggi));
    let controllo = controllaNeutro(testo);
    if (!controllo.neutro) {
      // Un solo secondo tentativo, chiedendo di correggere il genere
      const correzione = [...messaggi,
        { role: "assistant", content: testo },
        { role: "user", content: `Nel testo c'è un'espressione al maschile o al femminile riferita a chi legge ("${controllo.problema}"). Riscrivi tutta la lettura in forma neutra, senza cambiare il senso.` }];
      testo = pulisciUscita(await chiamaModello(env, modello, correzione));
      controllo = controllaNeutro(testo);
    }
    if (!testo || testo.length < 80) throw new Error("Risposta vuota");
    return { stato: 200, corpo: { testo, note: temi.note, fonte: "ia", modello, neutro: controllo.neutro } };
  } catch (e) {
    // Quota gratuita finita, modello non disponibile, ecc.: il sito userà la sintesi a regole
    return { stato: 200, corpo: { fallback: true, motivo: prova ? String(e.message || e) : "non disponibile", note: temi.note } };
  }
}

export default {
  async fetch(req, env) {
    const url = new URL(req.url);
    const cors = intestazioniCors(req, env);

    if (req.method === "OPTIONS") return new Response(null, { status: 204, headers: cors });

    if (req.method === "GET" && url.pathname === "/" && env.MODALITA_PROVA === "si") {
      const elenco = Object.entries(CARTE).map(([id, c]) => ({ id, nome: c.nome }));
      return new Response(PAGINA_PROVA(elenco, ARGOMENTI, [...MODELLI_CLOUDFLARE, "claude"]),
        { headers: { "content-type": "text/html; charset=utf-8" } });
    }

    if (req.method === "POST" && url.pathname === "/api/interpreta") {
      const ip = req.headers.get("cf-connecting-ip") || "locale";
      // Limite di utilizzo per indirizzo IP (l'IP non viene salvato)
      if (env.LIMITE) {
        const { success } = await env.LIMITE.limit({ key: ip });
        if (!success) return json({ errore: "Hai fatto molte richieste: riprova tra qualche minuto." }, 429, cors);
      }
      let dati;
      try { dati = await req.json(); } catch { return json({ errore: "Richiesta non valida." }, 400, cors); }
      if (!(await verificaTurnstile(env, dati.turnstile, ip))) return json({ errore: "Verifica anti-spam non superata." }, 403, cors);
      const r = await interpreta(dati, env);
      return json(r.corpo, r.stato, cors);
    }
    return new Response("Non trovato", { status: 404 });
  }
};
