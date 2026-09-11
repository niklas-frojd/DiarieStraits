"use strict";

// Fältordningen i Detaljer-panelen följer docs/png/Test Korrekt Skärmdump.png.
const DETALJFALT = [
  ["arende", "Ärende"],
  ["ankomstdatum", "Ankomstdatum"],
  ["dokumentdatum", "Dokumentdatum"],
  ["signerad", "Signerad"],
  ["signeringsdatum", "Signeringsdatum"],
  ["sista_svarsdatum", "Sista svarsdatum"],
  ["dokumentkategori", "Dokumentkategori"],
  ["status", "Status"],
  ["ansvarig_enhet", "Ansvarig enhet"],
  ["ansvarig_person", "Ansvarig person"],
  ["skyddskod", "Skyddskod"],
  ["atkomstgrupp", "Åtkomstgrupp"],
  ["delarkiv", "Delarkiv"],
  ["handlingstyp", "Handlingstyp"],
  ["process", "Process"],
];

const listvy = document.getElementById("listvy");
const detaljvy = document.getElementById("detaljvy");
const brodsmula = document.getElementById("brodsmula");
const tillbaka = document.getElementById("tillbaka");

function text(varde) {
  return varde === null || varde === undefined ? "" : String(varde);
}

function definitionslista(element, rader) {
  element.replaceChildren();
  for (const [etikett, varde] of rader) {
    const dt = document.createElement("dt");
    dt.textContent = etikett + ":";
    const dd = document.createElement("dd");
    dd.textContent = text(varde);
    element.append(dt, dd);
  }
}

function sattBrodsmula(delar) {
  brodsmula.replaceChildren();
  delar.forEach((del, i) => {
    if (i > 0) {
      const pil = document.createElement("span");
      pil.className = "pil";
      pil.textContent = "▸";
      brodsmula.append(pil);
    }
    const span = document.createElement("span");
    span.textContent = del;
    brodsmula.append(span);
  });
}

async function visaLista() {
  const arenden = await fetch("/api/arenden").then((r) => r.json());
  const rader = document.getElementById("listrader");
  rader.replaceChildren();
  for (const arende of arenden) {
    const tr = document.createElement("tr");
    for (const falt of ["arendenummer", "titel", "dokumentkategori", "ankomstdatum", "status"]) {
      const td = document.createElement("td");
      td.textContent = text(arende[falt]);
      tr.append(td);
    }
    tr.addEventListener("click", () => {
      history.pushState({}, "", "/arende/" + arende.arendenummer);
      visaArende(arende.arendenummer);
    });
    rader.append(tr);
  }
  sattBrodsmula(["Hem - Redo för diarieföring"]);
  listvy.hidden = false;
  detaljvy.hidden = true;
  tillbaka.hidden = true;
}

async function visaArende(arendenummer) {
  const svar = await fetch("/api/arenden/" + arendenummer);
  if (!svar.ok) {
    visaLista();
    return;
  }
  const arende = await svar.json();
  const dok = arende.dokument;

  definitionslista(
    document.getElementById("detaljer"),
    DETALJFALT.map(([nyckel, etikett]) => [etikett, dok.detaljer[nyckel]])
  );
  definitionslista(
    document.getElementById("kontakter"),
    dok.kontakter.map((k) => [
      k.roll,
      k.anteckning ? k.kontakt + " (" + k.anteckning + ")" : k.kontakt,
    ])
  );

  document.getElementById("filantal").textContent = "(" + dok.filer.length + ")";
  const filrader = document.getElementById("filrader");
  filrader.replaceChildren();
  for (const fil of dok.filer) {
    const tr = document.createElement("tr");
    for (const falt of ["titel", "typ", "filstorlek", "senast_andrad"]) {
      const td = document.createElement("td");
      td.textContent = text(fil[falt]);
      tr.append(td);
    }
    filrader.append(tr);
  }

  sattBrodsmula([
    "Hem - Redo för diarieföring",
    "Ärende: " + arende.titel,
    "Ärendedokument: " + dok.titel,
  ]);
  listvy.hidden = true;
  detaljvy.hidden = false;
  tillbaka.hidden = false;
}

function dirigera() {
  const match = location.pathname.match(/^\/arende\/(.+)$/);
  if (match) {
    visaArende(decodeURIComponent(match[1]));
  } else {
    visaLista();
  }
}

tillbaka.addEventListener("click", (e) => {
  e.preventDefault();
  history.pushState({}, "", "/");
  visaLista();
});

window.addEventListener("popstate", dirigera);
dirigera();
