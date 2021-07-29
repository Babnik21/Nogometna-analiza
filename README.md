Nogometna analiza
=======================

Analiziral bom nogometne tekme "top 5" lig v zadnjih nekaj sezonah in na podlagi statistik tekem iskal 
zaključke. Rezultate in statistike tekem bom dobil na spletni strani [Flashscore](https://www.flashscore.com/).

Za vsako tekmo bom zajel:
* Končni rezultat tekem
* Lokacijo tekme (doma/v gosteh) za obe ekipi
* Datum tekme
* Statistične podatke tekme (streli, koti, kartoni...)

Delovne hipoteze:
* Ali so v različnih ligah klubi pogosteje/redkeje dominantni?
* Ali liga v kateri nastopa klub vpliva na gole na tekmo?
* Ali se doseženi in prejeti goli različno vplivajo na število zmag?

Pri tem bom uporabil csv datoteke, ki jih najdemo v mapi data. Vsaka csv datoteka vsebuje vse
tekme odigrane v izbrani sezoni, za določeno ligo. V podmapah so tudi csv datoteke vsake posamezne
tekme, vendar za ta projekt niso pomembne. V vsaki tabeli so shranjeni podatki o obeh
nasprotnikih, lokaciji tekme, rezultatu, in raznih statističnih podatkih (npr. streli v okvir gola,
koti, kartoni, posest žoge...), vse za 1. polčas, 2. polčas ter skupno. Iz tega sem naredil tudi 
tabele, ki predstavljajo končno lestvico pripadajoče sezone. Te tabele lahko najdemo v mapi tables.

import.py vsebuje vse funkcije, uporabljene pri uvozu podatkov. Uporabil sem knjižnico selenium,
saj je bil potreben klik določenega gumba, da sem dobil dostop do vseh tekem. Rešitve brez uporabe
te knjižnice sem se izognil, saj sem jih ocenil kot prezahtevne (tudi po pogovoru s profesorjem
in asistentom).
