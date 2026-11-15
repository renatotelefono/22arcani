global.window = global;
require("./cielo.js"); require("./momento_dati.js"); require("../../sintesi_dati.js"); require("./motore_momento.js");
const L = { passato: { nome: "00_il_matto", dritta: true }, presente: { nome: "07_il_carro", dritta: false }, futuro: { nome: "17_la_stella", dritta: true } };
for (const d of ["2026-11-09T18:30", "2026-11-10T08:15", "2026-11-24T22:00", "2026-12-21T12:00"]) {
  const r = creaLetturaMomento(L, new Date(d));
  console.log("\n=== " + r.scheda + "  [" + r.risonanze.join(", ") + "]");
  r.paragrafi.forEach(p => console.log("  " + p));
}
