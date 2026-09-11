"""Testdata: de tre ärendena ur docs/markdown/testfall-metadata.md."""

import json
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
    """Hela ärendet, eller None om numret inte finns."""
    for arende in ARENDEN:
        if arende["arendenummer"] == arendenummer:
            return arende
    return None
