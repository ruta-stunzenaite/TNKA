# 2 laboratorinis darbas — Rekomendavimo sistema: knygos arba filmai

**Dalykas:** ELESB21501, Teksto ir natūralios kalbos apdorojimas
**Trukmė:** 4 akademinės valandos (180 min. be pertraukų): du susitikimai ir savarankiškas darbas tarp jų
**Darbas:** individualus; DI pagalba leidžiama, kaip aprašyta žemiau
**Pateikimas:** vienas ZIP su kodu ir ataskaita (be duomenų ir be virtualios aplinkos), tada praktinis gynimas. Terminą skelbia dėstytojas.

## Situacija

Platforma nori prie kiekvienos knygos ar filmo rodyti „panašius“. Pasirinkite **vieną** sritį – knygas arba filmus – sukurkite turiniu pagrįstą rekomendavimo sistemą ir nuspręskite, ar jos pasiūlymai būtų naudingi skaitytojui ar žiūrovui.

Platforma nori rekomendacijų, kurios remiasi kūrinio tema, o ne vien autoriaus ar režisieriaus pavarde ar populiarumu. Veikianti programa būtina, bet nepakankama: rekomendacija turi būti pagrįsta konkrečiais pavyzdžiais, palyginimu ir klaidų analize.

## Medžiaga ir ribos

Iš Moodle atsisiųskite **Lab02_Materials.zip**. Jame yra du duomenų rinkiniai, ši užduotis ir `report-template.md`. Pradinio kodo ar gatavo sprendimo nėra. Dirbate tik su vienu rinkiniu; kurį pasirinkote, užrašykite ataskaitos pradžioje.

**Knygos – `books_gutenberg_4000.csv`.** 4 000 populiariausių anglų kalbos Project Gutenberg knygų metaduomenys (viešai prieinami): `book_id`, `title`, `author`, `author_birth_year`, `subjects` (bibliotekos temų antraštės, atskirtos ` ; `), `bookshelves` (Gutenberg lentynos ir kategorijos), `downloads` (parsisiuntimų skaičius per 30 dienų – populiarumo matas).

**Filmai – `movies_wikidata_4000.csv`.** 4 000 populiariausių filmų metaduomenys iš Wikidata (CC0): `movie_id`, `title`, `director`, `year`, `genres` (žanrai, atskirti ` ; `), `subjects` (pagrindinės temos; maždaug pusėje filmų tuščia), `countries`, `sitelinks` (kiek Vikipedijos kalbų turi straipsnį apie filmą – populiarumo matas).

Abiejuose rinkiniuose **aprašymų nėra** – kūrinį apibūdina jo temos ar žanrai, kategorijos ir pavadinimas. Dalis reikšmių trūksta (autorius, gimimo metai, režisierius, temos). Tai tikri apribojimai, kuriuos turite aptarti: kokią „panašumo“ prasmę leidžia tokie požymiai?

Rašykite savo scenarijų arba notebook'ą. Galite naudoti pandas, scikit-learn, numpy ir matplotlib, įskaitant bibliotekų `TfidfVectorizer` ir `cosine_similarity`. GPU, mokamų paslaugų ir API raktų nereikia. Žodžių ar sakinių embeddingai (spaCy, sentence-transformers) yra **neprivalomas** priedas; jei juos naudojate, tai turi būti trečiasis, kontroliuojamas paleidimas, o ne pakaitalas privalomam TF-IDF.

**Duomenų failo į pateikimą nedėkite.** Jūsų kodas turi skaityti pasirinktą failą (`books_gutenberg_4000.csv` arba `movies_wikidata_4000.csv`) iš darbinio katalogo tuo pačiu vardu – tikrintuvas paleis jį su oficialiu failu.

## Darbo planas

| Etapas | Minutės | Įrodymai |
| --- | ---: | --- |
| Apžiūrėti 15 kūrinių ir suformuluoti, ką laikysite gera rekomendacija | 20 | Pradinė analizė su 5 užklausų kūriniais |
| Duomenys, tekstinis laukas, TF-IDF ir `recommend()` | 45 | Veikianti funkcija, užrašyti parametrai |
| Populiarumo bazinis modelis ir vienas kontroliuojamas pakeitimas | 40 | Trys paleidimai tose pačiose 5 užklausose |
| Nesėkmių analizė ir rekomendacija | 45 | Trys nesėkmingos rekomendacijos, kompromisas, sprendimas |
| Pasiruošimas gynimui ir gynimas | 30 | Prognozės nematytiems kūriniams |
| **Iš viso** | **180** | |

Ilgų hiperparametrų paieškų ir ilgų ataskaitų nesitikima.

## 1. Pradinė analizė prieš modeliavimą

Pašalinkite tuščius ir pasikartojančius pavadinimus (po tarpų sutvarkymo), užrašykite kiekius. Pasirinkite **5 užklausų kūrinius** atkartojamu būdu (užrašykite metodą ir sėklą), ne vien žinomiausius. Kiekvienam iš anksto užrašykite, kokie kūriniai, jūsų nuomone, būtų geros rekomendacijos ir kodėl (autorius ar režisierius, tema, žanras, laikotarpis, šalis). Bent viena užklausa turi būti sunki: reta tema arba labai bendri žanrai ir antraštės.

## 2. Veikianti rekomendavimo sistema

1. Sukurkite tekstinį lauką: knygoms iš `subjects`, `bookshelves`, filmams iš `genres`, `subjects`; abiem atvejais galite pridėti `title` ar kitus stulpelius, jei nusprendėte. Užrašykite, kodėl.
2. Paverskite jį TF-IDF vektoriais (`TfidfVectorizer`); užrašykite tokenizavimo, stop-žodžių ir `min_df` / `max_features` sprendimus.
3. Parašykite `recommend(title, k=5)`, kuri pagal kosinusinį panašumą grąžina k panašiausių kūrinių su panašumo reikšmėmis ir **neįtraukia paties kūrinio**. Panašumą skaičiuokite užklausai prieš visus kūrinius, ne visai matricai iš karto.
4. Parašykite **populiarumo bazinį modelį**: 5 populiariausi kūriniai (`downloads` arba `sitelinks`), nepriklausomai nuo užklausos. Jis rodo, ką reiškia „rekomendacija be turinio“.
5. Suskaičiuokite, kiek kūrinių turi tuščią tekstinį lauką po jūsų paruošimo, ir pasakykite, kas su jais daroma.

## 3. Vienas kontroliuojamas pakeitimas

Pasirinkite vieną pastebėtą problemą, pavyzdžiui: ar į tekstą įtraukti pavadinimą, ar naudoti bigramas, ar pašalinti bendrines antraštes ir žanrus („Fiction“, „drama film“), ar sverti temas kitaip. Prieš bandymą užrašykite prognozę: kas turėtų pagerėti ir kas gali pablogėti.

Palyginkite pradinį ir pakeistą modelį **tose pačiose 5 užklausose**, kitus nustatymus palikę fiksuotus. Privalomas minimumas – **trys paleidimai**: bazinis populiarumo modelis, pradinis TF-IDF, pakeistas TF-IDF. Kiekvienai užklausai pateikite penkias rekomendacijas iš kiekvieno paleidimo ir pažymėkite, kurios sutampa su jūsų pradine analize. Nepatvirtinta prognozė yra tinkamas rezultatas, jei parodyta įrodymais.

## 4. Rekomendacija ir jos silpnosios vietos

- Raskite **tris konkrečias nesėkmingas rekomendacijas**: kūrinys, sistemos atsakymas, kodėl skaitytojui ar žiūrovui tai netinka, galima priežastis (pvz., bendrinės temos ar žanrai, tas pats autorius ar režisierius užgožia temą, per trumpas tekstinis laukas) ir galimas sprendimas arba paaiškinimas, kodėl klaida neišvengiama su tokiais duomenimis. Bent dviejų skirtingų tipų.
- Parodykite vieną atvejį, kur populiarumo bazinis modelis atrodo geriau už TF-IDF, arba pagrįskite, kad tokio neradote.
- Parašykite trumpą rekomendaciją platformai: kuris variantas, koks kompromisas, kam dar reikia žmogaus redaktoriaus.

Panašumo reikšmė 0,8 nėra „80 % teisinga“ – tai tik vektorių kampas. Netvirtinkite, kad sistema apibendrina kitokiems duomenims.

## 5. Praktinis gynimas

Dėstytojas duos 2–3 nematytus kūrinius iš jūsų srities (pavadinimą iš rinkinio arba naują temų ar žanrų sąrašą). Prieš paleisdami pasakykite, kokių rekomendacijų tikitės ir kur abejojate. Tada paleiskite jau pritaikytą sistemą **be permokymo** ir paaiškinkite skirtumą. Jei tekstinis laukas tuščias, pasakykite, kad įrodymų nepakanka. Gynime DI nenaudojamas; bibliotekų dokumentacija leidžiama.

## DI naudojimas ir darbo autorystė

DI pagalba leidžiama po pradinės analizės: paaiškinimams, kodui, derinimui, ataskaitos redagavimui. Nurodykite įrankius, paskirtį ir kaip tikrinote rezultatus; pateikite vieną konkretų pasiūlymą, kurį patikrinote, pataisėte arba atmetėte. Jei DI nenaudojote, taip ir parašykite. Neišgalvokite rezultatų ir nepateikite kodo, kurio nepaleidote.

## Pateikimas

Į Moodle (ir, jei nurodyta, į kurso tikrinimo svetainę) įkelkite **Lab02_Vardas_Pavarde.zip**:

1. Kodą arba notebook'ą su `recommend(title, k=5)`, paleidimo instrukcija, parametrais, sėkla ir bibliotekų versijomis.
2. Ataskaitą pagal `report-template.md` (1–2 puslapiai): pasirinktas rinkinys, pradinė analizė, trijų paleidimų palyginimas, trys nesėkmės, rekomendacija, šaltiniai ir DI deklaracija.

Į ZIP **nedėkite** duomenų failų, virtualios aplinkos ar `site-packages`.

## Vertinimas — 10 balų

| Kriterijus | Balai | Pilno įvertinimo įrodymai |
| --- | ---: | --- |
| Pradinė analizė | 2 | Kiekiai po valymo, 5 atkartojamai parinktos užklausos su lūkesčiais, viena sunki užklausa |
| Veikianti sistema | 2 | `recommend()` be paties kūrinio, populiarumo bazinis modelis, užrašyti parametrai, tuščių laukų apskaita |
| Palyginimas ir nesėkmių analizė | 4 | Prognozė prieš pakeitimą ir trys paleidimai tose pačiose užklausose (1,5); trys pagrįstos nesėkmės dviejų tipų (1,5); rekomendacija ir kompromisas (1) |
| Praktinis gynimas | 2 | Pagrįstos prognozės nematytiems kūriniams (1); savarankiškas paleidimas ir paaiškinimas (1) |
| **Iš viso** | **10** | |

Knygų ir filmų pasirinkimas vertinamas vienodai. Vien veikiantis DI sugeneruotas kodas interpretacijos ir gynimo balų neduoda. Nepatvirtinta prognozė ar sprendimas palikti pradinį modelį nėra klaida, jei pagrįsta. Šis darbas yra vienas iš keturių laboratorinių, kurių vidurkis sudaro 20 % galutinio pažymio.
