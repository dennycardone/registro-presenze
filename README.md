# Registro Presenze — Denny

App web personale per il registro presenze: **📅 Calendario**, **📊 Report** e **⚙️ Impostazioni**.
Lo storico parte dal **25/09/2025** ed è stato importato dal calendario Google personale il 30/09/2026.

Il registro Excel di un collega è servito solo come modello di struttura e di logica. Nell'app non c'è nessun suo dato, e in questo repository pubblico non c'è nessun dato personale: i dati restano nel dispositivo di chi usa l'app.

## Cosa fa

- **Calendario**: il mese intero in una schermata, senza scorrere. Ogni giornata mostra uno o più stati (es. Trasferta + Corso), l'attività svolta, il turno pomeridiano (POM), straordinario, permesso e flessibilità. Tocca un giorno per modificarlo; il salvataggio è immediato. Barra in alto: Oggi · Giorno · Mese · Anno; si cambia mese anche scorrendo il dito.
- **Report** (Mese, Anno o Intervallo): giornate lavorate per stato, straordinari per semestre, flessibilità, congedo usato e residuo per anno di maturazione, permessi, malattia, riposi, festività, turni pomeridiani, andamento mensile e mezzi su cui hai lavorato.
- **Impostazioni**: codici, anni, parametri annuali, backup e ripristino, import/export Excel e CSV, controlli, tema, ripristino protetto da doppia conferma.

## Regole di calcolo

| Voce | Regola |
|---|---|
| Giornata lavorata | Giornata con almeno uno stato «lavorativo» (Lavoro, Scambi, AT in turno, Distolto, Visita medica, Corso, Trasferta). Con più stati conta una volta sola. «41 bis» e «ordine cattedrale» sono attività del codice Lavoro. |
| Congedo (= ferie) | Ogni giornata di congedo scala 1 giorno dall'anno scelto (anno della giornata o i 2 precedenti). Se non scegli, scala dall'anno più vecchio con giorni disponibili. La spettanza di un anno viene accreditata il 1° gennaio. Il congedo si seleziona da solo, senza altri stati. |
| Residui di avvio | Al 25/09/2025: 28 giorni del 2024 e 18 del 2025, ricostruiti dalle annotazioni del calendario. |
| Straordinario | Ore e minuti per giornata. Si accumula per semestre (gennaio–giugno, luglio–dicembre): il 1° gennaio e il 1° luglio il conteggio riparte da zero, lo storico resta nel Report. |
| Flessibilità | Si usa come un permesso ma scala dal saldo straordinario del semestre. |
| Permessi | 4 ore al mese, non cumulabili: le ore non usate si azzerano il 1° del mese successivo. |
| Domeniche e festività | Senza un codice diventano in automatico Riposo o Festività nazionale. Se hai lavorato, vale il tuo codice. |
| Nuovo anno | Il 1° gennaio l'app crea da sola il calendario dell'anno nuovo. Il congedo spettante va inserito in Impostazioni → Parametri annuali. |

## Dove sono salvati i dati

- **Versione su GitHub Pages** (questo repository): i dati restano nel browser del dispositivo. Ogni dispositivo ha i suoi dati e se cancelli i dati del browser li perdi: esporta spesso un backup (Impostazioni → Backup e dati). Se l'ultimo backup ha più di 14 giorni, su Impostazioni compare un pallino rosso.
- **Versione su Claude**: i dati stanno nel cloud dell'account Claude e si sincronizzano su tutti i dispositivi. Le due versioni non si scambiano dati.

## File

```
index.html            ← l'app completa (HTML + CSS + JS in un file, nessuna compilazione)
app.html              ← la stessa app nel formato della versione su Claude
sw.js                 ← funzionamento offline e aggiornamenti
manifest.webmanifest  ← installazione sul telefono
icon.svg, icon-*.png  ← icone
importa_calendario.py ← script usato per l'import iniziale dal calendario Google
```

L'unica libreria esterna è SheetJS, caricata solo quando importi o esporti un Excel.

## Aggiornamenti

Le modifiche vengono caricate direttamente su questo repository. Dopo un paio di minuti basta chiudere e riaprire l'app sul telefono.
