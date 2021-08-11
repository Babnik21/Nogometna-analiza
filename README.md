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
* Ali se doseženi in prejeti goli različno vplivajo na število točk?
* Ali je vpliv zmag in porazov na število točk enak? Kakšen je vpliv remijev?

Pri tem bom uporabil `.csv` datoteke, ki jih najdemo v mapi `/data`. Vsaka `.csv` datoteka vsebuje vse
tekme odigrane v izbrani sezoni, za določeno ligo. V podmapah so tudi `.csv` datoteke vsake posamezne
tekme, vendar za ta projekt niso pomembne. V vsaki tabeli so shranjeni podatki o obeh
nasprotnikih, lokaciji tekme, rezultatu, in raznih statističnih podatkih (npr. streli v okvir gola,
koti, kartoni, posest žoge...), vse za 1. polčas, 2. polčas ter skupno. Iz tega sem naredil tudi 
tabele, ki predstavljajo končno lestvico pripadajoče sezone.

`import.py` vsebuje vse funkcije, uporabljene pri uvozu podatkov. Uporabil sem knjižnico selenium,
saj je bil potreben klik določenega gumba, da sem dobil dostop do vseh tekem. Rešitve brez uporabe
te knjižnice sem se izognil, saj sem jih ocenil kot prezahtevne (tudi po pogovoru s profesorjem
in asistentom).

`tables.py` vsebuje funkcije, ki preberejo `.csv` datoteke iz mape `/data` in ustvarijo nove `.csv` 
datoteke z lestvicami in jih shrani v mapo `/tables`.

## Rezultati

Na podlagi analize podatkov sem prišel do naslednjih zaključkov:
* Zmagovalci francoske lige statistično izgledajo najbolj izrazito močnejši od svoje konkurence, vendar pa 
je razlika v primerjavi z ostalimi ligami dokaj majhna.
* Opazimo precejšno korelacijo. Nemška Bundesliga precej konsistentno izstopa v številu golov na tekmo, 
medtem ko se angleška Premier liga pogosto znajde na zadnjem mestu.
* Poleg tega, da je korelacija nasprotna, doseženi goli za malenkost bolj vplivajo na dosežene točke 
kot prejeti goli, vendar je razlika precej zanemarljiva. Korelacije so precej različne v različnih ligah.
* Ponovno, poleg tega, da je korelacija nasprotna, imajo zmage malo večji vpliv kot porazi. Remiji imajo 
rahlo negativen vpliv, vendar pa so korelacijski koeficienti od sezone do sezone zelo različni, nekje med 
-0.7 in 0.2 (v povprečju okoli -0.25)
