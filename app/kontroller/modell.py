"""Gemensam modell för kontrollerna: utfall, fynd och Checker-gränssnittet.

Uppdelningen i utfall följer skissen i `docs/markdown/adr.md`. Gränssnittet är
avsiktligt tunt: inkrement 3–5 lägger till fler Checkers — och en LLM-baserad
kontroll kan pluggas in senare — utan att flödet byggs om (Beslut 1).
"""

from dataclasses import dataclass
from enum import Enum


class Utfall(str, Enum):
    """Vad kontrollen kom fram till. Ett fjärde utfall, "går vidare oberört",
    behöver ingen egen post — det är frånvaron av fynd."""

    RATTAD = "rättad"
    FORSLAG = "förslag"
    BEDOMNING = "kräver_bedömning"


@dataclass(frozen=True)
class Fynd:
    """En rad i granskningsresultatet: vilken regel som triggade, på vilket fält,
    hur det landade och en mallbaserad förklaring (Beslut 2 — ingen LLM i v1)."""

    regel: str
    falt: str
    etikett: str
    utfall: Utfall
    forklaring: str
    fore: str = ""
    efter: str = ""


class Checker:
    """Ett kontrollområde — fält, format, klassificering, titel.

    `granska` får hela ärendet och får skriva i det: ett fynd med utfallet
    RATTAD ska ha genomfört sin rättning. Motorn arbetar på en kopia, så
    testdatan påverkas inte.
    """

    namn = ""

    def granska(self, arende: dict) -> list[Fynd]:
        raise NotImplementedError


def satt_falt(dokument: dict, nyckel: str, varde: str) -> None:
    """Skriver värdet överallt nyckeln finns.

    Detaljer och registrering speglar varandra i Janus-vyn; en rättning som bara
    slog igenom på ena stället skulle synas som ett nytt fel.
    """
    for block in (dokument["detaljer"], dokument["registrering"]):
        if nyckel in block:
            block[nyckel] = varde
