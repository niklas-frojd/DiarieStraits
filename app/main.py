"""FastAPI-appen: API för ärendena och den statiska Janus-liknande vyn."""

from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.data import hamta_arende, lista_arenden
from app.kontroller import kvalitetsgranska

STATIC = Path(__file__).parent / "static"

app = FastAPI(title="Kvalitetskontroll i diariet")


@app.get("/api/arenden")
def api_arenden():
    return lista_arenden()


@app.get("/api/arenden/{arendenummer}")
def api_arende(arendenummer: str):
    arende = hamta_arende(arendenummer)
    if arende is None:
        raise HTTPException(status_code=404, detail=f"Okänt ärende: {arendenummer}")
    return arende


@app.post("/api/arenden/{arendenummer}/kvalitetsgranska")
def api_kvalitetsgranska(arendenummer: str):
    """Kör regelmotorn över ärendet och lämnar fynden plus det rättade ärendet."""
    arende = hamta_arende(arendenummer)
    if arende is None:
        raise HTTPException(status_code=404, detail=f"Okänt ärende: {arendenummer}")
    return kvalitetsgranska(arende)


@app.get("/")
@app.get("/arende/{arendenummer}")
def index(arendenummer: str = ""):
    """Samma sida för både listan och en direktlänk till ett ärende."""
    return FileResponse(STATIC / "index.html")


app.mount("/static", StaticFiles(directory=STATIC), name="static")
