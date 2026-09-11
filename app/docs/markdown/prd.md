# AI som kvalitetskontrollant i diariet

Uppdragsgivare: Statskontoret Fokus: Kvalitetskontroll av handlingars metadata mot en klassificeringsmodell/regelverk i diarieflödet

## Problem

Handlingar som registreras i diariet får ofta metadata (t.ex. klassificering, ärendetyp, koder) som inte stämmer överens med gällande klassificeringsmodell och regelverk. Detta upptäcks sällan direkt utan felen fortplantar sig i flödet, vilket skapar merarbete längre fram, försenar handläggningen och försämrar kvaliteten i den offentliga förvaltningen. Manuell kvalitetskontroll av metadata är idag tidskrävande, ojämn mellan handläggare och skalar dåligt. Målet är en AI-lösning som kvalitetssäkrar metadata innan handlingen går vidare, utan att bli en svart låda som fattar beslut utan insyn.

## Roller

Registrator/diarieförare – registrerar handlingen och är första kvalitetsgrind; primär användare av lösningen.
Handläggare – hanterar ärendet vidare och drabbas av fel i metadata; primär användare av lösningen.

## Måsten (3–5)

- **M1.** Granska och kvalitetssäkra metadata mot den definierade klassificeringsmodellen/regelverket.
- **M2.** Identifiera fel, avvikelser och saknad information i metadatan.
- **M3.** Föreslå eller genomföra rättningar – rätta automatiskt vid tydliga, regelbaserade fel (t.ex. formaterings- eller kodfel), föreslå rättning som en människa godkänner vid mer osäkra fall.
- **M4.** Förklara varför något har flaggats eller ändrats, på ett sätt en registrator/handläggare förstår.
- **M5.** Markera ärenden som kräver mänsklig bedömning, så AI:n aldrig avgör tveksamma fall på egen hand.

## Utanför

Sakgranskning av handlingens innehåll (juridisk/materiell korrekthet) – prototypen granskar metadata, inte handlingens sakinnehåll.
Skarp integration mot det befintliga produktionsdiariesystemet – prototypen körs mot exempeldata i ett fristående/mockat gränssnitt.

Stöd för flera klassificeringsmodeller/regelverk parallellt – prototypen utgår från ett regelverk.
Fullständig behörighets- och säkerhetslösning – inloggning, roller och säkerhet förenklas eller mockas i demot.
Separat, fullskalig granskningslogg/revisionsmodul – grundläggande spårbarhet täcks via förklaringsfunktionen (måste 4), se antaganden.

Vad ni visar klockan 18:00

En helhetsbild av flödet och processen: hur en handling kommer in i diariet, körs igenom AI-kvalitetskontrollen mot klassificeringsmodellen, flaggas och/eller rättas, får en förklaring, och antingen går vidare automatiskt eller markeras för mänsklig bedömning. Demot visas på 2–3 förberedda exempelhandlingar som tillsammans täcker: ett korrekt fall (går igenom obehindrat), ett fall med enkelt fel (rättas automatiskt) och ett osäkert/gränsfall (flaggas för mänsklig bedömning med tydlig förklaring).



Antaganden vi gjorde i stället för att fråga:

Ett regelverk/en klassificeringsmodell används i prototypen, inte flera parallella.
Exempeldata och regelverk finns tillgängliga hos teamet och används som grund för kontrollerna.
"Enkla fall" för automatisk rättning avser tydligt regelbaserade fel (t.ex. felformaterat datum/diarienummer, uppenbart felaktig kod ur en fördefinierad lista); allt som kräver tolkning går till förslag eller mänsklig bedömning.
Dokumentation av genomförda kontroller hanteras i v1 som en lättviktig del av förklaringsfunktionen (måste 4), inte som en separat, fullständig revisionsmodul.
Prototypen är fristående från produktionsdiariet under hackathonet; en separat plan tas fram för hur lösningen senare kan integreras i det befintliga flödet utan onödiga manuella moment.
Behörighet och säkerhet mockas/förenklas i demot och är inte en del av det som utvärderas.

