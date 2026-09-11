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

Knappen **Kvalitetsgranska** kör regelmotorn på det öppna ärendet. Varje fynd
får en förklaring och ett av fyra utfall: rättat automatiskt, förslag att godkänna
eller avvisa, kräver mänsklig bedömning, eller orört. Ärenden som kräver bedömning
spärras med en banner, och varje åtgärd lämnar en loggrad med regel, före- och
efter-värde och tidpunkt.

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
  main.py                     FastAPI: API-rutter och den statiska vyn
  data.py                     läser och slår upp testdata
  data/arenden.json           de tre ärendena, fält för fält
  data/klassificering.json    den mockade kodlistan: 2.3.1, 2.3.1-5, 6.1, 6.1-1
  kontroller/                 regelmotorn — en Checker per kontrollområde
    motor.py                  REGISTER: kör alla Checkers och samlar fynden
    modell.py                 Fynd och de fyra utfallen
    falt.py datum.py          obligatoriska fält, datumformat, "Kopia till"
    klassificering.py         handlingstyp, process och riktning mot kodlistan
    titel.py gransfall.py     titelheuristik och de konstruerade gränsfallen
  static/                     index.html, app.js, style.css — inget byggsteg
tests/                        pytest mot API:t och per regel
docs/markdown/                PRD, beslut, plan, testfall, friktion, granskning
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
| `docs/markdown/review.md` | Granskningens fynd, en rubrik per tillfälle |
| `AGENTS.md` | Instruktionsfilen som AI-sessionerna läser |

## Status

Alla fem inkrement i `docs/markdown/plan.md` är klara, och `uv run pytest` ger
96 gröna tester.

| # | Inkrement | Status |
|---|-----------|--------|
| 1 | Skelett: ärendelista och detaljvy | Klar |
| 2 | Regelmotor: fält- och formatkontroller | Klar |
| 3 | Klassificerings- och riktningskontroller | Klar |
| 4 | Förklaring, förslag och mänsklig bedömning | Klar |
| 5 | Titelkontroll, heuristik | Klar |

Två saker att veta inför demot: klickkontrollerna för inkrement 2 och 4 är inte
körda — servern fick inte binda port i de sessionerna (`friction.md`) — och
titelheuristiken ger falska träffar som står beskrivna på samma ställe. En rad
per inkrement, med scenario och kontroll, står i `docs/markdown/plan.md`.
