// Test del motore "lettura del momento": node test_momento.js
global.window = global;
require("./cielo.js"); require("./momento_dati.js"); require("../../sintesi_dati.js"); require("./motore_momento.js");
const D = ZODIEL_MOMENTO, ids = Object.keys(ZODIEL_ARCANI);
let ok = 0, ko = 0; const errori = [];
const verifica = (n, c) => { c ? ok++ : (ko++, errori.push(n)); };
// parole che NON devono mai comparire (forme di genere riferite a chi legge, grammatica rotta)
const VIETATE = /\b(sei|sarai|ti senti|sentirti|essere|resta|rimani)\s+(pront|stanc|sicur|delus|confus|sol|arrabbiat|preoccupat|innamorat|bloccat|tranquill|contento|contenta|fortunat)\w*\b|\b(di|a|da|in|su) (il|lo|la|gli|i) [A-Z]|\{|\}|undefined|NaN/;
const casuale = (seme => () => (seme = (seme * 16807) % 2147483647) / 2147483647)(42);
const testi = new Set(), conteggioCause = {};
let letture = 0;
// 3000 letture casuali tra nov 2026 e dic 2027, ore casuali
for (let n = 0; n < 3000; n++) {
  const mazzo = [...ids].sort(() => casuale() - 0.5).slice(0, 3);
  const L = { passato: { nome: mazzo[0], dritta: casuale() < .5 }, presente: { nome: mazzo[1], dritta: casuale() < .5 }, futuro: { nome: mazzo[2], dritta: casuale() < .5 } };
  const t = new Date(Date.UTC(2026, 10, 1) + casuale() * 420 * 864e5);
  const r = creaLetturaMomento(L, t);
  const tutto = r.paragrafi.join(" ");
  letture++; testi.add(tutto);
  r.risonanze.forEach(x => { const c = x.split(": ")[1]; conteggioCause[c] = (conteggioCause[c] || 0) + 1; });
  if (VIETATE.test(tutto)) errori.push("Testo sospetto: " + tutto.match(VIETATE)[0] + " -> " + tutto.slice(0, 160));
  // stesso momento = stesso testo
  if (n < 50) verifica("ripetibilità", creaLetturaMomento(L, t).paragrafi.join(" ") === tutto);
}
verifica("nessun testo sospetto", !errori.some(e => e.startsWith("Testo sospetto")));
// ogni carta con ogni causa possibile produce frasi corrette
for (const id of ids) for (const dritta of [true, false]) for (const causa of Object.keys(D.cause)) {
  // finto cielo che forza la causa: verifichiamo solo la grammatica delle frasi
  const a = ZODIEL_ARCANI[id];
  for (const tpl of D.cause[causa]) {
    const nomeMin = a.nome[0].toLowerCase() + a.nome.slice(1);
    const s = tpl.replace("{Carta}", a.nome).replace(/\{carta\}/g, nomeMin);
    verifica("frase " + causa, !/\b(di|a) (il|la|gli|lo) /.test(s));
  }
  verifica("frase carta " + id, typeof D.carte[id][dritta ? 0 : 1] === "string");
}
// stesse carte, momenti diversi della stessa settimana -> testi diversi
const L = { passato: { nome: "00_il_matto", dritta: true }, presente: { nome: "07_il_carro", dritta: false }, futuro: { nome: "17_la_stella", dritta: true } };
const settimana = new Set();
for (let g = 0; g < 7; g++) for (const h of [7, 10, 15, 19, 23]) settimana.add(creaLetturaMomento(L, new Date(2026, 10, 9 + g, h)).paragrafi.join(" "));
verifica("35 momenti della settimana -> almeno 30 testi diversi", settimana.size >= 30);
console.log(`Letture casuali: ${letture}, testi diversi: ${testi.size}`);
console.log(`Stessa stesa in 35 momenti della settimana: ${settimana.size} testi diversi`);
console.log("Carte in risonanza per causa:", conteggioCause);
console.log(`\nRisultato: ${ok} controlli superati, ${ko} falliti`);
errori.slice(0, 10).forEach(e => console.log("  - " + e));
