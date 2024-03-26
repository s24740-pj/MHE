import random
import math

# wiersze 0 - kolumny 1
wymaganiaNonogram = [[[2,1,1],[2,2],[2,1,1],[1,2,1]],[2,[1,1],[2,1],[1,1],[1,1],1,4]]

rozwiazanieNonogram =  [[0, 1, 0, 0, 1, 0, 0], [0, 0, 1, 0, 0, 1, 0], [0, 1, 0, 1, 1, 0, 1], [1, 0, 0, 1, 0, 1, 1]]

poprawne_rozwiazanieNonogram =  [[0, 1, 1, 0, 1, 0, 1], [0, 0, 1, 1, 0, 1, 1], [1, 1, 0, 0, 1, 0, 1], [1, 0, 1, 1, 0, 0, 1]]

def znajdz_grupy(linia):
    grupy = []
    licznik = 0
    for pole in linia:
        if pole == 1:
            licznik += 1
        elif licznik > 0:
            grupy.append(licznik)
            licznik = 0
    if licznik > 0:
        grupy.append(licznik)
    return grupy

def porownaj_z_wymaganiami(grupy, wymaganie):
    if isinstance(wymaganie, int):
        wymaganie = [wymaganie] #przekształcamy pojedyncze inty na listę, jezeli takowe są

    kara = 0

    #obliczamy różnicę w liczbie grup
    roznica_liczby_grup = abs(len(grupy) - len(wymaganie))
    kara += roznica_liczby_grup * 2 #przykładowo, ważymy różnicę w liczbie grup

    #porównanie kolejnych grup zaznaczeń z wymaganiami, jeśli ich liczba się zgadza
    if len(grupy) == len(wymaganie):
        for grupa, wymagana_dlugosc in zip(grupy, wymaganie):
            #kara za niezgodność długości grupy z wymaganiem
            kara += abs(grupa - wymagana_dlugosc)
    else:
        #jeśli liczba grup się nie zgadza, to dodatkowo kara za potencjalną niezgodność kolejności
        kara += len(wymaganie) * 2 #przykładowo, zakładamy dużą karę za każdą brakującą/zbyt dużą grupę

    return kara


def cel(wymagania, rozwiazanie):
    kara = 0

    #analiza wierszy
    for i, wiersz in enumerate(rozwiazanie):
        grupy = znajdz_grupy(wiersz)
        kara += porownaj_z_wymaganiami(grupy, wymagania[0][i])
    
    #analiza kolumn
    for i in range(len(rozwiazanie[0])):
        kolumna = [rozwiazanie[j][i] for j in range(len(rozwiazanie))]
        grupy = znajdz_grupy(kolumna)
        kara += porownaj_z_wymaganiami(grupy, wymagania[1][i])
        
    return kara

def bliskieSasiedztwoLosowe(rozwiazanie):
    x = random.randrange(len(rozwiazanie))
    y = random.randrange(len(rozwiazanie[0]))
    rozwiazanie[x][y] = 1 - rozwiazanie[x][y]
    return rozwiazanie

def bliskieSasiedztwo(rozwiazanie, x):
    nowe_rozwiazanie = [row[:] for row in rozwiazanie]
    kolumny = math.floor(x/len(rozwiazanie[0]))
    wiersze = x%len(rozwiazanie[0])
    nowe_rozwiazanie[kolumny][wiersze] = 1 - nowe_rozwiazanie[kolumny][wiersze]
    return nowe_rozwiazanie
def losoweRozwiazanie(wymagania):
    rozwiazanie = [[0 for _ in range(len(wymagania[1]))] for _ in range(len(wymagania[0]))]
    for x in range(len(wymagania[0])):
        for y in range(len(wymagania[1])):
            rozwiazanie[x][y] = random.randrange(0, 10) % 2
    return rozwiazanie

def zamianaBinarna(wymagania, x):
    wiersze = len(wymagania[0])
    kolumny = len(wymagania[1])
    binarny_ciag = bin(x)[2:].zfill(wiersze*kolumny)
    rozwiazanie = []
    for i in range(0, wiersze*kolumny, kolumny): #iteruje przez ciąg, biorąc bloki po ilość znaków w wierszu
        wiersz = [int(bit) for bit in binarny_ciag[i:i+kolumny]] #konwertuje blok wierszów znaków na listę intów
        rozwiazanie.append(wiersz)
    return rozwiazanie

def pelnyPrzeglad(wymagania):
    najlepszy_cel = float('inf')
    najlepsze_rozwiazanie = None
    squared = len(wymagania[0]) * len(wymagania[1])
    ilosc_mozliwosci = 2 ** squared
    for x in range(ilosc_mozliwosci):
        biezace_rozwiazanie = zamianaBinarna(wymaganiaNonogram, x)
        ocena_biezacego_rozwiazania = cel(wymagania, biezace_rozwiazanie)
        
        if x % 500000 == 0:
            print(x, "/", ilosc_mozliwosci)
        if ocena_biezacego_rozwiazania < najlepszy_cel:
            najlepszy_cel = ocena_biezacego_rozwiazania
            najlepsze_rozwiazanie = biezace_rozwiazanie
            
        if najlepszy_cel == 0:
            print(x, "/", ilosc_mozliwosci, " Ocena: ", najlepszy_cel, " Rozwiazanie: ", najlepsze_rozwiazanie)
            break
    return najlepsze_rozwiazanie

def wspinaczkowyKlasyczny(wymagania, rozwiazanie):
    najlepszy_wynik = cel(wymagania, rozwiazanie)
    rozwiazanie_najlepsze = rozwiazanie

    while True:
        poprawa = False
        for x in range(len(rozwiazanie[0])*len(rozwiazanie)):
            nowe_rozwiazanie = bliskieSasiedztwo(rozwiazanie_najlepsze, x)
            wynik = cel(wymagania, nowe_rozwiazanie)

            if wynik < najlepszy_wynik:
                najlepszy_wynik = wynik
                rozwiazanie_najlepsze = nowe_rozwiazanie
                poprawa = True
                print(rozwiazanie_najlepsze, najlepszy_wynik)

            if najlepszy_wynik == 0:
                return rozwiazanie_najlepsze, najlepszy_wynik
        
        if not poprawa:
            break

    return rozwiazanie_najlepsze, najlepszy_wynik