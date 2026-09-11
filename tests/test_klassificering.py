"""Kontroll för inkrement 3: klassificerings- och riktningskontroller."""

from app.data import hamta_arende
from app.klassificering import KlassificeringsChecker

checker = KlassificeringsChecker()


def flaggor(arendenummer):
    return checker.granska(hamta_arende(arendenummer))


def test_felaktigt_arende_ger_minst_tre_flaggor_i_kategorin():
    resultat = flaggor("2026-00066")
    assert len(resultat) >= 3
    assert {flagga["kategori"] for flagga in resultat} == {"klassificering"}
    assert {flagga["falt"] for flagga in resultat} >= {"handlingstyp", "process", "kontakter"}


def test_korrekt_arende_ger_inga_flaggor():
    assert flaggor("2026-00064") == []
