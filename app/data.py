"""Testdata: de tre ärendena ur docs/markdown/testfall-metadata.md."""

import json
from copy import deepcopy
from pathlib import Path

DATAFIL = Path(__file__).parent / "data" / "arenden.json"

ARENDEN = json.loads(DATAFIL.read_text(encoding="utf-8"))


def lista_arenden():
    """Ärendena i demoordningen, med bara fälten listvyn visar."""
    return [
        {
            "arendenummer": arende["arendenummer"],
            "titel": arende["titel"],
            "dokumentkategori": arende["dokument"]["detaljer"]["dokumentkategori"],
            "ankomstdatum": arende["dokument"]["detaljer"]["ankomstdatum"],
            "status": arende["dokument"]["detaljer"]["status"],
        }
        for arende in ARENDEN
    ]


def hamta_arende(arendenummer):
    """Hela ärendet som en egen kopia, eller None om numret inte finns.

    Kopian gör att en automatisk rättning aldrig skriver i testdatan: samma
    ärende går att granska om och om igen med samma resultat.
    """
    for arende in ARENDEN:
        if arende["arendenummer"] == arendenummer:
            return deepcopy(arende)
    return None
