# AGENTS.md

Instruktionsfil enligt handbokens kort 04. `CLAUDE.md` importerar den här filen —
skriv ändringar här, inte där. Håll den under hundra rader.

## Vad det här är

Hackathon-prototyp åt Statskontoret: **AI som kvalitetskontrollant i diariet**.
Den granskar metadata på ärendedokument mot klassificeringsmodell och regelverk,
rättar tydliga fel, föreslår rättning vid osäkerhet och flaggar det som kräver
mänsklig bedömning. Demo klockan 18:00 samma dag.

Prototypen är fristående — den har ingen koppling till produktionsdiariet.
Vyn är en förenklad efterliknelse av Janus (Public 360), inte hela P360.

## Läs först

| Fil | Vad den ger |
|-----|-------------|
| `docs/markdown/prd.md` | Måstena M1–M5, vad som ligger utanför, demomålet |
| `docs/markdown/adr.md` | Besluten 1–3 med konsekvenser |
| `docs/markdown/plan.md` | Fem inkrement, scenario och kontroll per rad, Status-kolumn |
| `docs/markdown/testfall-metadata.md` | De tre testärendena, fält för fält — källan för testdata |
| `docs/markdown/handbok-kort.md` | Hackathon-handbokens sex kort |

## Kör och testa

```
uvicorn app.main:app --reload     # → localhost:8000
pytest                            # alla tester
pytest -k <regelnamn>             # en enskild regel
```

Stacken är Python med FastAPI som serverar både API och statisk HTML, testdata i
JSON och tester med pytest (plan.md, Antaganden — bör backas in i `adr.md` som
Beslut 4). `src/` är tomt: inkrement 1 är skelettet som ska skapa det.

## Arkitektur

Kärnan är en **regelmotor i kod, utan LLM-anrop**. Den ligger bakom ett gränssnitt
med en `Checker` per kontrollområde — fält, format, klassificering, titel — så att
en LLM-baserad kontroll kan pluggas in senare utan att flödet byggs om.

Varje kontroll landar i ett av fyra utfall, och det är den uppdelningen hela demot
vilar på:

1. **Rättas automatiskt** — tydligt regelbaserat fel (datumformat, ifyllt "Kopia till")
2. **Förslag** — människa godkänner eller avvisar (handlingstyp, kontakt)
3. **Kräver mänsklig bedömning** — stoppar ärendet (sekretess, riktning)
4. **Går vidare oberört**

Varje utfall får en mallbaserad förklaringstext kopplad till sin regel, plus en
loggrad: vilken regel som triggade, före/efter-värde och tidpunkt.

## Testärendena

Tre ärenden bär hela demot, i den här ordningen:

- **2026-00064 Test Korrekt** — passerar obehindrat
- **2026-00066 Test Felaktigt** — obegriplig titel, saknad Ansvarig person och
  Dokumentdatum, ifrågasatt handlingstyp 6.1-1/process 6.1, omkastad
  avsändare/mottagare
- **2026-00065 Test Gränsfall** — konstruerat, sju flaggor som mestadels *inte*
  går att avgöra maskinellt; stoppas för mänsklig bedömning

Fälten står i `testfall-metadata.md`. Klassificeringsstrukturen finns inte i repot:
kontrollera mot den mockade delmängden 2.3.1, 2.3.1-5, 6.1, 6.1-1 och säg det rakt ut.

## Arbetssätt

Ett inkrement per AI-session. Raden i `plan.md` plus scenariot är hela uppdraget.
**Uppdatera Status-kolumnen i `plan.md` innan sessionen avslutas** — den är enda
överlämningen mellan sessioner, inget annat följer med. Friktion loggas löpande i
`docs/markdown/friction.md`, granskningens fynd i `docs/markdown/review.md`.

## Gör inte

- **Inga LLM-anrop i kärnflödet i v1** (Beslut 1 och 2). Demot ska köra utan
  API-nyckel och utan nätverk. Claude API är förstahandsvalet *när* det läggs till.
- **Låt aldrig AI:n avgöra tveksamma fall själv** (M5). Bara entydigt regelbaserade
  fel rättas automatiskt; allt som kräver tolkning blir förslag eller bedömning.
- **Ingen integration mot produktionsdiariet**, ingen riktig inloggning eller
  behörighetslösning — det mockas.
- **Ingen sakgranskning av handlingens innehåll** — prototypen granskar metadata.
- **Skapa aldrig en andra version av prd/adr/plan.** En fil var.

## Filplacering

`docs/` är uppdelad i `markdown/`, `docx/` och `png/`. Nya `.md` läggs i
`docs/markdown/` — det gäller även `friction.md` och `review.md` när de skapas.
