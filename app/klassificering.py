"""Checker för klassificering: handlingstyp och process mot den mockade kodlistan,
samt avsändare och mottagare mot dokumentkategorin (riktningen)."""

import json
from pathlib import Path

KODLISTA = json.loads(
    (Path(__file__).parent / "data" / "klassificering.json").read_text(encoding="utf-8")
)

# Vilken kontaktroll som ska vara intern för respektive riktning.
INTERN_ROLL = {"Inkommande": "Mottagare", "Utgående": "Avsändare"}


def _kod(varde):
    """'6.1-1 - Beslut' -> '6.1-1'."""
    return varde.split(" - ")[0].strip()


def _flagga(regel, falt, varde, beskrivning):
    return {
        "kategori": KlassificeringsChecker.kategori,
        "regel": regel,
        "falt": falt,
        "varde": varde,
        "beskrivning": beskrivning,
    }


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


class KlassificeringsChecker:
    kategori = "klassificering"

    def granska(self, arende):
        dokument = arende["dokument"]
        detaljer = dokument["detaljer"]
        riktning = detaljer["dokumentkategori"]
        flaggor = []

        for falt, lista in (("handlingstyp", "handlingstyper"), ("process", "processer")):
            varde = detaljer[falt]
            kod = KODLISTA[lista].get(_kod(varde))
            if kod is None:
                flaggor.append(_flagga(f"{falt}_finns", falt, varde, f"{varde} finns inte i kodlistan."))
            elif riktning not in kod["dokumentkategorier"]:
                tillatna = ", ".join(kod["dokumentkategorier"])
                flaggor.append(_flagga(
                    f"{falt}_mot_riktning", falt, varde,
                    f"{varde} används för {tillatna}, men handlingen är {riktning}.",
                ))

        kontakter = dokument["kontakter"]
        if _omkastade(kontakter, riktning):
            varde = ", ".join(f"{k['roll']}: {k['kontakt']}" for k in kontakter)
            flaggor.append(_flagga(
                "avsandare_mottagare_omkastade", "kontakter", varde,
                f"Handlingen är {riktning}, men avsändaren är intern och mottagaren extern. "
                "Avsändare och mottagare verkar omkastade.",
            ))

        return flaggor
