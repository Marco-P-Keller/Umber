"""The App Store listing text, one block per app language.

name and subtitle are at most 30 characters, keywords at most 100 (comma separated, no spaces),
promo at most 170. The name carries the localized "brown noise" (almost nobody bids on it outside
the US); the subtitle carries white/pink noise, fan and rain; the keyword field carries the rest.
Every word is written once across name, subtitle and keywords: Apple indexes the three together.
"""

L = {}

L["en"] = dict(
    name="Umber: Brown Noise & Sleep",
    sub="White Noise, Pink, Fan, Rain",
    kw="machine,sounds,baby,adhd,focus,tinnitus,relax,study,womb,ocean,wind,green,timer,calm,nap,lullaby",
    promo="Brown noise that never loops. Nine generated sounds, a gentle sleep timer, no ads, no accounts and nothing collected. For sleep, focus and babies.",
    hook="Umber makes brown noise, pink noise, white noise and six more calming sounds, generated live on your device, so nothing ever loops and nothing repeats. Deep, warm and smooth for sleep, focus, studying and settling a baby.",
    label="Nine sounds",
    feats=[
        "Generated live, sample by sample. No recordings, no loop point, no seam.",
        "Blend all nine sounds and set the level of each.",
        "Sleep timer that fades out slowly over the last 20 seconds.",
        "Keeps playing with the screen off. Works with Siri, Shortcuts and the Lock Screen.",
        "No ads. No accounts. No tracking. Works offline.",
    ],
)

L["de"] = dict(
    name="Umber: Braunes Rauschen",
    sub="Weißes Rauschen, Ventilator",
    kw="einschlafhilfe,baby,schlafen,adhs,konzentration,lernen,tinnitus,rosa,regen,meer,wind,timer,ruhe",
    promo="Braunes Rauschen ohne Schleife. Neun live erzeugte Klänge, sanfter Einschlaf-Timer, keine Werbung, keine Konten, keine Datenerhebung. Für Schlaf, Fokus und Babys.",
    hook="Umber erzeugt braunes, rosa und weißes Rauschen und sechs weitere ruhige Klänge, live auf deinem Gerät. Deshalb gibt es keine Schleife und keine Wiederholung. Tief, warm und gleichmäßig für Schlaf, Fokus, Lernen und Babys.",
    label="Neun Klänge",
    feats=[
        "Live erzeugt, Sample für Sample. Keine Aufnahmen, keine Schleife, keine Naht.",
        "Mische alle neun Klänge und stelle jeden einzeln ein.",
        "Einschlaf-Timer, der in den letzten 20 Sekunden sanft ausblendet.",
        "Spielt bei ausgeschaltetem Bildschirm weiter. Mit Siri, Kurzbefehlen und Sperrbildschirm.",
        "Keine Werbung. Keine Konten. Kein Tracking. Funktioniert offline.",
    ],
)

L["fr"] = dict(
    name="Umber : Bruit brun",
    sub="Bruit blanc, ventilateur",
    kw="sommeil,bébé,dormir,tdah,concentration,étude,acouphènes,rose,pluie,océan,vent,minuteur,calme,sieste",
    promo="Un bruit brun sans boucle. Neuf sons générés en direct, minuteur de sommeil en fondu, sans pub, sans compte, sans collecte. Pour dormir, se concentrer et apaiser bébé.",
    hook="Umber génère du bruit brun, rose, blanc et six autres sons apaisants, en direct sur votre appareil : rien ne boucle, rien ne se répète. Grave, chaud et régulier pour le sommeil, la concentration, les révisions et les bébés.",
    label="Neuf sons",
    feats=[
        "Généré en direct, échantillon par échantillon. Aucun enregistrement, aucune boucle.",
        "Mélangez les neuf sons et réglez le niveau de chacun.",
        "Minuteur de sommeil qui s’éteint en fondu sur les 20 dernières secondes.",
        "Continue l’écran éteint. Compatible Siri, Raccourcis et écran verrouillé.",
        "Sans publicité. Sans compte. Sans suivi. Fonctionne hors ligne.",
    ],
)

L["es"] = dict(
    name="Umber: Ruido marrón",
    sub="Ruido blanco, ventilador",
    kw="dormir,bebé,tdah,concentración,estudiar,tinnitus,rosa,lluvia,océano,viento,temporizador,siesta",
    promo="Ruido marrón sin bucles. Nueve sonidos en directo, temporizador con fundido suave, sin anuncios, sin cuentas y sin recopilar datos. Para dormir, concentrarte y bebés.",
    hook="Umber genera ruido marrón, rosa, blanco y seis sonidos relajantes más, en directo en tu dispositivo: nada se repite y no hay bucles. Grave, cálido y uniforme para dormir, concentrarte, estudiar y calmar a un bebé.",
    label="Nueve sonidos",
    feats=[
        "Generado en directo, muestra a muestra. Sin grabaciones, sin bucles, sin cortes.",
        "Mezcla los nueve sonidos y ajusta el nivel de cada uno.",
        "Temporizador que se desvanece despacio en los últimos 20 segundos.",
        "Sigue sonando con la pantalla apagada. Compatible con Siri, Atajos y pantalla de bloqueo.",
        "Sin anuncios. Sin cuentas. Sin rastreo. Funciona sin conexión.",
    ],
)

L["it"] = dict(
    name="Umber: Rumore marrone",
    sub="Rumore bianco, ventilatore",
    kw="dormire,sonno,neonato,adhd,concentrazione,studio,acufene,rosa,pioggia,oceano,vento,timer,calma",
    promo="Rumore marrone senza loop. Nove suoni dal vivo, timer del sonno con dissolvenza, senza pubblicità né account, nessun dato raccolto. Per dormire, concentrarsi e neonati.",
    hook="Umber genera rumore marrone, rosa, bianco e altri sei suoni rilassanti, dal vivo sul tuo dispositivo: niente loop e niente ripetizioni. Profondo, caldo e uniforme per dormire, concentrarti, studiare e calmare un neonato.",
    label="Nove suoni",
    feats=[
        "Generato dal vivo, campione per campione. Nessuna registrazione, nessun loop.",
        "Mixa tutti e nove i suoni e regola il livello di ciascuno.",
        "Timer del sonno che sfuma lentamente negli ultimi 20 secondi.",
        "Continua a suonare a schermo spento. Funziona con Siri, Comandi rapidi e schermata di blocco.",
        "Senza pubblicità. Senza account. Senza tracciamento. Funziona offline.",
    ],
)

L["pt-BR"] = dict(
    name="Umber: Ruído marrom",
    sub="Ruído branco, ventilador",
    kw="dormir,sono,bebê,tdah,foco,estudar,zumbido,rosa,chuva,oceano,vento,timer,calma,soneca,relaxar",
    promo="Ruído marrom sem repetição. Nove sons gerados na hora, timer de sono com fade suave, sem anúncios, sem contas e sem coleta de dados. Para dormir, focar e acalmar bebês.",
    hook="O Umber gera ruído marrom, rosa, branco e mais seis sons relaxantes, ao vivo no seu aparelho: nada se repete e não há loop. Grave, quente e uniforme para dormir, focar, estudar e acalmar um bebê.",
    label="Nove sons",
    feats=[
        "Gerado ao vivo, amostra por amostra. Sem gravações, sem loop, sem emenda.",
        "Misture os nove sons e ajuste o volume de cada um.",
        "Timer de sono que reduz o som devagar nos últimos 20 segundos.",
        "Continua tocando com a tela apagada. Funciona com Siri, Atalhos e tela de bloqueio.",
        "Sem anúncios. Sem contas. Sem rastreamento. Funciona offline.",
    ],
)

L["pt-PT"] = dict(
    name="Umber: Ruído castanho",
    sub="Ruído branco, ventoinha",
    kw="dormir,sono,bebé,hiperatividade,foco,estudar,acufenos,rosa,chuva,oceano,vento,temporizador,calma",
    promo="Ruído castanho sem repetição. Nove sons gerados na hora, temporizador com esbatimento suave, sem anúncios, sem contas e sem recolha de dados. Para dormir, focar e bebés.",
    hook="O Umber gera ruído castanho, rosa, branco e mais seis sons relaxantes, em direto no seu dispositivo: nada se repete e não há ciclos. Grave, quente e uniforme para dormir, concentrar, estudar e acalmar um bebé.",
    label="Nove sons",
    feats=[
        "Gerado em direto, amostra a amostra. Sem gravações, sem ciclos, sem cortes.",
        "Misture os nove sons e ajuste o nível de cada um.",
        "Temporizador que esbate devagar nos últimos 20 segundos.",
        "Continua a tocar com o ecrã desligado. Funciona com a Siri, Atalhos e ecrã de bloqueio.",
        "Sem anúncios. Sem contas. Sem rastreio. Funciona offline.",
    ],
)

L["nl"] = dict(
    name="Umber: Bruine ruis",
    sub="Witte ruis, ventilator, regen",
    kw="slapen,baby,slaap,adhd,focus,studeren,tinnitus,roze,oceaan,wind,timer,rust,dutje,slaapgeluiden",
    promo="Bruine ruis zonder lus. Negen live gemaakte geluiden, slaaptimer met zacht vervagen, geen advertenties, geen accounts, niets verzameld. Voor slaap, focus en baby’s.",
    hook="Umber maakt bruine, roze en witte ruis en zes andere rustgevende geluiden, live op je apparaat: niets loopt in een lus en niets herhaalt zich. Diep, warm en gelijkmatig voor slaap, focus, studeren en baby’s.",
    label="Negen geluiden",
    feats=[
        "Live gemaakt, sample voor sample. Geen opnames, geen lus, geen naad.",
        "Meng alle negen geluiden en stel elk niveau apart in.",
        "Slaaptimer die in de laatste 20 seconden zacht vervaagt.",
        "Blijft spelen met het scherm uit. Werkt met Siri, Opdrachten en het toegangsscherm.",
        "Geen advertenties. Geen accounts. Geen tracking. Werkt offline.",
    ],
)

L["sv"] = dict(
    name="Umber: Brunt brus",
    sub="Vitt brus, fläkt, regn",
    kw="sova,bebis,sömn,adhd,fokus,studera,tinnitus,rosa,hav,vind,timer,lugn,tupplur,sömnljud",
    promo="Brunt brus som aldrig loopar. Nio ljud skapade live, sovtimer med mjuk uttoning, inga annonser, inga konton och ingen datainsamling. För sömn, fokus och bebisar.",
    hook="Umber skapar brunt, rosa och vitt brus och sex ljud till, live på din enhet: inget loopar och inget upprepas. Djupt, varmt och jämnt för sömn, fokus, studier och bebisar.",
    label="Nio ljud",
    feats=[
        "Skapas live, sample för sample. Inga inspelningar, ingen loop, ingen skarv.",
        "Blanda alla nio ljud och ställ in nivån för varje.",
        "Sovtimer som tonar ut mjukt under de sista 20 sekunderna.",
        "Fortsätter spela med skärmen släckt. Fungerar med Siri, Genvägar och låsskärmen.",
        "Inga annonser. Inga konton. Ingen spårning. Fungerar offline.",
    ],
)

L["da"] = dict(
    name="Umber: Brun støj",
    sub="Hvid støj, ventilator, regn",
    kw="sove,baby,søvn,adhd,fokus,studere,tinnitus,lyserød,hav,vind,timer,ro,lur,sovelyde",
    promo="Brun støj uden gentagelser. Ni lyde skabt live, sovetimer med blød udtoning, ingen reklamer, ingen konti og ingen dataindsamling. Til søvn, fokus og babyer.",
    hook="Umber skaber brun, lyserød og hvid støj og seks lyde mere, live på din enhed: intet gentages og intet looper. Dybt, varmt og jævnt til søvn, fokus, læring og babyer.",
    label="Ni lyde",
    feats=[
        "Skabt live, sample for sample. Ingen optagelser, ingen loop, ingen samling.",
        "Bland alle ni lyde og indstil niveauet for hver.",
        "Sovetimer, der toner blidt ud i de sidste 20 sekunder.",
        "Spiller videre med slukket skærm. Virker med Siri, Genveje og låseskærmen.",
        "Ingen reklamer. Ingen konti. Ingen sporing. Virker offline.",
    ],
)

L["nb"] = dict(
    name="Umber: Brunt støy",
    sub="Hvit støy, vifte, regn",
    kw="sove,baby,søvn,adhd,fokus,studere,tinnitus,rosa,hav,vind,timer,ro,lur,søvnlyder",
    promo="Brunt støy uten løkker. Ni lyder laget live, sovetimer med myk uttoning, ingen reklame, ingen kontoer og ingen datainnsamling. For søvn, fokus og babyer.",
    hook="Umber lager brunt, rosa og hvit støy og seks lyder til, live på enheten din: ingenting looper og ingenting gjentas. Dypt, varmt og jevnt for søvn, fokus, studier og babyer.",
    label="Ni lyder",
    feats=[
        "Laget live, sample for sample. Ingen opptak, ingen løkke, ingen skjøt.",
        "Bland alle ni lydene og still inn nivået på hver.",
        "Sovetimer som toner ut mykt de siste 20 sekundene.",
        "Spiller videre med skjermen av. Fungerer med Siri, Snarveier og låseskjermen.",
        "Ingen reklame. Ingen kontoer. Ingen sporing. Fungerer offline.",
    ],
)

L["fi"] = dict(
    name="Umber: Ruskea kohina",
    sub="Valkoinen kohina, tuuletin",
    kw="uni,nukkua,vauva,adhd,keskittyminen,opiskelu,tinnitus,vaaleanpunainen,sade,meri,tuuli,ajastin",
    promo="Ruskea kohina ilman silmukkaa. Yhdeksän äänestä, uniajastin pehmeällä häivytyksellä, ei mainoksia, ei tilejä eikä tietojen keruuta. Uneen, keskittymiseen ja vauvoille.",
    hook="Umber tuottaa ruskeaa, vaaleanpunaista ja valkoista kohinaa sekä kuusi muuta rauhoittavaa ääntä reaaliajassa laitteellasi: mikään ei toistu eikä silmukoidu. Syvä, lämmin ja tasainen uneen, keskittymiseen, opiskeluun ja vauvoille.",
    label="Yhdeksän ääntä",
    feats=[
        "Syntyy reaaliajassa näyte kerrallaan. Ei äänitteitä, ei silmukkaa, ei saumaa.",
        "Sekoita kaikki yhdeksän ääntä ja säädä kunkin voimakkuus.",
        "Uniajastin, joka häivyttää äänen pehmeästi viimeisten 20 sekunnin aikana.",
        "Soi myös näyttö sammutettuna. Toimii Sirin, Pikakomentojen ja lukitusnäytön kanssa.",
        "Ei mainoksia. Ei tilejä. Ei seurantaa. Toimii ilman verkkoa.",
    ],
)

L["pl"] = dict(
    name="Umber: Brązowy szum",
    sub="Biały szum, wentylator, deszcz",
    kw="sen,spanie,niemowlę,adhd,skupienie,nauka,szumy uszne,różowy,ocean,wiatr,timer,relaks,drzemka,dźwięki",
    promo="Brązowy szum bez zapętlenia. Dziewięć dźwięków na żywo, timer snu z płynnym wyciszaniem, bez reklam, kont i zbierania danych. Do snu, skupienia i dla niemowląt.",
    hook="Umber generuje brązowy, różowy i biały szum oraz sześć innych kojących dźwięków, na żywo na Twoim urządzeniu: nic się nie zapętla i nie powtarza. Głęboki, ciepły i równy szum do snu, skupienia, nauki i uspokajania niemowląt.",
    label="Dziewięć dźwięków",
    feats=[
        "Generowany na żywo, próbka po próbce. Bez nagrań, pętli i szwów.",
        "Połącz wszystkie dziewięć dźwięków i ustaw poziom każdego.",
        "Timer snu, który płynnie wycisza dźwięk w ostatnich 20 sekundach.",
        "Gra dalej przy wyłączonym ekranie. Działa z Siri, Skrótami i ekranem blokady.",
        "Bez reklam. Bez kont. Bez śledzenia. Działa offline.",
    ],
)

L["cs"] = dict(
    name="Umber: Hnědý šum",
    sub="Bílý šum, ventilátor, déšť",
    kw="spánek,spaní,miminko,adhd,soustředění,učení,tinnitus,růžový,oceán,vítr,časovač,klid,relaxace",
    promo="Hnědý šum bez smyčky. Devět zvuků generovaných živě, časovač spánku s plynulým zeslabením, bez reklam, účtů a sběru dat. Pro spánek, soustředění a miminka.",
    hook="Umber vytváří hnědý, růžový a bílý šum a dalších šest uklidňujících zvuků, živě ve vašem zařízení: nic se neopakuje ani nezacyklí. Hluboký, teplý a vyrovnaný zvuk pro spánek, soustředění, učení a miminka.",
    label="Devět zvuků",
    feats=[
        "Generováno živě, vzorek po vzorku. Bez nahrávek, smyček a švů.",
        "Smíchejte všech devět zvuků a nastavte hlasitost každého.",
        "Časovač spánku, který plynule zeslabí zvuk v posledních 20 sekundách.",
        "Hraje dál i s vypnutou obrazovkou. Funguje se Siri, Zkratkami a zamčenou obrazovkou.",
        "Bez reklam. Bez účtů. Bez sledování. Funguje offline.",
    ],
)

L["sk"] = dict(
    name="Umber: Hnedý šum",
    sub="Biely šum, ventilátor, dážď",
    kw="spánok,spanie,bábätko,adhd,sústredenie,učenie,tinnitus,ružový,oceán,vietor,časovač,pokoj,relax",
    promo="Hnedý šum bez opakovania. Deväť zvukov generovaných naživo, časovač spánku s plynulým stíšením, bez reklám, účtov a zberu údajov. Na spánok, sústredenie a bábätká.",
    hook="Umber vytvára hnedý, ružový a biely šum a ďalších šesť upokojujúcich zvukov, naživo vo vašom zariadení: nič sa neopakuje ani nezacyklí. Hlboký, teplý a vyrovnaný zvuk na spánok, sústredenie, učenie a bábätká.",
    label="Deväť zvukov",
    feats=[
        "Generované naživo, vzorka po vzorke. Bez nahrávok, slučiek a švov.",
        "Zmiešajte všetkých deväť zvukov a nastavte hlasitosť každého.",
        "Časovač spánku, ktorý plynulo stíši zvuk v posledných 20 sekundách.",
        "Hrá ďalej aj s vypnutou obrazovkou. Funguje so Siri, Skratkami a zamknutou obrazovkou.",
        "Bez reklám. Bez účtov. Bez sledovania. Funguje offline.",
    ],
)

L["hu"] = dict(
    name="Umber: Barna zaj",
    sub="Fehér zaj, ventilátor, eső",
    kw="alvás,altató,baba,adhd,fókusz,tanulás,fülzúgás,rózsaszín,óceán,szél,időzítő,nyugalom,szundi",
    promo="Barna zaj ismétlődés nélkül. Kilenc élőben generált hang, elalvás időzítő lágy elhalkulással, hirdetések, fiókok és adatgyűjtés nélkül. Alváshoz, fókuszhoz, babáknak.",
    hook="Az Umber barna, rózsaszín és fehér zajt, valamint hat további megnyugtató hangot állít elő élőben az eszközödön: semmi sem ismétlődik, nincs hurok. Mély, meleg és egyenletes hang alváshoz, fókuszhoz, tanuláshoz és babáknak.",
    label="Kilenc hang",
    feats=[
        "Élőben, mintáról mintára generálva. Nincs felvétel, hurok vagy vágás.",
        "Keverd össze mind a kilenc hangot, és állítsd be mindegyik hangerejét.",
        "Alvásidőzítő, amely az utolsó 20 másodpercben lágyan elhalkul.",
        "Kikapcsolt kijelzővel is szól. Működik Sirivel, Parancsokkal és a zárolt képernyővel.",
        "Nincs reklám. Nincs fiók. Nincs követés. Offline is működik.",
    ],
)

L["ro"] = dict(
    name="Umber: Zgomot maro",
    sub="Zgomot alb, ventilator, ploaie",
    kw="somn,dormit,bebeluși,adhd,concentrare,învățat,tinitus,roz,ocean,vânt,temporizator,liniște",
    promo="Zgomot maro fără repetiții. Nouă sunete live, temporizator de somn cu estompare, fără reclame, conturi sau colectare de date. Pentru somn, concentrare și bebeluși.",
    hook="Umber generează zgomot maro, roz și alb, plus alte șase sunete liniștitoare, live pe dispozitivul tău: nimic nu se repetă și nu există bucle. Profund, cald și uniform pentru somn, concentrare, învățat și bebeluși.",
    label="Nouă sunete",
    feats=[
        "Generat live, eșantion cu eșantion. Fără înregistrări, fără bucle, fără tăieturi.",
        "Amestecă toate cele nouă sunete și reglează nivelul fiecăruia.",
        "Temporizator de somn care estompează încet sunetul în ultimele 20 de secunde.",
        "Continuă să cânte cu ecranul stins. Funcționează cu Siri, Comenzi rapide și ecranul de blocare.",
        "Fără reclame. Fără conturi. Fără urmărire. Funcționează offline.",
    ],
)

L["hr"] = dict(
    name="Umber: Smeđi šum",
    sub="Bijeli šum, ventilator, kiša",
    kw="spavanje,san,bebe,adhd,fokus,učenje,tinitus,ružičasti,ocean,vjetar,timer,mir,drijemanje,opuštanje",
    promo="Smeđi šum bez ponavljanja. Devet zvukova generiranih uživo, timer za spavanje s blagim stišavanjem, bez oglasa, računa i prikupljanja podataka. Za san, fokus i bebe.",
    hook="Umber stvara smeđi, ružičasti i bijeli šum te još šest umirujućih zvukova, uživo na vašem uređaju: ništa se ne ponavlja i nema petlje. Dubok, topao i ujednačen zvuk za spavanje, fokus, učenje i bebe.",
    label="Devet zvukova",
    feats=[
        "Generirano uživo, uzorak po uzorak. Bez snimaka, petlji i spojeva.",
        "Pomiješajte svih devet zvukova i podesite razinu svakog.",
        "Timer za spavanje koji lagano stišava zvuk u posljednjih 20 sekundi.",
        "Svira i s ugašenim zaslonom. Radi sa Siri, Prečacima i zaključanim zaslonom.",
        "Bez oglasa. Bez računa. Bez praćenja. Radi izvan mreže.",
    ],
)

L["ca"] = dict(
    name="Umber: Soroll marró",
    sub="Soroll blanc, ventilador",
    kw="dormir,son,nadons,tdah,concentració,estudiar,acúfens,rosa,oceà,vent,temporitzador,calma,migdiada",
    promo="Soroll marró sense bucles. Nou sons en directe, temporitzador amb esvaïment suau, sense anuncis, comptes ni recollida de dades. Per dormir, concentrar-te i nadons.",
    hook="Umber genera soroll marró, rosa i blanc i sis sons relaxants més, en directe al teu dispositiu: res no es repeteix i no hi ha bucles. Profund, càlid i uniforme per dormir, concentrar-te, estudiar i calmar un nadó.",
    label="Nou sons",
    feats=[
        "Generat en directe, mostra a mostra. Sense gravacions, bucles ni talls.",
        "Barreja els nou sons i ajusta el nivell de cadascun.",
        "Temporitzador que s’esvaeix a poc a poc en els últims 20 segons.",
        "Continua sonant amb la pantalla apagada. Funciona amb Siri, Dreceres i pantalla de bloqueig.",
        "Sense anuncis. Sense comptes. Sense rastrejar. Funciona sense connexió.",
    ],
)

L["el"] = dict(
    name="Umber: Καφέ θόρυβος",
    sub="Λευκός θόρυβος, ανεμιστήρας",
    kw="ύπνος,μωρό,ύπνο,adhd,συγκέντρωση,μελέτη,εμβοές,ροζ,βροχή,ωκεανός,άνεμος,χρονόμετρο,ηρεμία,σιέστα",
    promo="Καφέ θόρυβος χωρίς επανάληψη. Εννέα ήχοι που παράγονται ζωντανά, χρονόμετρο ύπνου με απαλό σβήσιμο, χωρίς διαφημίσεις, λογαριασμούς και συλλογή δεδομένων.",
    hook="Το Umber παράγει καφέ, ροζ και λευκό θόρυβο και έξι ακόμη χαλαρωτικούς ήχους, ζωντανά στη συσκευή σου: τίποτα δεν επαναλαμβάνεται και δεν υπάρχει loop. Βαθύς, ζεστός και ομαλός για ύπνο, συγκέντρωση, διάβασμα και μωρά.",
    label="Εννέα ήχοι",
    feats=[
        "Παράγεται ζωντανά, δείγμα προς δείγμα. Χωρίς ηχογραφήσεις, loop ή ραφές.",
        "Ανάμειξε και τους εννέα ήχους και ρύθμισε την ένταση του καθενός.",
        "Χρονόμετρο ύπνου που σβήνει σταδιακά τα τελευταία 20 δευτερόλεπτα.",
        "Συνεχίζει να παίζει με σβηστή οθόνη. Λειτουργεί με Siri, Συντομεύσεις και οθόνη κλειδώματος.",
        "Χωρίς διαφημίσεις. Χωρίς λογαριασμούς. Χωρίς παρακολούθηση. Λειτουργεί εκτός σύνδεσης.",
    ],
)

L["tr"] = dict(
    name="Umber: Kahverengi Gürültü",
    sub="Beyaz gürültü, fan, yağmur",
    kw="uyku,bebek,uyumak,dikkat,odaklanma,ders,tinnitus,pembe,okyanus,rüzgar,zamanlayıcı,sakin,şekerleme",
    promo="Döngüsüz kahverengi gürültü. Canlı üretilen dokuz ses, yumuşakça kısılan uyku zamanlayıcısı, reklamsız, hesapsız ve veri toplamadan. Uyku, odak ve bebekler için.",
    hook="Umber kahverengi, pembe ve beyaz gürültüyü ve altı sakinleştirici sesi daha cihazında canlı üretir: hiçbir şey tekrar etmez, döngü yoktur. Uyku, odaklanma, ders çalışma ve bebekler için derin, sıcak ve düzgün bir ses.",
    label="Dokuz ses",
    feats=[
        "Canlı üretilir, örnek örnek. Kayıt yok, döngü yok, ek yeri yok.",
        "Dokuz sesi karıştır ve her birinin seviyesini ayarla.",
        "Son 20 saniyede sesi yavaşça kısan uyku zamanlayıcısı.",
        "Ekran kapalıyken çalmaya devam eder. Siri, Kısayollar ve kilit ekranıyla çalışır.",
        "Reklam yok. Hesap yok. İzleme yok. Çevrimdışı çalışır.",
    ],
)

L["ru"] = dict(
    name="Umber: Коричневый шум",
    sub="Белый шум, вентилятор, дождь",
    kw="сон,малыш,засыпание,сдвг,фокус,учёба,тиннитус,розовый,океан,ветер,таймер,покой,дневной сон",
    promo="Коричневый шум без повторов. Девять звуков, создаваемых на лету, таймер сна с плавным затуханием, без рекламы, аккаунтов и сбора данных. Для сна, фокуса и малышей.",
    hook="Umber создаёт коричневый, розовый и белый шум и ещё шесть успокаивающих звуков прямо на вашем устройстве: ничего не повторяется и не зацикливается. Глубокий, тёплый и ровный звук для сна, концентрации, учёбы и малышей.",
    label="Девять звуков",
    feats=[
        "Создаётся на лету, сэмпл за сэмплом. Без записей, петель и стыков.",
        "Смешивайте все девять звуков и настраивайте громкость каждого.",
        "Таймер сна, плавно затихающий в последние 20 секунд.",
        "Играет при выключенном экране. Работает с Siri, Быстрыми командами и экраном блокировки.",
        "Без рекламы. Без аккаунтов. Без слежки. Работает офлайн.",
    ],
)

L["uk"] = dict(
    name="Umber: Коричневий шум",
    sub="Білий шум, вентилятор, дощ",
    kw="сон,немовля,засинання,сдуг,фокус,навчання,тинітус,рожевий,океан,вітер,таймер,спокій,денний сон",
    promo="Коричневий шум без повторів. Дев’ять звуків, що створюються наживо, таймер сну з плавним згасанням, без реклами, акаунтів і збору даних. Для сну, фокусу й малюків.",
    hook="Umber створює коричневий, рожевий і білий шум та ще шість заспокійливих звуків просто на вашому пристрої: нічого не повторюється й не зациклюється. Глибокий, теплий і рівний звук для сну, концентрації, навчання й малюків.",
    label="Дев’ять звуків",
    feats=[
        "Створюється наживо, семпл за семплом. Без записів, петель і стиків.",
        "Змішуйте всі дев’ять звуків і налаштовуйте гучність кожного.",
        "Таймер сну, що плавно затихає в останні 20 секунд.",
        "Грає з вимкненим екраном. Працює із Siri, Командами та екраном блокування.",
        "Без реклами. Без акаунтів. Без стеження. Працює офлайн.",
    ],
)

L["ar"] = dict(
    name="Umber: ضجيج بني",
    sub="ضجيج أبيض ومروحة ومطر",
    kw="نوم,طفل,رضيع,تركيز,دراسة,طنين,وردي,محيط,رياح,مؤقت,هدوء,قيلولة,استرخاء,أصوات",
    promo="ضجيج بني بلا تكرار. تسعة أصوات تُولَّد مباشرة، مؤقّت نوم بتلاشٍ هادئ، بلا إعلانات ولا حسابات ولا جمع للبيانات. للنوم والتركيز والأطفال.",
    hook="يولّد Umber الضجيج البني والوردي والأبيض وستة أصوات هادئة أخرى مباشرة على جهازك، فلا شيء يتكرر ولا توجد حلقة. صوت عميق ودافئ ومتّزن للنوم والتركيز والدراسة وتهدئة الأطفال.",
    label="تسعة أصوات",
    feats=[
        "يُولَّد مباشرة عيّنةً بعد عيّنة. بلا تسجيلات ولا حلقات ولا وصلات.",
        "امزج الأصوات التسعة كلها واضبط مستوى كل صوت.",
        "مؤقّت نوم يخفت ببطء في آخر 20 ثانية.",
        "يستمر بالتشغيل والشاشة مطفأة. يعمل مع Siri والاختصارات وشاشة القفل.",
        "بلا إعلانات. بلا حسابات. بلا تتبّع. يعمل دون اتصال.",
    ],
)

L["he"] = dict(
    name="Umber: רעש חום",
    sub="רעש לבן, מאוורר, גשם",
    kw="שינה,תינוק,לישון,ריכוז,לימודים,טינטון,ורוד,אוקיינוס,רוח,טיימר,שקט,תנומה,הרפיה,צלילים",
    promo="רעש חום בלי לולאות. תשעה צלילים שנוצרים בזמן אמת, טיימר שינה עם עמעום הדרגתי, בלי פרסומות, בלי חשבונות ובלי איסוף מידע. לשינה, לריכוז ולתינוקות.",
    hook="Umber יוצר רעש חום, ורוד ולבן ועוד שישה צלילים מרגיעים, בזמן אמת על המכשיר שלכם: שום דבר לא חוזר על עצמו ואין לולאה. צליל עמוק, חם ואחיד לשינה, לריכוז, ללימודים ולתינוקות.",
    label="תשעה צלילים",
    feats=[
        "נוצר בזמן אמת, דגימה אחר דגימה. בלי הקלטות, בלי לולאה, בלי תפרים.",
        "ערבבו את כל תשעת הצלילים וכוונו את עוצמת כל אחד.",
        "טיימר שינה שמתעמעם לאט ב־20 השניות האחרונות.",
        "ממשיך לנגן כשהמסך כבוי. עובד עם Siri, קיצורי דרך ומסך הנעילה.",
        "בלי פרסומות. בלי חשבונות. בלי מעקב. עובד גם ללא חיבור.",
    ],
)

L["hi"] = dict(
    name="Umber: ब्राउन नॉइज़",
    sub="व्हाइट नॉइज़, पंखा, बारिश",
    kw="नींद,बच्चा,सोना,फ़ोकस,पढ़ाई,टिनिटस,पिंक,समुद्र,हवा,टाइमर,शांति,झपकी,रिलैक्स,आवाज़",
    promo="बिना दोहराव वाला ब्राउन नॉइज़। लाइव बनने वाली नौ ध्वनियाँ, धीमे फ़ेड वाला स्लीप टाइमर, कोई विज्ञापन या अकाउंट नहीं, कोई डेटा नहीं। नींद, फ़ोकस और शिशुओं के लिए।",
    hook="Umber आपके डिवाइस पर ही ब्राउन, पिंक और व्हाइट नॉइज़ और छह और सुकून देने वाली ध्वनियाँ लाइव बनाता है: कुछ भी दोहराता नहीं, कोई लूप नहीं। नींद, फ़ोकस, पढ़ाई और शिशुओं के लिए गहरी, गर्म और समतल आवाज़।",
    label="नौ ध्वनियाँ",
    feats=[
        "लाइव बनता है, सैंपल दर सैंपल। कोई रिकॉर्डिंग, लूप या जोड़ नहीं।",
        "नौ की नौ ध्वनियाँ मिलाएँ और हर एक का स्तर तय करें।",
        "स्लीप टाइमर जो आख़िरी 20 सेकंड में धीरे-धीरे धीमा हो जाता है।",
        "स्क्रीन बंद होने पर भी चलता रहता है। Siri, शॉर्टकट और लॉक स्क्रीन के साथ काम करता है।",
        "कोई विज्ञापन नहीं। कोई अकाउंट नहीं। कोई ट्रैकिंग नहीं। ऑफ़लाइन चलता है।",
    ],
)

L["th"] = dict(
    name="Umber: เสียงรบกวนสีน้ำตาล",
    sub="ไวท์นอยส์ พัดลม ฝน",
    kw="นอนหลับ,ทารก,เด็ก,โฟกัส,อ่านหนังสือ,หูอื้อ,สีชมพู,มหาสมุทร,ลม,ตั้งเวลา,สงบ,งีบ,ผ่อนคลาย,เสียง",
    promo="เสียงรบกวนสีน้ำตาลที่ไม่วนซ้ำ เก้าเสียงที่สร้างสดๆ ตั้งเวลานอนพร้อมเสียงค่อยๆ เบาลง ไม่มีโฆษณา ไม่มีบัญชี ไม่เก็บข้อมูล สำหรับโฟกัส การนอน และเด็กทารก",
    hook="Umber สร้างเสียงรบกวนสีน้ำตาล สีชมพู สีขาว และเสียงผ่อนคลายอีกหกเสียงสดๆ บนอุปกรณ์ของคุณ ไม่มีการวนซ้ำและไม่มีเสียงซ้ำ เสียงทุ้ม อุ่น และนุ่มเรียบสำหรับการนอน การโฟกัส การอ่านหนังสือ และเด็กทารก",
    label="เก้าเสียง",
    feats=[
        "สร้างสดทีละตัวอย่างเสียง ไม่มีไฟล์บันทึก ไม่มีจุดวนซ้ำ ไม่มีรอยต่อ",
        "ผสมทั้งเก้าเสียงและปรับระดับของแต่ละเสียงได้",
        "ตั้งเวลานอนที่ค่อยๆ เบาลงใน 20 วินาทีสุดท้าย",
        "เล่นต่อแม้ปิดหน้าจอ ใช้งานได้กับ Siri, คำสั่งลัด และหน้าจอล็อก",
        "ไม่มีโฆษณา ไม่มีบัญชี ไม่มีการติดตาม ใช้งานออฟไลน์ได้",
    ],
)

L["vi"] = dict(
    name="Umber: Tiếng ồn nâu",
    sub="Tiếng ồn trắng, quạt, mưa",
    kw="giấc ngủ,em bé,ngủ,tập trung,học bài,ù tai,hồng,đại dương,gió,hẹn giờ,yên tĩnh,ngủ trưa,thư giãn",
    promo="Tiếng ồn nâu không lặp lại. Chín âm thanh tạo trực tiếp, hẹn giờ ngủ nhỏ dần, không quảng cáo, không tài khoản, không thu thập dữ liệu. Cho giấc ngủ, tập trung và em bé.",
    hook="Umber tạo tiếng ồn nâu, hồng, trắng và sáu âm thanh dịu êm khác ngay trên thiết bị của bạn: không có gì lặp lại, không có vòng lặp. Âm trầm, ấm và đều cho giấc ngủ, tập trung, học bài và em bé.",
    label="Chín âm thanh",
    feats=[
        "Tạo trực tiếp, từng mẫu một. Không bản ghi, không vòng lặp, không mối nối.",
        "Trộn cả chín âm thanh và chỉnh mức của từng âm.",
        "Hẹn giờ ngủ nhỏ dần trong 20 giây cuối.",
        "Vẫn phát khi tắt màn hình. Hoạt động với Siri, Phím tắt và màn hình khóa.",
        "Không quảng cáo. Không tài khoản. Không theo dõi. Dùng được ngoại tuyến.",
    ],
)

L["id"] = dict(
    name="Umber: Derau Cokelat",
    sub="Derau putih, kipas, hujan",
    kw="tidur,bayi,fokus,belajar,tinitus,merah muda,samudra,angin,timer,tenang,tidur siang,rileks,suara,adhd",
    promo="Derau cokelat tanpa pengulangan. Sembilan suara langsung, timer tidur dengan pemudaran halus, tanpa iklan, akun, atau pengumpulan data. Untuk tidur, fokus, dan bayi.",
    hook="Umber membuat derau cokelat, merah muda, dan putih serta enam suara menenangkan lainnya, langsung di perangkatmu: tidak ada yang berulang dan tidak ada loop. Dalam, hangat, dan halus untuk tidur, fokus, belajar, dan menenangkan bayi.",
    label="Sembilan suara",
    feats=[
        "Dibuat langsung, sampel demi sampel. Tanpa rekaman, tanpa loop, tanpa sambungan.",
        "Campur kesembilan suara dan atur level masing-masing.",
        "Timer tidur yang memudar perlahan dalam 20 detik terakhir.",
        "Tetap berbunyi saat layar mati. Bekerja dengan Siri, Pintasan, dan layar kunci.",
        "Tanpa iklan. Tanpa akun. Tanpa pelacakan. Bisa dipakai offline.",
    ],
)

L["ms"] = dict(
    name="Umber: Bunyi Coklat",
    sub="Bunyi putih, kipas, hujan",
    kw="tidur,bayi,fokus,belajar,tinitus,merah jambu,lautan,angin,pemasa,tenang,relaks,suara,adhd",
    promo="Bunyi coklat tanpa ulangan. Sembilan bunyi secara langsung, pemasa tidur dengan pudar lembut, tanpa iklan, akaun atau pengumpulan data. Untuk tidur, fokus dan bayi.",
    hook="Umber menjana bunyi coklat, merah jambu dan putih serta enam bunyi menenangkan lagi, terus pada peranti anda: tiada yang berulang dan tiada gelung. Dalam, hangat dan lembut untuk tidur, fokus, belajar dan menenangkan bayi.",
    label="Sembilan bunyi",
    feats=[
        "Dijana secara langsung, sampel demi sampel. Tiada rakaman, gelung atau sambungan.",
        "Campurkan kesemua sembilan bunyi dan laraskan tahap setiap satu.",
        "Pemasa tidur yang pudar perlahan dalam 20 saat terakhir.",
        "Terus dimainkan semasa skrin dimatikan. Berfungsi dengan Siri, Pintasan dan skrin kunci.",
        "Tiada iklan. Tiada akaun. Tiada penjejakan. Berfungsi luar talian.",
    ],
)

L["ja"] = dict(
    name="Umber: ブラウンノイズ",
    sub="ホワイトノイズ・ピンク・扇風機・雨",
    kw="睡眠,赤ちゃん,寝かしつけ,集中,勉強,耳鳴り,海,風,タイマー,昼寝,リラックス,環境音,作業用,胎内音",
    promo="ループしないブラウンノイズ。その場で生成する9つの音、ゆっくりフェードするスリープタイマー。広告なし、アカウント不要、データ収集なし。集中、睡眠、赤ちゃんのために。",
    hook="Umberは、ブラウンノイズ、ピンクノイズ、ホワイトノイズと、さらに6つの心地よい音を、お使いのデバイス上でリアルタイムに生成します。繰り返しもループもありません。深く、温かく、なめらかな音で、睡眠、集中、勉強、赤ちゃんの寝かしつけに。",
    label="9つの音",
    feats=[
        "1サンプルずつ、その場で生成。録音もループもつなぎ目もありません。",
        "9つの音を自由に重ねて、それぞれの音量を調整。",
        "最後の20秒でゆっくりフェードアウトするスリープタイマー。",
        "画面をオフにしても再生を継続。Siri、ショートカット、ロック画面に対応。",
        "広告なし。アカウント不要。トラッキングなし。オフラインで動作。",
    ],
)

L["ko"] = dict(
    name="Umber: 브라운 노이즈",
    sub="백색소음, 핑크, 선풍기, 빗소리",
    kw="수면,아기,잠,집중,공부,이명,바다,바람,타이머,낮잠,휴식,자장가,asmr,태교",
    promo="반복 없는 브라운 노이즈. 실시간으로 생성되는 아홉 가지 소리, 서서히 줄어드는 수면 타이머. 광고 없음, 계정 없음, 데이터 수집 없음. 집중, 수면, 아기를 위해.",
    hook="Umber는 브라운 노이즈, 핑크 노이즈, 화이트 노이즈와 편안한 소리 여섯 가지를 기기에서 실시간으로 만들어 냅니다. 반복도 루프도 없습니다. 깊고 따뜻하고 부드러운 소리로 수면, 집중, 공부, 아기 재우기에 좋습니다.",
    label="아홉 가지 소리",
    feats=[
        "샘플 하나하나 실시간 생성. 녹음도, 루프도, 이음새도 없습니다.",
        "아홉 가지 소리를 모두 섞고 각각의 크기를 조절하세요.",
        "마지막 20초 동안 서서히 작아지는 수면 타이머.",
        "화면이 꺼져도 계속 재생. Siri, 단축어, 잠금 화면 지원.",
        "광고 없음. 계정 없음. 추적 없음. 오프라인에서 작동.",
    ],
)

L["zh-Hans"] = dict(
    name="Umber：布朗噪声",
    sub="白噪音、粉红噪声、风扇、雨声",
    kw="睡眠,助眠,宝宝,哄睡,专注,学习,耳鸣,海浪,风声,定时,午睡,放松,催眠,胎心音",
    promo="永不循环的布朗噪声。九种实时生成的声音，缓缓淡出的睡眠定时器。无广告，无账户，不收集数据。专注、睡眠、哄睡宝宝。",
    hook="Umber 在你的设备上实时生成布朗噪声、粉红噪声、白噪声，以及另外六种舒缓的声音：没有循环，也不会重复。低沉、温暖、平滑，适合睡眠、专注、学习和哄睡宝宝。",
    label="九种声音",
    feats=[
        "逐个采样实时生成。没有录音，没有循环点，没有接缝。",
        "混合全部九种声音，并分别调节各自音量。",
        "睡眠定时器会在最后 20 秒缓缓淡出。",
        "息屏后继续播放。支持 Siri、快捷指令和锁定屏幕。",
        "无广告。无账户。无追踪。离线可用。",
    ],
)

L["zh-Hant"] = dict(
    name="Umber：布朗噪音",
    sub="白噪音、粉紅噪音、風扇、雨聲",
    kw="睡眠,助眠,寶寶,哄睡,專注,學習,耳鳴,海浪,風聲,計時,午睡,放鬆,催眠,胎心音",
    promo="永不循環的布朗噪音。九種即時生成的聲音，緩緩淡出的睡眠計時器。無廣告、無帳號、不收集資料。專注、睡眠、哄寶寶入睡。",
    hook="Umber 在你的裝置上即時生成布朗噪音、粉紅噪音、白噪音，以及另外六種舒緩的聲音：沒有循環，也不會重複。低沉、溫暖、平滑，適合睡眠、專注、學習和哄寶寶入睡。",
    label="九種聲音",
    feats=[
        "逐個取樣即時生成。沒有錄音，沒有循環點，沒有接縫。",
        "混合全部九種聲音，並分別調整各自音量。",
        "睡眠計時器會在最後 20 秒緩緩淡出。",
        "螢幕關閉後繼續播放。支援 Siri、捷徑和鎖定畫面。",
        "無廣告。無帳號。無追蹤。離線可用。",
    ],
)

# Store locales whose text differs from the language they share: (locale, overrides).
# The keyword field of a locale is indexed for its own storefront; several storefronts also index a
# second locale, so es-MX (also read for the US) and the English variants carry English extras.
VARIANTS = {
    "en-GB": dict(kw="machine,sounds,baby,adhd,focus,tinnitus,relax,revision,womb,ocean,wind,green,timer,calm,nap,lullaby"),
    "en-AU": dict(kw="machine,sounds,baby,bub,adhd,focus,tinnitus,relax,study,womb,ocean,wind,timer,calm,nap,app"),
    "en-CA": dict(kw="machine,sounds,baby,adhd,focus,tinnitus,relax,study,womb,ocean,wind,timer,calm,nap,app,newborn"),
    "es-MX": dict(
        kw="dormir,bebé,tdah,estudiar,lluvia,viento,siesta,white,noise,pink,sleep,sounds,machine,baby,focus",
    ),
    "fr-CA": dict(),
}
