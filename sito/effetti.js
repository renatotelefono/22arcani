/* Effetti visivi della lettura: la carta scelta vola nello slot e si gira.
   Sostituisce selezionaCarta() di script.js (va caricato dopo). */
(function () {
  const ridotto = false; // effetto sempre attivo (molti PC hanno le animazioni di Windows spente senza saperlo)
  let occupato = false;   // blocca i clic mentre una carta e' in volo
  let giro = 0;           // cambia a ogni reset, per ignorare animazioni vecchie

  const stile = document.createElement("style");
  stile.textContent = `
    .flip3d { perspective: 1000px; margin-top: 6px; }
    .flip3d-interno { position: relative; width: 100%; height: 100%; transform-style: preserve-3d;
                      transition: transform 0.7s ease-in-out; }
    .flip3d.girata .flip3d-interno { transform: rotateY(180deg); }
    .flip3d-faccia { position: absolute; inset: 0; width: 100%; height: 100%; backface-visibility: hidden;
                     border-radius: 10px; object-fit: cover; box-shadow: 0 0 18px #40E0D0; }
    .flip3d-fronte { transform: rotateY(180deg); }
    .flip3d-ruota { width: 100%; height: 100%; }
    .flip3d.rovesciata .flip3d-ruota { transform: rotate(180deg); }
    .carta-in-volo { position: fixed; z-index: 100; pointer-events: none; border-radius: 8px;
                     box-shadow: 0 0 30px #40E0D0; }
  `;
  document.head.appendChild(stile);

  function misuraSlot(slot) {
    const h3 = slot.querySelector("h3");
    const altezza = slot.clientHeight - (h3 ? h3.offsetHeight + 24 : 0) - 16;
    const larghezza = Math.min(slot.clientWidth * 0.9, altezza / 1.675);
    return { w: Math.round(larghezza), h: Math.round(larghezza * 1.675) };
  }

  window.selezionaCarta = function (index) {
    if (occupato || selezionate.length >= 3) return;
    const carta = mazzo[index];
    if (!carta || carta.usata) return;

    carta.usata = true;
    selezionate.push(carta);
    const numero = selezionate.length;
    const slotId = ["passato", "presente", "futuro"][numero - 1];
    traccia("carta_scelta", { posizione: slotId, carta: carta.nome, orientamento: carta.dritta ? "dritta" : "rovesciata" });

    const fronte = new Image();
    fronte.src = carta.img;              // inizia a scaricarla durante il volo

    // carta 3D nello slot (ancora invisibile)
    const slot = document.getElementById(slotId);
    slot.innerHTML = `<h3>${slot.querySelector("h3").textContent}</h3>`;
    const dim = misuraSlot(slot);
    const box = document.createElement("div");
    box.className = "flip3d";
    box.style.width = dim.w + "px";
    box.style.height = dim.h + "px";
    box.innerHTML = `<div class="flip3d-ruota"><div class="flip3d-interno">
        <img class="flip3d-faccia" src="asset/dorso.jpeg" alt="">
        <img class="flip3d-faccia flip3d-fronte" alt="">
      </div></div>`;
    box.querySelector(".flip3d-fronte").src = carta.img;
    box.style.visibility = "hidden";
    if (!carta.dritta) box.classList.add("rovesciata"); // arriva gia' capovolta
    slot.appendChild(box);

    const sorgente = document.querySelectorAll("#mazzo img")[index];
    sorgente.style.visibility = "hidden";
    sorgente.style.pointerEvents = "none";

    const mioGiro = giro;
    const fine = () => {
      if (mioGiro !== giro) return;
      occupato = false;
      if (selezionate.length === 3) document.getElementById("btnInterpretazione").disabled = false;
    };

    if (ridotto) {
      box.style.visibility = "visible";
      box.classList.add("girata");
      if (!carta.dritta) box.classList.add("rovesciata");
      fine();
      return;
    }

    occupato = true;
    // se lo slot non si vede (es. sul telefono dopo aver scrollato), prima lo porta in vista
    const r = box.getBoundingClientRect();
    const visibile = r.top >= 0 && r.bottom <= window.innerHeight;
    if (!visibile) slot.scrollIntoView({ behavior: "smooth", block: "center" });
    setTimeout(() => vola(), visibile ? 0 : 500);

    function vola() {
    if (mioGiro !== giro) return;
    const da = sorgente.getBoundingClientRect();
    const a = box.getBoundingClientRect();
    const volo = document.createElement("img");
    volo.src = "asset/dorso.jpeg";
    volo.className = "carta-in-volo";
    Object.assign(volo.style, { left: da.left + "px", top: da.top + "px", width: da.width + "px", height: da.height + "px" });
    document.body.appendChild(volo);

    const dx = a.left - da.left, dy = a.top - da.top;
    const sx = a.width / da.width, sy = a.height / da.height;
    volo.style.transformOrigin = "0 0";
    const anim = volo.animate([
      { transform: "translate(0,0) scale(1,1) rotate(0deg)" },
      { transform: `translate(${dx * 0.5}px, ${dy * 0.5 - 120}px) scale(${(1 + sx) / 2}, ${(1 + sy) / 2}) rotate(-10deg)`, offset: 0.55 },
      { transform: `translate(${dx}px, ${dy}px) scale(${sx}, ${sy}) rotate(0deg)` }
    ], { duration: 800, easing: "ease-in-out", fill: "forwards" });

    anim.onfinish = () => {
      volo.remove();
      if (mioGiro !== giro) return;
      box.style.visibility = "visible";
      const gira = () => {
        requestAnimationFrame(() => box.classList.add("girata"));
        setTimeout(() => {
          fine();
        }, 750);
      };
      if (fronte.complete) setTimeout(gira, 150);
      else { fronte.onload = gira; fronte.onerror = gira; }
    };
    }
  };

  const resetOriginale = window.reset;
  window.reset = function () {
    giro++;
    occupato = false;
    document.querySelectorAll(".carta-in-volo").forEach(e => e.remove());
    resetOriginale();
  };
})();
