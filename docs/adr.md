# Arkitektur och beslut

## Skiss

```
flowchart TD
    A["Ärende + ärendedokument\n(testdata: riktiga exempelärenden\n+ Test Korrekt / Test Felaktigt)"] --> B["Egen webbapp\nsom visar ärendet\ni en vy inspirerad av Janus (P360)"]
    B --> C["Regelmotor\n(kod, ingen LLM i v1)"]
    C --> D["Checklista för kvalitetskontroller\ni Janus (Public 360)\n+ Statskontorets klassificeringsstruktur\n+ OSL 5 kap 2 §"]
    C --> E{Resultat per kontroll}
    E -->|Tydligt regelfel,\nt.ex. fel datumformat| F["Rättas automatiskt"]
    E -->|Osäkert fall,\nt.ex. Process/Handlingstyp\nverkar inte matcha| G["Föreslå rättning\n- människa godkänner"]
    E -->|Kräver bedömning,\nt.ex. obegriplig titel,\nsaknat fält| H["Flaggas för\nmänsklig bedömning"]
    E -->|Allt stämmer| I["Går vidare\noberört"]
    F --> J["Förklaringstext\n(mall per regel, t.ex.\n'Ansvarig person saknas - obligatoriskt fält')"]
    G --> J
    H --> J
    J --> K["Logg: vilken regel triggade,\nföre/efter-värde, tidpunkt"]
    K --> L["Registrator/handläggare\nser resultat + förklaring i webbappen"]

    M["Framtida tillägg:\nLLM (Claude API) för semantisk\nmatchning av innehåll mot\nProcess/Handlingstyp"] -. pluggas in bakom samma gränssnitt .-> C
```

Regelmotorn är kärnan i v1 och körs utan extern AI-tjänst. Den är byggd bakom ett gränssnitt (en "Checker" per kontrollområde: fält, format, klassificering, titel) så att en LLM-baserad kontroll kan läggas till senare utan att resten av flödet behöver byggas om.

## Beslut

**Beslut 1 – Kontrollmotor: ren regelmotor i v1, med öppning för LLM senare.** Läge: Kontrollerna vi ska göra – obligatoriska fält, giltiga koder, att Handlingstyp/Process/Skyddskod stämmer med Statskontorets klassificeringsstruktur, att titel och avsändare/mottagare är rimliga – finns redan definierade i Checklista för kvalitetskontroller i Janus (Public 360\) och i OSL 5 kap 2 §. Frågan var om kontrollerna ska köras av en regelmotor (kod), en LLM, eller en hybrid. Val: Vi bygger en ren regelmotor i kod för v1 – inga LLM-anrop i kärnflödet – men lägger den bakom ett gränssnitt så att en LLM-baserad kontroll kan pluggas in senare. Konsekvenser: Vi får ett snabbt, förutsägbart och lätt granskningsbart system utan API-nycklar eller nätverksberoenden i demot, men vissa fel som kräver språkförståelse (t.ex. att avgöra om en titel som "UUY HHT BB" är obegriplig, eller om Process verkligen matchar innehållet) kan i v1 bara upptäckas med enklare heuristik (t.ex. ordlistor/mönster) och riskerar att missas eller ge falska flaggningar tills en LLM-kontroll läggs till.

**Beslut 2 – AI-verktyg: inget krävs i v1, Claude API är förstahandsvalet när LLM läggs till.** Läge: Eftersom v1 klarar sig utan LLM (Beslut 1\) behöver vi ändå bestämma vilket verktyg som antas när ett LLM-steg läggs till, för explosionsfria (icke-blockerande) beslut senare i projektet. Val: Vi antar Claude via API som förstahandsval för framtida semantisk matchning och för att formulera mer naturliga förklaringar/rättningsförslag, men inget konto/nyckel behövs för att demot ska fungera – förklaringstexterna i v1 är fasta mallar kopplade till respektive regel. Konsekvenser: Demot blir oberoende av externa tjänster och nätverksanrop (mindre som kan gå sönder klockan 18:00), men förklaringarna blir mer robotaktiga/mallbaserade i v1 än en LLM-genererad text skulle vara, och integrationen av Claude API är ett uttryckligt uppföljningsarbete snarare än en del av prototypen.

**Beslut 3 – Gränssnitt och data: fristående webbapp som simulerar Janus (P360), med de riktiga exempelärendena som testdata.** Läge: Vi har ingen skarp integration mot produktionsdiariet (se docs/prd.md, Utanför), men vi har riktiga exempelärenden och skärmdumpar från Janus (P360) i repot, inklusive kända testfall (Test Korrekt samt Test Felaktigt med handmarkerade fel: obegriplig titel, saknad Ansvarig person, fel Skyddskod/Handlingstyp/Process, omvänd avsändare/mottagare). Val: Vi bygger en egen, liten webbapp (frontend \+ backend) som visar ärenden/ärendedokument i en vy inspirerad av Janus-skärmarna, med lokal lagring (JSON/SQLite) och just dessa exempelärenden som fördefinierad testdata. Konsekvenser: Vi kan visa ett trovärdigt, igenkännbart flöde på demot utan att bero på produktionssystemet eller nätverksåtkomst dit, men vyn är en förenklad approximation av Janus – den täcker bara de fält och vyer som behövs för kontrollerna, inte hela P360:s funktionalitet.  
