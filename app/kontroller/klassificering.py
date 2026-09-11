"""Checker för klassificering: handlingstyp och process mot den mockade kodlistan,
samt avsändare och mottagare mot dokumentkategorin (riktningen).

Byggd i inkrement 3 vid sidan av regelmotorn och flyttad in hit i inkrement 4
(`friction.md`). En ifrågasatt kod rättas aldrig automatiskt — vilken kod som är
rätt kräver kännedom om ärendets sammanhang, så kontrollen lämnar ett förslag
som en människa godkänner eller avvisar (M3, M5).
"""

import json
from pathlib import Path

from app.kontroller.modell import Checker, Fynd, Utfall

KODLISTA = json.loads(
    (Path(__file__).parent.parent / "data" / "klassificering.json").read_text(encoding="utf-8")
)

# Vilken kontaktroll som ska vara intern för respektive riktning.
INTERN_ROLL = {"Inkommande": "Mottagare", "Utgående": "Avsändare"}

ETIKETT = {"handlingstyp": "Handlingstyp", "process": "Process", "kontakter": "Kontakter"}


def _kod(varde):
    """'6.1-1 - Beslut' -> '6.1-1'."""
    return varde.split(" - ")[0].strip()


def _forslag(lista, riktning):
    """Första koden i listan som tillåter riktningen, skriven som i Detaljer-vyn.

    Kodlistan är den mockade delmängden — med bara två koder per lista finns det
    alltid högst ett alternativ, och förslaget är därför entydigt i demot.
    """
    for kod, post in KODLISTA[lista].items():
        if riktning in post["dokumentkategorier"]:
            return f"{kod} - {post['namn']}"
    return ""


def _omkastade(kontakter, riktning):
    """Sant om den roll som ska vara intern är extern, och tvärtom."""
    intern_roll = INTERN_ROLL.get(riktning)
    if intern_roll is None:
        return False
    extern_roll = "Avsändare" if intern_roll == "Mottagare" else "Mottagare"
    roller = {kontakt["roll"]: kontakt["kontakt"] for kontakt in kontakter}
    if intern_roll not in roller or extern_roll not in roller:
        return False
    interna = set(KODLISTA["interna_kontakter"])
    return roller[intern_roll] not in interna and roller[extern_roll] in interna


class KlassificeringsChecker(Checker):
    namn = "klassificering"

    def granska(self, arende):
        dokument = arende["dokument"]
        detaljer = dokument["detaljer"]
        riktning = detaljer["dokumentkategori"]
        fynd = []

        for falt, lista in (("handlingstyp", "handlingstyper"), ("process", "processer")):
            varde = detaljer[falt]
            post = KODLISTA[lista].get(_kod(varde))
            if post is None:
                forklaring = (
                    f"{ETIKETT[falt]} \"{varde}\" finns inte i klassificeringsstrukturen."
                )
            elif riktning not in post["dokumentkategorier"]:
                tillatna = ", ".join(post["dokumentkategorier"])
                forklaring = (
                    f"{ETIKETT[falt]} \"{varde}\" används för {tillatna}, men handlingen "
                    f"är {riktning}."
                )
            else:
                continue
            forslag = _forslag(lista, riktning)
            if forslag:
                forklaring += f" Ett alternativ som passar riktningen är {forslag}."
            fynd.append(
                Fynd(
                    regel=self.namn,
                    falt=falt,
                    etikett=ETIKETT[falt],
                    utfall=Utfall.FORSLAG,
                    forklaring=forklaring + " Registrator avgör vilken kod som är rätt.",
                    fore=varde,
                    forslag=forslag,
                )
            )

        kontakter = dokument["kontakter"]
        if _omkastade(kontakter, riktning):
            fore = ", ".join(f"{k['roll']}: {k['kontakt']}" for k in kontakter)
            fynd.append(
                Fynd(
                    regel=self.namn,
                    falt="kontakter",
                    etikett=ETIKETT["kontakter"],
                    utfall=Utfall.BEDOMNING,
                    forklaring=(
                        f"Kontakter: handlingen är {riktning}, men avsändaren är intern och "
                        "mottagaren extern. Avsändare och mottagare verkar omkastade. Vem som "
                        "faktiskt skickade handlingen går inte att avgöra ur metadatan."
                    ),
                    fore=fore,
                )
            )

        return fynd
