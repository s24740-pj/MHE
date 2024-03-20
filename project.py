import random
import math

# wiersze 0 - kolumny 1
wymaganiaNonogram = [[0,1,1,3,5],[1,2,4,2,1]]
# przykładowe rozwiązanie na podstawie wierszy
rozwiazanieNonogram =  [[0,1,0,1,0],
                        [0,0,0,0,0],
                        [0,1,1,1,0],
                        [0,1,0,1,1],
                        [0,1,1,1,1]]
#poprawne rozwiazanie
poprawne_rozwiazanieNonogram = [[0,0,0,0,0],
                                [0,0,1,0,0],
                                [0,0,1,0,0],
                                [0,1,1,1,0],
                                [1,1,1,1,1]]

def cel(wymagania, rozwiazanie):
    kara = 0
    kara_temp = 0
    col_sum = 0
    # sprawdzanie wierszy
    for x in range(len(wymagania[0])):
        kara_temp = wymagania[0][x] - sum(rozwiazanie[x])
        if kara_temp < 0:
            kara_temp *= -1
        kara += kara_temp
    # sprawdzanie kolumn
    for x in range(len(wymagania[1])):
        for y in range(len(rozwiazanie)):
            col_sum += rozwiazanie[y][x]
        kara_temp = wymagania[1][x] - col_sum
        col_sum = 0
        if kara_temp < 0:
            kara_temp *= -1
        kara += kara_temp 
    
    return kara

def bliskieSasiedztwoLosowe(rozwiazanie):
    x = random.randrange(len(rozwiazanie))
    y = random.randrange(len(rozwiazanie[0]))
    rozwiazanie[x][y] = 1 - rozwiazanie[x][y]
    return rozwiazanie

def bliskieSasiedztwo(rozwiazanie, x):
    nowe_rozwiazanie = [row[:] for row in rozwiazanie]
    nowe_rozwiazanie[math.floor(x/5)][x%5] = 1 - nowe_rozwiazanie[math.floor(x/5)][x%5]
    return nowe_rozwiazanie

def wspinaczkowyKlasyczny(wymagania, rozwiazanie):
    najlepszy_wynik = cel(wymagania, rozwiazanie)
    rozwiazanie_najlepsze = rozwiazanie

    while True:
        poprawa = False
        for x in range(len(rozwiazanie)**2):
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

def losoweRozwiazanie(wymagania):
    rozwiazanie = [[0 for _ in range(len(wymagania[1]))] for _ in range(len(wymagania[0]))]
    for x in range(len(wymagania[0])):
        for y in range(len(wymagania[1])):
            rozwiazanie[x][y] = random.randrange(0, 10) % 2
    return rozwiazanie

def zamianaBinarna(x):
    binarny_ciag = bin(x)[2:].zfill(len(wymaganiaNonogram[0])**2)
    rozwiazanie = []
    for i in range(0, 25, 5):  # iteruje przez ciąg, biorąc bloki po 5 znaków
        wiersz = [int(bit) for bit in binarny_ciag[i:i+5]]  # konwertuje blok 5 znaków na listę intów
        rozwiazanie.append(wiersz)
    return rozwiazanie

def pelnyPrzeglad(wymagania):
    najlepszy_cel = 100
    squared = len(wymagania[0])*len(wymagania[1])
    ilosc_mozliwosci = len(wymagania)**squared
    for x in range(ilosc_mozliwosci):
        if x % 1000000 == 0:
            print(x, "/", ilosc_mozliwosci)
        if cel(wymagania, zamianaBinarna(x)) < najlepszy_cel:
            najlepszy_cel = cel(wymagania, zamianaBinarna(x))
            najlepsze_rozwiazanie = zamianaBinarna(x)
        if najlepszy_cel == 0:
            print(x, "/", ilosc_mozliwosci, " Ocena: ", najlepszy_cel, " Rozwiazanie: ", najlepsze_rozwiazanie)
            najlepszy_cel = 100
    return najlepsze_rozwiazanie