"""Titelkontroll: heuristik för innehållslösa titlar, förkortningar, engelska ord
och personnamn.

Checklistans kort Titel gäller ordagrant både ärendet och ärendedokumentet: titeln
ska beskriva vad handlingen rör, får inte innehålla förkortningar som inte också är
utskrivna, ska vara på svenska (engelska får förekomma om ingen översättning finns)
och får inte innehålla personnamn.

Det är den här kontrollen som egentligen kräver språkförståelse (adr.md, Beslut 1).
I v1 är den ordlistor och mönster — och risken i det bärs av utfallet: varje träff
går till mänsklig bedömning, aldrig till automatisk rättning. En titel kan bara
skrivas om av den som vet vad handlingen rör (M5). Ordlistorna nedan är mockade,
precis som kodlistan; säg det rakt ut i demot. Checkern är inkapslad så att en
LLM-baserad titelkontroll kan ta dess plats i REGISTER utan att flödet byggs om.
"""

import re

from app.kontroller.modell import Checker, Fynd, Utfall

# Orden i titeln: bokstäver, utan siffror och skiljetecken. Ett diarienummer eller
# ett kommatecken är inget den här kontrollen har synpunkter på.
ORD = re.compile(r"[^\W\d_]+")

VOKALER = set("aeiouyåäöAEIOUYÅÄÖ")

# Mockat förkortningsregister. En förkortning är inte fel i sig — den ska bara vara
# utskriven också — så utskrivningen följer med in i förklaringen.
FORKORTNINGAR = {
    "ESV": "Ekonomistyrningsverket",
    "OSL": "offentlighets- och sekretesslagen",
    "SOU": "Statens offentliga utredningar",
    "EU": "Europeiska unionen",
    "GD": "generaldirektör",
    "HR": "personalfrågor",
    "IT": "informationsteknik",
    "PM": "promemoria",
    "VD": "verkställande direktör",
    "DNR": "diarienummer",
    "BL": "bland annat",
    "FL": "med flera",
    "KL": "klockan",
}

# Mockad ordlista över engelska ord som brukar slinka in i titlar. Ord som är
# etablerade i svenskan — test, budget, rapport — står medvetet inte här.
ENGELSKA = {
    "assessment",
    "benchmarking",
    "briefing",
    "compliance",
    "deadline",
    "feedback",
    "framework",
    "guidelines",
    "kickoff",
    "meeting",
    "onboarding",
    "outsourcing",
    "performance",
    "review",
    "roadmap",
    "screening",
    "statement",
    "workshop",
}

# Mockat namnregister — i skarp drift är det Janus kontaktregister. Ärendets
# Ansvarig person läggs till vid granskningen, den är per definition en person.
NAMNREGISTER = {
    "agnes",
    "andersson",
    "anna",
    "berglund",
    "erik",
    "johansson",
    "karlsson",
    "larsson",
    "ljungqvist",
    "nilsson",
    "olsson",
    "persson",
    "rex",
    "svensson",
}


def ord_i(titel):
    """Titelns ord, i den ordning de står."""
    return ORD.findall(titel)


def utskrivet(ord):
    """Förkortningens utskrivna form, eller None om ordet inte är en förkortning."""
    return FORKORTNINGAR.get(ord.upper())


def ar_obegripligt(ord):
    """Ser ordet ut som skräptext?

    Två mönster räcker för demot: inget svenskt ord saknar vokal, och ett ord mitt i
    en titel skrivs inte med versaler om det inte är en förkortning. Det är heuristik
    — en titel skriven helt i versaler ger falska träffar. Det är priset för att
    fånga "UUY HHT BB" utan språkmodell, och därför går träffen till mänsklig
    bedömning i stället för till en rättning.
    """
    if len(ord) < 2 or utskrivet(ord):
        return False
    return not (set(ord) & VOKALER) or ord.isupper()


def ar_namn(ord, namn):
    """Står ordet i namnregistret? Genitivformen räknas — "Svenssons yttrande" är
    lika mycket ett personnamn i titeln som "Svensson"."""
    liten = ord.lower()
    return liten in namn or (liten.endswith("s") and liten[:-1] in namn)


def _citat(ord_lista):
    return ", ".join(f'"{ord}"' for ord in ord_lista)


def _bojning(ord_lista, singular, plural):
    return singular if len(ord_lista) == 1 else plural


class TitelChecker(Checker):
    """Checklistans fyra titelregler, körda på både ärendets och dokumentets titel."""

    namn = "titel"

    def granska(self, arende):
        dokument = arende["dokument"]
        namn = NAMNREGISTER | {
            ord.lower() for ord in ord_i(dokument["detaljer"].get("ansvarig_person", ""))
        }
        return [
            *self._titel(arende.get("titel", ""), "arendetitel", "Ärendets titel", namn),
            *self._titel(dokument.get("titel", ""), "titel", "Dokumentets titel", namn),
        ]

    def _titel(self, titel, falt, etikett, namn):
        titel = titel.strip()
        if not titel:
            return [
                self._fynd(
                    "saknas",
                    falt,
                    etikett,
                    titel,
                    f"{etikett} är tom. Titeln är obligatorisk och ska beskriva vad "
                    "handlingen rör — vad den ska heta går inte att härleda ur övrig "
                    "metadata.",
                )
            ]
        orden = ord_i(titel)
        fynd = []

        obegripliga = [ord for ord in orden if ar_obegripligt(ord)]
        if obegripliga:
            fynd.append(
                self._fynd(
                    "obegriplig",
                    falt,
                    etikett,
                    titel,
                    f"{etikett} innehåller {_bojning(obegripliga, 'ordet', 'orden')} "
                    f"{_citat(obegripliga)}, som inte ser ut att betyda något. Titeln "
                    "ska beskriva vad handlingen rör. Vad den ska heta i stället går "
                    "inte att avgöra maskinellt — registrator får skriva om den.",
                )
            )

        forkortningar = [(ord, utskrivet(ord)) for ord in orden if utskrivet(ord)]
        if forkortningar:
            uppraknade = ", ".join(f'"{ord}" ({text})' for ord, text in forkortningar)
            fynd.append(
                self._fynd(
                    "förkortning",
                    falt,
                    etikett,
                    titel,
                    f"{etikett} innehåller "
                    f"{_bojning(forkortningar, 'förkortningen', 'förkortningarna')} "
                    f"{uppraknade}. En förkortning får stå i titeln bara om den också "
                    "är utskriven. Registrator får avgöra hur titeln formuleras om.",
                )
            )

        engelska = [ord for ord in orden if ord.lower() in ENGELSKA]
        if engelska:
            fynd.append(
                self._fynd(
                    "språk",
                    falt,
                    etikett,
                    titel,
                    f"{etikett} innehåller "
                    f"{_bojning(engelska, 'det engelska ordet', 'de engelska orden')} "
                    f"{_citat(engelska)}. Titeln ska vara på svenska; engelska får "
                    "förekomma om ingen översättning finns. Om det finns en vedertagen "
                    "svensk översättning är en språklig bedömning — registrator får "
                    "avgöra.",
                )
            )

        personnamn = [ord for ord in orden if ar_namn(ord, namn)]
        if personnamn:
            fynd.append(
                self._fynd(
                    "personnamn",
                    falt,
                    etikett,
                    titel,
                    f"{etikett} innehåller "
                    f"{_bojning(personnamn, 'personnamnet', 'personnamnen')} "
                    f"{_citat(personnamn)}. Personnamn får inte förekomma i titeln. "
                    "Vad som ska stå i stället beror på vad handlingen rör och avgörs "
                    "inte maskinellt.",
                )
            )
        return fynd

    def _fynd(self, sort, falt, etikett, titel, forklaring):
        """Alla titelfynd landar i mänsklig bedömning (M5) — motorn skriver aldrig en
        titel åt registratorn, den säger bara vad som skaver."""
        return Fynd(
            regel=f"{self.namn}-{sort}",
            falt=falt,
            etikett=etikett,
            utfall=Utfall.BEDOMNING,
            forklaring=forklaring,
            fore=titel,
        )
