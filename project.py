import random
import math
import json

# wiersze 0 - kolumny 1
# wymaganiaNonogram = [[[2,1,1],[2,2],[2,1,1],[1,2,1]],[2,[1,1],[2,1],[1,1],[1,1],1,4]]
# wymaganiaNonogram = [[[1,1],3,1,[1,1]],[[2,1],2,[2,1]]]
# wymaganiaNonogram = [[[1,2],[2,1],[2],[1,1],[2]],[[2,1],[2,1],[1,1,1],[2,1]]]
# wymaganiaNonogram = [[[2,1],[2,1,1],[2,1,1],[3,2],[2,1],[8],[2,1],[1,2]],[[1,1],[3,2],[2,4],[1,3,1],[2,1],[1,1],[1,4,1],[1,1,2]]]

# rozwiazanieNonogram =  [[0, 1, 0, 0, 1, 0, 0], [0, 0, 1, 0, 0, 1, 0], [0, 1, 0, 1, 1, 0, 1], [1, 0, 0, 1, 0, 1, 1]]
rozwiazanieNonogram = [[0,0,0],[0,1,1],[1,0,0],[0,1,0]]

# poprawne_rozwiazanieNonogram =  [[0, 1, 1, 0, 1, 0, 1], [0, 0, 1, 1, 0, 1, 1], [1, 1, 0, 0, 1, 0, 1], [1, 0, 1, 1, 0, 0, 1]]
poprawne_rozwiazanieNonogram = [[1,0,1],[1,1,1],[0,1,0],[1,0,1]]

def czytaj_wymagania_z_pliku(file_path):
    with open(file_path, 'r') as file:
        wymagania = json.load(file)
    return wymagania

wymaganiaNonogram = czytaj_wymagania_z_pliku('wymagania.txt')

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
        wymaganie = [wymaganie] # Przekształcamy pojedyncze inty na listę, jezeli takowe są

    kara = 0

    # Obliczamy różnicę w liczbie grup
    roznica_liczby_grup = abs(len(grupy) - len(wymaganie))
    kara += roznica_liczby_grup * 2 #przykładowo, ważymy różnicę w liczbie grup

    # Porównanie kolejnych grup zaznaczeń z wymaganiami, jeśli ich liczba się zgadza
    if len(grupy) == len(wymaganie):
        for grupa, wymagana_dlugosc in zip(grupy, wymaganie):
            # Kara za niezgodność długości grupy z wymaganiem
            kara += abs(grupa - wymagana_dlugosc)
    else:
        # Jeśli liczba grup się nie zgadza, to dodatkowo kara za potencjalną niezgodność kolejności
        kara += len(wymaganie) + 1 #przykładowo, zakładamy dużą karę za każdą brakującą/zbyt dużą grupę

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

# print(cel(wymaganiaNonogram, poprawne_rozwiazanieNonogram))

def bliskieSasiedztwoLosowe(rozwiazanie):
    x = random.randrange(len(rozwiazanie))
    y = random.randrange(len(rozwiazanie[0]))
    rozwiazanie[x][y] = 1 - rozwiazanie[x][y]
    return rozwiazanie

# print(rozwiazanieNonogram)
# print(bliskieSasiedztwoLosowe(rozwiazanieNonogram))

def bliskieSasiedztwo(rozwiazanie, x):
    nowe_rozwiazanie = [row[:] for row in rozwiazanie]
    kolumny = math.floor(x/len(rozwiazanie[0]))
    wiersze = x%len(rozwiazanie[0])
    nowe_rozwiazanie[kolumny][wiersze] = 1 - nowe_rozwiazanie[kolumny][wiersze]
    return nowe_rozwiazanie

# print(rozwiazanieNonogram)
# print(bliskieSasiedztwo(rozwiazanieNonogram, 2))

def losoweRozwiazanie(wymagania):
    rozwiazanie = [[0 for _ in range(len(wymagania[1]))] for _ in range(len(wymagania[0]))]
    for x in range(len(wymagania[0])):
        for y in range(len(wymagania[1])):
            rozwiazanie[x][y] = random.randrange(0, 10) % 2
    return rozwiazanie

# print(losoweRozwiazanie(wymaganiaNonogram))

def zamianaBinarna(wymagania, x):
    wiersze = len(wymagania[0])
    kolumny = len(wymagania[1])
    binarny_ciag = bin(x)[2:].zfill(wiersze*kolumny)
    rozwiazanie = []
    for i in range(0, wiersze*kolumny, kolumny): # Iteruje przez ciąg, biorąc bloki po ilość znaków w wierszu
        wiersz = [int(bit) for bit in binarny_ciag[i:i+kolumny]] # Konwertuje blok wierszów znaków na listę intów
        rozwiazanie.append(wiersz)
    return rozwiazanie

# print(zamianaBinarna(wymaganiaNonogram, 23))

def zRozwiazanieDoBinarna(rozwiazanie):
    binarny_ciag = ''.join(str(bit) for wiersz in rozwiazanie for bit in wiersz)
    return int(binarny_ciag, 2)

# print(zWymaganiaDoBinarna(rozwiazanieNonogram))

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

# print(pelnyPrzeglad(wymaganiaNonogram))

def wspinaczkowyKlasyczny(wymagania, rozwiazanie):
    najlepszy_wynik = cel(wymagania, rozwiazanie)
    najlepsze_rozwiazanie = rozwiazanie

    while True:
        poprawa = False
        for x in range(len(rozwiazanie[0])*len(rozwiazanie)):
            nowe_rozwiazanie = bliskieSasiedztwo(najlepsze_rozwiazanie, x)
            wynik = cel(wymagania, nowe_rozwiazanie)

            if wynik < najlepszy_wynik:
                najlepszy_wynik = wynik
                najlepsze_rozwiazanie = nowe_rozwiazanie
                poprawa = True
                najlepsza_zmiana = x
                # print(najlepsze_rozwiazanie, najlepszy_wynik)

            if najlepszy_wynik == 0:
                return najlepsze_rozwiazanie, najlepszy_wynik
        
        if not poprawa:
            break

    return najlepsze_rozwiazanie, najlepszy_wynik, najlepsza_zmiana

# print(wspinaczkowyKlasyczny(wymaganiaNonogram, rozwiazanieNonogram))

def algorytmTabu(wymagania, rozwiazanie, max_dl_tabu, iteracje):
    sasiedzi = []
    tabu = []
    stos_odwiedzonych = []

    sprawdzane_rozwiazanie = rozwiazanie
    aktualne_rozwiazanie = rozwiazanie
    najlepsze_rozwiazanie_globalne = rozwiazanie
    najlepszy_sasiad = rozwiazanie
    aktualny_wynik = cel(wymagania, rozwiazanie)
    najlepszy_wynik = cel(wymagania, rozwiazanie)
    
    if(najlepszy_wynik == 0):
        return rozwiazanie

    for i in range(iteracje):
        if i % (2000) == 0:
            print(i, " / ", iteracje, (i/iteracje)*100,"%")
        for x in range(len(rozwiazanie[0])*len(rozwiazanie)):
            if zRozwiazanieDoBinarna(bliskieSasiedztwo(sprawdzane_rozwiazanie, x)) not in tabu:
                aktualne_rozwiazanie = bliskieSasiedztwo(sprawdzane_rozwiazanie, x)
                aktualny_wynik = cel(wymagania, aktualne_rozwiazanie)

                sasiedzi.append([aktualne_rozwiazanie, aktualny_wynik])

        if(zRozwiazanieDoBinarna(sprawdzane_rozwiazanie)) not in stos_odwiedzonych and len(sasiedzi) > 0:
            stos_odwiedzonych.append(zRozwiazanieDoBinarna(sprawdzane_rozwiazanie))

        if(len(sasiedzi) == 0):
            sprawdzane_rozwiazanie = zamianaBinarna(wymagania, stos_odwiedzonych[len(stos_odwiedzonych)-1])
            stos_odwiedzonych.pop(len(stos_odwiedzonych)-1)
            sasiedzi.clear()
        else:
            najlepszy_sasiad = min(sasiedzi, key=lambda x: x[1])
            sprawdzane_rozwiazanie = najlepszy_sasiad[0]

            if len(tabu) >= max_dl_tabu:
                    tabu.pop(0)
            tabu.append(zRozwiazanieDoBinarna(najlepszy_sasiad[0]))

            if(najlepszy_sasiad[1] == 0):
                return najlepszy_sasiad, i
            
            if(najlepszy_sasiad[1] < najlepszy_wynik):
                najlepszy_wynik = najlepszy_sasiad[1]
                najlepsze_rozwiazanie_globalne = najlepszy_sasiad[0]
            
            sasiedzi.clear()

    return najlepsze_rozwiazanie_globalne, cel(wymagania,najlepsze_rozwiazanie_globalne)

# print(algorytmTabu(wymaganiaNonogram, losoweRozwiazanie(wymaganiaNonogram), max_dl_tabu = 1000000, iteracje = 1000000))

def symulowaneWyzarzanie(wymagania, poczatkowe_rozwiazanie, T_0, alpha, T_min, max_iter):
    obecne_rozwiazanie = poczatkowe_rozwiazanie
    najlepsze_rozwiazanie = obecne_rozwiazanie
    obecny_cel = cel(wymagania, obecne_rozwiazanie)
    najlepszy_cel = obecny_cel
    T = T_0

    for i in range(max_iter):

        if T <= T_min:
            break
        
        # Generowanie nowego sąsiada
        nowe_rozwiazanie = bliskieSasiedztwoLosowe(obecne_rozwiazanie)
        nowy_cel = cel(wymagania, nowe_rozwiazanie)
        
        # Obliczenie różnicy celu
        delta = nowy_cel - obecny_cel
        
        # Akceptacja nowego rozwiązania
        if delta < 0 or random.random() < math.exp(-delta / T):
            obecne_rozwiazanie = nowe_rozwiazanie
            obecny_cel = nowy_cel
            if nowy_cel < najlepszy_cel:
                najlepsze_rozwiazanie = nowe_rozwiazanie
                najlepszy_cel = nowy_cel
        
        # Schładzanie
        T = T_0 * (alpha ** i)

    return najlepsze_rozwiazanie, najlepszy_cel

# print(symulowaneWyzarzanie(wymaganiaNonogram, losoweRozwiazanie(wymaganiaNonogram), T_0=100, alpha=0.9999, T_min=0.01, max_iter=10000))