# Elections_Scraper - 3. projekt pro Engeto

Tento projekt slouží k extrahování výsledků parlamentních voleb v roce 2017. Odkaz lze najít [zde](https://www.volby.cz/pls/ps2017nss/ps3?xjazyk=CZ).




## Instalace knihoven

Knihovny použité v tomto kódu, jsou uložené v souboru `Requirements.txt` . Pro instalaci doporučuji použít nové virtuální prostředí a spustit následovně:

```bash
pip install -r requirements.txt # nainstaluje knihovny
```



## Spuštění projektu

Spuštění projektu `Elections_Scraper.py` v rámci příkazového řádku vyžaduje 2 povinné argumenty:

```bash
python Elections_Scraper.py <odkaz-uzemniho-celku> <vysledny-soubor>
```
Následně se Vám stáhnout výsledky jako soubor s příponou `.csv`



## Ukázka projektu

Výsledky hlasování pro okres Prostějov:
```bash
Argument č. 1: https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103
Argument č. 2: vysledky_prostejov.csv
Argument č. 1 musí obsahovat "www"
```
Spuštění programu:
```bash
python "Elections_Scraper.py" "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103" "vysledky_prostejov.csv"
```
Průběh stahování:
```bash
Downloading data from selected URL: https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103
Saving to the file: vysledky_prostejov.csv
Terminating the Election Scraper
```
Je zapotřebí chvilku vyčkat - větší objem dat se může stahovat déle než 20 sec.

Částečný výstup:
```bash
code,location,registered,envelopes,valid ...
506761,Alojzov,205,145,144,29,0,0,9,0,5,17,4,1,1,0,0,18,0,5,32,0,0,6,0,0,1,1,15,0
589268,Bedihošť,834,527,524,51,0,0,28,1,13,123,2,2,14,1,0,34,0,6,140,0,0,26,0,0,0,0,82,1
```


## Otevření .csv souboru

Otevřít prázdný excel soubor -> záložka data -> načíst externí data -> z textu -> vybrat .csv soubor -> oddělovač -> typ souboru UTF-8 -> jako oddělovač je zapotřebí vybrat "čárku"
