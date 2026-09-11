"""Kontroll för inkrement 4: gränsfallet 2026-00065 stoppas för mänsklig bedömning.

Flaggorna följer `docs/markdown/testfall-metadata.md`, Fall 3.
"""

import pytest

from app.data import hamta_arende
from app.kontroller import Utfall, kvalitetsgranska
from app.kontroller.gransfall import (
    AnkomstdatumIOrdning,
    BlandadRiktning,
    ExternProcess,
    KontaktForm,
    Sekretess,
)

ALLA = [Sekretess(), BlandadRiktning(), KontaktForm(), AnkomstdatumIOrdning(), ExternProcess()]


def fynd_for(arendenummer, checker):
    return checker.granska(hamta_arende(arendenummer))


# --- Planens kontroll ----------------------------------------------------------


def test_gransfallet_kraver_mansklig_bedomning():
    assert kvalitetsgranska(hamta_arende("2026-00065"))["status"] == "kräver_bedömning"


@pytest.mark.parametrize("checker", ALLA, ids=lambda c: c.namn)
def test_ingen_gransfallskontroll_flaggar_det_korrekta_arendet(checker):
    assert fynd_for("2026-00064", checker) == []


# --- Flagga 1: sekretess -------------------------------------------------------


def test_oppen_skyddskod_pa_upphandlingsmaterial_flaggas():
    fynd = fynd_for("2026-00065", Sekretess())
    assert [(f.falt, f.utfall) for f in fynd] == [("skyddskod", Utfall.BEDOMNING)]


def test_sekretess_flaggas_inte_nar_skyddskoden_redan_ar_satt():
    arende = hamta_arende("2026-00065")
    arende["dokument"]["detaljer"]["skyddskod"] = "Sekretess"
    assert Sekretess().granska(arende) == []


# --- Flagga 2: blandad riktning ------------------------------------------------


def test_mejltrad_med_tva_meddelanden_flaggas():
    fynd = fynd_for("2026-00065", BlandadRiktning())
    assert [(f.falt, f.utfall) for f in fynd] == [("dokumentkategori", Utfall.BEDOMNING)]


# --- Flagga 3: kontaktform -----------------------------------------------------


def test_mejladress_som_avsandare_ger_forslag():
    fynd = fynd_for("2026-00065", KontaktForm())
    assert [f.utfall for f in fynd] == [Utfall.FORSLAG]
    assert fynd[0].forslag == "Konsultbolaget"
    assert fynd[0].efter == ""  # M5: förslaget skrivs aldrig in av AI:n


# --- Flagga 5: ankomstdatum ----------------------------------------------------


def test_ankomstdatum_efter_dokumentdatum_flaggas():
    fynd = fynd_for("2026-00065", AnkomstdatumIOrdning())
    assert [(f.falt, f.utfall) for f in fynd] == [("ankomstdatum", Utfall.BEDOMNING)]


def test_samma_datum_ger_inget_fynd():
    assert fynd_for("2026-00066", AnkomstdatumIOrdning()) == []


# --- Flagga 7: extern process --------------------------------------------------


def test_intern_process_med_extern_avsandare_ger_forslag():
    fynd = fynd_for("2026-00065", ExternProcess())
    assert [(f.falt, f.utfall) for f in fynd] == [("process", Utfall.FORSLAG)]


def test_avsandare_utan_mejladress_lamnas_at_klassificeringen():
    """"Statskontoret" och "Rex Ljungqvist" säger inget om riktningen."""
    arende = hamta_arende("2026-00065")
    arende["dokument"]["registrering"]["avsandare"] = "Statskontoret"
    assert ExternProcess().granska(arende) == []


# --- Hela gränsfallet ----------------------------------------------------------


def test_gransfallet_far_sina_sju_flaggor():
    """Alla sju flaggorna ur testfallsdokumentet. Flagga 6 — det engelska ordet i
    titeln — kom med i inkrement 5 och faller ut som `titel-språk`."""
    rapport = kvalitetsgranska(hamta_arende("2026-00065"))
    assert [f["regel"] for f in rapport["fynd"]] == [
        "sekretess",
        "blandad-riktning",
        "ankomstdatum",
        "titel-språk",
        "kontaktform",
        "extern-process",
        "kopia-till",
    ]
    assert rapport["antal_rattade"] == 1
