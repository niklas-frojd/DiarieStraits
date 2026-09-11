"""Kontroll för inkrement 1: API:t ger de tre ärendena och deras detaljer."""

import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


@pytest.fixture
def arenden():
    svar = client.get("/api/arenden")
    assert svar.status_code == 200
    return svar.json()


def test_listan_ger_tre_arenden(arenden):
    assert len(arenden) == 3


def test_listan_foljer_demoordningen(arenden):
    nummer = [arende["arendenummer"] for arende in arenden]
    assert nummer == ["2026-00064", "2026-00066", "2026-00065"]


def test_listraden_har_falten_listvyn_visar(arenden):
    assert arenden[0] == {
        "arendenummer": "2026-00064",
        "titel": "Test Korrekt",
        "dokumentkategori": "Inkommande",
        "ankomstdatum": "2026-08-25",
        "status": "Registrerat",
    }


def test_korrekt_arende_har_detaljerna_ur_skarmdumpen():
    svar = client.get("/api/arenden/2026-00064")
    assert svar.status_code == 200
    detaljer = svar.json()["dokument"]["detaljer"]
    assert detaljer["handlingstyp"] == "2.3.1-5 - Korrespondens"
    assert detaljer["process"] == "2.3.1 - Kommunicera internt"
    assert detaljer["ansvarig_person"] == "Rex Ljungqvist"
    assert detaljer["ankomstdatum"] == "2026-08-25"


def test_felaktigt_arende_bar_felen_som_inkrement_2_ska_hitta():
    detaljer = client.get("/api/arenden/2026-00066").json()["dokument"]["detaljer"]
    assert detaljer["ansvarig_person"] == ""
    assert detaljer["dokumentdatum"] == "25/8-2026"  # felskrivet, ska rättas i inkrement 2
    assert detaljer["handlingstyp"] == "6.1-1 - Beslut"


def test_gransfallet_har_ifyllt_kopia_till():
    registrering = client.get("/api/arenden/2026-00065").json()["dokument"]["registrering"]
    assert registrering["kopia_till"] == "registrator@statskontoret.se"


def test_okant_arende_ger_404():
    assert client.get("/api/arenden/2026-99999").status_code == 404


def test_startsidan_ger_html():
    svar = client.get("/")
    assert svar.status_code == 200
    assert "text/html" in svar.headers["content-type"]


# --- Inkrement 2: Kvalitetsgranska-endpointen ---------------------------------


def test_kvalitetsgranska_ger_rapport():
    rapport = client.post("/api/arenden/2026-00066/kvalitetsgranska").json()
    assert rapport["status"] == "kräver_bedömning"
    assert rapport["antal_rattade"] == 1
    assert rapport["arende"]["dokument"]["detaljer"]["dokumentdatum"] == "2026-08-25"


def test_kvalitetsgranska_lamnar_hamtningen_oror():
    """Rättningen lever i rapporten, inte i testdatan."""
    client.post("/api/arenden/2026-00065/kvalitetsgranska")
    registrering = client.get("/api/arenden/2026-00065").json()["dokument"]["registrering"]
    assert registrering["kopia_till"] == "registrator@statskontoret.se"


def test_kvalitetsgranska_okant_arende_ger_404():
    assert client.post("/api/arenden/2026-99999/kvalitetsgranska").status_code == 404


# --- Inkrement 4: förslag, bedömning och logg ---------------------------------


def test_gransfallet_stoppas_for_mansklig_bedomning():
    rapport = client.post("/api/arenden/2026-00065/kvalitetsgranska").json()
    assert rapport["status"] == "kräver_bedömning"


def test_rapporten_bar_loggen():
    rapport = client.post("/api/arenden/2026-00066/kvalitetsgranska").json()
    assert len(rapport["logg"]) == len(rapport["fynd"])
    assert set(rapport["logg"][0]) == {
        "tidpunkt",
        "regel",
        "falt",
        "etikett",
        "utfall",
        "fore",
        "efter",
    }


def test_forslagen_nar_ut_i_api_svaret():
    fynd = client.post("/api/arenden/2026-00066/kvalitetsgranska").json()["fynd"]
    forslag = {f["falt"]: f["forslag"] for f in fynd if f["utfall"] == "förslag"}
    assert forslag == {
        "handlingstyp": "2.3.1-5 - Korrespondens",
        "process": "2.3.1 - Kommunicera internt",
    }
