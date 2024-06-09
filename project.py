import random
import math
import json
import copy

# wiersze 0 - kolumny 1
wymaganiaNonogram = [[[2,1,1],[2,2],[2,1,1],[1,2,1]],[2,[1,1],[2,1],[1,1],[1,1],1,4]]
# wymaganiaNonogram = [[[1,1],3,1,[1,1]],[[2,1],2,[2,1]]]
# wymaganiaNonogram = [[[1,2],[2,1],[2],[1,1],[2]],[[2,1],[2,1],[1,1,1],[2,1]]]
# wymaganiaNonogram = [[[2,1],[2,1,1],[2,1,1],[3,2],[2,1],[8],[2,1],[1,2]],[[1,1],[3,2],[2,4],[1,3,1],[2,1],[1,1],[1,4,1],[1,1,2]]]

rozwiazanieNonogram =  [[0, 1, 0, 0, 1, 0, 0], [0, 0, 1, 0, 0, 1, 0], [0, 1, 0, 1, 1, 0, 1], [1, 0, 0, 1, 0, 1, 1]]
# rozwiazanieNonogram = [[0,0,0],[0,1,1],[1,0,0],[0,1,0]]

poprawne_rozwiazanieNonogram =  [[0, 1, 1, 0, 1, 0, 1], [0, 0, 1, 1, 0, 1, 1], [1, 1, 0, 0, 1, 0, 1], [1, 0, 1, 1, 0, 0, 1]]
# poprawne_rozwiazanieNonogram = [[1,0,1],[1,1,1],[0,1,0],[1,0,1]]

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

def wizualizacjaRozwiazania(rozwiazanie, wymagania):
    wymagania_wierszy = wymagania[0]
    wymagania_kolumn = wymagania[1]

    # Konwersja wszystkich wymagań do list
    wymagania_wierszy = [w if isinstance(w, list) else [w] for w in wymagania_wierszy]
    wymagania_kolumn = [k if isinstance(k, list) else [k] for k in wymagania_kolumn]

    # Maksymalna liczba wymagań w wierszach i kolumnach
    max_wymagania_wierszy = max(len(w) for w in wymagania_wierszy)
    max_wymagania_kolumn = max(len(k) for k in wymagania_kolumn)

    # Przygotowanie nagłówka z wymaganiami kolumn
    naglowek = [' ' * max_wymagania_wierszy * 2]
    for i in range(max_wymagania_kolumn):
        linia = []
        for k in wymagania_kolumn:
            if len(k) >= max_wymagania_kolumn - i:
                linia.append(f'{k[len(k) - (max_wymagania_kolumn - i)]} ')
            else:
                linia.append('  ')
        naglowek.append(' ' * (max_wymagania_wierszy * 2) + ''.join(linia))

    # Drukowanie nagłówka
    for linia in naglowek:
        print(linia)

    # Przygotowanie i drukowanie każdego wiersza rozwiązania z wymaganiami
    for row, wiersz_wymagania in zip(rozwiazanie, wymagania_wierszy):
        linia_wymagania = ' '.join(str(w) for w in wiersz_wymagania)
        linia_wymagania = linia_wymagania.rjust(max_wymagania_wierszy * 1 + 2)
        linia_rozwiazania = ''.join(['⬛' if cell == 1 else '⬜' for cell in row])
        print(f'{linia_wymagania} {linia_rozwiazania}')

# wizualizacjaRozwiazania(losoweRozwiazanie(wymaganiaNonogram), wymaganiaNonogram)
# testowe = algorytmTabu(wymaganiaNonogram, losoweRozwiazanie(wymaganiaNonogram), max_dl_tabu = 1000000, iteracje = 1000000)
# print(testowe[0][0])
# wizualizacjaRozwiazania(testowe[0][0], wymaganiaNonogram)

# Inicjalizacja populacji
def inicjalizuj_populacje(rozmiar_populacji, wymagania):
    populacja = []
    for _ in range(rozmiar_populacji):
        rozwiazanie = losoweRozwiazanie(wymagania)
        populacja.append(rozwiazanie)
    return populacja

# Ocena populacji
def ocena_populacji(populacja, wymagania):
    wyniki = []
    for osobnik in populacja:
        wynik = cel(wymagania, osobnik)
        wyniki.append((osobnik, wynik))
    return wyniki

# Selekcja rodziców
def selekcja(populacja, wyniki, liczba_rodzicow):
    wybrani = random.choices(populacja, weights=[1/(wynik + 1e-6) for _, wynik in wyniki], k=liczba_rodzicow)
    return wybrani

# Krzyżowanie jednopunktowe
def krzyzowanie_jednopunktowe(rodzic1, rodzic2):
    punkt = random.randint(1, len(rodzic1) - 1)
    potomek1 = rodzic1[:punkt] + rodzic2[punkt:]
    potomek2 = rodzic2[:punkt] + rodzic1[punkt:]
    return potomek1, potomek2

# Krzyżowanie dwupunktowe
def krzyzowanie_dwupunktowe(rodzic1, rodzic2):
    punkt1 = random.randint(1, len(rodzic1) - 2)
    punkt2 = random.randint(punkt1 + 1, len(rodzic1) - 1)
    potomek1 = rodzic1[:punkt1] + rodzic2[punkt1:punkt2] + rodzic1[punkt2:]
    potomek2 = rodzic2[:punkt1] + rodzic1[punkt1:punkt2] + rodzic2[punkt2:]
    return potomek1, potomek2

# Mutacja losowa
def mutacja_losowa(osobnik):
    x = random.randint(0, len(osobnik) - 1)
    y = random.randint(0, len(osobnik[0]) - 1)
    osobnik[x][y] = 1 - osobnik[x][y]
    return osobnik

# Mutacja swap
def mutacja_swap(osobnik):
    x1, y1 = random.randint(0, len(osobnik) - 1), random.randint(0, len(osobnik[0]) - 1)
    x2, y2 = random.randint(0, len(osobnik) - 1), random.randint(0, len(osobnik[0]) - 1)
    osobnik[x1][y1], osobnik[x2][y2] = osobnik[x2][y2], osobnik[x1][y1]
    return osobnik

# Główna funkcja algorytmu genetycznego
def algorytm_genetyczny(wymagania, rozmiar_populacji, liczba_pokolen, wspolczynnik_krzyzowania, wspolczynnik_mutacji, metoda_krzyzowania, metoda_mutacji, warunek_zakonczenia, elita):
    populacja = inicjalizuj_populacje(rozmiar_populacji, wymagania)
    najlepszy_osobnik = None
    najlepszy_wynik = float('inf')

    for pokolenie in range(liczba_pokolen):
        wyniki = ocena_populacji(populacja, wymagania)

        # Aktualizacja najlepszego osobnika
        for osobnik, wynik in wyniki:
            if wynik < najlepszy_wynik:
                najlepszy_wynik = wynik
                najlepszy_osobnik = copy.deepcopy(osobnik)

        nowa_populacja = []

        # Elityzm: Przenoszenie najlepszych osobników do nowej populacji
        sorted_wyniki = sorted(wyniki, key=lambda x: x[1])
        elita_osobniki = [copy.deepcopy(osobnik) for osobnik, _ in sorted_wyniki[:elita]]
        nowa_populacja.extend(elita_osobniki)

        while len(nowa_populacja) < rozmiar_populacji:
            rodzic1, rodzic2 = selekcja(populacja, wyniki, 2)
            if random.random() < wspolczynnik_krzyzowania:
                if metoda_krzyzowania == 'jednopunktowe':
                    potomek1, potomek2 = krzyzowanie_jednopunktowe(rodzic1, rodzic2)
                elif metoda_krzyzowania == 'dwupunktowe':
                    potomek1, potomek2 = krzyzowanie_dwupunktowe(rodzic1, rodzic2)
                nowa_populacja.extend([potomek1, potomek2])
            else:
                nowa_populacja.extend([rodzic1, rodzic2])

        populacja = nowa_populacja[:rozmiar_populacji]

        for i in range(rozmiar_populacji):
            if random.random() < wspolczynnik_mutacji:
                if metoda_mutacji == 'losowa':
                    populacja[i] = mutacja_losowa(copy.deepcopy(populacja[i]))
                elif metoda_mutacji == 'swap':
                    populacja[i] = mutacja_swap(copy.deepcopy(populacja[i]))

        # Diagnostyka wyników w każdej iteracji
        # koncowy_wynik_populacji = [cel(wymagania, osobnik) for osobnik in populacja]
        # print(f"Pokolenie {pokolenie}: Wyniki populacji: {koncowy_wynik_populacji}")

        # Warunki zakończenia algorytmu
        if warunek_zakonczenia == 'liczba_iteracji' and pokolenie >= liczba_pokolen - 1:
            print("koniec z powodu liczby iteracji")
            break
        elif warunek_zakonczenia == 'minimalna_wartosc' and najlepszy_wynik <= 0:
            print("koniec z powodu minimalnej wartości")
            break

    return najlepszy_osobnik, najlepszy_wynik

najlepsze_rozwiazanie, najlepszy_wynik = algorytm_genetyczny(
    wymaganiaNonogram,
    rozmiar_populacji = 100,
    liczba_pokolen = 1000,
    wspolczynnik_krzyzowania = 0.9,
    wspolczynnik_mutacji = 0.1,
    metoda_krzyzowania = 'jednopunktowe',
    metoda_mutacji = 'losowa',
    warunek_zakonczenia = 'liczba_iteracji',
    elita = 1
)

print("Najlepsze rozwiązanie:")
wizualizacjaRozwiazania(najlepsze_rozwiazanie, wymaganiaNonogram)
print("Wynik:", najlepsze_rozwiazanie, najlepszy_wynik)

# wizualizacjaRozwiazania(poprawne_rozwiazanieNonogram, wymaganiaNonogram)