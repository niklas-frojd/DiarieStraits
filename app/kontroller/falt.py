"""Fältkontroller: uppgifter som måste finnas, och en som måste vara tom.

Källa: checklistans avsnitt Ärendedokument och de fält som är markerade
obligatoriska i registreringsformuläret (`docs/markdown/testfall-metadata.md`).
"""

from app.kontroller.modell import Checker, Fynd, Utfall, satt_falt

# Fälten läses ur Detaljer-panelen, den vy registratorn faktiskt tittar på.
# Dokumentdatum är inte stjärnmärkt i formuläret men krävs av checklistan:
# "Datum på ärendedokumentet ska stämma överens med när handlingen inkom".
OBLIGATORISKA = [
    ("ankomstdatum", "Ankomstdatum"),
    ("dokumentdatum", "Dokumentdatum"),
    ("dokumentkategori", "Dokumentkategori"),
    ("ansvarig_enhet", "Ansvarig enhet"),
    ("ansvarig_person", "Ansvarig person"),
    ("skyddskod", "Skyddskod"),
    ("atkomstgrupp", "Åtkomstgrupp"),
    ("handlingstyp", "Handlingstyp"),
    ("process", "Process"),
]


class ObligatoriskaFalt(Checker):
    """Saknad uppgift går aldrig att fylla i maskinellt — den flaggas (M2, M5)."""

    namn = "obligatoriska-fält"

    def granska(self, arende):
        detaljer = arende["dokument"]["detaljer"]
        return [
            Fynd(
                regel=self.namn,
                falt=nyckel,
                etikett=etikett,
                utfall=Utfall.BEDOMNING,
                forklaring=(
                    f"{etikett} saknas. Fältet är obligatoriskt och värdet går inte "
                    "att härleda ur övrig metadata — registrator får fylla i det."
                ),
                fore="",
            )
            for nyckel, etikett in OBLIGATORISKA
            if not detaljer.get(nyckel, "").strip()
        ]


class KopiaTill(Checker):
    """Checklistan: "Fältet för kontakter ska vara rensade på 'kopia till'".

    Entydigt regelbaserat, alltså en automatisk rättning (M3).
    """

    namn = "kopia-till"

    def granska(self, arende):
        dokument = arende["dokument"]
        fore = dokument["registrering"].get("kopia_till", "").strip()
        if not fore:
            return []
        satt_falt(dokument, "kopia_till", "")
        return [
            Fynd(
                regel=self.namn,
                falt="kopia_till",
                etikett="Kopia till",
                utfall=Utfall.RATTAD,
                forklaring=(
                    "Kopia till var ifyllt. Enligt checklistan ska kontaktfältet vara "
                    "rensat på \"kopia till\", så fältet har tömts automatiskt."
                ),
                fore=fore,
                efter="",
            )
        ]
