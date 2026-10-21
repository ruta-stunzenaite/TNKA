# 2 laboratorinis darbas — Rekomendacija platformai

Vardas, pavardė: Rūta Stunžėnaitė

Data: 2026-10-23

Python / pandas / scikit-learn versijos: Python 3.15.0 | pandas 3.0.6 | scikit-learn 1.9.1


- Duomenų rinkinys (vienas): movies_wikidata_4000.csv
- Kūrinių po valymo: 4000        Pašalinta tuščių / pasikartojančių: 0 / 0
- Tekstinis laukas (iš kokių stulpelių ir kodėl): genres + subjects. Pavadinimas ir režisierius neįtraukti, nes platforma nori panašumo pagal temą, ne pagal pavardę; subjects tuščias 49,8 % filmų, todėl pusei filmų panašumą lems tik žanrai.
- TF-IDF nustatymai (tokenizavimas, stop-žodžiai, min_df / max_features, n-gramos): lowercase=True, token_pattern=(?u)\b[a-zA-Z][a-zA-Z]+\b, ngram_range=(1, 1), min_df=2, max_features=None, sublinear_tf=False, norm=l2, stop_words=english+{film, films}
- Sėkla ir užklausų parinkimo metodas: sėkla 42, numpy default_rng; 4 užklausos atsitiktinai iš filmų, turinčių temų arba > 2 žanrų, 1 – iš filmų be temų ir su ≤ 2 žanrais (530 kandidatų)
- Tuščių tekstinių laukų po paruošimo: B – 0; C – 38 tušti, 48 nuliniai vektoriai
  (visi žodžiai už žodyno ribų). Tokiems filmams sistema nerekomenduoja nieko
  ir praneša, kad įrodymų nepakanka.

## 1. Pradinė analizė

| Užklausos kūrinys | Kokių rekomendacijų tikiuosi ir kodėl | Sunki? |
| --- | --- | --- |
| Q1 - Carlito's Way (1993) | Tikiuosi gangsterių dramų, tokių kaip Goodfellas, Casino ir The Godfather. Filmas turi daug aiškių signalų: 9 žanrus, temas organized crime ir revenge, režisierių. Gangsterių žanras duomenyse gausus, todėl atitikmenys turėtų būti tikslūs. | Ne |
| Q2 - The Intouchables (2011) | Tikiuosi šiltų komedijų-dramų, tokių kaip Green Book, Amélie, The Artist ir The Chorus. Temų nėra, o žanrų derinys biographical + comedy + drama platus, tad gali pasitaikyti ir nuotaika netinkamų europietiškų filmų (pvz., Fellini). Režisieriaus signalo nėra, nes kitų jų filmų duomenyse nėra. | Vidutiniškai |
| Q3 - The Wrong man (1956) | Tikiuosi kitų Hitchcocko filmų (Vertigo, Psycho, Strangers on a Train), film noir klasikos ir teismo dramų, tokių kaip 12 Angry Men. Žanrų rinkinys specifinis (film noir, trial film, docudrama), o Hitchcocko filmų duomenyse daugiau nei 20. Rizika ta, kad rekomendacijose dominuos vien Hitchcockas, nors šis filmas tonu artimesnis dokumentikai. | Ne |
| Q4 - Bob Marley: One Love (2024) | Tikiuosi muzikantų biografijų: Bohemian Rhapsody, Elvis, Walk the Line, Ray, taip pat King Richard, nes režisierius tas pats. Derinys biographical + musical gerai išskiria šią grupę, bet tema Bob Marley unikali ir atitikmenų neduos. Gali įsimaišyti klasikiniai miuziklai (The Sound of Music, Evita), nes jie turi tą patį musical film žanrą. | Vidutiniškai |
| Q5 - Anchorman 2: The Legend Continues (2013) | Norėčiau McKay ir Ferrello komedijų, tokių kaip Step Brothers, Talladega Nights ir The Other Guys; pirmojo Anchorman duomenyse nėra. Temų nėra, o reta ir klaidinanti žymė LGBTQ-related film (225 filmai, palyginti su 1 295 komedijomis) greičiausiai dominuos panašumo skaičiavime. Todėl tikėtinos nesusijusios rekomendacijos, pavyzdžiui, Some Like It Hot, Tootsie, Mrs. Doubtfire ar Mean Girls. | Taip |

### Trūkstamos reikšmės
- subjects tuščias 49,8 % filmų. Pusei filmų tekstinį lauką sudarys tik žanrai, o jie dažnai bendriniai („drama film“).
- director trūksta 1,6 % filmų. Tai nesvarbu, nes režisieriaus į tekstą nededame.
- genres ir countries užpildyti visiems filmams.

## 2. Kontroliuojamas pakeitimas: prognozė prieš bandymą

Kas keičiama: iš tekstinio lauko pašalinami bendriniai žanrai, kuriuos turi
daugiau nei 20 % filmų: drama film (55,6 %), action film (29,7 %),
thriller film (20,7 %), comedy film (20,3 %). Slenkstis apskaičiuotas iš
duomenų. Visi kiti nustatymai (TF-IDF parametrai, stop-žodžiai, min_df=2,
užklausos, sėkla) nekeičiami.

Kas turėtų pagerėti: filmams su specifiniais žanrais ir temomis panašumą
labiau lems tema, o ne tai, kad abu filmai yra „drama“ ar „action“.
Pvz., The Wrong Man (trial film, film noir) turėtų gauti daugiau teismo
filmų, Carlito's Way – daugiau gangsterių filmų, o ne bet kokių veiksmo
filmų. Nors TF-IDF jau sumažina dažnų žodžių svorį, jie vis tiek sudaro
didelę trumpo teksto dalį.

Kas gali pablogėti: filmams be temų ir su keliais žanrais tekstas
labai sutrumpės arba visai ištuštės. Pvz., The Intouchables liks tik
„biographical film“, Anchorman 2 – tik „LGBTQ-related film“. Tada daug
filmų turės vienodą panašumą, tvarką lems populiarumas, o viena atsitiktinė
žyma gali nulemti visas rekomendacijas. Dalis filmų gaus tuščią tekstinį
lauką, ir sistema jiems nieko nerekomenduos.

## 3. Trys paleidimai tose pačiose užklausose

| Užklausa | A · populiarumo bazinis | B · pradinis TF-IDF | C · pakeistas TF-IDF | Sutapimai su 1 dalimi (✓ / ≈ iš 5) |
| --- | --- | --- | --- | --- |
| Q1 Carlito's Way | Titanic, The Godfather ✓, Avatar, The Matrix, Gladiator | The Public Enemy ≈, The Roaring Twenties ≈, White Heat ≈, Key Largo ≈, The Godfather Part III ≈ | tie patys kaip B | A 1/0 · B 0/5 · C 0/5 |
| Q2 The Intouchables | tie patys 5 | Florence Foster Jenkins ≈, Hitchcock, Patch Adams ≈, The Pursuit of Happyness ≈, Sully | The Pursuit of Happyness ≈, Sully, The Insider, My Week with Marilyn, Frost/Nixon | A 0/0 · B 0/3 · C 0/1 |
| Q3 The Wrong Man | tie patys 5 | In Cold Blood, To Kill a Mockingbird ≈, Anatomy of a Murder ≈, The Accused ≈, The Lincoln Lawyer ≈ | In Cold Blood, The Judge ≈, To Kill a Mockingbird ≈, Anatomy of a Fall ≈, Witness for the Prosecution ≈ | A 0/0 · B 0/4 · C 0/4 |
| Q4 Bob Marley: One Love | tie patys 5 | The Great Ziegfeld, Evita, Ray ✓, The Doors ≈, Selena ≈ | tie patys kaip B | A 0/0 · B 1/2 · C 1/2 |
| Q5 Anchorman 2 (sunki) | tie patys 5 | Anger Management ≈, Jack and Jill ≈, Neighbors 2 ≈, Big Momma's House 2 ≈, Rough Night ≈ | Pain and Glory, Anger Management ≈, The Best Exotic Marigold Hotel, Youth, Suddenly, Last Summer | A 0/0 · B 0/5 · C 0/1 |

✓ – filmas įvardytas 1 dalyje; ≈ – atitinka 1 dalyje aprašytą kategoriją.

Ar prognozė pasitvirtino? Kokia nauda ir kokia kaina (bent du konkretūs kūriniai):
Iš dalies. Pagerėjimas beveik nepasireiškė: Q1 ir Q4 rekomendacijos liko
tos pačios, o Q3 C tik pakeitė vienas teismo dramas kitomis (The Judge,
Witness for the Prosecution vietoj The Accused, The Lincoln Lawyer).
Pablogėjimas pasitvirtino: The Intouchables C liko tik „biographical film“,
todėl gavo politines dramas (The Insider, Frost/Nixon); Anchorman 2 C
komedijas pakeitė nesusijusios dramos (Pain and Glory, Suddenly, Last Summer).
Kaina didesnė už naudą, todėl renkuosi B.

## 4. Trys nesėkmingos rekomendacijos

| Užklausa ir sistemos atsakymas | Kodėl skaitytojui ar žiūrovui netinka | Tikėtina priežastis | Sprendimas arba kodėl neišvengiama |
| --- | --- | --- | --- |
| 1. Anchorman 2 → C: Pain and Glory, Suddenly, Last Summer, Youth | Plataus vartotojo komedijos žiūrovas gauna autorinės ir psichologinės dramos filmus, nesusijusius nei tonu, nei tema | Pašalinus „comedy film“ liko viena netipiška Wikidata žyma; 14 filmų panašumas vienodas (1,00) | Nešalinti žanrų, jei laukas lieka trumpesnis nei 2 žodžiai (grįžti prie B); žymų kokybę turi tikrinti redaktorius |
| 2. The Intouchables → C: The Insider, Frost/Nixon (visi 1,00) | Šilta draugystės komedija-drama apie neįgalumą siūloma kartu su politiniais ir korporaciniais trileriais | Temų nėra; liko tik „biographical film“; 25 filmai turi vienodą panašumą, tvarką lemia populiarumas | Su šiais duomenimis neišvengiama: be temų ar aprašymo „draugystės“ ar „neįgalumo“ nėra iš ko atpažinti. Reikėtų aprašymų arba redaktoriaus papildytų temų |
| 3. Bob Marley: One Love → The Great Ziegfeld (1936) ir kt., visi 0,57 | 1936 m. Brodvėjaus prodiuserio biografija mažai ką sako regio ar Marley gerbėjui | Tema „Bob Marley“ yra tik šiame filme, todėl „marley“ neįtrauktas į žodyną (min_df=2); liko tik „biographical“ + „musical“, ir 5 filmai susilygino | Iš dalies neišvengiama: unikali tema negali sutapti su jokiu kitu filmu. Galima pridėti laikotarpį ar šalį arba žemesnį min_df, bet tai nepadėtų rasti kito filmo apie Marley |

Atvejis, kur bazinis modelis atrodė geriau (arba kodėl neradote):
Tokio atvejo nerasta. Populiarumo modelis visoms užklausoms rodo tuos pačius 5 filmus (Titanic, The Godfather, Avatar, The Matrix, Gladiator), kurių nė vienas nesusijęs su užklausų tema Vienintelis artimas atvejis yra Carlito's Way, kuriam A atsitiktinai pasiūlė The Godfather, bet ir B, ir C pasiūlė gangsterių filmų, įskaitant The Godfather Part III. Q2-C ir Q5-C TF-IDF iš esmės virto populiarumo modeliu siauroje kategorijoje, nes tvarką tarp vienodo panašumo filmų lemia sitelinks. Tai rodo, kad be informatyvaus teksto turinio modelis praranda pranašumą.

## 5. Rekomendacija platformai

Pasirinktas variantas ir kompromisas: 
B (pradinis TF-IDF). Filmams su temomis C beveik nieko nepagerino, o filmams be temų (49,8 %) pablogino ir sukūrė 38 tuščius laukus. Kompromisas: B kartais remiasi bendriniais žanrais, o žanrų žymos netiesiogiai atspindi režisieriaus stilių (pvz., Vertigo gauna 4 Hitchcocko filmus, nors režisieriaus tekste nėra). Siūlau rekomendacijų nerodyti, kai atpažinti mažiau nei 2 žodžiai arba visų 5 rekomendacijų panašumas vienodas, nes tada tvarką lemia populiarumas, ne turinys. Panašumo reikšmė nėra tikimybė, kad rekomendacija tinka.

Kam dar reikia žmogaus redaktoriaus: 
filmams be temų (≈ 2000), nes jų rekomendacijos remiasi tik žanrais; filmams su netipiškomis ar klaidingomis Wikidata žymomis (Anchorman 2 – „LGBTQ-related film“); filmams su unikaliomis temomis (Bob Marley, VDR), kurių sistema negali susieti; tęsiniams ir serijoms, kurias reikėtų rodyti atskirai.

## 6. DI deklaracija

Claude Opus 5.5
