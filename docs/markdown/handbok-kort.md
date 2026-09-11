# Handbokens kort 01–06

Transkribering av de sex korten i hackathon-handboken (skärmdumpar i `docs/Screenshot 2026-09-11 at 13.16.46–13.17.15.png`). Korten beskriver vilka dokument som ska finnas och i vilken ordning de tas fram.

| # | Kort | Fas · tid | Fil(er) |
|---|------|-----------|---------|
| 01 | PRD, en sida | Ringa in · 30 + 10 min | `docs/prd.md` |
| 02 | Arkitektur och beslut | Utforma · 30 + 10 min | `docs/adr.md` |
| 03 | Inkrementell plan med kontroller | Planen · 15 min | `docs/plan.md` |
| 04 | Rules-fil | Rigga · 30 + 15 min | `AGENTS.md` |
| 05 | Prototyp | Bygg + spurten · 130 min | repot · startas med ett kommando |
| 06 | Friktionslogg och granskning | Bygg → granska | `docs/friction.md` · `docs/review.md` |

---

## 01 — PRD, en sida

**Ringa in · 30 + 10 min** · `docs/prd.md`

Problem, rollerna, tre till fem måsten, vad som inte ingår och vad ni visar klockan 18:00. AI:n skriver utkastet, ni kortar ner.

Sidan som säger vad ni bygger och åt vem. Hela teamet läser och godkänner den, och varje senare AI-session utgår från den. Filen heter `docs/prd.md`, en fil, aldrig två versioner.

```
Problem · Roller · Måsten (3–5)
Utanför · Demomål klockan 18:00
Antaganden vi gjorde i stället för att fråga
```

---

## 02 — Arkitektur och beslut

**Utforma · 30 + 10 min** · `docs/adr.md`

En skiss över hur prototypen hänger ihop, och två eller tre beslut på ett stycke var.

Varje beslut skrivs som ett stycke: läget, vad ni valde och vad det kostar. Handboken kallar det ADR, och för en prototyp räcker en fil, `docs/adr.md`, med skissen överst och besluten under. Besluten följer med in i varje AI-session.

```
Skiss (mermaid eller rutor i text, en skärm)
Beslut 1..3: Läge · Val · Konsekvenser
```

---

## 03 — Inkrementell plan med kontroller

**Planen · 15 min** · `docs/plan.md`

Tre eller fyra inkrement i den ordning ni vill visa dem. Varje rad har ett scenario och ett sätt att kontrollera det.

Ett inkrement är en bit av prototypen som fungerar hela vägen och går att visa för sig. Det första är skelettet: det minsta som kör. Raden i `docs/plan.md` är hela beskrivningen av inkrementet; det finns ingen egen fil per inkrement.

```
#  Inkrement  Demovärde  Scenario
   Kontroll (test | klick)  Status
```

---

## 04 — Rules-fil

**Rigga · 30 + 15 min** · `AGENTS.md`

En kort instruktionsfil, under hundra rader, som AI:n läser varje gång: vad projektet är, besluten, hur man kör och testar.

Det är den som gör att AI:n håller sig till det ni bestämt. Utan den är PRD:n och besluten filer som ingen läser. Den ligger som `AGENTS.md` i repots rot; Claude Code läser `CLAUDE.md`, så gör den till en symlänk till samma fil.

```
Vad det här är · Kör · Testa
Läs först: docs/prd.md · docs/adr.md · docs/plan.md
Gör inte
```

---

## 05 — Prototyp

**Bygg + spurten · 130 min** · repot · startas med ett kommando

Går att köra med ett kommando. Skelettet före fikat, två inkrement till efter. Inte snygg, men går att visa.

Bygg ett inkrement per ny AI-session: klistra in raden och scenariot, låt AI:n bygga, kör själv, godkänn, spara.

```
per inkrement: ny session → rad + scenario
→ AI:n bygger → ni kör → godkänn → spara
```

---

## 06 — Friktionslogg och granskning

**Bygg → granska** · `docs/friction.md` · `docs/review.md`

En rad för varje gång något skavde. Granskningens fynd. Den enda sak ni skulle automatisera nästa gång.

Friktionsloggen är `docs/friction.md` och fylls på under hela bygget. Granskningen är en ny AI-session som jämför prototypen med `docs/prd.md` och `docs/adr.md` och skriver luckorna till `docs/review.md`. Loggen gör demon jämförbar mellan teamen.

```
Friktion: vad · när · kostnad
Granskning: missat måste · brutet beslut
Nästa gång: en automatisering
```