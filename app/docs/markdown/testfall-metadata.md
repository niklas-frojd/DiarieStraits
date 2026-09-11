# Testfall: metadata i Public 360

De tre fallen som demot bygger på.

Fall 1 och 2 är transkriberingar av skärmdumparna från diariet (`docs/png/Test Korrekt Metadata.png`, `docs/png/Test Korrekt Skärmdump.png`, `docs/png/Test Felaktigt Skärmdump 1.png`, `docs/png/Test Felaktigt Skärmdump 2.png`): ett korrekt referensfall och ett med fel som markerats för hand i rött. Fall 3 är konstruerat — det finns ingen skärmdump — och är gränsfallet som ska flaggas för mänsklig bedömning.

| # | Fall | Ärende | Förväntat utfall |
|---|------|--------|------------------|
| 1 | Test Korrekt | 2026-00064 | Passerar utan anmärkning |
| 2 | Test Felaktigt | 2026-00066 | Fel hittas: rättas automatiskt eller föreslås |
| 3 | Test Gränsfall | 2026-00065 | Flaggas för mänsklig bedömning med förklaring |

---

## Fall 1 — Test Korrekt (2026-00064)

Referensfallet: metadata som stämmer mot klassificeringsmodellen och ska passera kvalitetskontrollen obehindrat.

### Registreringsformuläret — "Nytt dokument: Ärendedokument", fliken Generellt

Fält markerade med `*` är obligatoriska i formuläret.

| Fält | Värde |
|------|-------|
| Ärende | 2026-00064 Test Korrekt |
| Handlingstyp `*` | 2.3.1-5 (Korrespondens) |
| Dokumentkategori `*` | Inkommande |
| Skyddskod `*` | Allmän handling - Offentlig |
| Åtkomstgrupp `*` | Alla |
| Titel `*` | Test Korrekt |
| Avsändare `*` | Statskontoret |
| Kopia till | *(tomt)* |
| Ankomstdatum `*` | 2026-08-25 |
| Dokumentdatum | 2026-08-25 |
| Sista svarsdatum | *(tomt)* |
| Ansvarig `*` | Rex Ljungqvist - Stöd - HR |
| Status | Registrerat |
| Avsändarens ref. | *(tomt)* |
| Antal bilagor | *(tomt)* |
| Sparat på papper/media | Nej |

Flikar i formuläret: Generellt `*` · Kontakter · Filer · Kommentar. Knappar: **Slutför** / Avbryt.

### Dokumentvyn — Detaljer

Sökväg: Hem - Redo för diarieföring → Ärende: Test Korrekt → Ärendedokument: Test Korrekt. Inloggad användare: Rex Ljungqvist.

| Fält | Värde |
|------|-------|
| Ärende | 2026-00064 Test Korrekt |
| Ankomstdatum | 2026-08-25 |
| Dokumentdatum | 2026-08-25 |
| Signerad | *(tomt)* |
| Signeringsdatum | *(tomt)* |
| Sista svarsdatum | *(tomt)* |
| Dokumentkategori | Inkommande |
| Status | Registrerat |
| Ansvarig enhet | Stöd - HR |
| Ansvarig person | Rex Ljungqvist |
| Skyddskod | Offentlig |
| Åtkomstgrupp | Alla |
| Delarkiv | ESV 2022 |
| Handlingstyp | 2.3.1-5 - Korrespondens |
| Process | 2.3.1 - Kommunicera internt |

**Filer (2)**

| Titel | Typ | Filstorlek | Senast ändrad |
|-------|-----|-----------|---------------|
| Test | e-post | 50 KB | 2026-08-25 |
| Test | pdf | 67 KB | 2026-08-25 |

**Kontakter**

| Roll | Kontakt |
|------|---------|
| Avsändare | Statskontoret |
| Mottagare | Rex Ljungqvist *(Mottagen för kännedom)* |

---

## Fall 2 — Test Felaktigt (2026-00066)

Felfallet. De röda markeringarna i skärmdumparna är gjorda för hand och pekar ut vad kvalitetskontrollen ska hitta.

### Dokumentvyn — huvud

Sökväg: Hem - Redo för diarieföring → Ärende: Test Felaktigt UTY GGG BBO → Ärendedokument: UUY HHT BB.

| Fält | Värde | Markering |
|------|-------|-----------|
| Dokumenttitel | UUY HHT BB | 🔴 understruken — innehållslös/slumpmässig titel |
| Ärendedokument | 2026-00066-1 | |
| Ärendets titel | Test Felaktigt **UTY GGG BBO** | 🔴 "UTY GGG BBO" överstruket — skräptext i ärendemeningen |

**Filer (1)**

| Titel | Typ | Filstorlek | Senast ändrad |
|-------|-----|-----------|---------------|
| Test | e-post | 50 KB | 2026-08-25 |

### Dokumentvyn — Detaljer

| Fält | Värde | Markering |
|------|-------|-----------|
| Ärende | 2026-00066 Test Felaktigt ~~UTY GGG BBO~~ | 🔴 överstruket |
| Ankomstdatum | 2026-08-25 | |
| Dokumentdatum | *(tomt)* | saknas (satt i det korrekta fallet) |
| Signerad | *(tomt)* | |
| Signeringsdatum | *(tomt)* | |
| Sista svarsdatum | *(tomt)* | |
| Dokumentkategori | Inkommande | |
| Status | Registrerat | |
| Ansvarig enhet | Statskontoret | jfr. Stöd - HR i det korrekta fallet |
| Ansvarig person | *(tomt)* | saknas |
| Skyddskod | Offentlig | 🔴 understruken med frågetecken |
| Åtkomstgrupp | Alla | |
| Delarkiv | ESV 2022 | |
| Handlingstyp | 6.1-1 - **Beslut** | 🔴 "Beslut" understruket med frågetecken |
| Process | 6.1 - Hantera revisionsstrategi | 🔴 understruken med frågetecken |

**Kontakter**

| Roll | Kontakt | Markering |
|------|---------|-----------|
| Avsändare | Rex Ljungqvist | 🔴 pil mellan raderna — avsändare och mottagare är omkastade |
| Mottagare | Statskontoret *(Mottagen för kännedom)* | 🔴 |

### Sammanfattning av felen

1. **Titel utan innebörd** — dokumenttiteln "UUY HHT BB" och skräptexten "UTY GGG BBO" i ärendemeningen beskriver inte handlingen.
2. **Avsändare och mottagare omkastade** — en inkommande handling från Statskontoret har Rex Ljungqvist som avsändare och Statskontoret som mottagare.
3. **Handlingstyp och process ifrågasatta** — 6.1-1 Beslut / 6.1 Hantera revisionsstrategi stämmer inte med en inkommande handling av det här slaget; jfr. 2.3.1-5 Korrespondens / 2.3.1 Kommunicera internt i det korrekta fallet.
4. **Skyddskod ifrågasatt** — Offentlig är markerad med frågetecken och behöver bedömas.
5. **Saknade uppgifter** — Dokumentdatum och Ansvarig person är tomma.
---

## Fall 3 — Test Gränsfall (2026-00065)

Gränsfallet. Konstruerat testfall, ingen skärmdump. Inget av fälten är entydigt fel — poängen är att flera kontroller landar i "det går inte att avgöra maskinellt". Ärendet ska därför **inte** rättas automatiskt utan markeras för mänsklig bedömning med en förklaring per flagga.

Scenariot: ett mejl kommer in till registraturen från en konsult som deltar i en pågående upphandling. Mejlet kompletterar ett tidigare lämnat anbud och innehåller uppgifter om bolagets priser och kalkyler. I mejltråden ligger även Statskontorets eget svar överst. Mejlet kom in fredag 2026-08-22 kl. 17:41 och registrerades måndag 2026-08-25.

### Registreringsformuläret — "Nytt dokument: Ärendedokument", fliken Generellt

| Fält | Värde |
|------|-------|
| Ärende | 2026-00065 Upphandling av utvärderingstjänster |
| Handlingstyp `*` | 2.3.1-5 (Korrespondens) |
| Dokumentkategori `*` | Inkommande |
| Skyddskod `*` | Allmän handling - Offentlig |
| Åtkomstgrupp `*` | Alla |
| Titel `*` | Komplettering till anbud, benchmarking av utvärderingsmetod |
| Avsändare `*` | anna.svensson@konsultbolaget.se |
| Kopia till | registrator@statskontoret.se |
| Ankomstdatum `*` | 2026-08-25 |
| Dokumentdatum | 2026-08-22 |
| Sista svarsdatum | *(tomt)* |
| Ansvarig `*` | Rex Ljungqvist - Stöd - HR |
| Status | Registrerat |
| Avsändarens ref. | *(tomt)* |
| Antal bilagor | 1 |
| Sparat på papper/media | Nej |

### Dokumentvyn — Detaljer

| Fält | Värde |
|------|-------|
| Ärende | 2026-00065 Upphandling av utvärderingstjänster |
| Ankomstdatum | 2026-08-25 |
| Dokumentdatum | 2026-08-22 |
| Signerad | *(tomt)* |
| Signeringsdatum | *(tomt)* |
| Sista svarsdatum | *(tomt)* |
| Dokumentkategori | Inkommande |
| Status | Registrerat |
| Ansvarig enhet | Stöd - HR |
| Ansvarig person | Rex Ljungqvist |
| Skyddskod | Offentlig |
| Åtkomstgrupp | Alla |
| Delarkiv | ESV 2022 |
| Handlingstyp | 2.3.1-5 - Korrespondens |
| Process | 2.3.1 - Kommunicera internt |

**Filer (2)**

| Titel | Typ | Filstorlek | Senast ändrad |
|-------|-----|-----------|---------------|
| SV: Komplettering till anbud | e-post (tråd med två meddelanden) | 62 KB | 2026-08-22 |
| Prisbilaga | xlsx | 48 KB | 2026-08-22 |

**Kontakter**

| Roll | Kontakt |
|------|---------|
| Avsändare | anna.svensson@konsultbolaget.se |
| Mottagare | Rex Ljungqvist *(Mottagen för kännedom)* |

### Flaggor: vad AI:n ser och vad människan ska avgöra

| # | Flagga | Vad AI:n kan konstatera | Varför den inte avgörs maskinellt | Åtgärd |
|---|--------|-------------------------|-----------------------------------|--------|
| 1 | **Skyddskod / sekretess** | Filerna innehåller priser och kalkyler från en anbudsgivare i en pågående upphandling. Skyddskoden är satt till Offentlig och åtkomstgruppen till Alla. | Om sekretess föreligger för affärsförhållandena är en rättslig bedömning, inte en regeltillämpning. | Mänsklig bedömning — registrator eller jurist. |
| 2 | **Riktning / dokumentkategori** | Filen är en mejltråd med två meddelanden: ett inkommande och Statskontorets eget svar. Checklistan säger att handlingar med olika riktning inte ska ligga i samma ärendedokument. | AI:n kan se att det finns två meddelanden, men inte om svaret faktiskt expedierats och därmed ska registreras som en egen utgående handling. | Mänsklig bedömning. |
| 3 | **Kontakt** | Avsändaren är angiven som en mejladress. Enligt checklistan är varken en mejladress eller en enskild tjänsteperson en giltig kontakt. | Rätt kontakt är sannolikt bolaget, men det måste finnas i Janus kontaktregister — annars krävs en beställning hos registraturen. | Förslag till registrator: byt till bolaget; kontrollera registret. |
| 4 | **Kopia till** | Fältet "Kopia till" är ifyllt. Checklistan säger att kontaktfältet ska vara rensat på "kopia till". | Regelbaserat och entydigt. | Rättas automatiskt. |
| 5 | **Ankomstdatum** | Mejlet inkom 2026-08-22, ankomstdatum är satt till 2026-08-25. Datumet ska stämma med när handlingen faktiskt inkom, och registrering ska ske utan dröjsmål. | Skillnaden är en helg. Om det är ett felaktigt ankomstdatum eller en korrekt registrering efter helgen går inte att avgöra ur metadatan. | Flaggas med förklaring; människan avgör. |
| 6 | **Titel** | Titeln innehåller det engelska ordet "benchmarking". Checklistan tillåter engelska om ingen översättning finns. | Om en vedertagen svensk översättning finns i sammanhanget är en språklig bedömning. | Flaggas som låg prioritet. |
| 7 | **Handlingstyp och process** | 2.3.1-5 Korrespondens / 2.3.1 Kommunicera internt är vald, men handlingen rör en upphandling och är extern. | Vilken processkod i klassificeringsstrukturen som är rätt kräver kännedom om ärendets sammanhang. | Förslag med alternativ; människan väljer. |

### Förväntat utfall i demot

Ärendet stoppas före vidare handläggning och visas som **Kräver mänsklig bedömning**. Flagga 4 rättas automatiskt och redovisas som gjord rättning. Flagga 1 och 2 lyfts överst med motivering; flagga 3 och 7 visas som förslag att godkänna eller avvisa; flagga 5 och 6 visas som upplysningar. Ingen flagga avgörs av AI:n på egen hand, och varje rad har en förklaring i klartext som en registrator kan läsa och bemöta.
