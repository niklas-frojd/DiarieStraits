"""Kontroller för gränsfallet: det AI:n ser men inte får avgöra själv.

Flaggorna kommer ur `docs/markdown/testfall-metadata.md`, Fall 3. Poängen är att
ingen av dem är entydigt fel — de stoppar ärendet för mänsklig bedömning eller
lämnar ett förslag (M5). Flagga 4 (Kopia till) ägs av `KopiaTill` i `falt.py`,
och flagga 6 (engelskt ord i titeln) hör till inkrement 5.

Signalorden nedan är mockade för demot, på samma sätt som kodlistan i
`app/data/klassificering.json`. De ersätts av en LLM-kontroll bakom samma
gränssnitt när Beslut 2 verkställs.
"""

from app.kontroller.modell import Checker, Fynd, Utfall

# Flagga 1: affärsuppgifter i en pågående upphandling kan omfattas av sekretess
# enligt OSL. Orden är en grov indikator, inte en rättslig prövning.
SEKRETESSORD = ("upphandling", "anbud", "prisbilaga", "kalkyl", "offert")
OPPEN_SKYDDSKOD = ("offentlig",)

# Flagga 2: checklistan säger att handlingar med olika riktning inte ska ligga i
# samma ärendedokument. En mejltråd med flera meddelanden är signalen.
TRADORD = ("tråd", "två meddelanden", "flera meddelanden")

# Statskontorets egen domän räknas som intern avsändare.
EGEN_DOMAN = "statskontoret.se"


def _text(*delar):
    return " ".join(delar).lower()


def _doman(adress):
    return adress.split("@")[-1].strip().lower()


def _extern_avsandare(registrering):
    """Sant bara för en mejladress utanför Statskontoret.

    En avsändare utan snabel-a — "Statskontoret", "Rex Ljungqvist" — säger inget
    om riktningen, så den lämnas åt klassificeringskontrollen.
    """
    avsandare = registrering.get("avsandare", "").strip()
    return "@" in avsandare and not _doman(avsandare).endswith(EGEN_DOMAN)


def _organisation(adress):
    """anna.svensson@konsultbolaget.se -> Konsultbolaget."""
    return _doman(adress).split(".")[0].capitalize()


class Sekretess(Checker):
    """Flagga 1: öppen skyddskod trots uppgifter som kan vara affärskänsliga."""

    namn = "sekretess"

    def granska(self, arende):
        dokument = arende["dokument"]
        detaljer = dokument["detaljer"]
        skyddskod = detaljer.get("skyddskod", "").strip()
        if skyddskod.lower() not in OPPEN_SKYDDSKOD:
            return []
        underlag = _text(
            arende["titel"], dokument["titel"], *(fil["titel"] for fil in dokument["filer"])
        )
        traffar = [ord for ord in SEKRETESSORD if ord in underlag]
        if len(traffar) < 2:
            return []
        return [
            Fynd(
                regel=self.namn,
                falt="skyddskod",
                etikett="Skyddskod",
                utfall=Utfall.BEDOMNING,
                forklaring=(
                    f"Skyddskod är satt till {skyddskod} och Åtkomstgrupp till "
                    f"{detaljer.get('atkomstgrupp', '')}, men handlingen rör "
                    f"{' och '.join(traffar)}. Om sekretess föreligger för "
                    "affärsförhållandena är en rättslig bedömning, inte en regeltillämpning "
                    "— registrator eller jurist får avgöra."
                ),
                fore=skyddskod,
            )
        ]


class BlandadRiktning(Checker):
    """Flagga 2: en mejltråd med både inkommande och utgående meddelanden."""

    namn = "blandad-riktning"

    def granska(self, arende):
        dokument = arende["dokument"]
        trad = [fil for fil in dokument["filer"] if any(o in fil["typ"].lower() for o in TRADORD)]
        if not trad:
            return []
        return [
            Fynd(
                regel=self.namn,
                falt="dokumentkategori",
                etikett="Dokumentkategori",
                utfall=Utfall.BEDOMNING,
                forklaring=(
                    f"Dokumentkategori är {dokument['detaljer'].get('dokumentkategori', '')}, "
                    f"men filen \"{trad[0]['titel']}\" är en mejltråd med flera meddelanden. "
                    "Handlingar med olika riktning ska inte ligga i samma ärendedokument. "
                    "Om svaret har expedierats och ska registreras som en egen utgående "
                    "handling går inte att avgöra maskinellt."
                ),
                fore=dokument["detaljer"].get("dokumentkategori", ""),
            )
        ]


class KontaktForm(Checker):
    """Flagga 3: en mejladress är ingen giltig kontakt enligt checklistan."""

    namn = "kontaktform"

    def granska(self, arende):
        registrering = arende["dokument"]["registrering"]
        avsandare = registrering.get("avsandare", "").strip()
        if "@" not in avsandare:
            return []
        organisation = _organisation(avsandare)
        return [
            Fynd(
                regel=self.namn,
                falt="avsandare",
                etikett="Avsändare",
                utfall=Utfall.FORSLAG,
                forklaring=(
                    f"Avsändare är angiven som mejladressen {avsandare}. Enligt checklistan "
                    "är varken en mejladress eller en enskild tjänsteperson en giltig kontakt. "
                    f"Rätt kontakt är sannolikt {organisation}, men kontakten måste finnas i "
                    "Janus kontaktregister — annars krävs en beställning hos registraturen."
                ),
                fore=avsandare,
                forslag=organisation,
            )
        ]


class AnkomstdatumIOrdning(Checker):
    """Flagga 5: ankomstdatum senare än dokumentdatum — dröjsmål eller felskrivet?"""

    namn = "ankomstdatum"

    def granska(self, arende):
        detaljer = arende["dokument"]["detaljer"]
        ankomst = detaljer.get("ankomstdatum", "").strip()
        dokument = detaljer.get("dokumentdatum", "").strip()
        # Datumformat har redan rättat det som gick att tolka; strängjämförelsen
        # håller för ISO-format och lämnar resten åt de kontrollerna.
        if not (ankomst and dokument) or ankomst <= dokument:
            return []
        return [
            Fynd(
                regel=self.namn,
                falt="ankomstdatum",
                etikett="Ankomstdatum",
                utfall=Utfall.BEDOMNING,
                forklaring=(
                    f"Ankomstdatum är {ankomst} medan handlingen är daterad {dokument}. "
                    "Datumet ska stämma med när handlingen faktiskt inkom, och registrering "
                    "ska ske utan dröjsmål. Om det är ett felaktigt ankomstdatum eller en "
                    "korrekt registrering efter en helg går inte att avgöra ur metadatan."
                ),
                fore=ankomst,
            )
        ]


class ExternProcess(Checker):
    """Flagga 7: intern process på en handling från en extern avsändare."""

    namn = "extern-process"

    INTERN_PROCESS = "kommunicera internt"

    def granska(self, arende):
        dokument = arende["dokument"]
        process = dokument["detaljer"].get("process", "")
        if self.INTERN_PROCESS not in process.lower():
            return []
        if not _extern_avsandare(dokument["registrering"]):
            return []
        avsandare = dokument["registrering"]["avsandare"].strip()
        return [
            Fynd(
                regel=self.namn,
                falt="process",
                etikett="Process",
                utfall=Utfall.FORSLAG,
                forklaring=(
                    f"Process är \"{process}\", men handlingen kommer från {avsandare}, "
                    "en avsändare utanför Statskontoret. Vilken processkod i "
                    "klassificeringsstrukturen som är rätt kräver kännedom om ärendets "
                    "sammanhang — registrator väljer."
                ),
                fore=process,
                forslag="Processkod för ärendets sakområde",
            )
        ]
