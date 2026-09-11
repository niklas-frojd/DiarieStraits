"""Formatkontroll för datumfält: felskrivna datum rättas till ISO-format.

Ett datum som går att tolka entydigt är ett tydligt regelbaserat fel och rättas
automatiskt (M3, prd.md: "felformaterat datum/diarienummer"). Går det inte att
tolka avgör AI:n ingenting själv — då flaggas det för mänsklig bedömning (M5).
"""

import re
from datetime import date

from app.kontroller.modell import Checker, Fynd, Utfall, satt_falt

DATUMFALT = [
    ("ankomstdatum", "Ankomstdatum"),
    ("dokumentdatum", "Dokumentdatum"),
    ("signeringsdatum", "Signeringsdatum"),
    ("sista_svarsdatum", "Sista svarsdatum"),
]

# Dag före månad i de tvetydiga fallen — svensk skrivkonvention.
MONSTER = [
    (re.compile(r"^(\d{4})[-/.](\d{1,2})[-/.](\d{1,2})$"), "åmd"),
    (re.compile(r"^(\d{1,2})[/.](\d{1,2})[-/. ](\d{4})$"), "dmå"),
    (re.compile(r"^(\d{4})(\d{2})(\d{2})$"), "åmd"),
]


def tolka_datum(varde):
    """Värdet som ISO-datum, eller None om det inte går att tolka entydigt."""
    text = varde.strip()
    for monster, ordning in MONSTER:
        traff = monster.match(text)
        if not traff:
            continue
        forst, mitten, sist = traff.groups()
        ar, manad, dag = (forst, mitten, sist) if ordning == "åmd" else (sist, mitten, forst)
        try:
            return date(int(ar), int(manad), int(dag)).isoformat()
        except ValueError:
            return None  # Träffade mönstret men är inget riktigt datum, t.ex. 31/2.
    return None


class Datumformat(Checker):
    namn = "datumformat"

    def granska(self, arende):
        dokument = arende["dokument"]
        detaljer = dokument["detaljer"]
        fynd = []
        for nyckel, etikett in DATUMFALT:
            fore = detaljer.get(nyckel, "").strip()
            if not fore:
                continue  # Tomma fält äger ObligatoriskaFalt.
            iso = tolka_datum(fore)
            if iso == fore:
                continue
            if iso is None:
                fynd.append(
                    Fynd(
                        regel=self.namn,
                        falt=nyckel,
                        etikett=etikett,
                        utfall=Utfall.BEDOMNING,
                        forklaring=(
                            f"{etikett} \"{fore}\" går inte att tolka som ett datum. "
                            "Vilket datum som avses kan inte avgöras maskinellt."
                        ),
                        fore=fore,
                    )
                )
                continue
            satt_falt(dokument, nyckel, iso)
            fynd.append(
                Fynd(
                    regel=self.namn,
                    falt=nyckel,
                    etikett=etikett,
                    utfall=Utfall.RATTAD,
                    forklaring=(
                        f"{etikett} var skrivet som \"{fore}\". Datum ska anges som "
                        f"ÅÅÅÅ-MM-DD, så värdet har rättats till {iso}."
                    ),
                    fore=fore,
                    efter=iso,
                )
            )
        return fynd
