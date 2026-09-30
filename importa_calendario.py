"""Converte gli eventi del calendario di Denny in dati per l'app Registro Presenze.

Uso: python3 importa_calendario.py eventi.json ../seed.json
Regole (confermate da Denny il 30/09/2026):
- ☠️☠️☠️ = turno pomeridiano (attributo del giorno, non un codice)
- scambi, at in turno, 41 bis, distolto, ordine cattedrale, corso = giornate lavorative
- "+ X" nelle trasferte = ore di straordinario ("+1 ora e 30, totale 6 ore" -> conta 1h30)
- permessi disponibili = 0; il congedo sono le ferie
- domeniche = riposo automatico, festivi = festività nazionale automatica (calcolati dall'app)
- compleanni ed eventi a orario (non giornate di lavoro) esclusi
"""
import json, re, sys, collections

START = "2025-09-25"
SKULL = "☠️☠️☠️"

def clean(t):
    return " · ".join(p.strip() for p in t.strip().split("\n") if p.strip())

def classify(t):
    l = t.lower()
    if "congedo" in l: return "congedo"
    if "malattia" in l: return "malattia"
    if l.strip() == "riposo": return "riposo"
    if "trasferta" in l: return "trasferta"
    if l.strip() == "41 bis": return "41bis"
    if "at in turno" in l: return "at_turno"
    if l.strip() == "scambi": return "scambi"
    if "distolto" in l: return "distolto"
    if "corso" in l: return "corso"
    if "ordine cattedrale" in l: return "ordine_cattedrale"
    if "visita medica" in l: return "visita_medica"
    return "lavoro"

def overtime_min(t):
    l = t.lower().replace("\n", " ")
    m = re.search(r"\+\s*(\d+)\s*or[ae]\s*(?:e\s*(\d+))?", l)
    if m: return int(m.group(1)) * 60 + int(m.group(2) or 0)
    m = re.search(r"\+\s*(\d+)\s*(?:minuti)?", l)
    if m: return int(m.group(1))
    return 0

def mezzi(t):
    return sorted(set(x.upper() for x in re.findall(r"\b(sbt\d+|sb\d+|st\d+)\b", t.lower())),
                  key=lambda s: (re.sub(r"\d", "", s), int(re.sub(r"\D", "", s))))

def congedo_note(t):
    nums = [p.strip() for p in t.split("\n")]
    m = re.match(r"(\d+)\s*congedo", nums[0].lower())
    if not m: return None
    res = {"totale": int(m.group(1)), "perAnno": {}}
    for p in nums[1:]:
        mm = re.match(r"(\d+)\s+(20\d\d)", p)
        if mm: res["perAnno"][mm.group(2)] = int(mm.group(1))
    return res

def main(src, dst):
    evs = json.load(open(src))
    days = {}
    excluded = []
    for e in sorted(evs, key=lambda e: e["start_time"]):
        title = e["title"]
        d = e["start_time"][:10]
        if d < START: continue
        if "compleanno" in title.lower():
            continue
        if not e.get("all_day"):
            excluded.append({"data": d, "titolo": clean(title), "motivo": "evento a orario, non una giornata di lavoro"})
            continue
        day = days.setdefault(d, {})
        if title.strip() == SKULL:
            day["turno"] = "pomeriggio"
            continue
        txt = clean(title)
        if day.get("dettaglio") == txt:  # doppione nel calendario
            continue
        code = classify(title)
        day["codice"] = code
        day["dettaglio"] = txt
        mz = mezzi(title)
        if mz: day["mezzi"] = mz
        ot = overtime_min(title)
        if ot: day["straordinarioMin"] = ot
        if code == "congedo":
            cn = congedo_note(title)
            if cn: day["residuoCalendario"] = cn
            day.pop("dettaglio")
        day["origine"] = "calendario" if e.get("status") == "confirmed" else "calendario (provvisorio)"
    for d in days.values():
        d.setdefault("origine", "calendario")
    years = collections.defaultdict(dict)
    for d, v in sorted(days.items()):
        years[d[:4]][d] = v
    seed = {
        "formato": "registro-presenze",
        "versione": 1,
        "config": {
            "dataInizio": START,
            "codici": CODICI,
            "parametri": {
                "2025": {"congedoSpettante": 0, "permessiOre": 0, "note": "Il congedo 2025 (18 gg) è già nei residui di avvio."},
                "2026": {"congedoSpettante": 29, "permessiOre": 0, "note": ""},
            },
            "congedoAvvio": {"2024": 28, "2025": 18},
            "festivita": ["01-01", "01-06", "04-25", "05-01", "06-02", "08-15", "11-01", "12-08", "12-25", "12-26"],
            "pasquetta": True,
            "domenicaRiposo": True,
            "preferenze": {"tema": "auto", "primoGiorno": 1, "formatoData": "gg/mm/aaaa"},
            "anniArchiviati": [],
        },
        "anni": {y: {"giorni": v} for y, v in years.items()},
        "meta": {"importatoIl": "2026-09-30", "fonte": "Calendario Google dennycardone@gmail.com", "esclusi": excluded},
    }
    json.dump(seed, open(dst, "w"), ensure_ascii=False, indent=1)
    print("giorni:", len(days), {y: len(v) for y, v in years.items()})
    print("esclusi:", excluded)

# Codici ricavati dal calendario di Denny (nomi per esteso). Colori modificabili in Impostazioni.
CODICI = [
    {"id": "lavoro", "nome": "Lavoro", "categoria": "Presenza", "colore": "#2563A8", "lavorativo": True, "attivo": True},
    {"id": "scambi", "nome": "Scambi", "categoria": "Presenza", "colore": "#0F8A83", "lavorativo": True, "attivo": True},
    {"id": "at_turno", "nome": "AT in turno", "categoria": "Presenza", "colore": "#5B4FC4", "lavorativo": True, "attivo": True},
    {"id": "41bis", "nome": "41 bis", "categoria": "Presenza", "colore": "#56708A", "lavorativo": True, "attivo": True},
    {"id": "distolto", "nome": "Distolto", "categoria": "Presenza", "colore": "#8A6A2E", "lavorativo": True, "attivo": True},
    {"id": "ordine_cattedrale", "nome": "Ordine cattedrale", "categoria": "Presenza", "colore": "#6B7F2A", "lavorativo": True, "attivo": True},
    {"id": "visita_medica", "nome": "Visita medica", "categoria": "Presenza", "colore": "#2E86B5", "lavorativo": True, "attivo": True},
    {"id": "corso", "nome": "Corso", "categoria": "Formazione", "colore": "#9A4DB3", "lavorativo": True, "attivo": True},
    {"id": "trasferta", "nome": "Trasferta", "categoria": "Trasferta", "colore": "#D2691E", "lavorativo": True, "attivo": True},
    {"id": "congedo", "nome": "Congedo", "categoria": "Congedo", "colore": "#2E9B57", "lavorativo": False, "attivo": True, "scalaCongedo": True},
    {"id": "malattia", "nome": "Malattia", "categoria": "Malattia", "colore": "#C8453B", "lavorativo": False, "attivo": True},
    {"id": "riposo", "nome": "Riposo", "categoria": "Riposo", "colore": "#8A9199", "lavorativo": False, "attivo": True},
    {"id": "festivita", "nome": "Festività nazionale", "categoria": "Festività", "colore": "#C2507F", "lavorativo": False, "attivo": True},
]

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
