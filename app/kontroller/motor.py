"""Regelmotorn: kör varje Checker över ärendet och samlar fynden.

Ingen LLM i kärnflödet (Beslut 1) — demot kör utan API-nyckel och utan nätverk.
"""

from copy import deepcopy
from dataclasses import asdict

from app.kontroller.datum import Datumformat
from app.kontroller.falt import KopiaTill, ObligatoriskaFalt
from app.kontroller.modell import Utfall

# Ordningen styr hur fynden radas upp i vyn: rättade fältvärden först, sedan
# formatet, sist det som saknas. Inkrement 3–5 lägger till fler Checkers här.
REGISTER = [ObligatoriskaFalt(), Datumformat(), KopiaTill()]


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


def kvalitetsgranska(arende):
    """Granskar en kopia av ärendet och lämnar tillbaka rapporten.

    Testdatan rörs inte: granskningen är alltid omkörbar och ger samma svar varje
    gång, vilket demot klockan 18:00 bygger på.
    """
    granskat = deepcopy(arende)
    fynd = [f for checker in REGISTER for f in checker.granska(granskat)]
    return {
        "arendenummer": granskat["arendenummer"],
        "status": samlad_status(fynd),
        "antal_rattade": sum(1 for f in fynd if f.utfall is Utfall.RATTAD),
        "fynd": [asdict(f) for f in fynd],
        "arende": granskat,
    }
