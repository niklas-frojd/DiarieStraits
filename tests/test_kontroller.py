"""Kontroll för inkrement 2: en testgrupp per regel i regelmotorn.

Inkrement 4 lade till sorteringen, loggen och förslagen längst ned.
"""

from datetime import datetime

import pytest

from app.data import hamta_arende
from app.kontroller import Utfall, kvalitetsgranska
from app.kontroller.datum import Datumformat, tolka_datum
from app.kontroller.falt import KopiaTill, ObligatoriskaFalt


def fynd_for(arendenummer, checker):
    return checker.granska(hamta_arende(arendenummer))


# --- Regel: obligatoriska fält -------------------------------------------------


def test_korrekt_arende_saknar_inget_falt():
    assert fynd_for("2026-00064", ObligatoriskaFalt()) == []


def test_felaktigt_arende_saknar_ansvarig_person():
    fynd = fynd_for("2026-00066", ObligatoriskaFalt())
    assert [f.falt for f in fynd] == ["ansvarig_person"]
    assert fynd[0].utfall is Utfall.BEDOMNING


def test_saknat_falt_rattas_aldrig_automatiskt():
    """M5: ett tomt fält kan AI:n inte fylla i åt registratorn."""
    for fynd in fynd_for("2026-00066", ObligatoriskaFalt()):
        assert fynd.utfall is not Utfall.RATTAD
        assert fynd.efter == ""


def test_blanktecken_raknas_som_tomt():
    arende = hamta_arende("2026-00064")
    arende["dokument"]["detaljer"]["ansvarig_person"] = "   "
    assert [f.falt for f in ObligatoriskaFalt().granska(arende)] == ["ansvarig_person"]


# --- Regel: datumformat --------------------------------------------------------


@pytest.mark.parametrize(
    "skrivet, iso",
    [
        ("25/8-2026", "2026-08-25"),
        ("25/8/2026", "2026-08-25"),
        ("25.8.2026", "2026-08-25"),
        ("2026-8-5", "2026-08-05"),
        ("2026/08/25", "2026-08-25"),
        ("20260825", "2026-08-25"),
        ("2026-08-25", "2026-08-25"),
    ],
)
def test_tolkbara_datum(skrivet, iso):
    assert tolka_datum(skrivet) == iso


@pytest.mark.parametrize("skrivet", ["31/2-2026", "i förrgår", "2026", "25 augusti", ""])
def test_otolkbara_datum(skrivet):
    assert tolka_datum(skrivet) is None


def test_korrekt_arende_har_inga_datumfel():
    assert fynd_for("2026-00064", Datumformat()) == []


def test_felskrivet_dokumentdatum_rattas_automatiskt():
    fynd = fynd_for("2026-00066", Datumformat())
    assert [f.falt for f in fynd] == ["dokumentdatum"]
    assert (fynd[0].utfall, fynd[0].fore, fynd[0].efter) == (
        Utfall.RATTAD,
        "25/8-2026",
        "2026-08-25",
    )


def test_rattningen_slar_igenom_i_bada_blocken():
    """Detaljer och registrering speglar varandra i Janus-vyn."""
    arende = hamta_arende("2026-00066")
    Datumformat().granska(arende)
    dokument = arende["dokument"]
    assert dokument["detaljer"]["dokumentdatum"] == "2026-08-25"
    assert dokument["registrering"]["dokumentdatum"] == "2026-08-25"


def test_otolkbart_datum_flaggas_i_stallet_for_att_gissas():
    arende = hamta_arende("2026-00064")
    arende["dokument"]["detaljer"]["dokumentdatum"] = "nästa vecka"
    fynd = Datumformat().granska(arende)
    assert fynd[0].utfall is Utfall.BEDOMNING
    assert arende["dokument"]["detaljer"]["dokumentdatum"] == "nästa vecka"


def test_tomt_datumfalt_lamnas_till_faltkontrollen():
    arende = hamta_arende("2026-00064")
    arende["dokument"]["detaljer"]["dokumentdatum"] = ""
    assert Datumformat().granska(arende) == []


# --- Regel: kopia till ---------------------------------------------------------


def test_kopia_till_rensas_automatiskt():
    arende = hamta_arende("2026-00065")
    fynd = KopiaTill().granska(arende)
    assert [f.utfall for f in fynd] == [Utfall.RATTAD]
    assert fynd[0].fore == "registrator@statskontoret.se"
    assert arende["dokument"]["registrering"]["kopia_till"] == ""


def test_tomt_kopia_till_ger_inget_fynd():
    assert fynd_for("2026-00064", KopiaTill()) == []


# --- Motorn som helhet ---------------------------------------------------------


def test_korrekt_arende_passerar_rent():
    rapport = kvalitetsgranska(hamta_arende("2026-00064"))
    assert rapport["fynd"] == []
    assert rapport["status"] == "rent"


def test_felaktigt_arende_far_en_rattning_och_flera_flaggor():
    rapport = kvalitetsgranska(hamta_arende("2026-00066"))
    regler = [f["regel"] for f in rapport["fynd"]]
    assert regler == [
        "obligatoriska-fält",
        "klassificering",
        "titel-obegriplig",  # ärendets titel
        "titel-obegriplig",  # dokumentets titel
        "klassificering",
        "klassificering",
        "datumformat",
    ]
    assert rapport["antal_rattade"] == 1
    assert rapport["status"] == "kräver_bedömning"


def test_gransfallet_far_sin_automatiska_rattning():
    rapport = kvalitetsgranska(hamta_arende("2026-00065"))
    assert "kopia-till" in [f["regel"] for f in rapport["fynd"]]
    assert rapport["antal_rattade"] == 1


def test_varje_fynd_har_en_forklaring():
    """M4: ingen flagga utan text som en registrator förstår."""
    for nummer in ("2026-00064", "2026-00065", "2026-00066"):
        for fynd in kvalitetsgranska(hamta_arende(nummer))["fynd"]:
            assert fynd["forklaring"].strip()
            assert fynd["etikett"] in fynd["forklaring"]


def test_granskningen_ror_inte_testdatan():
    """Demot ska gå att köra om: samma ärende, samma svar."""
    nu = datetime(2026, 9, 11, 17, 0, 0)
    forst = kvalitetsgranska(hamta_arende("2026-00066"), nu=nu)
    igen = kvalitetsgranska(hamta_arende("2026-00066"), nu=nu)
    assert forst == igen
    assert hamta_arende("2026-00066")["dokument"]["detaljer"]["dokumentdatum"] == "25/8-2026"


# --- Inkrement 4: ordning, förslag och logg ------------------------------------


@pytest.mark.parametrize("nummer", ["2026-00064", "2026-00065", "2026-00066"])
def test_fynden_kommer_i_strangaste_ordning(nummer):
    """Det som stoppar ärendet ligger överst, det som redan är gjort underst."""
    rang = {"kräver_bedömning": 0, "förslag": 1, "rättad": 2}
    ordning = [rang[f["utfall"]] for f in kvalitetsgranska(hamta_arende(nummer))["fynd"]]
    assert ordning == sorted(ordning)


@pytest.mark.parametrize("nummer", ["2026-00064", "2026-00065", "2026-00066"])
def test_forslag_rattar_aldrig_sjalvt(nummer):
    """M5: ett förslag bär ett värde men skriver inte in det."""
    for fynd in kvalitetsgranska(hamta_arende(nummer))["fynd"]:
        if fynd["utfall"] == "förslag":
            assert fynd["forslag"]
            assert fynd["efter"] == ""


@pytest.mark.parametrize("nummer", ["2026-00064", "2026-00065", "2026-00066"])
def test_loggen_har_en_rad_per_fynd(nummer):
    """Spårbarheten enligt adr.md: regel, före/efter-värde och tidpunkt."""
    nu = datetime(2026, 9, 11, 17, 0, 0)
    rapport = kvalitetsgranska(hamta_arende(nummer), nu=nu)
    assert len(rapport["logg"]) == len(rapport["fynd"])
    for rad, fynd in zip(rapport["logg"], rapport["fynd"]):
        assert rad["tidpunkt"] == "2026-09-11T17:00:00"
        assert rad["regel"] == fynd["regel"]
        assert rad["fore"] == fynd["fore"]
        assert rad["efter"] == (fynd["efter"] or fynd["forslag"])
