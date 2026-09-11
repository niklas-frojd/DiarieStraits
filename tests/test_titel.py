"""Kontroll för inkrement 5: ordlista med giltiga och ogiltiga titlar.

Raden i `plan.md` är just den här listan — heuristiken ska fånga "UUY HHT BB" utan
att fälla en vanlig, beskrivande titel.
"""

import pytest

from app.data import hamta_arende
from app.kontroller import Utfall, kvalitetsgranska
from app.kontroller.titel import TitelChecker

checker = TitelChecker()

# Titlar som ska passera obehindrat — de beskriver vad handlingen rör, på svenska,
# utan förkortningar och utan personnamn.
GILTIGA = [
    "Test Korrekt",
    "Upphandling av utvärderingstjänster",
    "Komplettering till anbud",
    "Begäran om utlämnande av allmän handling",
    "Yttrande över remissen om ny förordning",
    "Avtal om lokalvård 2026",
    "Beslut om anställning av utredare",
]

# Titlar som ska flaggas, med den regel i checklistan som fäller dem.
OGILTIGA = [
    ("UUY HHT BB", "titel-obegriplig"),
    ("Test Felaktigt UTY GGG BBO", "titel-obegriplig"),
    ("Underlag GGG till beslut", "titel-obegriplig"),
    ("Svar på frågor om ESV:s revision", "titel-förkortning"),
    ("PM inför mötet", "titel-förkortning"),
    ("Komplettering till anbud, benchmarking av utvärderingsmetod", "titel-språk"),
    ("Workshop om nya rutiner", "titel-språk"),
    ("Anställningsbeslut för Rex Ljungqvist", "titel-personnamn"),
    ("Yttrande från Anna Svensson", "titel-personnamn"),
]


def granska_titel(titel, ansvarig_person=None):
    """Fynden för dokumentets titel. Ärendets titel lämnas som referensfallets."""
    arende = hamta_arende("2026-00064")
    arende["dokument"]["titel"] = titel
    if ansvarig_person is not None:
        arende["dokument"]["detaljer"]["ansvarig_person"] = ansvarig_person
    return [fynd for fynd in checker.granska(arende) if fynd.falt == "titel"]


# --- Ordlistan ----------------------------------------------------------------


@pytest.mark.parametrize("titel", GILTIGA)
def test_giltig_titel_passerar(titel):
    assert granska_titel(titel) == []


@pytest.mark.parametrize("titel, regel", OGILTIGA)
def test_ogiltig_titel_flaggas_av_ratt_regel(titel, regel):
    assert [fynd.regel for fynd in granska_titel(titel)] == [regel]


# --- Regeln bakom heuristiken -------------------------------------------------


def test_hela_skraptexten_raknas_upp_i_forklaringen():
    """Demovärdet i planen: registratorn ska se vilka ord som fälldes."""
    fynd = granska_titel("UUY HHT BB")[0]
    for ord in ("UUY", "HHT", "BB"):
        assert f'"{ord}"' in fynd.forklaring


def test_forkortningen_forklaras_med_sin_utskrivna_form():
    fynd = granska_titel("PM inför mötet")[0]
    assert "promemoria" in fynd.forklaring


def test_ansvarig_person_raknas_som_personnamn():
    """Namnregistret är mockat, men ärendets egen Ansvarig person är alltid en
    person och läggs till vid granskningen."""
    fynd = granska_titel("Beslut om Dalgrens anställning", ansvarig_person="Kim Dalgren")
    assert [f.regel for f in fynd] == ["titel-personnamn"]
    assert granska_titel("Beslut om Dalgrens anställning") == []


def test_flera_regler_kan_falla_samma_titel():
    regler = [fynd.regel for fynd in granska_titel("PM om workshop med Rex")]
    assert regler == ["titel-förkortning", "titel-språk", "titel-personnamn"]


def test_tom_titel_flaggas():
    assert [fynd.regel for fynd in granska_titel("   ")] == ["titel-saknas"]


def test_bade_arendets_och_dokumentets_titel_granskas():
    """Checklistan har samma kort för ärendet och för ärendedokumentet."""
    fynd = checker.granska(hamta_arende("2026-00066"))
    assert [(f.falt, f.regel) for f in fynd] == [
        ("arendetitel", "titel-obegriplig"),
        ("titel", "titel-obegriplig"),
    ]


def test_titeln_rattas_aldrig_automatiskt():
    """M5: en titel kan bara skrivas om av den som vet vad handlingen rör."""
    arende = hamta_arende("2026-00066")
    fore = arende["dokument"]["titel"]
    fynd = checker.granska(arende)
    assert fynd and all(f.utfall is Utfall.BEDOMNING and f.efter == "" for f in fynd)
    assert arende["dokument"]["titel"] == fore


# --- I motorn -----------------------------------------------------------------


def test_referensfallet_har_fortfarande_ingen_titelanmarkning():
    assert checker.granska(hamta_arende("2026-00064")) == []


def test_gransfallets_engelska_ord_faller_ut_i_rapporten():
    """Flagga 6 i `testfall-metadata.md`: "benchmarking" är en språklig bedömning."""
    rapport = kvalitetsgranska(hamta_arende("2026-00065"))
    fynd = next(f for f in rapport["fynd"] if f["regel"] == "titel-språk")
    assert fynd["utfall"] == "kräver_bedömning"
    assert "benchmarking" in fynd["forklaring"]
