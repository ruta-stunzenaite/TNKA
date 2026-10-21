# 2 laboratorinis darbas — Rekomendacija platformai

Vardas, pavardė: Rūta Stunžėnaitė
Data: 2026-10-21
Python / pandas / scikit-learn versijos: python 3.15.0, pandas 3.0.6, scikit-learn 1.9.1

Duomenų rinkinys (vienas): books_gutenberg_4000.csv
Kūrinių po valymo:  4000   Pašalinta tuščių / pasikartojančių: 0
Tekstinis laukas (iš kokių stulpelių ir kodėl): 
TF-IDF nustatymai (tokenizavimas, stop-žodžiai, min_df / max_features, n-gramos):
Sėkla ir užklausų parinkimo metodas: df.sample(5, random_state=42)
Tuščių tekstinių laukų po paruošimo:

## 1. Pradinė analizė (be DI)

| Užklausos kūrinys | Kokių rekomendacijų tikiuosi ir kodėl | Sunki? |
| --- | --- | --- |
| Q1 — *Oliver Twist* (Dickens, Charles; #730) | Great Expectations (1400), David Copperfield (766), Nicholas Nickleby (967), Bleak House (1023); then Jane Eyre (1260) - Tas pats autorius; romanai apie našlaičių brendimą; Viktorijos laikų Londonas, skurdas ir nusikalstamumas.| Ne. Tas pats autorius ir bendros temos (Našlaičiai, Londonas, brandos romanai) atitikmenis rasti lengva. |
| Q2 — *The Great Speeches and Orations of Daniel Webster With an Essay on Daniel Webster as a Master of English Style* (Webster, Daniel; #12606) |Speeches & Letters of Abraham Lincoln (14721), Give Me Liberty or Give Me Death, Patrick Henry (6), Charles Sumner: Complete Works (45473), Speeches of Benjamin Harrison (44682) - Tas pats žanras (Speeches, addresses, etc., American); XIX a. JAV politika, tas pats laikotarpis kaip Websterio. | Vidutinė. Kitų Websterio knygų nėra; gana specifinė tema. |
| Q3 — *The Bābur-nāma in English (Memoirs of Bābur)* (Babur, Emperor of Hindustan; #44608) | Tuzuk-i-Jahangiri: Memoirs of Jahangir 1 ir 2 t. (53674, 53716), The Moghul, Hoover (34322); silpnesnė: Tamburlaine the Great, Marlowe (1094) - Kito Mogolų imperatoriaus memuarai, artimiausias įmanomas atitikmuo; ta pati imperija ir laikotarpis; Timūras buvo Baburo protėvis. | Taip. Reta tema: „Mogul Empire“ turi tik 3 knygos, o autoriaus tema pasitaiko vos kartą. |
| Q4 — *Vice Versa; or, A Lesson to Fathers* (Anstey, F.; #26853) | The Pickwick Papers (580), Pendennis (9904), Letters from a Self-Made Merchant to His Son (21959) - To paties laikotarpio britų komiškas romanas; tėvo ir sūnaus tema (stebuklingas jų apsikeitimas kūnais). | Gana sunki. Yra tik viena Anstey knyga; „Humorous stories“ – bendrinis žanras; „Fathers and sons“ dažniausiai atitinka rimtus romanus, pvz., Turgenevo ir Dostojevskio. |
| Q5 — *An Investigation of the Laws of Thought On which are founded the mathematical theories of logic and probabilities* (Boole, George; #15114) | The Logic of Chance, Venn (57359), The Game of Logic, Lewis Carroll (4763), Principia Mathematica 1 t. (78050), A Budget of Paradoxes, De Morgan (26408), A System of Logic, Mill (27942) - Ta pati sritis (simbolinė logika ir tikimybės), Viktorijos laikų britų logikai, tiesioginė linija nuo Boole’io iki „Principia“. | Taip. Reta tema: kiekvieną temą turi tik 2–4 knygos; vienintelė lentyna – „Mathematics“. |

## 2. Kontroliuojamas pakeitimas: prognozė prieš bandymą

Kas keičiama:
Kas turėtų pagerėti:
Kas gali pablogėti:

## 3. Trys paleidimai tose pačiose užklausose

| Užklausa | A · populiarumo bazinis | B · pradinis TF-IDF | C · pakeistas TF-IDF | Sutapimai su 1 dalimi |
| --- | --- | --- | --- | --- |
| Q1 | | | | |
| Q2 | | | | |
| Q3 | | | | |
| Q4 | | | | |
| Q5 | | | | |

Ar prognozė pasitvirtino? Kokia nauda ir kokia kaina (bent du konkretūs kūriniai):

## 4. Trys nesėkmingos rekomendacijos

| Užklausa ir sistemos atsakymas | Kodėl skaitytojui ar žiūrovui netinka | Tikėtina priežastis | Sprendimas arba kodėl neišvengiama |
| --- | --- | --- | --- |
| 1 | | | |
| 2 | | | |
| 3 | | | |

Atvejis, kur bazinis modelis atrodė geriau (arba kodėl neradote):

## 5. Rekomendacija platformai

Pasirinktas variantas ir kompromisas:
Kam dar reikia žmogaus redaktoriaus:

## 6. Šaltiniai ir DI deklaracija

Šaltiniai:
DI įrankiai, paskirtis, tikrinimas; vienas patikrintas / pataisytas / atmestas pasiūlymas:
