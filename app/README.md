# AI som kvalitetskontrollant i diariet

Hackathon-prototyp åt Statskontoret. Den granskar metadata på ärendedokument mot
klassificeringsmodell och regelverk, rättar tydliga fel, föreslår rättning vid
osäkerhet och flaggar det som kräver mänsklig bedömning.

Prototypen är fristående — ingen koppling till produktionsdiariet. Vyn är en
förenklad efterliknelse av Janus (Public 360), inte hela P360.

## Kom igång

Miljön riggas med [uv](https://docs.astral.sh/uv/). Det är det enda du behöver
installera: uv hämtar rätt Python och alla beroenden själv, och du behöver aldrig
aktivera någon venv. Systemets Python 3.9 på macOS räcker inte — `pyproject.toml`
kräver 3.11 eller senare, och det ordnar uv åt dig.

```
brew install uv                              # eller:
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Klona repot och kör. Första kommandot skapar `.venv/` och installerar allt.

```
git clone https://github.com/niklas-frojd/DiarieStraits.git
cd DiarieStraits
uv sync
```

## Kör och testa

```
uv run uvicorn app.main:app --reload   # → http://localhost:8000
uv run pytest                          # alla tester
uv run pytest -k <regelnamn>           # en enskild regel
```

`uv sync` är valfritt — `uv run` installerar det som saknas innan kommandot körs.

## Vad du ser

`localhost:8000` listar ärendena som ligger redo för diarieföring. Klick på en rad
öppnar ärendedokumentet med panelerna Filer, Detaljer och Kontakter, i samma
fältordning som Janus.

Tre testärenden bär demot, i den här ordningen:

| Ärende | Fall | Vad det visar |
|--------|------|---------------|
| 2026-00064 | Test Korrekt | Passerar kvalitetskontrollen obehindrat |
| 2026-00066 | Test Felaktigt | Obegriplig titel, saknad Ansvarig person, felskrivet datum, ifrågasatt handlingstyp och omkastad avsändare/mottagare |
| 2026-00065 | Test Gränsfall | Sju flaggor som mestadels inte går att avgöra maskinellt; stoppas för mänsklig bedömning |

Fälten står i `docs/markdown/testfall-metadata.md`.

## Struktur

```
app/
  main.py            FastAPI: API-rutter och den statiska vyn
  data.py            läser och slår upp testdata
  data/arenden.json  de tre ärendena, fält för fält
  static/            index.html, app.js, style.css — inget byggsteg
tests/               pytest mot API:t
docs/markdown/       PRD, beslut, plan, testfall, friktionslogg
docs/png/ docs/docx/ skärmdumpar och underlag från Janus
```

## Dokumentation

| Fil | Vad den ger |
|-----|-------------|
| `docs/markdown/prd.md` | Måstena M1–M5, vad som ligger utanför, demomålet |
| `docs/markdown/adr.md` | Besluten 1–3 med konsekvenser |
| `docs/markdown/plan.md` | Fem inkrement, scenario och kontroll per rad, Status-kolumn |
| `docs/markdown/testfall-metadata.md` | De tre testärendena, fält för fält — källan för testdata |
| `docs/markdown/handbok-kort.md` | Hackathon-handbokens sex kort |
| `docs/markdown/friction.md` | Friktionslogg: vad som skavde under bygget |
| `AGENTS.md` | Instruktionsfilen som AI-sessionerna läser |

## Status

Inkrement 1 är klart: skelettet med ärendelista och detaljvy. Regelmotorn och
kontrollerna byggs i inkrement 2 och framåt — aktuell status står i
`docs/markdown/plan.md`, en rad per inkrement.
