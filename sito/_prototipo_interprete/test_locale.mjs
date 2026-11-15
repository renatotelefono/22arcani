// Test offline: verifica controlli, temi delicati, prompt e correzione del genere.
// Non chiama nessuna IA vera (usa un finto modello). Si lancia con: node test_locale.mjs
import { interpreta } from "./worker.js";
import { costruisciMessaggi, controllaNeutro } from "./logica.js";

let chiamate = 0;
const finto = {
  MODALITA_PROVA: "si",
  AI: { run: async (modello, { messages }) => {
    chiamate++;
    // 1a risposta volutamente sbagliata ("sei pronto"), la 2a corretta
    return { response: chiamate === 1
      ? "Nel passato il Matto ti ha spinto a osare. Oggi sei pronto a scegliere con calma e a fidarti di ciò che senti dentro di te, senza fretta. ".repeat(2)
      : "Nel passato il Matto ha portato il desiderio di osare. Oggi hai la forza di scegliere con calma, ascoltando ciò che senti. Il futuro invita a fare un passo alla volta. Quale piccolo passo senti possibile già questa settimana?" };
  } }
};
const carte = [{ id: "00_il_matto", dritta: true }, { id: "07_il_carro", dritta: false }, { id: "17_la_stella", dritta: true }];
let ok = 0, ko = 0;
function verifica(nome, cond) { cond ? ok++ : ko++; console.log((cond ? "OK  " : "NO  ") + nome); }

// 1. richieste non valide
verifica("rifiuta 2 carte", (await interpreta({ carte: carte.slice(0, 2) }, finto)).stato === 400);
verifica("rifiuta carta inventata", (await interpreta({ carte: [{ id: "99_x" }, carte[1], carte[2]] }, finto)).stato === 400);
verifica("rifiuta testo troppo lungo", (await interpreta({ carte, situazione: "a".repeat(600) }, finto)).stato === 400);

// 2. temi delicati gestiti dal codice
const crisi = await interpreta({ carte, situazione: "non ce la faccio più, voglio farla finita" }, finto);
verifica("crisi -> messaggio fisso con 112, nessuna IA", crisi.corpo.fonte === "messaggio-fisso" && crisi.corpo.testo.includes("112") && chiamate === 0);
const viol = await interpreta({ carte, situazione: "il mio compagno mi picchia" }, finto);
verifica("violenza -> 1522", viol.corpo.testo.includes("1522"));

// 3. lettura normale con correzione automatica del genere
const r = await interpreta({ carte, situazione: "Ho paura di lasciare il lavoro e perdere i soldi del mutuo", argomento: "lavoro" }, finto);
verifica("lettura generata", r.corpo.fonte === "ia");
verifica("seconda chiamata per correggere 'sei pronto'", chiamate === 2 && r.corpo.neutro === true);
verifica("nota automatica su soldi/mutuo", r.corpo.note.some(n => n.includes("professionista")));

// 4. il controllo neutro
verifica("rileva 'ti senti sola'", !controllaNeutro("A volte ti senti sola.").neutro);
verifica("accetta frase neutra", controllaNeutro("Hai la forza di ricominciare.").neutro);

// 5. errore del modello -> fallback alla sintesi a regole
const rotto = { AI: { run: async () => { throw new Error("quota finita"); } } };
verifica("fallback se l'IA non risponde", (await interpreta({ carte }, rotto)).corpo.fallback === true);

// Dimensione del prompt (per stimare i costi)
const m = costruisciMessaggi({ carte, situazione: "x".repeat(300), argomento: "amore" });
const caratteri = m.reduce((s, x) => s + x.content.length, 0);
console.log(`\nPrompt: ${caratteri} caratteri ≈ ${Math.round(caratteri / 3.5)} token (stima)`);
console.log(`\nRisultato: ${ok} superati, ${ko} falliti`);
console.log("\n--- Esempio del messaggio inviato al modello (parte finale) ---\n" + m[1].content.slice(0, 900) + " ...");
