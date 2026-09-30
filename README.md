# Registro Presenze — Denny

App web personale per gestire il registro presenze: **📅 Calendario**, **📊 Report** e **⚙️ Impostazioni**.
Lo storico parte dal **25/09/2025** ed è stato importato dal calendario Google personale il 30/09/2026.

Il registro Excel di un collega è servito solo come modello di struttura e di logica. Nell'app non c'è nessun suo dato.

## Cosa fa

- **Calendario**: vista mensile con il codice di ogni giornata (Lavoro, Scambi, Trasferta, Congedo…), il turno pomeridiano (POM), gli straordinari e le note. Tocca un giorno per modificarlo; il salvataggio è immediato.
- **Report**: per anno, mese o intervallo di date mostra:
  - giornate lavorate per codice;
  - straordinari per mese, con l'elenco dei giorni;
  - congedo usato e residuo per anno di maturazione;
  - permessi, malattia, riposi, festività e turni pomeridiani;
  - l'andamento mensile e i mezzi su cui hai lavorato.
- **Impostazioni**:
  - codici, anni e parametri annuali;
  - backup JSON e ripristino, con copia automatica prima di sostituire i dati;
  - import ed export Excel, export CSV;
  - gestione dati e controlli;
  - tema chiaro/scuro;
  - ripristino protetto da doppia conferma.

## Regole di calcolo

| Voce | Regola |
|---|---|
| Giornata lavorata | Giornata con un codice segnato come «lavorativo» (Lavoro, Scambi, AT in turno, 41 bis, Distolto, Ordine cattedrale, Visita medica, Corso, Trasferta). |
| Congedo (= ferie) | Ogni giornata «Congedo» scala 1 giorno, consumando **prima l'anno di maturazione più vecchio** (2024 → 2025 → 2026), come nel registro modello. La spettanza di un anno viene accreditata il 1° gennaio. |
| Residui di avvio | Al 25/09/2025: 28 giorni del 2024 e 18 del 2025. Sono ricostruiti dalle annotazioni del calendario («64 congedo · 17 2024 · 18 2025 · 29 2026» del 05/01/2026). |
| Straordinario | Ore e minuti per giornata. Dal calendario: «+30 minuti», «+3 ore e 20», «+1 ora e 30». |
| Permessi | Disponibili per anno (ore) meno quelli usati. Oggi il saldo è 0. |
| Domeniche e festività | Senza un codice diventano in automatico Riposo o Festività nazionale (in calendario sono tratteggiate). Se hai lavorato, vale il tuo codice. |
| Turno pomeridiano | Attributo della giornata. Nel calendario Google è l'evento ☠️☠️☠️. |

I valori calcolati (residui, totali) non si modificano a mano: derivano dalle giornate e dai parametri annuali.

## Dove sono salvati i dati

- **Versione su Claude**: i dati stanno nel database cloud dell'app e si sincronizzano su tutti i tuoi dispositivi. In alto vedi 🟢 sincronizzati, 🟠 in attesa o 🔴 errore.
- **Versione su GitHub Pages**: i dati restano nel browser del dispositivo (localStorage). Non c'è un server da gestire e non costa nulla, ma ogni dispositivo ha i suoi dati. Esporta spesso un backup (Impostazioni → Backup e dati) e usa «Importa backup» per spostare i dati su un altro dispositivo.

Al primo avvio la versione GitHub carica in automatico `seed.json`, cioè i dati importati dal tuo calendario.

## Struttura del progetto

```
registro-presenze/
├── index.html            ← l'app completa (HTML + CSS + JS, nessuna compilazione)
├── app.html              ← sorgente dell'app (index.html si genera da qui)
├── seed.json             ← i tuoi dati iniziali importati dal calendario
├── manifest.webmanifest  ← per installarla come app sul telefono
├── icon.svg, icon-180.png
├── .nojekyll
└── tools/
    ├── importa_calendario.py  ← conversione calendario → seed.json
    └── build.py               ← rigenera index.html da app.html
```

Stack: HTML, CSS e JavaScript senza framework, in un solo file. Si pubblica senza build e dura nel tempo senza aggiornare dipendenze. L'unica libreria esterna è SheetJS, caricata dal CDN solo quando importi o esporti un Excel. Non servono variabili d'ambiente.

## Provarla sul computer

```bash
cd registro-presenze
python3 -m http.server 8000
```

Poi apri http://localhost:8000. Serve un piccolo server perché il browser non carica `seed.json` da un file aperto con doppio clic.

## Pubblicarla su GitHub Pages (passo per passo)

1. Vai su https://github.com e accedi (o crea un account gratuito).
2. In alto a destra premi **+** → **New repository**.
3. Nome: `registro-presenze`. Scegli **Private** se hai GitHub Pro; con l'account gratuito Pages funziona solo con **Public**. Premi **Create repository**.
4. Nella pagina del repository premi **uploading an existing file**.
5. Trascina **tutti i file** della cartella `registro-presenze`, compresa la cartella `tools`. Il file `.nojekyll` è nascosto: se non lo vedi non è un problema. Premi **Commit changes**.
6. Vai su **Settings** → **Pages**. In «Build and deployment» scegli **Deploy from a branch**, branch **main**, cartella **/ (root)**, e premi **Save**.
7. Dopo 1–2 minuti in cima alla pagina compare il link, del tipo `https://TUONOME.github.io/registro-presenze/`.
8. Sul telefono apri il link:
   - iPhone (Safari): **Condividi → Aggiungi alla schermata Home**;
   - Android (Chrome): **⋮ → Aggiungi a schermata Home**.

> ⚠️ Con un repository **pubblico** chiunque conosca l'indirizzo può scaricare `seed.json`, che contiene il tuo storico. Per evitarlo, prima del passo 5 elimina `seed.json` dai file da caricare. Poi, al primo avvio, usa «Ripristina backup» con un backup esportato dall'app su Claude.

## Aggiornare i dati nel tempo

Aggiungi e correggi le giornate direttamente dal Calendario. A inizio anno vai in **Impostazioni → Anni → Crea anno**: il calendario del nuovo anno si genera da solo, con gli anni bisestili, e i residui passano all'anno nuovo.
