/* Mescolata scenografica: le carte si raccolgono in un mazzo, vengono
   tagliate e intrecciate due volte, poi ridistribuite una alla volta.
   Sostituisce mescolaCarte() di script.js (va caricato dopo). */
(function () {
  let inCorso = false;
  const pausa = ms => new Promise(r => setTimeout(r, ms));

  function anima(el, keyframes, opzioni) {
    return el.animate(keyframes, Object.assign({ fill: "forwards", easing: "ease-in-out" }, opzioni)).finished;
  }

  // stende le carte una alla volta partendo dal punto (cx, cy)
  async function distribuisci(cx, cy, ritmo = 1) {
    renderCarteCoperte();
    const contenitore = document.getElementById("mazzo");
    const nuove = Array.from(contenitore.querySelectorAll("img"));
    const rect = nuove.map(i => i.getBoundingClientRect());
    await Promise.all(nuove.map((img, i) => {
      const r = rect[i];
      return img.animate([
        { transform: `translate(${cx - r.left}px, ${cy - r.top}px) rotate(-4deg)`, opacity: 1 },
        { transform: "translate(0,0) rotate(0deg)", opacity: 1 }
      ], { duration: 295 * ritmo, delay: i * 32 * ritmo, easing: "cubic-bezier(.2,.7,.3,1)", fill: "backwards" }).finished;
    }));
  }

  function centroMazzo() {
    const contenitore = document.getElementById("mazzo");
    const zona = contenitore.getBoundingClientRect();
    const prima = contenitore.querySelector("img");
    const r0 = prima ? prima.getBoundingClientRect() : { width: 0, height: 0 };
    return { cx: zona.left + zona.width / 2 - r0.width / 2, cy: zona.top + zona.height / 2 - r0.height / 2 };
  }

  window.mescolaCarte = async function (silenzioso) {
    if (inCorso) return;
    const contenitore = document.getElementById("mazzo");
    const visibili = Array.from(contenitore.querySelectorAll("img")).filter(i => i.style.visibility !== "hidden");
    if (visibili.length === 0) return;
    inCorso = true;
    if (silenzioso !== true) traccia("mescola_carte");

    // stessa logica di prima: restano solo le carte non scelte, nuovo orientamento, nuovo ordine
    mazzo = mazzo.filter(c => !c.usata);
    mazzo.forEach(c => (c.dritta = Math.random() < 0.5));
    mazzo.sort(() => Math.random() - 0.5);

    // centro della zona del mazzo
    const zona = contenitore.getBoundingClientRect();
    const r0 = visibili[0].getBoundingClientRect();
    const w = r0.width, h = r0.height;
    const cx = zona.left + zona.width / 2 - w / 2;
    const cy = zona.top + zona.height / 2 - h / 2;

    // copie "volanti" sopra la pagina, le originali spariscono
    const strato = document.createElement("div");
    strato.style.cssText = "position:fixed;inset:0;pointer-events:none;z-index:100";
    document.body.appendChild(strato);
    const copie = visibili.map((img, i) => {
      const r = img.getBoundingClientRect();
      const c = document.createElement("img");
      c.src = "asset/dorso.jpeg";
      c.style.cssText = `position:fixed;left:${cx}px;top:${cy}px;width:${w}px;height:${h}px;border-radius:6px;box-shadow:0 0 0 1px #c9a45c,0 0 0 3px #0c0905,0 0 0 4px #8a6a2f,0 4px 10px rgba(0,0,0,.7)`;
      c.style.transform = `translate(${r.left - cx}px, ${r.top - cy}px)`;
      c.style.zIndex = i;
      strato.appendChild(c);
      img.style.visibility = "hidden";
      return c;
    });

    // 1) raccolta: le carte volano al centro una dopo l'altra
    await Promise.all(copie.map((c, i) => {
      const da = c.style.transform;
      const rot = (Math.random() * 6 - 3).toFixed(1);
      return anima(c, [{ transform: da }, { transform: `translate(${i * -0.6}px, ${i * -0.6}px) rotate(${rot}deg)` }],
                   { duration: 455, delay: i * 25 });
    }));
    await pausa(140);

    // 2) taglio e intreccio, due volte
    const passo = Math.min(w * 1.1, zona.width / 3);
    for (let giro = 0; giro < 2; giro++) {
      const meta = Math.ceil(copie.length / 2);
      await Promise.all(copie.map((c, i) => {
        const sx = i < meta ? -passo : passo;
        const rot = i < meta ? -8 : 8;
        return anima(c, [{ transform: getComputedStyle(c).transform }, { transform: `translate(${sx}px, ${-10 - (i % meta) * 0.6}px) rotate(${rot}deg)` }],
                     { duration: 265 });
      }));
      await pausa(85);
      // le carte rientrano alternando sinistra e destra
      const ordine = [];
      for (let k = 0; k < meta; k++) { ordine.push(copie[k]); if (copie[meta + k]) ordine.push(copie[meta + k]); }
      await Promise.all(ordine.map((c, k) => {
        c.style.zIndex = k;
        return anima(c, [{ transform: getComputedStyle(c).transform }, { transform: `translate(${k * -0.6}px, ${k * -0.6}px) rotate(0deg)` }],
                     { duration: 180, delay: k * 20, easing: "ease-out" });
      }));
      copie.splice(0, copie.length, ...ordine);
      await pausa(105);
    }

    // 3) distribuzione: il mazzo nuovo viene steso carta per carta
    strato.remove();
    await distribuisci(cx, cy);
    inCorso = false;
  };

  // all'apertura: solo la distribuzione, veloce (circa 1 secondo)
  window.addEventListener("DOMContentLoaded", async () => {
    inCorso = true;
    const c = centroMazzo();
    await distribuisci(c.cx, c.cy, 0.6);
    inCorso = false;
  });

  // dopo Reset: mazzo nuovo, poi mescolata completa
  const resetPrecedente = window.reset;
  window.reset = function () {
    if (inCorso) return;
    resetPrecedente();
    window.mescolaCarte(true);
  };
})();
