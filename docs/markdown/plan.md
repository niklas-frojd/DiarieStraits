# Inkrementell plan med kontroller

Fem inkrement i den ordning de ska visas. Varje rad är hela beskrivningen av sitt inkrement: den klistras in i en ny AI-session tillsammans med scenariot, sessionen bygger, teamet kör kontrollen och uppdaterar Status innan sessionen avslutas. Utgår från måstena i `prd.md` och besluten i `adr.md`.

| # | Inkrement | Demovärde | Scenario | Kontroll | Måste | Status |
|---|-----------|-----------|----------|----------|-------|--------|
| 1 | Skelett: ärendelista och detaljvy | Något kör och känns igen från Janus | `uvicorn app.main:app --reload` → localhost:8000 listar de tre ärendena; klick på 2026-00064 visar fälten ur Detaljer-panelen | klick: öppna alla tre · `pytest`: `/api/arenden` ger 3 ärenden | — | **Klar** — kontrollen körd 2026-09-11: 8 tester gröna, alla tre ärendena öppnas. Fynd i `review.md` |
| 2 | Regelmotor: fält- och formatkontroller | Första automatiska rättningen syns | Kvalitetsgranska 2026-00064 → rent. 2026-00066 → Ansvarig person och Dokumentdatum saknas, felskrivet datum rättas automatiskt. 2026-00065 → "Kopia till" rensas automatiskt | `pytest` per regel · klick: knappen Kvalitetsgranska | M1 M2 M3 | Ej påbörjad |
| 3 | Klassificerings- och riktningskontroller | Felfallet faller ut som fel | 2026-00066 flaggar handlingstyp 6.1-1 och process 6.1 mot kodlistan, samt omkastad avsändare/mottagare mot riktningen Inkommande | `pytest`: 2026-00066 ger minst tre flaggor i kategorin | M1 M2 | **Klar** — kontrollen körd 2026-09-11 på grenen `inkrement-3`: 00066 ger tre flaggor, 00064 och 00065 inga, 10 tester gröna. `KlassificeringsChecker` i `app/klassificering.py` kopplas till knappen Kvalitetsgranska när inkrement 2 är klart |
| 4 | Förklaring, förslag och mänsklig bedömning | Hela demoflödet hänger ihop | Varje flagga får mallförklaring och en av tre utgångar: rättad, förslag att godkänna eller avvisa, kräver bedömning. 2026-00065 stoppas med banner. Logg: regel, före/efter-värde, tidpunkt | klick: 00064 → 00066 → 00065 · `pytest`: 2026-00065 får status kräver_bedömning | M3 M4 M5 | Ej påbörjad |
| 5 | *(om tid)* Titelkontroll, heuristik | Fångar "UUY HHT BB" | Obegriplig titel, förkortningar och personnamn enligt checklistan, som egen Checker så att en LLM kan ersätta heuristiken senare | `pytest`: ordlista med giltiga och ogiltiga titlar | M2 | Ej påbörjad |

## Demoordning klockan 18:00

2026-00064 passerar obehindrat → 2026-00066 visar en automatisk rättning och flera flaggor → 2026-00065 stoppas för mänsklig bedömning med en förklaring per rad.

## Antaganden

- **Klassificeringsstrukturen finns inte i repot.** Inkrement 3 kontrollerar mot en mockad delmängd av koderna, hämtade från skärmdumparna och checklistan: 2.3.1 Kommunicera internt, 2.3.1-5 Korrespondens, 6.1 Hantera revisionsstrategi, 6.1-1 Beslut. Det sägs rakt ut i demot.
- **Testdatan för 2026-00066 kompletteras i inkrement 1** med ett felskrivet datum. Inget av de handmarkerade felen i skärmdumpen går att rätta maskinellt, så M3 saknar annars demonstrationsobjekt.
- **Ett inkrement per AI-session.** Status-kolumnen är överlämningen mellan sessionerna; inget annat följer med.
- **Stacken** är Python med FastAPI som serverar både API och statisk HTML, testdata i JSON och tester med pytest. Bör backas in i `adr.md` som Beslut 4.
