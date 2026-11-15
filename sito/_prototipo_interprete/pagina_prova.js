// Pagina di prova (solo per te, in locale). Non è la pagina del sito.
export const PAGINA_PROVA = (carte, argomenti, modelli) => `<!doctype html>
<html lang="it"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Prova interprete Zodiel</title>
<style>
 body{background:#000;color:#40E0D0;font-family:Georgia,serif;max-width:760px;margin:0 auto;padding:16px}
 h1{text-shadow:0 0 10px #40E0D0;font-size:26px}
 label{display:block;margin:12px 0 4px}
 select,textarea,button{font:inherit;background:#111;color:#40E0D0;border:1px solid #40E0D0;border-radius:8px;padding:8px;width:100%;box-sizing:border-box}
 .riga{display:grid;grid-template-columns:90px 1fr 120px;gap:8px;align-items:center;margin:6px 0}
 button{background:#40E0D0;color:#000;font-weight:bold;margin-top:16px;cursor:pointer}
 #esito{white-space:pre-wrap;line-height:1.6;margin-top:20px;padding:16px;border:1px solid #40E0D0;border-radius:12px;min-height:60px}
 .info{color:#9ee;font-size:14px;margin-top:8px}
</style></head><body>
<h1>Prova interprete Zodiel</h1>
<p class="info">Pagina di test locale. Ciò che scrivi qui va solo al modello scelto e non viene salvato.</p>
${["Passato","Presente","Futuro"].map((p,i)=>`<div class="riga"><span>${p}</span>
 <select id="c${i}">${carte.map((c,j)=>`<option value="${c.id}" ${j===[0,7,17][i]?"selected":""}>${c.nome}</option>`).join("")}</select>
 <select id="v${i}"><option value="1">dritta</option><option value="0">rovesciata</option></select></div>`).join("")}
<label>Argomento</label><select id="arg">${argomenti.map(a=>`<option>${a}</option>`).join("")}</select>
<label>La tua situazione (max 500 caratteri)</label>
<textarea id="sit" rows="4" maxlength="500">Da mesi penso di cambiare lavoro ma ho paura di lasciare la sicurezza che ho.</textarea>
<label>Modello</label><select id="mod">${modelli.map(m=>`<option>${m}</option>`).join("")}</select>
<button id="vai">Interpreta</button>
<div id="esito"></div><div class="info" id="meta"></div>
<script>
document.getElementById("vai").onclick = async () => {
  const esito = document.getElementById("esito"), meta = document.getElementById("meta");
  esito.textContent = "Le carte stanno parlando..."; meta.textContent = "";
  const carte = [0,1,2].map(i => ({ id: document.getElementById("c"+i).value, dritta: document.getElementById("v"+i).value === "1" }));
  const t0 = Date.now();
  const r = await fetch("/api/interpreta", { method: "POST", headers: { "content-type": "application/json" },
    body: JSON.stringify({ carte, situazione: document.getElementById("sit").value,
      argomento: document.getElementById("arg").value, modello: document.getElementById("mod").value }) });
  const d = await r.json();
  if (d.errore) { esito.textContent = "Errore: " + d.errore; return; }
  if (d.fallback) { esito.textContent = "Modello non disponibile (" + d.motivo + "): sul sito qui comparirebbe la sintesi a regole."; return; }
  esito.textContent = d.testo + (d.note && d.note.length ? "\\n\\n" + d.note.join("\\n") : "");
  meta.textContent = "Fonte: " + d.fonte + (d.modello ? " | modello: " + d.modello : "") +
    (d.neutro === false ? " | ATTENZIONE: possibile forma non neutra" : "") + " | " + ((Date.now()-t0)/1000).toFixed(1) + " s";
};
</script></body></html>`;
