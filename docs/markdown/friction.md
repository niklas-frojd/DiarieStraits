# Friktionslogg

En rad varje gång något skavde: vad, när, vad det kostade.

| # | Vad | När | Kostnad |
|---|-----|-----|---------|
| 1 | Systemets Python är 3.9 och saknade fastapi. Miljön riggades med `uv` och `pyproject.toml` (Python >=3.11) i stället för en handpåsatt venv. Kommandona i `AGENTS.md` fick prefixet `uv run`. | Inkrement 1 | Några minuter, ett beslut som inte stod i planen |
| 2 | `AGENTS.md` sa att koden skulle ligga i `src/`, medan `plan.md` och handbokens kontroll skrev `app.main:app`. `app/` valdes och `AGENTS.md` rättades. | Inkrement 1 | Litet, men hade kostat mer i en senare session |
| 3 | Skärmdumpen för 2026-00066 har tomt Dokumentdatum, och inget av de handmarkerade felen går att rätta maskinellt. Enligt antagandet i `plan.md` sattes fältet i stället till det felskrivna `25/8-2026`, så att M3 har ett demonstrationsobjekt i inkrement 2. Avvikelsen från skärmdumpen står i `_kommentar` i testdatan. | Inkrement 1 | Testdatan avviker medvetet från källan; måste sägas i demot |
| 4 | Planen sa inte om en automatisk rättning ska sparas eller bara redovisas. Valet blev att granskningen arbetar på en kopia och lämnar rättningen i rapporten — testdatan rörs inte, så demot går att köra om utan omstart. `hamta_arende` returnerar numera en kopia. | Inkrement 2 | Ett beslut som borde ha stått i planen; inkrement 4:s logg får bära spårbarheten i stället |
| 5 | Klickkontrollen "knappen Kvalitetsgranska" gick inte att köra härifrån — webbläsarverktyget finns inte i sessionen. API:t är verifierat mot alla tre ärendena och gränssnittets kopplingar är kontrollerade statiskt, men själva klicket är oprövat. | Inkrement 2 | Måste klickas igenom för hand före demot |
