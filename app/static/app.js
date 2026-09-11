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

// Sammanfattningen överst i kontrollpanelen, en rad per samlad status ur motorn.
const STATUSTEXT = {
  rent: "Inga anmärkningar. Metadatan passerar kvalitetskontrollen.",
  "rättat": "Rättat automatiskt. Inget kräver mänsklig bedömning.",
  "förslag": "Förslag att godkänna eller avvisa.",
  "kräver_bedömning": "Kräver mänsklig bedömning innan ärendet går vidare.",
};

const listvy = document.getElementById("listvy");
const detaljvy = document.getElementById("detaljvy");
const brodsmula = document.getElementById("brodsmula");
const tillbaka = document.getElementById("tillbaka");
const granskaKnapp = document.getElementById("granska");
const granskningsstatus = document.getElementById("granskningsstatus");
const fyndlista = document.getElementById("fyndlista");
const spärr = document.getElementById("spärr");
const loggpanel = document.getElementById("logg");
const loggrader = document.getElementById("loggrader");
const loggantal = document.getElementById("loggantal");

let oppetArende = "";
// Rapporten lever i webbläsaren under demot: godkända förslag skrivs aldrig
// tillbaka till testdatan, så ärendet går att granska om från början.
let oppetDokument = null;
let rattadeFalt = new Set();
let logg = [];

function text(varde) {
  return varde === null || varde === undefined ? "" : String(varde);
}

function definitionslista(element, rader) {
  element.replaceChildren();
  for (const [etikett, varde, klass] of rader) {
    const dt = document.createElement("dt");
    dt.textContent = etikett + ":";
    const dd = document.createElement("dd");
    dd.textContent = text(varde);
    if (klass) {
      dd.className = klass;
    }
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
  const rader = document.getElementById("listrader");
  rader.replaceChildren();
  let arenden = [];
  try {
    arenden = await fetch("/api/arenden").then((r) => r.json());
  } catch (fel) {
    sattBrodsmula(["Kunde inte hämta ärendena: " + fel.message]);
    return;
  }
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

function visaDetaljer() {
  definitionslista(
    document.getElementById("detaljer"),
    DETALJFALT.map(([nyckel, etikett]) => [
      etikett,
      oppetDokument.detaljer[nyckel],
      rattadeFalt.has(nyckel) ? "rattad" : "",
    ])
  );
}

function tidpunkt() {
  const nu = new Date();
  return new Date(nu - nu.getTimezoneOffset() * 60000).toISOString().slice(0, 19);
}

function ritaLogg() {
  loggrader.replaceChildren();
  for (const rad of logg) {
    const tr = document.createElement("tr");
    for (const cell of [
      rad.tidpunkt,
      rad.regel,
      rad.etikett || rad.falt,
      (rad.fore || "(tomt)") + " → " + (rad.efter || "(tomt)"),
    ]) {
      const td = document.createElement("td");
      td.textContent = text(cell);
      tr.append(td);
    }
    loggrader.append(tr);
  }
  loggantal.textContent = "(" + logg.length + ")";
  loggpanel.hidden = logg.length === 0;
}

function laggTillLogg(rad) {
  logg.push(rad);
  ritaLogg();
}

function nollstallGranskning() {
  granskningsstatus.hidden = true;
  fyndlista.hidden = true;
  fyndlista.replaceChildren();
  spärr.hidden = true;
  rattadeFalt = new Set();
  logg = [];
  ritaLogg();
}

async function visaArende(arendenummer) {
  const svar = await fetch("/api/arenden/" + arendenummer);
  if (!svar.ok) {
    visaLista();
    return;
  }
  const arende = await svar.json();
  const dok = arende.dokument;
  oppetArende = arende.arendenummer;
  oppetDokument = dok;
  nollstallGranskning();

  visaDetaljer();
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

function beslut(fynd, li, knappar, godkand) {
  // Beslutet lever i vyn under demot. Godkänner registratorn skrivs värdet in i
  // Detaljer-panelen; testdatan på servern rörs inte (M3 — människan avgör).
  if (godkand && oppetDokument.detaljer[fynd.falt] !== undefined) {
    oppetDokument.detaljer[fynd.falt] = fynd.forslag;
    rattadeFalt.add(fynd.falt);
    visaDetaljer();
  }
  li.classList.toggle("avvisad", !godkand);
  const kvitto = document.createElement("p");
  kvitto.className = "kvitto";
  kvitto.textContent = godkand
    ? "Godkänt av Rex Ljungqvist — värdet är infört."
    : "Avvisat av Rex Ljungqvist — värdet står kvar.";
  knappar.replaceWith(kvitto);
  laggTillLogg({
    tidpunkt: tidpunkt(),
    regel: fynd.regel,
    falt: fynd.falt,
    etikett: fynd.etikett,
    fore: fynd.fore,
    efter: godkand ? fynd.forslag : fynd.fore,
  });
}

function forslagsknappar(fynd, li) {
  const knappar = document.createElement("p");
  knappar.className = "knappar";
  for (const [etikett, godkand] of [["Godkänn", true], ["Avvisa", false]]) {
    const knapp = document.createElement("button");
    knapp.type = "button";
    knapp.className = godkand ? "godkann" : "avvisa";
    knapp.textContent = etikett;
    knapp.addEventListener("click", () => beslut(fynd, li, knappar, godkand));
    knappar.append(knapp);
  }
  return knappar;
}

function fyndrad(fynd) {
  const li = document.createElement("li");
  li.className = "fynd-" + fynd.utfall.replace("ä", "a").replace("ö", "o");

  const rubrik = document.createElement("p");
  rubrik.className = "fyndrubrik";
  const markning = document.createElement("span");
  markning.className = "markning";
  markning.textContent = fynd.utfall.replace("_", " ");
  rubrik.append(markning, document.createTextNode(fynd.etikett));
  li.append(rubrik);

  const forklaring = document.createElement("p");
  forklaring.textContent = fynd.forklaring;
  li.append(forklaring);

  if (fynd.utfall === "rättad") {
    const andring = document.createElement("p");
    andring.className = "andring";
    andring.textContent = (fynd.fore || "(tomt)") + " → " + (fynd.efter || "(tomt)");
    li.append(andring);
  }

  if (fynd.utfall === "förslag" && fynd.forslag) {
    const andring = document.createElement("p");
    andring.className = "andring";
    andring.textContent = (fynd.fore || "(tomt)") + " → " + fynd.forslag + " (förslag)";
    li.append(andring, forslagsknappar(fynd, li));
  }

  const regel = document.createElement("p");
  regel.className = "regel";
  regel.textContent = "Regel: " + fynd.regel;
  li.append(regel);

  return li;
}

function visaRapport(rapport) {
  oppetDokument = rapport.arende.dokument;
  rattadeFalt = new Set(
    rapport.fynd.filter((f) => f.utfall === "rättad").map((f) => f.falt)
  );
  visaDetaljer();

  // M5: ärendet stoppas innan det går vidare, och AI:n avgör ingenting själv.
  spärr.hidden = rapport.status !== "kräver_bedömning";
  spärr.textContent =
    "Stoppat: ärendet går inte vidare till handläggning förrän flaggorna nedan " +
    "är bemötta av en människa.";

  logg = rapport.logg.slice();
  ritaLogg();

  granskningsstatus.className = "status status-" + rapport.status.replace("ä", "a").replace("ö", "o");
  granskningsstatus.textContent = STATUSTEXT[rapport.status] || rapport.status;
  granskningsstatus.hidden = false;

  fyndlista.replaceChildren(...rapport.fynd.map(fyndrad));
  fyndlista.hidden = rapport.fynd.length === 0;
}

async function granska() {
  granskaKnapp.disabled = true;
  granskaKnapp.textContent = "Granskar…";
  try {
    const svar = await fetch("/api/arenden/" + oppetArende + "/kvalitetsgranska", {
      method: "POST",
    });
    if (!svar.ok) {
      throw new Error("servern svarade " + svar.status);
    }
    visaRapport(await svar.json());
  } catch (fel) {
    granskningsstatus.className = "status status-kraver_bedomning";
    granskningsstatus.textContent = "Granskningen gick inte att köra: " + fel.message;
    granskningsstatus.hidden = false;
  } finally {
    granskaKnapp.disabled = false;
    granskaKnapp.textContent = "Kvalitetsgranska";
  }
}

function dirigera() {
  const match = location.pathname.match(/^\/arende\/(.+)$/);
  if (match) {
    visaArende(decodeURIComponent(match[1]));
  } else {
    visaLista();
  }
}

granskaKnapp.addEventListener("click", granska);

tillbaka.addEventListener("click", (e) => {
  e.preventDefault();
  history.pushState({}, "", "/");
  visaLista();
});

window.addEventListener("popstate", dirigera);
dirigera();
