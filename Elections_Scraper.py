"""
projekt_3.py: druhý projekt do Engeto Online Python Akademie - Elections Scraper
author: Václav Kryštof
email: v.krystof@seznam.cz
discord: Vašek K.#0340
"""

import sys
import requests
from bs4 import BeautifulSoup
import csv

def zapis_do_csv(final_seznam, seznam_stran):

    with open(sys.argv[2], mode="w", encoding="utf-8") as zapis_csv:
        zapisovac = csv.writer(zapis_csv, lineterminator="\n")
        zapisovac.writerow(seznam_stran)
        for k in final_seznam:                        
            zapisovac.writerow(k)
    
    print(f"Saving to the file: {sys.argv[2]}\nTerminating the Election Scraper")

def vytvor_hlavicku(seznam_linku_okrsku):
    
    url = seznam_linku_okrsku[0]
    response = requests.get(url)
    soup = BeautifulSoup(response.text, features="html.parser")
    nazvy_stran = soup.find_all("td", class_="overflow_name")                  

    seznam_stran = ["code", "location", "registered", "envelopes", "valid"]

    for a in nazvy_stran:
        seznam_stran.append(a.getText())
    
    return seznam_stran

def hlasy_kazde_strany(i, seznam_linku_okrsku):
    
    url = seznam_linku_okrsku[i]
    response = requests.get(url)
    soup = BeautifulSoup(response.text, features="html.parser")
    strana_hlasy = soup.find_all("td", headers="t1sa2 t1sb3")                  
    strana_hlasy2 = soup.find_all("td", headers="t2sa2 t2sb3")

    seznamek = []
    for a in strana_hlasy:
        if "\xa0" in a:
            d = a.replace("\xa0", "")
            seznamek.append(d.getText())
        else:
            seznamek.append(a.getText())

    for b in strana_hlasy2:
        if "\xa0" in b:
            f = b.replace("\xa0", "")
            seznamek.append(f.getText())
        else:
            seznamek.append(b.getText())
    
    seznamek_update = []
    for u in seznamek:
        if "\xa0" in u:
            u = u.replace("\xa0", "")
            seznamek_update.append(u)
        else:
            seznamek_update.append(u)

    return seznamek_update

def platne_hlasy(i, seznam_linku_okrsku):

    url = seznam_linku_okrsku[i]
    response = requests.get(url)
    soup = BeautifulSoup(response.text, features="html.parser")
    registrovany = soup.select("td", headers_="sa5")

    for g in registrovany[7]:
        if "\xa0" in g:
            g = g.replace("\xa0", "")
            return g
        else:
            return g

def odevzdane_obalky(i, seznam_linku_okrsku):
    
    url = seznam_linku_okrsku[i]
    response = requests.get(url)
    soup = BeautifulSoup(response.text, features="html.parser")
    registrovany = soup.select("td", headers_="sa5")

    for g in registrovany[6]:
        if "\xa0" in g:
            g = g.replace("\xa0", "")
            return g
        else:
            return g

def pocet_registrovanych(i, seznam_linku_okrsku):

    url = seznam_linku_okrsku[i]
    response = requests.get(url)
    soup = BeautifulSoup(response.text, features="html.parser")
    registrovany = soup.select("td", headers_="sa2")

    for f in registrovany[3]:
        if "\xa0" in f:
            op = f.replace("\xa0", "")
            return op
        else:
            return f

def nazev_obce(i):

    url = sys.argv[1]
    response = requests.get(url)
    soup = BeautifulSoup(response.text, features="html.parser")
    odkazy = soup.find_all("td", class_="overflow_name")

    a = [a.getText() for a in odkazy]
    return a[i]

def kod_obce(i, seznam_linku_okrsku):

    kody = []
    for a in seznam_linku_okrsku:
        kody.append(a[-18:-12])
    return kody[i]    

def radky(seznam_linku_okrsku):

    final_seznam = []
    for i in range(len(seznam_linku_okrsku)):
        seznam = []
        seznam.clear()
        kod = kod_obce(i, seznam_linku_okrsku)
        seznam.append(kod)
        jmeno_obce = nazev_obce(i)
        seznam.append(jmeno_obce)
        registrovani = pocet_registrovanych(i, seznam_linku_okrsku)
        seznam.append(registrovani)
        obalky = odevzdane_obalky(i, seznam_linku_okrsku)
        seznam.append(obalky)
        hlasy = platne_hlasy(i, seznam_linku_okrsku)
        seznam.append(hlasy)
        hlasy_stran = hlasy_kazde_strany(i, seznam_linku_okrsku)
        seznam.extend(hlasy_stran)                                     
        final_seznam.append(seznam)
    
    return final_seznam

def seznam_odkazu_okrsku():
    
    okresy_odkazy = requests.get(sys.argv[1])
    soup_okresy = BeautifulSoup(okresy_odkazy.text, features="html.parser")

    okresy_links = soup_okresy.select("a")
    seznam_linku_okrsku = []

    for odkaz in okresy_links:
        if odkaz.get("href") != None:
            if "ps311?xjazyk" in odkaz.get("href") and "X" not in odkaz.getText():
                seznam_linku_okrsku.append("https://www.volby.cz/pls/ps2017nss/" + odkaz.get("href"))
        else:
            continue

    return seznam_linku_okrsku

def pripojeni_url():

    try:
        url_odpoved = requests.get(sys.argv[1])
    except ConnectionError:
        print("Connection error, try later...")
    else:
        print(f"Downloading data from selected URL: {sys.argv[1]}")    

def kontrola_argv(seznam_odkazu_vsech_uzemnich_celku: list) -> None:

    if len(sys.argv) != 3 or not sys.argv[2].endswith(".csv"):
        print(f"Incorrect number of arguments. Required 3 arguments.\n1st = 'Election Scraper.py', 2nd = valid web link including https:// and www, 3rd = output csv file with .csv")
        sys.exit()
    elif sys.argv[1] not in seznam_odkazu_vsech_uzemnich_celku:
        print("Incorrect 2nd argument - web link is not correct for Election Scraping - link must include https:// and 'www' as well")
        sys.exit()
 
def seznam_odkazu_uzemnich_celku():
    
    vsechny_odkazy = requests.get("https://www.volby.cz/pls/ps2017nss/ps3?xjazyk=CZ")
    soup = BeautifulSoup(vsechny_odkazy.text, features="html.parser")

    odkazy = soup.select("a")
    seznam_odkazu_vsech_uzemnich_celku = []

    for odkaz in odkazy:
        if odkaz.get("href") != None:
            if "ps32?xjazyk" in odkaz.get("href") or "ps36?xjazyk" in odkaz.get("href"):
                seznam_odkazu_vsech_uzemnich_celku.append("https://www.volby.cz/pls/ps2017nss/" + odkaz.get("href"))
            else:
                continue
    return seznam_odkazu_vsech_uzemnich_celku

def main():
    seznam_odkazu_uzemnich_celku()
    kontrola_argv(seznam_odkazu_uzemnich_celku())
    pripojeni_url()
    seznam_odkazu_okrsku()
    final_seznam = radky(seznam_odkazu_okrsku())
    seznam_stran = vytvor_hlavicku(seznam_odkazu_okrsku())
    zapis_do_csv(final_seznam, seznam_stran)
    
if __name__ == "__main__":
    main()
