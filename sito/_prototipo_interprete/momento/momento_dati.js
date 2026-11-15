// Zodiel – "La lettura del momento": corrispondenze carta-astro e frasi.
// BOZZA DA RIVEDERE: puoi modificare liberamente le frasi (resta neutro: niente aggettivi
// maschili/femminili riferiti a chi legge). Segnaposto tra {graffe}: non cambiarli.
window.ZODIEL_MOMENTO = {

 // ---------- Corrispondenze tradizionali (Golden Dawn / Rider-Waite) ----------
 // tipo: "pianeta" | "segno" (0=Ariete ... 11=Pesci) | "elemento"
 corrispondenze: {
  "00_il_matto":              { tipo: "elemento", astro: "aria",      elemento: "aria" },
  "01_il_mago":               { tipo: "pianeta",  astro: "mercurio",  elemento: "aria" },
  "02_la_papessa":            { tipo: "pianeta",  astro: "luna",      elemento: "acqua" },
  "03_l_imperatrice":         { tipo: "pianeta",  astro: "venere",    elemento: "terra" },
  "04_l_imperatore":          { tipo: "segno",    astro: 0,           elemento: "fuoco" },
  "05_il_papa":               { tipo: "segno",    astro: 1,           elemento: "terra" },
  "06_gli_amanti":            { tipo: "segno",    astro: 2,           elemento: "aria" },
  "07_il_carro":              { tipo: "segno",    astro: 3,           elemento: "acqua" },
  "08_la_forza":              { tipo: "segno",    astro: 4,           elemento: "fuoco" },
  "09_l_eremita":             { tipo: "segno",    astro: 5,           elemento: "terra" },
  "10_la_ruota_della_fortuna":{ tipo: "pianeta",  astro: "giove",     elemento: "fuoco" },
  "11_la_giustizia":          { tipo: "segno",    astro: 6,           elemento: "aria" },
  "12_l_appeso":              { tipo: "elemento", astro: "acqua",     elemento: "acqua" },
  "13_la_morte":              { tipo: "segno",    astro: 7,           elemento: "acqua" },
  "14_la_temperanza":         { tipo: "segno",    astro: 8,           elemento: "fuoco" },
  "15_il_diavolo":            { tipo: "segno",    astro: 9,           elemento: "terra" },
  "16_la_torre":              { tipo: "pianeta",  astro: "marte",     elemento: "fuoco" },
  "17_la_stella":             { tipo: "segno",    astro: 10,          elemento: "aria" },
  "18_la_luna":               { tipo: "segno",    astro: 11,          elemento: "acqua" },
  "19_il_sole":               { tipo: "pianeta",  astro: "sole",      elemento: "fuoco" },
  "20_il_giudizio":           { tipo: "elemento", astro: "fuoco",     elemento: "fuoco" },
  "21_il_mondo":              { tipo: "pianeta",  astro: "saturno",   elemento: "terra" }
 },

 // ---------- Nomi e articoli ----------
 segni:      ["Ariete","Toro","Gemelli","Cancro","Leone","Vergine","Bilancia","Scorpione","Sagittario","Capricorno","Acquario","Pesci"],
 segniDel:   ["dell'Ariete","del Toro","dei Gemelli","del Cancro","del Leone","della Vergine","della Bilancia","dello Scorpione","del Sagittario","del Capricorno","dell'Acquario","dei Pesci"],
 segniArt:   ["l'Ariete","il Toro","i Gemelli","il Cancro","il Leone","la Vergine","la Bilancia","lo Scorpione","il Sagittario","il Capricorno","l'Acquario","i Pesci"],
 elementoSegno: ["fuoco","terra","aria","acqua","fuoco","terra","aria","acqua","fuoco","terra","aria","acqua"],
 elementoDi: { fuoco: "di fuoco", acqua: "d'acqua", aria: "d'aria", terra: "di terra" },
 pianeti:    { sole: "Sole", luna: "Luna", mercurio: "Mercurio", venere: "Venere", marte: "Marte", giove: "Giove", saturno: "Saturno" },
 pianetiDi:  { sole: "del Sole", luna: "della Luna", mercurio: "di Mercurio", venere: "di Venere", marte: "di Marte", giove: "di Giove", saturno: "di Saturno" },
 pianetiA:   { sole: "al Sole", luna: "alla Luna", mercurio: "a Mercurio", venere: "a Venere", marte: "a Marte", giove: "a Giove", saturno: "a Saturno" },
 giorni:     ["domenica","lunedì","martedì","mercoledì","giovedì","venerdì","sabato"],
 pianetaGiorno: ["sole","luna","marte","mercurio","giove","venere","saturno"],
 fasiNomi:   ["Luna nuova","Luna crescente","primo quarto di Luna","Luna gibbosa crescente","Luna piena","Luna gibbosa calante","ultimo quarto di Luna","Luna calante"],
 fasceNomi:  { alba: "alba", mattino: "mattino", pomeriggio: "pomeriggio", sera: "sera", notte: "notte" },

 // ---------- 1. Il momento della giornata ----------
 fasce: {
  alba: ["All'alba il giorno è ancora tutto da scrivere: è il momento delle intenzioni.",
         "La luce dell'alba porta con sé un senso di inizio: ciò che leggi ora è un seme per la giornata.",
         "Le prime ore del giorno favoriscono la chiarezza: la mente è ancora libera dal rumore."],
  mattino: ["Il mattino è il tempo dell'azione: le carte parlano a chi si prepara a muoversi.",
            "Nella luce del mattino le idee prendono forma: è un buon momento per decidere da dove cominciare.",
            "Il mattino porta energia nuova: ciò che leggi ora può orientare le scelte della giornata."],
  pomeriggio: ["Il pomeriggio invita a fare il punto: a metà del cammino si vede meglio la direzione.",
               "Nelle ore del pomeriggio l'energia si fa più calma: è il momento di valutare ciò che hai avviato.",
               "Il pomeriggio è un tempo di passaggio, adatto a correggere la rotta senza fretta."],
  sera: ["La sera porta il tempo del bilancio: le carte aiutano a rileggere la giornata.",
         "Mentre la luce cala, l'attenzione si sposta verso l'interno: è il momento di ascoltarsi.",
         "La sera è il tempo del raccoglimento: ciò che leggi ora parla soprattutto al cuore."],
  notte: ["Di notte il mondo tace e le intuizioni si fanno più forti: è l'ora delle domande profonde.",
          "Nelle ore notturne le carte parlano a voce bassa: ascoltale con calma, senza fretta di risposte.",
          "La notte è il regno della Luna e dei sogni: ciò che emerge ora merita attenzione."]
 },

 // ---------- 2. La fase della Luna (0=nuova ... 4=piena ... 7=calante) ----------
 fasi: [
  ["La Luna è nuova in {segno_luna}: il cielo è buio e pronto ad accogliere nuove intenzioni.",
   "Con la Luna nuova in {segno_luna} si apre un nuovo ciclo: è il momento di seminare un desiderio.",
   "La Luna nuova, in {segno_luna}, invita a ricominciare in silenzio, partendo da ciò che conta davvero."],
  ["La Luna crescente in {segno_luna} sostiene ciò che sta nascendo: piccoli passi diventano slancio.",
   "Con la Luna che cresce in {segno_luna}, le intenzioni prendono forza giorno dopo giorno.",
   "La Luna crescente, in {segno_luna}, favorisce i nuovi inizi e il coraggio di provarci."],
  ["La Luna al primo quarto in {segno_luna} chiede una scelta: è il momento di agire su ciò che hai avviato.",
   "Con il primo quarto di Luna in {segno_luna} arrivano le prime prove: superarle rafforza il cammino.",
   "Il primo quarto di Luna, in {segno_luna}, porta una tensione costruttiva: un ostacolo può diventare una spinta."],
  ["La Luna, quasi piena in {segno_luna}, invita a perfezionare e a pazientare ancora un poco.",
   "Con la Luna che si avvicina al pieno in {segno_luna}, ciò che stai costruendo chiede gli ultimi ritocchi.",
   "La Luna gibbosa in {segno_luna} porta attesa e maturazione: il raccolto è vicino."],
  ["La Luna piena in {segno_luna} illumina tutto: emozioni e verità vengono alla luce.",
   "Con la Luna piena in {segno_luna} il cielo è al massimo della luce: un momento di culmine e consapevolezza.",
   "La Luna piena, in {segno_luna}, amplifica le emozioni: osserva ciò che ti mostra, senza reagire d'impulso."],
  ["La Luna inizia a calare in {segno_luna}: è il tempo di condividere ciò che hai capito.",
   "Con la Luna calante in {segno_luna}, dopo il culmine arriva il momento della gratitudine.",
   "La Luna che decresce in {segno_luna} invita a raccogliere i frutti e a fare spazio."],
  ["La Luna all'ultimo quarto in {segno_luna} chiede di lasciare andare ciò che non serve più.",
   "Con l'ultimo quarto di Luna in {segno_luna} si fa ordine: un buon momento per chiudere le questioni aperte.",
   "L'ultimo quarto di Luna, in {segno_luna}, porta revisione: meglio alleggerire che aggiungere."],
  ["La Luna sta per scomparire in {segno_luna}: è il tempo del riposo e della riflessione.",
   "Con l'ultima falce di Luna in {segno_luna} il ciclo si chiude: prepara lo spazio per ciò che verrà.",
   "La Luna calante in {segno_luna} favorisce il silenzio e il congedo da ciò che è finito."]
 ],

 // ---------- 3. Eventi del giorno ----------
 eventi: {
  equinozio_primavera: ["Oggi è l'equinozio di primavera: luce e buio si equilibrano e la natura si risveglia."],
  solstizio_estate:    ["Oggi è il solstizio d'estate, il giorno più luminoso dell'anno: un invito a lasciar splendere ciò che sei."],
  equinozio_autunno:   ["Oggi è l'equinozio d'autunno: giorno e notte si equilibrano, ed è tempo di raccogliere."],
  solstizio_inverno:   ["Oggi è il solstizio d'inverno, la notte più lunga dell'anno: da qui la luce ricomincia a crescere."],
  sole_ingresso:       ["Oggi il Sole entra in {segno_sole}: cambia l'atmosfera delle prossime settimane.",
                        "Con l'ingresso del Sole in {segno_sole} si apre una nuova stagione dello zodiaco."],
  stazione_retrograda: ["Oggi {pianeta} si ferma nel cielo e inizia il suo moto retrogrado: un invito a rallentare."],
  stazione_diretta:    ["Oggi {pianeta} riprende il suo moto diretto: ciò che era bloccato può tornare a scorrere."]
 },

 // ---------- 4. Pianeti retrogradi in corso ----------
 retrogradi: {
  mercurio: ["Mercurio è retrogrado: un buon momento per rileggere, chiarire e ricontrollare, più che per firmare o partire.",
             "Con Mercurio retrogrado le parole possono essere fraintese: meglio una domanda in più che una risposta affrettata.",
             "Mercurio retrogrado invita a tornare su ciò che è rimasto in sospeso: messaggi, idee, conversazioni."],
  venere:   ["Venere è retrograda: gli affetti chiedono di essere guardati con occhi nuovi, senza fretta di decidere.",
             "Con Venere retrograda, legami e desideri del passato possono tornare a farsi sentire."],
  marte:    ["Marte è retrogrado: l'energia va dosata, meglio rivedere le strategie che forzare.",
             "Con Marte retrogrado, la fretta rischia di diventare attrito: scegli con cura dove mettere la tua forza."]
 },

 // ---------- 5. Perché una carta è "in risonanza" con il cielo ----------
 cause: {
  sole_nel_segno: ["{Carta} {è} {legame}, e in questo periodo il Sole attraversa proprio {segno_carta_art}: il suo messaggio risuona con più forza.",
                   "Il Sole si trova in {segno_carta}, il segno che la tradizione lega {a_carta}: non è un caso che {sia} uscit{o} proprio ora."],
  luna_nel_segno: ["{Carta} {è} {legame}, e proprio ora la Luna si trova in {segno_carta}: ciò che {carta} {rappresenta} tocca da vicino le emozioni di questo momento.",
                   "La Luna attraversa {segno_carta_art}, il segno {di_carta}: un richiamo che rende questa carta particolarmente vicina a ciò che senti."],
  fase:           ["{Carta} {è} {legame}, e con la {fase_nome} il suo richiamo all'ascolto interiore diventa più nitido.",
                   "Con la {fase_nome} in cielo, {carta}, carta della Luna, parla a voce più alta."],
  giorno:         ["{Carta} {è} {legame}, e oggi è {giorno}, il giorno che la tradizione dedica {pianeta_a}: una coincidenza che merita attenzione.",
                   "Oggi è {giorno}, giorno {pianeta_di}, e {carta} {è} proprio la sua carta."],
  retrogrado:     ["{Carta} {è} {legame}, e {pianeta} in questi giorni è {retrogrado}: il suo invito è a rivedere, più che a correre avanti.",
                   "Con {pianeta} {retrogrado}, {carta} chiede di tornare sui propri passi con calma."],
  stazione:       ["{Carta} {è} {legame}, e proprio oggi {pianeta} cambia direzione nel cielo: un momento di svolta per i temi di questa carta."],
  luna_elemento:  ["{Carta} {è} {legame}, e la Luna oggi si trova in {segno_luna}, segno {di_el}: elementi che si richiamano e si rafforzano.",
                   "La Luna in {segno_luna}, segno {di_el}, accende l'elemento {di_carta}."],
  evento_sole:    ["{Carta} {è} {legame}, e oggi il Sole vive uno dei suoi giorni speciali: la sua luce dà ancora più forza a questa carta."]
 },

 // ---------- 6. Il messaggio della carta in risonanza [dritta, rovesciata] ----------
 carte: {
  "00_il_matto": ["Il cielo sostiene la voglia di libertà: una scelta fatta con fiducia può aprire una strada nuova.",
                  "Il cielo invita però a non confondere coraggio e fretta: guarda bene prima di fare il salto."],
  "01_il_mago": ["Le parole e le idee hanno più forza del solito: è un buon momento per comunicare ciò che desideri.",
                 "Attenzione a malintesi e promesse vaghe: prima di parlare, chiarisci dentro di te cosa vuoi davvero."],
  "02_la_papessa": ["L'intuizione parla a voce più alta: concediti un momento di silenzio per ascoltarla.",
                    "Qualcosa che hai tenuto per te chiede di emergere: dargli voce può alleggerire il cuore."],
  "03_l_imperatrice": ["La bellezza, la cura e la creatività trovano terreno fertile: lascia crescere ciò che hai seminato.",
                       "Ricordati di nutrire anche te: la cura che dai agli altri ha bisogno di tornare a casa."],
  "04_l_imperatore": ["È un momento favorevole per dare struttura ai progetti e prendere in mano le decisioni.",
                      "Il rischio è irrigidirsi: la vera forza oggi sta nel guidare senza imporre."],
  "05_il_papa": ["Un consiglio saggio, un insegnamento o una tradizione possono indicare la via.",
                 "È il momento di chiederti quali regole senti ancora tue e quali puoi lasciare andare."],
  "06_gli_amanti": ["Le scelte del cuore e gli incontri hanno un significato speciale: ascolta cosa desideri davvero.",
                    "Una scelta rimandata chiede chiarezza: restare in mezzo al guado costa più che decidere."],
  "07_il_carro": ["La determinazione trova sostegno: puoi andare avanti mantenendo il controllo delle emozioni.",
                  "Prima di ripartire serve ritrovare la direzione: tirare le redini da tutte le parti porta solo fatica."],
  "08_la_forza": ["Il coraggio gentile è la tua risorsa: la calma vince più della forza.",
                  "Le emozioni possono prendere il sopravvento: concediti pazienza, anche nei tuoi confronti."],
  "09_l_eremita": ["Il cielo favorisce la riflessione e l'ordine: un passo indietro può farti vedere meglio.",
                   "Ritirarsi è utile, chiudersi del tutto no: lascia entrare qualcuno nei tuoi pensieri."],
  "10_la_ruota_della_fortuna": ["Le circostanze si muovono a tuo favore: osserva le occasioni che si presentano.",
                                "Non tutto dipende da te, e va bene così: adattarsi al cambiamento è già un modo di guidarlo."],
  "11_la_giustizia": ["Equilibrio e onestà sono le chiavi: le decisioni prese con chiarezza porteranno frutto.",
                      "Qualcosa è fuori equilibrio: guarda la situazione con occhi imparziali, anche nei tuoi confronti."],
  "12_l_appeso": ["Fermarsi non è perdere tempo: cambiare prospettiva può svelare una soluzione inattesa.",
                  "Un'attesa che dura troppo chiede una scelta: chiediti che cosa stai davvero aspettando."],
  "13_la_morte": ["Un ciclo si chiude per lasciare spazio al nuovo: accogli la trasformazione senza paura.",
                  "Resistere al cambiamento lo rende solo più faticoso: lasciar andare è il primo passo."],
  "14_la_temperanza": ["Pazienza e misura portano armonia: unire le parti diverse della tua vita è possibile.",
                       "Gli eccessi chiedono attenzione: ritrova il tuo ritmo, un passo alla volta."],
  "15_il_diavolo": ["È il momento di riconoscere ciò che ti trattiene: vederlo con chiarezza è già un modo per scioglierlo.",
                    "Una catena si allenta: hai più libertà di quanta ne immagini."],
  "16_la_torre": ["Ciò che non è solido può crollare, ma solo per lasciare spazio a fondamenta più vere.",
                  "Un cambiamento rimandato preme per arrivare: meglio accompagnarlo che subirlo."],
  "17_la_stella": ["Speranza e ispirazione tornano a brillare: fidati della direzione che senti.",
                   "Anche quando la fiducia vacilla, la luce non è spenta: cerca un piccolo segnale di speranza."],
  "18_la_luna": ["Sogni e intuizioni sono più vivi: ascoltali, ma verifica prima di trarre conclusioni.",
                 "Le nebbie iniziano a diradarsi: ciò che era confuso diventa più chiaro."],
  "19_il_sole": ["Energia, gioia e chiarezza sono a portata di mano: lascia che la tua luce si veda.",
                 "La luce c'è anche se velata: un piccolo gesto di fiducia può farla tornare."],
  "20_il_giudizio": ["Una chiamata interiore chiede ascolto: è il momento di rinascere a una nuova consapevolezza.",
                     "Il passato chiede di essere perdonato, non giudicato: solo così puoi rispondere al nuovo."],
  "21_il_mondo": ["Un traguardo è vicino: riconosci la strada percorsa e celebra ciò che hai raggiunto.",
                  "Manca un ultimo passo per chiudere il cerchio: non lasciare le cose a metà."]
 },

 // ---------- 7. Gli elementi della stesa ----------
 elementi: {
  prevale: {
   fuoco: ["Nella stesa prevale il fuoco: passione, iniziativa e voglia di agire guidano questo momento.",
           "Il fuoco domina le carte: l'energia c'è, va solo indirizzata con saggezza."],
   acqua: ["Nella stesa prevale l'acqua: emozioni e intuizione sono la chiave di lettura.",
           "L'acqua domina le carte: ascoltare ciò che senti conta più di ogni ragionamento."],
   aria:  ["Nella stesa prevale l'aria: idee, parole e scelte ragionate sono al centro.",
           "L'aria domina le carte: la chiarezza dei pensieri aprirà la strada."],
   terra: ["Nella stesa prevale la terra: concretezza, pazienza e questioni pratiche chiedono attenzione.",
           "La terra domina le carte: ciò che costruisci passo dopo passo durerà."]
  },
  tutte: {
   fuoco: ["Tutte e tre le carte appartengono al fuoco: un momento intenso, da vivere con slancio ma senza bruciare le tappe."],
   acqua: ["Tutte e tre le carte appartengono all'acqua: le emozioni sono profonde, lasciale scorrere senza farti travolgere."],
   aria:  ["Tutte e tre le carte appartengono all'aria: la mente lavora molto, ricordati di tornare anche al corpo e al cuore."],
   terra: ["Tutte e tre le carte appartengono alla terra: è il tempo del concreto, delle basi solide e della pazienza."]
  },
  diverse: ["Le tre carte appartengono a elementi diversi: la lettura chiede equilibrio tra mente, cuore e azione.",
            "Elementi diversi si incontrano in questa stesa: la risposta sta nel trovare un'armonia tra le parti."],
  rinforzo: ["E la Luna in {segno_luna}, segno {di_el}, ne amplifica l'effetto.",
             "La Luna in {segno_luna}, anch'essa {di_el}, rende questo tono ancora più evidente."]
 },

 // ---------- 8. Chiusura: il giorno e una domanda ----------
 chiusureGiorno: {
  sole:     ["La domenica è il giorno del Sole: concediti qualcosa che ti faccia stare bene.",
             "Nel giorno del Sole, la luce che cerchi può partire da un piccolo gesto di gioia."],
  luna:     ["Il lunedì è il giorno della Luna: dai ascolto alle emozioni prima di decidere.",
             "Nel giorno della Luna, l'intuizione è una buona consigliera."],
  marte:    ["Il martedì è il giorno di Marte: usa la tua energia per ciò che conta davvero.",
             "Nel giorno di Marte, il coraggio va unito alla misura."],
  mercurio: ["Il mercoledì è il giorno di Mercurio: una parola detta al momento giusto può cambiare molto.",
             "Nel giorno di Mercurio, comunicare con chiarezza apre porte."],
  giove:    ["Il giovedì è il giorno di Giove: guarda lontano e lascia spazio alla fiducia.",
             "Nel giorno di Giove, la generosità torna indietro moltiplicata."],
  venere:   ["Il venerdì è il giorno di Venere: coltiva la bellezza e i legami che ti fanno bene.",
             "Nel giorno di Venere, un gesto d'affetto vale più di mille parole."],
  saturno:  ["Il sabato è il giorno di Saturno: è il momento di mettere ordine e dare tempo al tempo.",
             "Nel giorno di Saturno, la pazienza costruisce basi solide."]
 },
 domande: ["Quale piccolo passo senti possibile già oggi?",
           "Che cosa vuoi lasciare andare, e che cosa vuoi accogliere?",
           "Di che cosa hai davvero bisogno in questo momento?",
           "Quale voce interiore merita più ascolto?",
           "Che cosa cambierebbe se ti fidassi un po' di più?",
           "Quale parte di questa lettura risuona di più con la tua vita adesso?"],

 avvertenza: "I riferimenti al cielo seguono la tradizione simbolica dei tarocchi: sono uno spunto di riflessione, non una previsione."
};
