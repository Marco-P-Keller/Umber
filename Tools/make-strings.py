#!/usr/bin/env python3
"""Generates Umber/Resources/Localizable.xcstrings from the table below and checks it.

Every language is one block of lines, in the order of KEYS. Run:  python3 Tools/make-strings.py
"""
import json, pathlib, re, sys

KEYS = """sound.brown sound.pink sound.white sound.green sound.fan sound.rain sound.ocean sound.wind sound.womb
preset.focus preset.sleep preset.storm preset.shore preset.baby
dock.idle dock.idle.hint dock.live dock.paused dock.play dock.pause
timer.title timer.stopsIn timer.cancel timer.footer common.done
settings.title settings.mix settings.mix.footer settings.privacy settings.support settings.version settings.promise
error.title error.message a11y.off intent.sound intent.play.title intent.stop.title""".split()

L = {}
L["en"] = """Brown Noise
Pink Noise
White Noise
Green Noise
Fan
Rain
Ocean
Wind
Womb
Focus
Sleep
Storm
Shore
Baby
Choose a sound
Tap a sound to begin
Generated live · never loops
Paused
Play
Pause
Sleep Timer
Stops in
Turn Off Timer
Umber fades out slowly during the last 20 seconds, then stops.
Done
Settings
Mix with Other Audio
Keep music or a podcast playing underneath Umber.
Privacy Policy
Support
Version
No ads, no accounts, no tracking. Umber works completely offline, and every sound is generated live on your device.
Can't Play Audio
Umber couldn't start the audio engine. Close other audio apps and try again.
Off
Sound
Play Sound
Stop Sound"""
L["de"] = """Braunes Rauschen
Rosa Rauschen
Weißes Rauschen
Grünes Rauschen
Ventilator
Regen
Meer
Wind
Mutterleib
Fokus
Schlaf
Gewitter
Küste
Baby
Klang wählen
Tippe auf einen Klang
Live erzeugt · ohne Wiederholung
Pausiert
Wiedergabe
Pause
Einschlaf-Timer
Endet in
Timer ausschalten
Umber blendet in den letzten 20 Sekunden langsam aus und stoppt dann.
Fertig
Einstellungen
Mit anderem Audio mischen
Lass Musik oder einen Podcast unter Umber weiterlaufen.
Datenschutz
Support
Version
Keine Werbung, keine Konten, kein Tracking. Umber funktioniert komplett offline, und jeder Klang wird live auf deinem Gerät erzeugt.
Wiedergabe nicht möglich
Umber konnte die Audio-Engine nicht starten. Beende andere Audio-Apps und versuche es erneut.
Aus
Klang
Klang abspielen
Klang stoppen"""
L["fr"] = """Bruit brun
Bruit rose
Bruit blanc
Bruit vert
Ventilateur
Pluie
Océan
Vent
Utérus
Concentration
Sommeil
Orage
Rivage
Bébé
Choisissez un son
Touchez un son pour commencer
Généré en direct · sans boucle
En pause
Lecture
Pause
Minuteur de sommeil
S’arrête dans
Désactiver le minuteur
Umber s’estompe lentement pendant les 20 dernières secondes, puis s’arrête.
Terminé
Réglages
Mélanger avec d’autres sons
Gardez de la musique ou un podcast en fond sous Umber.
Politique de confidentialité
Assistance
Version
Ni publicité, ni compte, ni suivi. Umber fonctionne entièrement hors ligne et chaque son est généré en direct sur votre appareil.
Lecture impossible
Umber n’a pas pu démarrer le moteur audio. Fermez les autres apps audio et réessayez.
Désactivé
Son
Lire un son
Arrêter le son"""
L["es"] = """Ruido marrón
Ruido rosa
Ruido blanco
Ruido verde
Ventilador
Lluvia
Océano
Viento
Útero
Concentración
Sueño
Tormenta
Orilla
Bebé
Elige un sonido
Toca un sonido para empezar
Generado en directo · sin bucles
En pausa
Reproducir
Pausa
Temporizador de sueño
Se detiene en
Desactivar temporizador
Umber se desvanece despacio durante los últimos 20 segundos y luego se detiene.
Hecho
Ajustes
Mezclar con otro audio
Mantén música o un pódcast sonando por debajo de Umber.
Política de privacidad
Soporte
Versión
Sin anuncios, sin cuentas, sin seguimiento. Umber funciona sin conexión y cada sonido se genera en directo en tu dispositivo.
No se puede reproducir
Umber no pudo iniciar el motor de audio. Cierra otras apps de audio e inténtalo de nuevo.
Desactivado
Sonido
Reproducir sonido
Detener sonido"""
L["it"] = """Rumore marrone
Rumore rosa
Rumore bianco
Rumore verde
Ventilatore
Pioggia
Oceano
Vento
Grembo
Concentrazione
Sonno
Temporale
Riva
Neonato
Scegli un suono
Tocca un suono per iniziare
Generato dal vivo · senza loop
In pausa
Riproduci
Pausa
Timer del sonno
Si ferma tra
Disattiva timer
Umber sfuma lentamente negli ultimi 20 secondi, poi si ferma.
Fine
Impostazioni
Mixa con altri audio
Lascia musica o un podcast in sottofondo sotto Umber.
Informativa sulla privacy
Assistenza
Versione
Niente pubblicità, niente account, nessun tracciamento. Umber funziona completamente offline e ogni suono viene generato dal vivo sul tuo dispositivo.
Impossibile riprodurre
Umber non è riuscito ad avviare il motore audio. Chiudi le altre app audio e riprova.
Off
Suono
Riproduci suono
Ferma suono"""
L["pt-BR"] = """Ruído marrom
Ruído rosa
Ruído branco
Ruído verde
Ventilador
Chuva
Oceano
Vento
Útero
Foco
Sono
Tempestade
Litoral
Bebê
Escolha um som
Toque em um som para começar
Gerado ao vivo · sem repetição
Em pausa
Reproduzir
Pausar
Timer de sono
Para em
Desativar timer
O Umber diminui o volume devagar nos últimos 20 segundos e depois para.
Concluído
Ajustes
Misturar com outros áudios
Deixe música ou um podcast tocando por baixo do Umber.
Política de privacidade
Suporte
Versão
Sem anúncios, sem contas, sem rastreamento. O Umber funciona totalmente offline e cada som é gerado ao vivo no seu aparelho.
Não foi possível reproduzir
O Umber não conseguiu iniciar o mecanismo de áudio. Feche outros apps de áudio e tente de novo.
Desligado
Som
Reproduzir som
Parar som"""
L["pt-PT"] = """Ruído castanho
Ruído rosa
Ruído branco
Ruído verde
Ventoinha
Chuva
Oceano
Vento
Útero
Concentração
Sono
Tempestade
Costa
Bebé
Escolha um som
Toque num som para começar
Gerado em direto · sem repetição
Em pausa
Reproduzir
Pausa
Temporizador de sono
Para em
Desativar temporizador
O Umber esbate lentamente nos últimos 20 segundos e depois para.
Concluído
Definições
Misturar com outro áudio
Deixe música ou um podcast a tocar por baixo do Umber.
Política de privacidade
Apoio
Versão
Sem anúncios, sem contas, sem rastreio. O Umber funciona totalmente offline e cada som é gerado em direto no seu dispositivo.
Não é possível reproduzir
O Umber não conseguiu iniciar o motor de áudio. Feche outras apps de áudio e tente novamente.
Desligado
Som
Reproduzir som
Parar som"""
L["nl"] = """Bruine ruis
Roze ruis
Witte ruis
Groene ruis
Ventilator
Regen
Oceaan
Wind
Baarmoeder
Focus
Slaap
Onweer
Kust
Baby
Kies een geluid
Tik op een geluid om te beginnen
Live gegenereerd · nooit een lus
Gepauzeerd
Afspelen
Pauze
Slaaptimer
Stopt over
Timer uitzetten
Umber vervaagt langzaam in de laatste 20 seconden en stopt dan.
Klaar
Instellingen
Mixen met andere audio
Laat muziek of een podcast onder Umber doorspelen.
Privacybeleid
Support
Versie
Geen advertenties, geen accounts, geen tracking. Umber werkt volledig offline en elk geluid wordt live op je apparaat gegenereerd.
Kan niet afspelen
Umber kon de audio-engine niet starten. Sluit andere audio-apps en probeer het opnieuw.
Uit
Geluid
Geluid afspelen
Geluid stoppen"""
L["sv"] = """Brunt brus
Rosa brus
Vitt brus
Grönt brus
Fläkt
Regn
Hav
Vind
Livmoder
Fokus
Sömn
Storm
Strand
Bebis
Välj ett ljud
Tryck på ett ljud för att börja
Skapas live · loopar aldrig
Pausad
Spela
Pausa
Sovtimer
Stoppar om
Stäng av timern
Umber tonar ut långsamt under de sista 20 sekunderna och stannar sedan.
Klar
Inställningar
Blanda med annat ljud
Låt musik eller en podcast spela under Umber.
Integritetspolicy
Support
Version
Inga annonser, inga konton, ingen spårning. Umber fungerar helt offline och varje ljud skapas live på din enhet.
Kan inte spela upp
Umber kunde inte starta ljudmotorn. Stäng andra ljudappar och försök igen.
Av
Ljud
Spela ljud
Stoppa ljud"""
L["da"] = """Brun støj
Lyserød støj
Hvid støj
Grøn støj
Ventilator
Regn
Hav
Vind
Livmoder
Fokus
Søvn
Storm
Kyst
Baby
Vælg en lyd
Tryk på en lyd for at starte
Skabt live · gentager aldrig
På pause
Afspil
Pause
Sovetimer
Stopper om
Slå timer fra
Umber toner langsomt ud i de sidste 20 sekunder og stopper derefter.
Færdig
Indstillinger
Bland med anden lyd
Lad musik eller en podcast spille under Umber.
Privatlivspolitik
Support
Version
Ingen reklamer, ingen konti, ingen sporing. Umber virker helt offline, og hver lyd skabes live på din enhed.
Kan ikke afspille
Umber kunne ikke starte lydmotoren. Luk andre lydapps, og prøv igen.
Fra
Lyd
Afspil lyd
Stop lyd"""
L["nb"] = """Brunt støy
Rosa støy
Hvit støy
Grønn støy
Vifte
Regn
Hav
Vind
Livmor
Fokus
Søvn
Storm
Kyst
Baby
Velg en lyd
Trykk på en lyd for å starte
Lages live · går aldri i loop
På pause
Spill av
Pause
Sovetimer
Stopper om
Slå av timeren
Umber tones sakte ut de siste 20 sekundene og stopper deretter.
Ferdig
Innstillinger
Bland med annen lyd
La musikk eller en podkast spille under Umber.
Personvern
Kundestøtte
Versjon
Ingen reklame, ingen kontoer, ingen sporing. Umber fungerer helt uten nett, og hver lyd lages live på enheten din.
Kan ikke spille av
Umber kunne ikke starte lydmotoren. Lukk andre lydapper og prøv igjen.
Av
Lyd
Spill av lyd
Stopp lyd"""
L["fi"] = """Ruskea kohina
Vaaleanpunainen kohina
Valkoinen kohina
Vihreä kohina
Tuuletin
Sade
Meri
Tuuli
Kohtu
Keskittyminen
Uni
Myrsky
Ranta
Vauva
Valitse ääni
Aloita napauttamalla ääntä
Luodaan livenä · ei koskaan silmukkaa
Tauolla
Toista
Tauko
Uniajastin
Pysähtyy ajan kuluttua
Poista ajastin käytöstä
Umber hiljenee hitaasti viimeisten 20 sekunnin aikana ja pysähtyy sitten.
Valmis
Asetukset
Yhdistä muuhun ääneen
Anna musiikin tai podcastin soida Umberin alla.
Tietosuojakäytäntö
Tuki
Versio
Ei mainoksia, ei tilejä, ei seurantaa. Umber toimii täysin offline-tilassa, ja jokainen ääni luodaan livenä laitteellasi.
Toisto ei onnistu
Umber ei voinut käynnistää äänimoottoria. Sulje muut ääniappit ja yritä uudelleen.
Pois
Ääni
Toista ääni
Pysäytä ääni"""
L["pl"] = """Szum brązowy
Szum różowy
Szum biały
Szum zielony
Wentylator
Deszcz
Ocean
Wiatr
Łono
Skupienie
Sen
Burza
Wybrzeże
Niemowlę
Wybierz dźwięk
Dotknij dźwięku, aby zacząć
Generowany na żywo · bez pętli
Wstrzymano
Odtwarzaj
Pauza
Timer snu
Zatrzyma się za
Wyłącz timer
Umber powoli wycisza się w ostatnich 20 sekundach, a potem się zatrzymuje.
Gotowe
Ustawienia
Miksuj z innym dźwiękiem
Pozwól, by muzyka lub podcast grały pod Umber.
Polityka prywatności
Pomoc
Wersja
Bez reklam, bez kont, bez śledzenia. Umber działa w pełni offline, a każdy dźwięk jest generowany na żywo na Twoim urządzeniu.
Nie można odtworzyć
Umber nie mógł uruchomić silnika audio. Zamknij inne aplikacje audio i spróbuj ponownie.
Wył.
Dźwięk
Odtwórz dźwięk
Zatrzymaj dźwięk"""
L["cs"] = """Hnědý šum
Růžový šum
Bílý šum
Zelený šum
Ventilátor
Déšť
Oceán
Vítr
Lůno
Soustředění
Spánek
Bouřka
Pobřeží
Miminko
Vyberte zvuk
Klepnutím na zvuk začnete
Generováno živě · nikdy se neopakuje
Pozastaveno
Přehrát
Pozastavit
Časovač spánku
Skončí za
Vypnout časovač
Umber v posledních 20 sekundách pomalu ztichne a pak se zastaví.
Hotovo
Nastavení
Mixovat s jiným zvukem
Nechte hrát hudbu nebo podcast pod Umberem.
Zásady ochrany soukromí
Podpora
Verze
Žádné reklamy, žádné účty, žádné sledování. Umber funguje zcela offline a každý zvuk se generuje živě ve vašem zařízení.
Nelze přehrát
Umber nemohl spustit zvukový modul. Zavřete ostatní zvukové aplikace a zkuste to znovu.
Vypnuto
Zvuk
Přehrát zvuk
Zastavit zvuk"""
L["sk"] = """Hnedý šum
Ružový šum
Biely šum
Zelený šum
Ventilátor
Dážď
Oceán
Vietor
Lono
Sústredenie
Spánok
Búrka
Pobrežie
Bábätko
Vyberte zvuk
Ťuknutím na zvuk začnete
Generované naživo · nikdy sa neopakuje
Pozastavené
Prehrať
Pozastaviť
Časovač spánku
Skončí o
Vypnúť časovač
Umber v posledných 20 sekundách pomaly stíchne a potom sa zastaví.
Hotovo
Nastavenia
Miešať s iným zvukom
Nechajte hrať hudbu alebo podcast popod Umber.
Zásady ochrany osobných údajov
Podpora
Verzia
Žiadne reklamy, žiadne účty, žiadne sledovanie. Umber funguje úplne offline a každý zvuk sa generuje naživo vo vašom zariadení.
Nedá sa prehrať
Umber nedokázal spustiť zvukový modul. Zatvorte ostatné zvukové aplikácie a skúste to znova.
Vypnuté
Zvuk
Prehrať zvuk
Zastaviť zvuk"""
L["hu"] = """Barna zaj
Rózsaszín zaj
Fehér zaj
Zöld zaj
Ventilátor
Eső
Óceán
Szél
Méh
Fókusz
Alvás
Vihar
Part
Baba
Válassz hangot
Koppints egy hangra az induláshoz
Élőben generálva · sosem ismétlődik
Szüneteltetve
Lejátszás
Szünet
Elalvás időzítő
Leáll ennyi idő múlva
Időzítő kikapcsolása
Az Umber az utolsó 20 másodpercben lassan elhalkul, majd leáll.
Kész
Beállítások
Keverés más hanggal
Hagyd, hogy zene vagy podcast szóljon az Umber alatt.
Adatvédelmi irányelvek
Támogatás
Verzió
Nincs reklám, nincs fiók, nincs követés. Az Umber teljesen offline működik, és minden hang élőben készül az eszközödön.
Nem lehet lejátszani
Az Umber nem tudta elindítani a hangmotort. Zárd be a többi hangalkalmazást, és próbáld újra.
Ki
Hang
Hang lejátszása
Hang leállítása"""
L["ro"] = """Zgomot maro
Zgomot roz
Zgomot alb
Zgomot verde
Ventilator
Ploaie
Ocean
Vânt
Uter
Concentrare
Somn
Furtună
Țărm
Bebeluș
Alege un sunet
Atinge un sunet pentru a începe
Generat live · fără repetiții
În pauză
Redă
Pauză
Temporizator de somn
Se oprește în
Dezactivează temporizatorul
Umber se estompează lent în ultimele 20 de secunde, apoi se oprește.
Gata
Setări
Amestecă cu alt audio
Lasă muzica sau un podcast să ruleze sub Umber.
Politica de confidențialitate
Asistență
Versiune
Fără reclame, fără conturi, fără urmărire. Umber funcționează complet offline, iar fiecare sunet este generat live pe dispozitivul tău.
Nu se poate reda
Umber nu a putut porni motorul audio. Închide celelalte aplicații audio și încearcă din nou.
Oprit
Sunet
Redă sunetul
Oprește sunetul"""
L["hr"] = """Smeđi šum
Ružičasti šum
Bijeli šum
Zeleni šum
Ventilator
Kiša
Ocean
Vjetar
Maternica
Fokus
San
Oluja
Obala
Beba
Odaberi zvuk
Dodirni zvuk za početak
Generirano uživo · bez ponavljanja
Pauzirano
Reproduciraj
Pauza
Timer za spavanje
Zaustavlja se za
Isključi timer
Umber se polako stišava u posljednjih 20 sekundi, a zatim staje.
Gotovo
Postavke
Miješaj s drugim zvukom
Neka glazba ili podcast sviraju ispod Umbera.
Pravila privatnosti
Podrška
Verzija
Bez oglasa, bez računa, bez praćenja. Umber radi potpuno izvan mreže, a svaki se zvuk generira uživo na tvom uređaju.
Reprodukcija nije moguća
Umber nije mogao pokrenuti audio mehanizam. Zatvori druge audio aplikacije i pokušaj ponovno.
Isklj.
Zvuk
Reproduciraj zvuk
Zaustavi zvuk"""
L["ca"] = """Soroll marró
Soroll rosa
Soroll blanc
Soroll verd
Ventilador
Pluja
Oceà
Vent
Úter
Concentració
Son
Tempesta
Platja
Nadó
Tria un so
Toca un so per començar
Generat en directe · sense bucles
En pausa
Reprodueix
Pausa
Temporitzador de son
S’atura en
Desactiva el temporitzador
Umber s’esvaeix lentament durant els últims 20 segons i després s’atura.
Fet
Ajustos
Barreja amb altre àudio
Deixa que la música o un pòdcast sonin per sota d’Umber.
Política de privadesa
Assistència
Versió
Sense anuncis, sense comptes, sense seguiment. Umber funciona totalment sense connexió i cada so es genera en directe al teu dispositiu.
No es pot reproduir
Umber no ha pogut iniciar el motor d’àudio. Tanca les altres apps d’àudio i torna-ho a provar.
Desactivat
So
Reprodueix un so
Atura el so"""
L["el"] = """Καφέ θόρυβος
Ροζ θόρυβος
Λευκός θόρυβος
Πράσινος θόρυβος
Ανεμιστήρας
Βροχή
Ωκεανός
Άνεμος
Μήτρα
Συγκέντρωση
Ύπνος
Καταιγίδα
Ακτή
Μωρό
Διάλεξε έναν ήχο
Πάτα έναν ήχο για να ξεκινήσεις
Παράγεται ζωντανά · χωρίς επανάληψη
Σε παύση
Αναπαραγωγή
Παύση
Χρονόμετρο ύπνου
Σταματά σε
Απενεργοποίηση χρονομέτρου
Το Umber σβήνει αργά τα τελευταία 20 δευτερόλεπτα και μετά σταματά.
Τέλος
Ρυθμίσεις
Ανάμειξη με άλλον ήχο
Άφησε μουσική ή podcast να παίζει κάτω από το Umber.
Πολιτική απορρήτου
Υποστήριξη
Έκδοση
Χωρίς διαφημίσεις, χωρίς λογαριασμούς, χωρίς παρακολούθηση. Το Umber λειτουργεί εντελώς εκτός σύνδεσης και κάθε ήχος παράγεται ζωντανά στη συσκευή σου.
Δεν είναι δυνατή η αναπαραγωγή
Το Umber δεν μπόρεσε να ξεκινήσει τη μηχανή ήχου. Κλείσε άλλες εφαρμογές ήχου και δοκίμασε ξανά.
Ανενεργό
Ήχος
Αναπαραγωγή ήχου
Διακοπή ήχου"""
L["tr"] = """Kahverengi gürültü
Pembe gürültü
Beyaz gürültü
Yeşil gürültü
Vantilatör
Yağmur
Okyanus
Rüzgâr
Rahim
Odak
Uyku
Fırtına
Sahil
Bebek
Bir ses seç
Başlamak için bir sese dokun
Canlı üretilir · asla tekrarlamaz
Duraklatıldı
Oynat
Duraklat
Uyku zamanlayıcısı
Durmasına
Zamanlayıcıyı kapat
Umber son 20 saniyede yavaşça kısılır ve sonra durur.
Bitti
Ayarlar
Diğer sesle karıştır
Müzik veya podcast Umber’in altında çalmaya devam etsin.
Gizlilik Politikası
Destek
Sürüm
Reklam yok, hesap yok, izleme yok. Umber tamamen çevrimdışı çalışır ve her ses cihazında canlı üretilir.
Oynatılamıyor
Umber ses motorunu başlatamadı. Diğer ses uygulamalarını kapatıp tekrar dene.
Kapalı
Ses
Sesi oynat
Sesi durdur"""
L["ru"] = """Коричневый шум
Розовый шум
Белый шум
Зелёный шум
Вентилятор
Дождь
Океан
Ветер
Утроба
Фокус
Сон
Гроза
Побережье
Малыш
Выберите звук
Нажмите на звук, чтобы начать
Создаётся в реальном времени · без повторов
На паузе
Играть
Пауза
Таймер сна
Остановится через
Выключить таймер
Umber плавно затихает в последние 20 секунд, а затем останавливается.
Готово
Настройки
Смешивать с другим аудио
Пусть музыка или подкаст играют под Umber.
Политика конфиденциальности
Поддержка
Версия
Без рекламы, без аккаунтов, без слежки. Umber работает полностью офлайн, а каждый звук создаётся прямо на вашем устройстве.
Не удаётся воспроизвести
Umber не удалось запустить аудиодвижок. Закройте другие аудиоприложения и повторите попытку.
Выкл.
Звук
Воспроизвести звук
Остановить звук"""
L["uk"] = """Коричневий шум
Рожевий шум
Білий шум
Зелений шум
Вентилятор
Дощ
Океан
Вітер
Лоно
Фокус
Сон
Гроза
Узбережжя
Малюк
Оберіть звук
Торкніться звуку, щоб почати
Створюється наживо · без повторів
На паузі
Відтворити
Пауза
Таймер сну
Зупиниться через
Вимкнути таймер
Umber повільно стихає в останні 20 секунд, а потім зупиняється.
Готово
Налаштування
Змішувати з іншим аудіо
Нехай музика чи подкаст грають під Umber.
Політика конфіденційності
Підтримка
Версія
Без реклами, без облікових записів, без стеження. Umber працює повністю офлайн, а кожен звук створюється наживо на вашому пристрої.
Не вдається відтворити
Umber не вдалося запустити аудіодвигун. Закрийте інші аудіододатки й повторіть спробу.
Вимк.
Звук
Відтворити звук
Зупинити звук"""
L["ar"] = """ضجيج بني
ضجيج وردي
ضجيج أبيض
ضجيج أخضر
مروحة
مطر
محيط
رياح
رحم
تركيز
نوم
عاصفة
شاطئ
طفل
اختر صوتًا
اضغط على صوت للبدء
يُولَّد مباشرةً · بلا تكرار
متوقف مؤقتًا
تشغيل
إيقاف مؤقت
مؤقّت النوم
يتوقف بعد
إيقاف المؤقّت
يتلاشى Umber ببطء خلال آخر 20 ثانية ثم يتوقف.
تم
الإعدادات
المزج مع صوت آخر
اترك الموسيقى أو البودكاست يعمل تحت Umber.
سياسة الخصوصية
الدعم
الإصدار
بلا إعلانات ولا حسابات ولا تتبّع. يعمل Umber دون اتصال بالكامل، ويُولَّد كل صوت مباشرةً على جهازك.
تعذّر التشغيل
تعذّر على Umber بدء محرّك الصوت. أغلق تطبيقات الصوت الأخرى وحاول مجددًا.
إيقاف
الصوت
تشغيل صوت
إيقاف الصوت"""
L["he"] = """רעש חום
רעש ורוד
רעש לבן
רעש ירוק
מאוורר
גשם
אוקיינוס
רוח
רחם
ריכוז
שינה
סערה
חוף
תינוק
בחר צליל
הקש על צליל כדי להתחיל
נוצר בזמן אמת · בלי לולאות
מושהה
הפעל
השהה
טיימר שינה
ייעצר בעוד
כבה את הטיימר
Umber מתעמעם לאט ב-20 השניות האחרונות ואז נעצר.
סיום
הגדרות
ערבב עם שמע אחר
השאר מוזיקה או פודקאסט מתנגנים מתחת ל-Umber.
מדיניות פרטיות
תמיכה
גרסה
בלי פרסומות, בלי חשבונות, בלי מעקב. Umber פועל לגמרי ללא חיבור, וכל צליל נוצר בזמן אמת במכשיר שלך.
לא ניתן להפעיל
Umber לא הצליח להפעיל את מנוע השמע. סגור אפליקציות שמע אחרות ונסה שוב.
כבוי
צליל
הפעל צליל
עצור צליל"""
L["hi"] = """ब्राउन नॉइज़
पिंक नॉइज़
व्हाइट नॉइज़
ग्रीन नॉइज़
पंखा
बारिश
समुद्र
हवा
गर्भ
फ़ोकस
नींद
तूफ़ान
समुद्रतट
शिशु
कोई ध्वनि चुनें
शुरू करने के लिए किसी ध्वनि पर टैप करें
लाइव बनाई गई · कभी दोहराई नहीं जाती
रुका हुआ
चलाएँ
रोकें
स्लीप टाइमर
रुकेगा
टाइमर बंद करें
Umber आख़िरी 20 सेकंड में धीरे-धीरे धीमा होकर रुक जाता है।
पूरा हुआ
सेटिंग्स
दूसरी ऑडियो के साथ मिलाएँ
संगीत या पॉडकास्ट को Umber के नीचे चलता रहने दें।
गोपनीयता नीति
सहायता
संस्करण
न विज्ञापन, न अकाउंट, न ट्रैकिंग। Umber पूरी तरह ऑफ़लाइन चलता है और हर ध्वनि आपके डिवाइस पर लाइव बनती है।
चला नहीं सकते
Umber ऑडियो इंजन शुरू नहीं कर सका। दूसरे ऑडियो ऐप बंद करके फिर कोशिश करें।
बंद
ध्वनि
ध्वनि चलाएँ
ध्वनि रोकें"""
L["th"] = """เสียงรบกวนสีน้ำตาล
เสียงรบกวนสีชมพู
เสียงรบกวนสีขาว
เสียงรบกวนสีเขียว
พัดลม
ฝน
มหาสมุทร
ลม
ครรภ์
โฟกัส
นอนหลับ
พายุ
ชายฝั่ง
เด็กทารก
เลือกเสียง
แตะเสียงเพื่อเริ่ม
สร้างสดแบบเรียลไทม์ · ไม่วนซ้ำ
หยุดอยู่
เล่น
หยุดชั่วคราว
ตั้งเวลานอน
จะหยุดใน
ปิดตัวตั้งเวลา
Umber จะค่อย ๆ เบาลงใน 20 วินาทีสุดท้าย แล้วหยุด
เสร็จสิ้น
การตั้งค่า
ผสมกับเสียงอื่น
ให้เพลงหรือพอดแคสต์เล่นอยู่ใต้ Umber
นโยบายความเป็นส่วนตัว
การสนับสนุน
เวอร์ชัน
ไม่มีโฆษณา ไม่มีบัญชี ไม่มีการติดตาม Umber ทำงานออฟไลน์ได้เต็มที่ และทุกเสียงถูกสร้างสดบนอุปกรณ์ของคุณ
เล่นไม่ได้
Umber เริ่มเอนจินเสียงไม่ได้ ปิดแอปเสียงอื่นแล้วลองอีกครั้ง
ปิด
เสียง
เล่นเสียง
หยุดเสียง"""
L["vi"] = """Tiếng ồn nâu
Tiếng ồn hồng
Tiếng ồn trắng
Tiếng ồn xanh lá
Quạt
Mưa
Đại dương
Gió
Tử cung
Tập trung
Giấc ngủ
Bão
Bờ biển
Em bé
Chọn một âm thanh
Chạm vào một âm thanh để bắt đầu
Tạo trực tiếp · không lặp lại
Đã tạm dừng
Phát
Tạm dừng
Hẹn giờ ngủ
Dừng sau
Tắt hẹn giờ
Umber nhỏ dần trong 20 giây cuối rồi dừng.
Xong
Cài đặt
Trộn với âm thanh khác
Để nhạc hoặc podcast phát bên dưới Umber.
Chính sách quyền riêng tư
Hỗ trợ
Phiên bản
Không quảng cáo, không tài khoản, không theo dõi. Umber hoạt động hoàn toàn ngoại tuyến và mọi âm thanh đều được tạo trực tiếp trên thiết bị của bạn.
Không thể phát
Umber không thể khởi động công cụ âm thanh. Hãy đóng các ứng dụng âm thanh khác và thử lại.
Tắt
Âm thanh
Phát âm thanh
Dừng âm thanh"""
L["id"] = """Derau cokelat
Derau merah muda
Derau putih
Derau hijau
Kipas
Hujan
Samudra
Angin
Rahim
Fokus
Tidur
Badai
Pantai
Bayi
Pilih suara
Ketuk suara untuk memulai
Dibuat langsung · tanpa pengulangan
Dijeda
Putar
Jeda
Timer tidur
Berhenti dalam
Matikan timer
Umber memudar perlahan selama 20 detik terakhir, lalu berhenti.
Selesai
Pengaturan
Campur dengan audio lain
Biarkan musik atau podcast tetap berputar di bawah Umber.
Kebijakan Privasi
Dukungan
Versi
Tanpa iklan, tanpa akun, tanpa pelacakan. Umber bekerja sepenuhnya offline, dan setiap suara dibuat langsung di perangkat Anda.
Tidak dapat memutar
Umber tidak dapat memulai mesin audio. Tutup aplikasi audio lain dan coba lagi.
Mati
Suara
Putar suara
Hentikan suara"""
L["ms"] = """Bunyi coklat
Bunyi merah jambu
Bunyi putih
Bunyi hijau
Kipas
Hujan
Lautan
Angin
Rahim
Fokus
Tidur
Ribut
Pantai
Bayi
Pilih bunyi
Ketik bunyi untuk mula
Dijana secara langsung · tanpa ulangan
Dijeda
Main
Jeda
Pemasa tidur
Berhenti dalam
Matikan pemasa
Umber pudar perlahan dalam 20 saat terakhir, kemudian berhenti.
Selesai
Tetapan
Campur dengan audio lain
Biarkan muzik atau podcast terus dimainkan di bawah Umber.
Dasar Privasi
Sokongan
Versi
Tiada iklan, tiada akaun, tiada penjejakan. Umber berfungsi sepenuhnya luar talian dan setiap bunyi dijana secara langsung pada peranti anda.
Tidak dapat dimainkan
Umber tidak dapat memulakan enjin audio. Tutup apl audio lain dan cuba lagi.
Mati
Bunyi
Main bunyi
Henti bunyi"""
L["ja"] = """ブラウンノイズ
ピンクノイズ
ホワイトノイズ
グリーンノイズ
扇風機
雨
海
風
胎内
集中
睡眠
嵐
海辺
赤ちゃん
サウンドを選択
サウンドをタップして開始
リアルタイム生成・ループなし
一時停止中
再生
一時停止
スリープタイマー
停止まで
タイマーをオフ
Umberは最後の20秒でゆっくりフェードアウトして停止します。
完了
設定
他のオーディオとミックス
音楽やPodcastをUmberの下で再生し続けます。
プライバシーポリシー
サポート
バージョン
広告なし、アカウントなし、トラッキングなし。Umberは完全オフラインで動作し、すべての音はデバイス上でリアルタイムに生成されます。
再生できません
Umberはオーディオエンジンを起動できませんでした。他のオーディオアプリを閉じて、もう一度お試しください。
オフ
サウンド
サウンドを再生
サウンドを停止"""
L["ko"] = """브라운 노이즈
핑크 노이즈
화이트 노이즈
그린 노이즈
선풍기
빗소리
바다
바람
자궁
집중
수면
폭풍
해변
아기
사운드 선택
사운드를 탭하여 시작
실시간 생성 · 반복 없음
일시 정지됨
재생
일시 정지
수면 타이머
종료까지
타이머 끄기
Umber는 마지막 20초 동안 천천히 페이드 아웃한 후 멈춥니다.
완료
설정
다른 오디오와 함께 재생
음악이나 팟캐스트를 Umber 아래에서 계속 재생합니다.
개인정보 처리방침
지원
버전
광고도, 계정도, 추적도 없습니다. Umber는 완전히 오프라인으로 작동하며 모든 소리는 기기에서 실시간으로 생성됩니다.
재생할 수 없음
Umber가 오디오 엔진을 시작하지 못했습니다. 다른 오디오 앱을 종료하고 다시 시도하세요.
끔
사운드
사운드 재생
사운드 정지"""
L["zh-Hans"] = """布朗噪声
粉红噪声
白噪声
绿噪声
风扇
雨声
海洋
风声
子宫
专注
睡眠
风暴
海岸
宝宝
选择声音
轻点声音即可开始
实时生成 · 永不循环
已暂停
播放
暂停
睡眠定时器
将在以下时间后停止
关闭定时器
Umber 会在最后 20 秒缓缓淡出，然后停止。
完成
设置
与其他音频混合
让音乐或播客在 Umber 之下继续播放。
隐私政策
支持
版本
无广告、无账户、无跟踪。Umber 完全离线运行，每一种声音都在你的设备上实时生成。
无法播放
Umber 无法启动音频引擎。请关闭其他音频 App 后重试。
关
声音
播放声音
停止声音"""
L["zh-Hant"] = """布朗噪音
粉紅噪音
白噪音
綠噪音
風扇
雨聲
海洋
風聲
子宮
專注
睡眠
暴風雨
海岸
寶寶
選擇聲音
輕點聲音即可開始
即時生成 · 永不循環
已暫停
播放
暫停
睡眠計時器
將在以下時間後停止
關閉計時器
Umber 會在最後 20 秒緩緩淡出，然後停止。
完成
設定
與其他音訊混合
讓音樂或 Podcast 在 Umber 之下繼續播放。
隱私權政策
支援
版本
沒有廣告、沒有帳號、沒有追蹤。Umber 完全離線運作，每種聲音都在你的裝置上即時生成。
無法播放
Umber 無法啟動音訊引擎。請關閉其他音訊 App 後再試一次。
關
聲音
播放聲音
停止聲音"""

ROOT = pathlib.Path(__file__).resolve().parent.parent

def problems():
    bad = []
    project = (ROOT / "project.yml").read_text()
    declared = set(re.findall(r"^\s+- ([A-Za-z-]+)$", project.split("CFBundleLocalizations:")[1].split("settings:")[0], re.M))
    if declared != set(L):
        bad.append(f"project.yml localizations differ: missing {sorted(declared - set(L))}, extra {sorted(set(L) - declared)}")
    en = L["en"].split("\n")
    for lang, block in L.items():
        lines = block.split("\n")
        if len(lines) != len(KEYS):
            bad.append(f"{lang}: {len(lines)} lines, expected {len(KEYS)}")
            continue
        for key, text in zip(KEYS, lines):
            if not text.strip():
                bad.append(f"{lang}/{key}: empty")
            if "%" in text or "{" in text:
                bad.append(f"{lang}/{key}: stray format character")
            if lang != "en" and text == en[KEYS.index(key)] and key not in ("settings.support", "preset.baby", "common.done", "a11y.off", "intent.sound", "settings.title", "settings.version") and len(text) > 5:
                bad.append(f"{lang}/{key}: identical to English")
        if "20" not in lines[KEYS.index("timer.footer")] and not any(c.isdigit() for c in lines[KEYS.index("timer.footer")]):
            bad.append(f"{lang}: timer footer lost its 20 seconds")
    return bad

def build():
    strings = {}
    for i, key in enumerate(KEYS):
        strings[key] = {"extractionState": "manual", "localizations": {
            lang: {"stringUnit": {"state": "translated", "value": block.split("\n")[i]}} for lang, block in L.items()}}
    return {"sourceLanguage": "en", "strings": strings, "version": "1.0"}

if __name__ == "__main__":
    bad = problems()
    if bad:
        print("\n".join(bad)); sys.exit(1)
    out = ROOT / "Umber" / "Resources" / "Localizable.xcstrings"
    out.write_text(json.dumps(build(), ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    print(f"{len(KEYS)} keys x {len(L)} languages -> {out.relative_to(ROOT)}")
