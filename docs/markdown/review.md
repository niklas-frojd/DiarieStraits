# Granskning

Fynd från kodgranskningar. En rubrik per granskningstillfälle.

## 2026-09-11 — efter inkrement 1

Granskat: `app/main.py`, `app/data.py`, `app/data/arenden.json`, `app/static/`,
`tests/test_api.py`. Kontrollen i `plan.md` rad 1 är körd: `uv run pytest` ger
8 godkända tester, och servern svarar 200 på `/`, `/arende/<nr>` för alla tre
ärendena samt på de statiska filerna. Inkrement 1 är därmed klart.

### Testdatans trohet mot källan

Fall 1 och 3 följer `testfall-metadata.md` fält för fält. Fall 2 avviker på en
punkt — Dokumentdatum är `25/8-2026` i stället för tomt — vilket är det antagande
som står i `plan.md` och i `friction.md` rad 3, och som `_kommentar` i testdatan
upprepar. Avvikelsen är alltså medveten och dokumenterad på tre ställen. Den
måste sägas rakt ut i demot.

Registreringsblocket för fall 2 finns inte i källan (skärmdumparna visar bara
dokumentvyn) utan är härlett ur Detaljer. Det är konsekvent — tomt `ansvarig`
speglar tom `ansvarig_person` — men det är konstruerat, inte transkriberat.

### Att rätta före inkrement 2

1. ~~**`hamta_arende` lämnar ut den delade dikten**~~ *(åtgärdat i inkrement 2: `hamta_arende` returnerar en kopia och motorn granskar en `deepcopy`.)* (`app/data.py:25`). `ARENDEN`
   läses in en gång vid import, och funktionen returnerar objektet ur listan utan
   kopia. Så fort inkrement 2 skriver tillbaka en automatisk rättning ändras
   modulens globala testdata för resten av processen — mellan anrop och mellan
   tester. Bestäm medvetet: antingen `deepcopy` vid utlämning och rättningar som
   rent resultat, eller en uttalad "rättningarna lever i minnet"-modell med en
   återställningsfunktion som testerna kan kalla.

### Småsaker, ingen brådska

2. **`index` har en parameter den inte använder** (`app/main.py:31`). Samma
   funktion bär både `/` och `/arende/{arendenummer}`, och defaultvärdet gör att
   `/` får en meningslös query-parameter i OpenAPI-schemat. Vyn fungerar; det är
   bara schemat som ljuger.
3. **`_kommentar` följer med ut i API-svaret** för 2026-00066 och 2026-00065.
   Interna anteckningar syns för den som öppnar `/api/arenden/2026-00066`.
   Harmlöst i demot, men filtrera bort nycklar med inledande `_` om svaret ska
   visas för publik.
4. **Inget felfall i gränssnittet** (`app/static/app.js:58`). Om `/api/arenden`
   fallerar blir listan tyst tom. En rad i `catch` räcker.
5. **Varningar från `starlette.testclient`** om httpx vid varje testkörning. Brus
   från beroendet, inte från koden.

## 2026-09-11 — efter inkrement 4

Granskat: `app/kontroller/` i sin helhet, `app/static/`, `tests/`. Planens
pytest-kontroll är körd: 71 tester gröna, och 2026-00065 får status
`kräver_bedömning`. Klickkontrollen är **inte** körd — se `friction.md` rad 12.

### Vad som byggdes

`Fynd` fick fältet `forslag`, det värde en människa kan godkänna. Motorn
sorterar fynden efter hur strängt utfallet är och bygger en logg med tidpunkt,
regel och före/efter-värde. Fem nya Checkers i `gransfall.py` täcker flagga 1,
2, 3, 5 och 7 ur Fall 3 i `testfall-metadata.md`. Vyn fick spärrbanner,
Godkänn/Avvisa per förslag och en logg-panel.

### Att bära med sig

1. **Heuristiken i `gransfall.py` är mockad.** Sekretessflaggan tänder på två
   signalord i ärendets och filernas titlar, riktningsflaggan på ordet "tråd" i
   filtypen. Det räcker för de tre testärendena och inte för något annat. Det är
   precis den gräns Beslut 1 pekar ut, och det måste sägas i demot.
2. **Besluten lever bara i webbläsaren.** Ett godkänt förslag skrivs in i
   Detaljer-panelen och i loggen, men försvinner vid omladdning. Medvetet — det
   håller demot omkörbart och API-ytan liten — men spårbarheten i `adr.md` är
   därmed bara halvvägs: motorns logg går till servern, människans beslut inte.
3. **Flagga 6 saknas.** Det engelska ordet i 2026-00065:s titel fångas först när
   inkrement 5 bygger titelkontrollen. Gränsfallet visar sex av sju flaggor.
4. **`ExternProcess` och `KontaktForm` tänder båda på snabel-a i avsändaren.** De
   är avsiktligt två regler med två olika utfall, men flaggar samma ärende av
   samma grundorsak. Om demot känns repetitivt är det den raden att stryka.
