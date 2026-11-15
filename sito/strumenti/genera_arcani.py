# -*- coding: utf-8 -*-
"""
Genera le pagine dei 22 Arcani Maggiori (arcani/<slug>.html) e l'indice (arcani/index.html)
partendo dai testi in asset/descrizione_it/*.md.
Uso (dalla cartella del sito):  python strumenti/genera_arcani.py
Le immagini leggere in asset/img_web/ si rigenerano con:  python strumenti/genera_arcani.py --immagini
"""
import html, json, os, re

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOM = "https://22arcani.it"

ARCANI = [
 ("00_il_matto","Il Matto","0","libertà, nuovi inizi, spontaneità, fiducia nella vita","imprudenza, distrazione, rischi inutili"),
 ("01_il_mago","Il Mago","I","volontà, abilità, iniziativa, comunicazione","manipolazione, insicurezza, talenti sprecati"),
 ("02_la_papessa","La Papessa","II","intuizione, saggezza interiore, mistero, silenzio","segreti, chiusura, intuizione ignorata"),
 ("03_l_imperatrice","L'Imperatrice","III","abbondanza, creatività, fertilità, cura","blocco creativo, dipendenza, trascuratezza"),
 ("04_l_imperatore","L'Imperatore","IV","autorità, struttura, stabilità, protezione","rigidità, controllo eccessivo, autoritarismo"),
 ("05_il_papa","Il Papa","V","tradizione, insegnamento, valori, guida spirituale","ribellione, dogmatismo, scelte fuori dagli schemi"),
 ("06_gli_amanti","Gli Amanti","VI","amore, scelta, armonia, unione","indecisione, disarmonia, scelte affrettate"),
 ("07_il_carro","Il Carro","VII","determinazione, vittoria, controllo, movimento","perdita di controllo, ostacoli, mancanza di direzione"),
 ("08_la_forza","La Forza","VIII","coraggio, pazienza, dominio di sé, compassione","insicurezza, debolezza, impulsività"),
 ("09_l_eremita","L'Eremita","IX","introspezione, ricerca interiore, saggezza, solitudine","isolamento, chiusura, rifiuto dei consigli"),
 ("10_la_ruota_della_fortuna","La Ruota della Fortuna","X","cambiamento, destino, cicli, opportunità","battute d'arresto, resistenza al cambiamento, sfortuna"),
 ("11_la_giustizia","La Giustizia","XI","equilibrio, verità, responsabilità, decisioni","ingiustizia, squilibrio, disonestà"),
 ("12_l_appeso","L'Appeso","XII","pausa, sacrificio, nuova prospettiva, attesa","stallo, resistenza, sacrifici inutili"),
 ("13_la_morte","La Morte","XIII","trasformazione, fine di un ciclo, rinascita","paura del cambiamento, stagnazione, attaccamento al passato"),
 ("14_la_temperanza","La Temperanza","XIV","equilibrio, moderazione, pazienza, armonia","eccessi, squilibrio, impazienza"),
 ("15_il_diavolo","Il Diavolo","XV","tentazione, attaccamento, desiderio, materialismo","liberazione, presa di coscienza, rottura delle catene"),
 ("16_la_torre","La Torre","XVI","cambiamento improvviso, crollo, rivelazione","crisi rimandata, paura del cambiamento, resistenza"),
 ("17_la_stella","La Stella","XVII","speranza, ispirazione, rinnovamento, serenità","sfiducia, scoraggiamento, speranze deluse"),
 ("18_la_luna","La Luna","XVIII","illusione, inconscio, paure, intuizione","chiarezza ritrovata, paure che si dissolvono, confusione"),
 ("19_il_sole","Il Sole","XIX","gioia, successo, vitalità, chiarezza","entusiasmo offuscato, ritardi, ottimismo eccessivo"),
 ("20_il_giudizio","Il Giudizio","XX","risveglio, rinascita, chiamata interiore, bilancio","autocritica, dubbi, occasioni mancate"),
 ("21_il_mondo","Il Mondo","XXI","compimento, realizzazione, viaggio, integrazione","incompletezza, ritardi, obiettivi non raggiunti"),
]

NOTE = {
 "13_la_morte": "Nonostante il nome, la Morte nei tarocchi non annuncia una morte fisica: rappresenta la chiusura di una fase e l'inizio di qualcosa di nuovo.",
 "16_la_torre": "La Torre è una delle carte più temute, ma il crollo che annuncia libera spazio per costruire su basi più solide.",
 "15_il_diavolo": "Il Diavolo non va letto come una carta \"malvagia\": parla dei legami e delle abitudini che ci tengono prigionieri.",
}

POSIZIONI = ["Passato", "Presente", "Futuro"]

# Messaggio generale della "Carta del giorno" (dritta, rovesciata): non dipende da passato/presente/futuro
MESSAGGI_GIORNO = {
 "00_il_matto": ("Oggi il Matto ti invita a lasciare spazio alla spontaneità. Un'idea nuova, un incontro o una piccola avventura possono portare aria fresca: fidati del tuo istinto e non avere paura di uscire dai soliti schemi.",
                 "Il Matto rovesciato oggi chiede prudenza. La voglia di cambiare è forte, ma prima di fare un salto nel vuoto guarda bene dove metti i piedi: una decisione presa con leggerezza potrebbe costarti più del previsto."),
 "01_il_mago": ("Il Mago ti ricorda che hai già tutto ciò che ti serve. È una giornata adatta per cominciare qualcosa, comunicare un'idea o mettere alla prova le tue capacità: la tua volontà fa la differenza.",
                "Il Mago rovesciato invita a fare attenzione alle apparenze. Qualcuno potrebbe non essere del tutto sincero, oppure sei tu a dubitare delle tue capacità: resta concreto e non disperdere le energie."),
 "02_la_papessa": ("La Papessa porta una giornata di ascolto interiore. Le risposte che cerchi non arriveranno dal rumore esterno ma dal silenzio: osserva, rifletti e lascia parlare l'intuizione.",
                   "La Papessa rovesciata segnala qualcosa di non detto. Un segreto, un'emozione trattenuta o un'intuizione che stai ignorando chiedono di venire alla luce: oggi è meglio essere sinceri, prima di tutto con te."),
 "03_l_imperatrice": ("L'Imperatrice porta abbondanza e creatività. È un buon giorno per prenderti cura di te e delle persone che ami, coltivare un progetto o goderti la bellezza delle piccole cose.",
                      "L'Imperatrice rovesciata ti chiede di non trascurarti. Forse stai dando molto agli altri e poco a te, o la creatività è bloccata: concediti una pausa e ritrova ciò che ti nutre."),
 "04_l_imperatore": ("L'Imperatore invita all'ordine e alla concretezza. Oggi sei in grado di prendere in mano la situazione, organizzare e decidere: una struttura solida ti aiuterà a ottenere risultati.",
                     "L'Imperatore rovesciato avverte di un eccesso di controllo. Rigidità o scontri con l'autorità possono complicare la giornata: prova ad ascoltare prima di imporre il tuo punto di vista."),
 "05_il_papa": ("Il Papa porta saggezza e buoni consigli. Oggi può essere utile confrontarti con una persona di fiducia o tornare ai valori in cui credi: la tradizione può indicarti la strada.",
                "Il Papa rovesciato ti invita a pensare con la tua testa. Regole e opinioni altrui potrebbero starti strette: non temere di seguire una strada diversa, se senti che è quella giusta."),
 "06_gli_amanti": ("Gli Amanti parlano di relazioni e di scelte. Oggi il cuore ha voce in capitolo: è una giornata favorevole per i legami affettivi e per decisioni prese in armonia con ciò in cui credi.",
                   "Gli Amanti rovesciati segnalano un'indecisione o una piccola disarmonia. Prima di scegliere, chiarisci che cosa desideri davvero: un dialogo sincero può sciogliere molti nodi."),
 "07_il_carro": ("Il Carro porta slancio e determinazione. È il giorno giusto per andare avanti verso un obiettivo: mantieni la direzione e non lasciarti distrarre, la vittoria è a portata di mano.",
                 "Il Carro rovesciato indica un momento in cui le cose sembrano sfuggire al controllo. Prima di accelerare, fermati e decidi dove vuoi andare davvero: oggi la fretta non è una buona alleata."),
 "08_la_forza": ("La Forza ti ricorda che la vera forza è gentile. Oggi puoi affrontare una difficoltà con calma e pazienza, senza alzare la voce: la tua serenità sarà la tua arma migliore.",
                 "La Forza rovesciata segnala insicurezza o impulsività. Se ti senti fragile o reagisci d'istinto, fai un respiro profondo: hai più risorse di quanto pensi."),
 "09_l_eremita": ("L'Eremita invita a rallentare e a guardarti dentro. Una giornata di riflessione, magari in solitudine, può portarti la chiarezza che cerchi: non tutte le risposte stanno fuori.",
                  "L'Eremita rovesciato avverte del rischio di chiuderti troppo nel tuo mondo. Isolarti non risolve: oggi aprirti a qualcuno di fiducia può illuminare la situazione."),
 "10_la_ruota_della_fortuna": ("La Ruota della Fortuna gira a tuo favore. Oggi possono arrivare novità, coincidenze fortunate o un cambio di rotta: resta aperto alle opportunità e coglile al volo.",
                               "La Ruota della Fortuna rovesciata parla di un momento di stallo o di piccoli contrattempi. Non tutto dipende da te: accetta il ritmo delle cose, perché la ruota prima o poi torna a girare."),
 "11_la_giustizia": ("La Giustizia chiede equilibrio e onestà. È una buona giornata per prendere decisioni ponderate, chiarire una questione o rimettere in ordine ciò che è rimasto in sospeso.",
                     "La Giustizia rovesciata segnala uno squilibrio. Forse qualcosa ti sembra ingiusto, o stai evitando una responsabilità: oggi conviene essere onesti e cercare una soluzione equa."),
 "12_l_appeso": ("L'Appeso invita a fermarti e a guardare le cose da un'altra prospettiva. Un'attesa o una rinuncia momentanea possono rivelarsi preziose: non tutto va risolto subito.",
                 "L'Appeso rovesciato indica un'attesa che si è prolungata troppo. Se senti di essere in stallo, oggi è il momento di fare anche solo un piccolo passo: restare fermi non porta da nessuna parte."),
 "13_la_morte": ("La Morte, nonostante il nome, annuncia una trasformazione. Oggi qualcosa si chiude per lasciare spazio al nuovo: lascia andare ciò che non ti serve più e guarda avanti.",
                 "La Morte rovesciata parla di un cambiamento che fai fatica ad accettare. Trattenere il passato ti tiene fermo: oggi prova a lasciar andare, anche solo un po'."),
 "14_la_temperanza": ("La Temperanza porta calma ed equilibrio. È una giornata adatta per trovare la giusta misura, fare pace con qualcuno o procedere con pazienza, un passo alla volta.",
                      "La Temperanza rovesciata segnala eccessi o impazienza. Se ti senti fuori equilibrio, rallenta: oggi conviene evitare gli estremi e ritrovare il tuo ritmo."),
 "15_il_diavolo": ("Il Diavolo parla di desideri e di legami. Oggi chiediti che cosa ti tiene attaccato a una persona, un'abitudine o una situazione: riconoscerlo è il primo passo per scegliere liberamente.",
                   "Il Diavolo rovesciato annuncia una liberazione. Un legame che ti pesava, una cattiva abitudine o una paura possono perdere forza: oggi è un buon giorno per spezzare le catene."),
 "16_la_torre": ("La Torre annuncia un cambiamento improvviso. Qualcosa potrebbe non andare come previsto, ma ciò che crolla lascia spazio a basi più solide: accogli la novità senza paura.",
                 "La Torre rovesciata indica un cambiamento che stai rimandando. Evitare lo scossone non lo fa sparire: oggi affronta con calma ciò che sai che va cambiato."),
 "17_la_stella": ("La Stella porta speranza e serenità. È una giornata luminosa, adatta ai sogni e ai progetti: abbi fiducia, sei sulla strada giusta.",
                  "La Stella rovesciata parla di un momento di sfiducia. Anche se senti un po' di scoraggiamento, la luce non è spenta: oggi cerca i piccoli segnali positivi e riparti da lì."),
 "18_la_luna": ("La Luna porta una giornata di emozioni e intuizioni. Non tutto è chiaro come sembra: ascolta il tuo sesto senso, ma verifica bene prima di trarre conclusioni.",
                "La Luna rovesciata annuncia che le nebbie si diradano. Paure e dubbi perdono forza e inizi a vedere le cose con più lucidità: fidati di ciò che ora ti appare chiaro."),
 "19_il_sole": ("Il Sole è una delle carte più positive del mazzo. Oggi porta gioia, energia e successo: goditi la giornata e condividi il tuo entusiasmo con chi ti sta vicino.",
                "Il Sole rovesciato offusca un po' l'entusiasmo, ma non lo spegne. Se le cose vanno più a rilento del previsto, non scoraggiarti: la luce tornerà presto a splendere."),
 "20_il_giudizio": ("Il Giudizio porta un risveglio. Oggi può arrivare una chiamata, una notizia o una presa di coscienza importante: ascoltala, potrebbe segnare un nuovo inizio.",
                    "Il Giudizio rovesciato invita a trattarti con meno severità. Dubbi e autocritica possono frenarti: oggi perdona i tuoi errori e guarda a ciò che puoi ancora fare."),
 "21_il_mondo": ("Il Mondo annuncia compimento e soddisfazione. Un ciclo si chiude nel migliore dei modi: oggi celebra ciò che hai raggiunto e preparati a un nuovo viaggio.",
                 "Il Mondo rovesciato indica qualcosa di ancora incompiuto. Il traguardo è vicino, ma manca un ultimo passo: oggi concentrati su ciò che hai lasciato in sospeso."),
}

# Consiglio di ogni carta (dritta, rovesciata) usato nella sintesi finale della lettura
CONSIGLI = {
 "00_il_matto": ("segui l'istinto e accogli il nuovo con fiducia", "prima di lanciarti, prenditi il tempo di valutare i rischi"),
 "01_il_mago": ("usa i tuoi talenti: hai già gli strumenti per cominciare", "agisci con sincerità e non disperdere le tue capacità"),
 "02_la_papessa": ("ascolta la tua voce interiore prima di decidere", "non ignorare ciò che senti: porta alla luce ciò che tieni nascosto"),
 "03_l_imperatrice": ("dai spazio alla creatività e prenditi cura di ciò che ami", "ritrova il contatto con te prima di dedicarti agli altri"),
 "04_l_imperatore": ("dai una struttura ai tuoi progetti e prendi in mano la situazione", "allenta il controllo: la rigidità può frenarti"),
 "05_il_papa": ("cerca il consiglio di una persona saggia e resta fedele ai tuoi valori", "non temere di seguire una strada tutta tua"),
 "06_gli_amanti": ("scegli con il cuore, restando coerente con ciò in cui credi", "prima di scegliere, chiarisci che cosa desideri davvero"),
 "07_il_carro": ("vai avanti con determinazione: la direzione è giusta", "riprendi il controllo e fissa una meta chiara"),
 "08_la_forza": ("affronta le difficoltà con calma e coraggio gentile", "abbi fiducia in te e non lasciarti guidare dall'impulso"),
 "09_l_eremita": ("concediti un momento di silenzio per trovare le tue risposte", "non isolarti: aprirti agli altri può illuminare il cammino"),
 "10_la_ruota_della_fortuna": ("cogli le opportunità: il cambiamento gioca a tuo favore", "accetta ciò che non puoi controllare e aspetta il momento giusto"),
 "11_la_giustizia": ("agisci con equilibrio e assumiti le tue responsabilità", "usa onestà verso di te e rimetti in equilibrio ciò che non lo è"),
 "12_l_appeso": ("fermati e guarda la situazione da un'altra prospettiva", "non restare bloccato nell'attesa: fai un piccolo passo"),
 "13_la_morte": ("lascia andare ciò che è finito per fare spazio al nuovo", "non avere paura del cambiamento: trattenere il passato ti blocca"),
 "14_la_temperanza": ("cerca la giusta misura e procedi con pazienza", "evita gli eccessi e ritrova il tuo equilibrio"),
 "15_il_diavolo": ("riconosci ciò che ti lega e chiediti se ti fa davvero bene", "è il momento di liberarti di un legame o di un'abitudine che ti pesa"),
 "16_la_torre": ("accogli il cambiamento: ciò che crolla lascia spazio a basi più solide", "non rimandare un cambiamento ormai necessario"),
 "17_la_stella": ("coltiva la speranza: sei sulla strada giusta", "ritrova la fiducia, partendo dai piccoli segnali positivi"),
 "18_la_luna": ("ascolta l'intuito, ma verifica prima di trarre conclusioni", "le paure si stanno dissolvendo: guarda le cose con lucidità"),
 "19_il_sole": ("goditi il momento e condividi la tua gioia", "non perdere l'entusiasmo: i risultati arriveranno, anche se con un po' di ritardo"),
 "20_il_giudizio": ("ascolta la chiamata interiore e fai il bilancio di ciò che hai vissuto", "perdonati e non lasciarti frenare dai dubbi"),
 "21_il_mondo": ("porta a termine ciò che hai iniziato: il traguardo è vicino", "completa ciò che hai lasciato in sospeso prima di iniziare qualcosa di nuovo"),
}

FEMMINILI = {"02_la_papessa","03_l_imperatrice","08_la_forza","10_la_ruota_della_fortuna","11_la_giustizia",
             "13_la_morte","14_la_temperanza","16_la_torre","17_la_stella","18_la_luna"}
PLURALI = {"06_gli_amanti"}

def accorda(fid, parola):
    """dritto/rovesciato concordati con il nome della carta."""
    radice = parola[:-1]
    if fid in PLURALI: return radice + "i"
    if fid in FEMMINILI: return radice + "a"
    return parola

def slug(file_id):
    return file_id[3:].replace("_", "-")

def leggi(file_id, rov, pos):
    nome = f"{file_id}{'_r' if rov else ''}_{pos}.md"
    with open(os.path.join(BASE, "asset", "descrizione_it", nome), encoding="utf-8-sig") as f:
        testo = f.read()
    paragrafi = [p.strip() for p in re.split(r"\r?\n", testo) if p.strip()]
    return "\n".join(f"        <p>{html.escape(p, quote=False)}</p>" for p in paragrafi)

def pagina(i):
    fid, nome, num, kw_d, kw_r = ARCANI[i]
    s = slug(fid)
    url = f"{DOM}/arcani/{s}"
    prev_ = ARCANI[i-1] if i > 0 else None
    next_ = ARCANI[i+1] if i < len(ARCANI)-1 else None
    dr, rv = accorda(fid, "dritto"), accorda(fid, "rovesciato")
    titolo = f"{nome} nei Tarocchi: significato {dr} e {rv} | 22 Arcani"
    desc = (f"Cosa {'significano' if fid in PLURALI else 'significa'} {nome} nei tarocchi? {dr.capitalize()}: {kw_d}. {rv.capitalize()}: {kw_r}. "
            f"Il significato nel passato, nel presente e nel futuro e la lettura gratuita online.")
    faq = [
        (f"Cosa {'significano' if fid in PLURALI else 'significa'} {nome} nei tarocchi?",
         f"{nome} {'sono' if fid in PLURALI else 'è'} l'Arcano Maggiore numero {num}. Quando {'escono dritti' if fid in PLURALI else 'esce ' + dr} {'indicano' if fid in PLURALI else 'indica'} {kw_d}. {MESSAGGI_GIORNO[fid][0]}"),
        (f"Cosa {'significano' if fid in PLURALI else 'significa'} {nome} {rv}?",
         f"Quando {'escono' if fid in PLURALI else 'esce'} {rv}, {nome} {'indicano' if fid in PLURALI else 'indica'} {kw_r}. {MESSAGGI_GIORNO[fid][1]}"),
    ]
    faq_ld = {"@context": "https://schema.org", "@type": "FAQPage",
              "mainEntity": [{"@type": "Question", "name": q,
                              "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}
    faq_html = "\n".join(f"      <h3>{html.escape(q, quote=False)}</h3>\n      <p>{html.escape(a, quote=False)}</p>" for q, a in faq)
    tutte = " ".join(f'<a href="/arcani/{slug(a[0])}">{a[1]}</a>' for a in ARCANI if a[0] != fid)
    img = f"/asset/img_it/{fid}.jpeg"          # originale (anteprima social)
    img_web = f"/asset/img_web/{fid}.webp"     # 400 px, per la pagina
    img_mini = f"/asset/img_web/{fid}_240.webp" # 240 px, miniature
    nota = f'\n      <p class="nota">{html.escape(NOTE[fid], quote=False)}</p>' if fid in NOTE else ""

    def sezione(rov):
        blocchi = []
        for pos in POSIZIONI:
            blocchi.append(
                f'      <h3>{nome}{" " + accorda(fid, "rovesciato") if rov else ""} nel {pos.lower()}</h3>\n'
                f'{leggi(fid, rov, pos)}')
        return "\n".join(blocchi)

    breadcrumb = {
        "@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "22 Arcani", "item": DOM + "/"},
            {"@type": "ListItem", "position": 2, "name": "Arcani Maggiori", "item": DOM + "/arcani/"},
            {"@type": "ListItem", "position": 3, "name": nome, "item": url},
        ]}

    nav = '    <nav class="prevnext">\n'
    nav += (f'      <a href="/arcani/{slug(prev_[0])}">&larr; {prev_[1]}</a>\n' if prev_ else '      <span></span>\n')
    nav += '      <a href="/arcani/">Tutti gli Arcani</a>\n'
    nav += (f'      <a href="/arcani/{slug(next_[0])}">{next_[1]} &rarr;</a>\n' if next_ else '      <span></span>\n')
    nav += '    </nav>'

    return f"""<!DOCTYPE html>
<html lang="it">
<head>
  <meta charset="UTF-8">
  <link rel="icon" href="/favicon.svg" type="image/svg+xml">
  <link rel="icon" href="/favicon-48.png" sizes="48x48" type="image/png">
  <link rel="apple-touch-icon" href="/apple-touch-icon.png">
  <link rel="manifest" href="/manifest.webmanifest">
  <meta name="theme-color" content="#111111">
  <script src="/pwa.js" defer></script>
  <script src="/analytics.js"></script>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(titolo)}</title>
  <meta name="description" content="{html.escape(desc)}">
  <link rel="canonical" href="{url}">
  <meta property="og:type" content="article">
  <meta property="og:title" content="{html.escape(titolo)}">
  <meta property="og:description" content="{html.escape(desc)}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{DOM}{img}">
  <link href="https://fonts.googleapis.com/css2?family=Cinzel+Decorative:wght@400;700&family=Playfair+Display:wght@400;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/arcani/arcani.css">
  <script type="application/ld+json">{json.dumps(breadcrumb, ensure_ascii=False)}</script>
  <script type="application/ld+json">{json.dumps(faq_ld, ensure_ascii=False)}</script>
</head>
<body>
  <header class="testata">
    <a class="logo" href="/">22 Arcani</a>
    <nav><a href="/arcani/">Arcani Maggiori</a> <a class="pill" href="/master">Fai una lettura</a></nav>
  </header>

  <main class="arcano">
    <p class="briciole"><a href="/">Home</a> &rsaquo; <a href="/arcani/">Arcani Maggiori</a> &rsaquo; {nome}</p>
    <h1>{nome} nei Tarocchi: significato {dr} e {rv}</h1>

    <section class="intro">
      <img src="{img_web}" alt="Carta dei tarocchi {nome}, Arcano Maggiore {num}" width="240" height="403">
      <div>
        <p><strong>{nome}</strong> {'sono' if fid in PLURALI else 'è'} l'Arcano Maggiore numero <strong>{num}</strong> dei tarocchi. Il suo significato cambia a seconda che la carta esca <strong>dritta</strong> o <strong>rovesciata</strong> e della posizione che occupa nella stesa: passato, presente o futuro.</p>
        <p><span class="etichetta">Dritto:</span> {kw_d}.</p>
        <p><span class="etichetta">Rovesciato:</span> {kw_r}.</p>{nota}
        <a class="cta" href="/master">Scopri cosa dicono le carte per te</a>
      </div>
    </section>

    <section>
      <h2>{nome} {dr}: significato</h2>
{sezione(False)}
    </section>

    <section>
      <h2>{nome} {rv}: significato</h2>
      <img class="rovesciata" src="{img_mini}" alt="{nome} {accorda(fid, 'rovesciato')}" width="120" height="201" loading="lazy">
{sezione(True)}
    </section>

    <section class="faq">
      <h2>Domande frequenti su {nome}</h2>
{faq_html}
    </section>

    <section class="finale">
      <h2>Fai la tua lettura gratuita</h2>
      <p>Mescola il mazzo, scegli tre carte e scopri cosa raccontano del tuo passato, presente e futuro. È gratuita e non serve registrarsi.</p>
      <a class="cta" href="/master">Inizia la lettura</a>
    </section>

{nav}

    <section class="tutte">
      <h2>Gli altri Arcani Maggiori</h2>
      <p>{tutte}</p>
    </section>
  </main>

  <footer class="piede"><a href="/">22arcani.it</a> · <a href="/arcani/">Arcani Maggiori</a> · <a href="/privacy">Privacy e cookie</a></footer>
</body>
</html>
"""

def indice():
    voci = "\n".join(
        f'      <li><a href="/arcani/{slug(fid)}"><img src="/asset/img_web/{fid}_240.webp" alt="{nome}, Arcano Maggiore {num}" width="120" height="201" loading="lazy">'
        f'<span class="num">{num}</span><span class="nome">{nome}</span><span class="kw">{", ".join(k.strip() for k in kw_d.split(",")[:2])}</span></a></li>'
        for fid, nome, num, kw_d, _ in ARCANI)
    righe = "\n".join(
        f'        <tr><td>{num}</td><td><a href="/arcani/{slug(fid)}">{nome}</a></td><td>{kw_d}</td><td>{kw_r}</td></tr>'
        for fid, nome, num, kw_d, kw_r in ARCANI)
    nomi = ", ".join(f"{nome} ({num})" for _, nome, num, _, _ in ARCANI)
    titolo = "I 22 Arcani Maggiori dei Tarocchi: significato di tutte le carte | 22 Arcani"
    desc = ("I 22 Arcani Maggiori dei tarocchi, dal Matto al Mondo: elenco completo e significato di ogni carta, "
            "dritta e rovesciata, nel passato, nel presente e nel futuro. Lettura gratuita online.")
    faq = [
        ("Quali sono i 22 Arcani Maggiori dei tarocchi?",
         f"Gli Arcani Maggiori sono 22 carte numerate da 0 a XXI: {nomi}."),
        ("Che differenza c'è tra Arcani Maggiori e Arcani Minori?",
         "Un mazzo di tarocchi ha 78 carte: 22 Arcani Maggiori e 56 Arcani Minori. I Maggiori rappresentano i grandi temi e le tappe importanti della vita; i Minori, divisi in quattro semi (Coppe, Denari, Spade e Bastoni), descrivono le situazioni di tutti i giorni."),
        ("Cosa significa una carta dei tarocchi rovesciata?",
         "Una carta rovesciata esce capovolta. Di solito indica che l'energia della carta è bloccata, rallentata o vissuta in modo eccessivo: per esempio la Torre rovesciata parla di un cambiamento rimandato, la Morte rovesciata della paura di lasciar andare."),
        ("Come si fa una lettura con gli Arcani Maggiori?",
         "La stesa più semplice usa tre carte: la prima per il passato, la seconda per il presente, la terza per il futuro. Su 22 Arcani puoi mescolare il mazzo, scegliere le tue tre carte e leggere l'interpretazione completa gratis."),
    ]
    faq_ld = {"@context": "https://schema.org", "@type": "FAQPage",
              "mainEntity": [{"@type": "Question", "name": q,
                              "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]}
    lista_ld = {"@context": "https://schema.org", "@type": "ItemList", "name": "I 22 Arcani Maggiori dei Tarocchi",
                "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": a[1],
                                     "url": f"{DOM}/arcani/{slug(a[0])}"} for i, a in enumerate(ARCANI)]}
    faq_html = "\n".join(f"      <h3>{html.escape(q, quote=False)}</h3>\n      <p>{html.escape(a, quote=False)}</p>" for q, a in faq)
    return f"""<!DOCTYPE html>
<html lang="it">
<head>
  <meta charset="UTF-8">
  <link rel="icon" href="/favicon.svg" type="image/svg+xml">
  <link rel="icon" href="/favicon-48.png" sizes="48x48" type="image/png">
  <link rel="apple-touch-icon" href="/apple-touch-icon.png">
  <link rel="manifest" href="/manifest.webmanifest">
  <meta name="theme-color" content="#111111">
  <script src="/pwa.js" defer></script>
  <script src="/analytics.js"></script>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(titolo)}</title>
  <meta name="description" content="{html.escape(desc)}">
  <link rel="canonical" href="{DOM}/arcani/">
  <meta property="og:title" content="I 22 Arcani Maggiori dei Tarocchi: significato di tutte le carte">
  <meta property="og:description" content="{html.escape(desc)}">
  <meta property="og:url" content="{DOM}/arcani/">
  <meta property="og:image" content="{DOM}/asset/tarot_corona.jpg">
  <link href="https://fonts.googleapis.com/css2?family=Cinzel+Decorative:wght@400;700&family=Playfair+Display:wght@400;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/arcani/arcani.css">
  <script type="application/ld+json">{json.dumps(lista_ld, ensure_ascii=False)}</script>
  <script type="application/ld+json">{json.dumps(faq_ld, ensure_ascii=False)}</script>
</head>
<body>
  <header class="testata">
    <a class="logo" href="/">22 Arcani</a>
    <nav><a href="/arcani/">Arcani Maggiori</a> <a class="pill" href="/master">Fai una lettura</a></nav>
  </header>

  <main class="arcano">
    <p class="briciole"><a href="/">Home</a> &rsaquo; Arcani Maggiori</p>
    <h1>I 22 Arcani Maggiori dei Tarocchi</h1>
    <p class="lead">Gli Arcani Maggiori sono le 22 carte principali dei tarocchi, numerate dal Matto (0) al Mondo (XXI). Ognuna racconta una tappa importante della vita e ha un significato diverso se esce dritta o rovesciata, e se si trova nella posizione del passato, del presente o del futuro. Scegli una carta per leggere tutte le sue interpretazioni.</p>
    <ul class="griglia">
{voci}
    </ul>

    <section>
      <h2>Elenco e significato dei 22 Arcani Maggiori</h2>
      <div class="tabella">
      <table class="elenco">
        <thead><tr><th>N.</th><th>Carta</th><th>Dritta</th><th>Rovesciata</th></tr></thead>
        <tbody>
{righe}
        </tbody>
      </table>
      </div>
    </section>

    <section>
      <h2>Arcani Maggiori dritti e rovesciati</h2>
      <p>Ogni Arcano Maggiore può uscire <strong>dritto</strong> o <strong>rovesciato</strong>. Da dritta, la carta esprime la sua energia in modo pieno e diretto; da rovesciata, quella stessa energia è bloccata, rimandata oppure vissuta in eccesso. Per questo su 22 Arcani trovi per ogni carta sei interpretazioni: dritta e rovesciata, nel passato, nel presente e nel futuro.</p>
    </section>

    <section class="faq">
      <h2>Domande frequenti sugli Arcani Maggiori</h2>
{faq_html}
    </section>

    <section class="finale">
      <h2>Fai la tua lettura gratuita</h2>
      <p>Mescola il mazzo e scegli tre carte: scoprirai cosa raccontano del tuo passato, presente e futuro.</p>
      <a class="cta" href="/master">Inizia la lettura</a>
    </section>
  </main>

  <footer class="piede"><a href="/">22arcani.it</a> · <a href="/privacy">Privacy e cookie</a></footer>
</body>
</html>
"""

def scrivi_sintesi_js():
    """Crea sintesi_dati.js: nomi, parole chiave e consigli delle carte per la sintesi finale."""
    dati = {}
    for fid, nome, num, kw_d, kw_r in ARCANI:
        genere = "p" if fid in PLURALI else ("f" if fid in FEMMINILI else "m")
        dati[fid] = {"nome": nome, "genere": genere,
                     "kw": [[k.strip() for k in kw_d.split(",")], [k.strip() for k in kw_r.split(",")]],
                     "consiglio": list(CONSIGLI[fid]),
                     "giorno": list(MESSAGGI_GIORNO[fid])}
    with open(os.path.join(BASE, "sintesi_dati.js"), "w", encoding="utf-8", newline="\r\n") as f:
        f.write("// File generato da strumenti/genera_arcani.py: non modificare a mano.\n")
        f.write("window.ZODIEL_ARCANI = " + json.dumps(dati, ensure_ascii=False, indent=1) + ";\n")
    print("Creato sintesi_dati.js")

def scrivi(nome_file, testo):
    with open(os.path.join(BASE, "arcani", nome_file), "w", encoding="utf-8", newline="\r\n") as f:
        f.write(testo)

def genera_immagini():
    """Crea in asset/img_web/ le versioni WebP leggere delle carte (400 px e 240 px)."""
    from PIL import Image
    os.makedirs(os.path.join(BASE, "asset", "img_web"), exist_ok=True)
    for fid, *_ in ARCANI:
        im = Image.open(os.path.join(BASE, "asset", "img_it", fid + ".jpeg")).convert("RGB")
        for larghezza, suffisso in ((400, ""), (240, "_240")):
            altezza = round(im.height * larghezza / im.width)
            im.resize((larghezza, altezza), Image.LANCZOS).save(
                os.path.join(BASE, "asset", "img_web", f"{fid}{suffisso}.webp"), "WEBP", quality=70, method=6)
    print("Immagini WebP create in asset/img_web/")

if __name__ == "__main__":
    import sys
    if "--immagini" in sys.argv:
        genera_immagini()
    os.makedirs(os.path.join(BASE, "arcani"), exist_ok=True)
    for i in range(len(ARCANI)):
        scrivi(slug(ARCANI[i][0]) + ".html", pagina(i))
    scrivi("index.html", indice())
    scrivi_sintesi_js()
    print("Create", len(ARCANI), "pagine + indice")
