"""Regelmotorn: kör varje Checker över ärendet och samlar fynden.

Ingen LLM i kärnflödet (Beslut 1) — demot kör utan API-nyckel och utan nätverk.
"""

from copy import deepcopy
from dataclasses import asdict
from datetime import datetime

from app.kontroller.datum import Datumformat
from app.kontroller.falt import KopiaTill, ObligatoriskaFalt
from app.kontroller.gransfall import (
    AnkomstdatumIOrdning,
    BlandadRiktning,
    ExternProcess,
    KontaktForm,
    Sekretess,
)
from app.kontroller.klassificering import KlassificeringsChecker
from app.kontroller.modell import Utfall
from app.kontroller.titel import TitelChecker

# Ordningen här styr bara i vilken ordning kontrollerna körs — Datumformat måste
# gå före AnkomstdatumIOrdning, som jämför färdigrättade datum. Hur fynden radas
# upp i vyn avgörs av `sortera`.
REGISTER = [
    ObligatoriskaFalt(),
    Datumformat(),
    KopiaTill(),
    KlassificeringsChecker(),
    Sekretess(),
    BlandadRiktning(),
    KontaktForm(),
    AnkomstdatumIOrdning(),
    ExternProcess(),
    TitelChecker(),
]

# Det som stoppar ärendet ligger överst, det som redan är gjort underst
# (`testfall-metadata.md`, Fall 3: "flagga 1 och 2 lyfts överst").
STRANGHET = {Utfall.BEDOMNING: 0, Utfall.FORSLAG: 1, Utfall.RATTAD: 2}


def sortera(fynd):
    """Fynden i visningsordning. Stabil, så registerordningen avgör inom en grupp."""
    return sorted(fynd, key=lambda f: STRANGHET[f.utfall])


def samlad_status(fynd):
    """Ärendets utfall som helhet — det strängaste fyndet avgör."""
    utfall = {f.utfall for f in fynd}
    if Utfall.BEDOMNING in utfall:
        return "kräver_bedömning"
    if Utfall.FORSLAG in utfall:
        return "förslag"
    if Utfall.RATTAD in utfall:
        return "rättat"
    return "rent"


def loggrad(fynd, tidpunkt):
    """Spårbarheten enligt skissen i `adr.md`: regel, före/efter-värde, tidpunkt."""
    return {
        "tidpunkt": tidpunkt,
        "regel": fynd.regel,
        "falt": fynd.falt,
        "etikett": fynd.etikett,
        "utfall": fynd.utfall.value,
        "fore": fynd.fore,
        "efter": fynd.efter or fynd.forslag,
    }


def kvalitetsgranska(arende, nu=None):
    """Granskar en kopia av ärendet och lämnar tillbaka rapporten.

    Testdatan rörs inte: granskningen är alltid omkörbar och ger samma svar varje
    gång, vilket demot klockan 18:00 bygger på. `nu` går att sätta i test så att
    tidpunkten i loggen blir förutsägbar.
    """
    tidpunkt = (nu or datetime.now()).isoformat(timespec="seconds")
    granskat = deepcopy(arende)
    fynd = sortera([f for checker in REGISTER for f in checker.granska(granskat)])
    return {
        "arendenummer": granskat["arendenummer"],
        "status": samlad_status(fynd),
        "antal_rattade": sum(1 for f in fynd if f.utfall is Utfall.RATTAD),
        "fynd": [asdict(f) for f in fynd],
        "logg": [loggrad(f, tidpunkt) for f in fynd],
        "arende": granskat,
    }
