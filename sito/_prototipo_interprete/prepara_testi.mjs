// Crea testi_carte.js partendo dai TUOI file (asset/descrizione_it/*.md e sintesi_dati.js).
// Si lancia con:  node prepara_testi.mjs   (da dentro la cartella _prototipo_interprete)
// Va rilanciato solo se modifichi i testi delle carte.
import fs from "node:fs";
import path from "node:path";
import vm from "node:vm";

const radice = path.resolve(process.cwd(), "..");
const cartellaTesti = path.join(radice, "asset", "descrizione_it");

// 1) Legge sintesi_dati.js come farebbe il browser
const codice = fs.readFileSync(path.join(radice, "sintesi_dati.js"), "utf8");
const finestra = { window: {} };
vm.runInNewContext(codice, finestra);
const arcani = finestra.window.ZODIEL_ARCANI;

// 2) Legge i 132 testi
const carte = {};
for (const id of Object.keys(arcani)) {
  const a = arcani[id];
  carte[id] = { nome: a.nome, kw: a.kw, consiglio: a.consiglio, testi: { dritta: {}, rovesciata: {} } };
  for (const pos of ["Passato", "Presente", "Futuro"]) {
    const d = path.join(cartellaTesti, `${id}_${pos}.md`);
    const r = path.join(cartellaTesti, `${id}_r_${pos}.md`);
    carte[id].testi.dritta[pos] = fs.readFileSync(d, "utf8").replace(/\s+/g, " ").trim();
    carte[id].testi.rovesciata[pos] = fs.readFileSync(r, "utf8").replace(/\s+/g, " ").trim();
  }
}
const uscita = "// File generato da prepara_testi.mjs: non modificare a mano.\nexport const CARTE = " +
  JSON.stringify(carte, null, 1) + ";\n";
fs.writeFileSync("testi_carte.js", uscita);
console.log(`OK: ${Object.keys(carte).length} carte, ${Object.keys(carte).length * 6} testi -> testi_carte.js`);
