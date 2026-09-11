"""Kontroll för inkrement 3: klassificerings- och riktningskontroller.

Checkern flyttades in i regelmotorn i inkrement 4 och returnerar `Fynd`.
"""

from app.data import hamta_arende
from app.kontroller import Utfall
from app.kontroller.klassificering import KlassificeringsChecker

checker = KlassificeringsChecker()


def flaggor(arendenummer):
    return checker.granska(hamta_arende(arendenummer))


def test_felaktigt_arende_ger_minst_tre_flaggor_i_kategorin():
    resultat = flaggor("2026-00066")
    assert len(resultat) >= 3
    assert {flagga.regel for flagga in resultat} == {"klassificering"}
    assert {flagga.falt for flagga in resultat} >= {"handlingstyp", "process", "kontakter"}


def test_korrekt_arende_ger_inga_flaggor():
    assert flaggor("2026-00064") == []


def test_ifragasatt_kod_blir_forslag_och_rattas_inte():
    """M5: vilken kod som är rätt kräver tolkning — AI:n avgör den inte själv."""
    koder = [f for f in flaggor("2026-00066") if f.falt in ("handlingstyp", "process")]
    assert [f.utfall for f in koder] == [Utfall.FORSLAG, Utfall.FORSLAG]
    for fynd in koder:
        assert fynd.forslag
        assert fynd.efter == ""


def test_forslaget_ar_en_kod_som_tillater_riktningen():
    forslag = {f.falt: f.forslag for f in flaggor("2026-00066")}
    assert forslag["handlingstyp"] == "2.3.1-5 - Korrespondens"
    assert forslag["process"] == "2.3.1 - Kommunicera internt"


def test_omkastade_kontakter_kraver_bedomning():
    kontakter = [f for f in flaggor("2026-00066") if f.falt == "kontakter"]
    assert [f.utfall for f in kontakter] == [Utfall.BEDOMNING]
