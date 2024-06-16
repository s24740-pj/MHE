import random
import math
import json
import copy
import argparse

# Todo | Oddać
# Zczytywanie z terminala
# Jaka to selekcja jaką uzyłem w genetycznym, jak sie nazywa: done?

# wiersze 0 - kolumny 1
# wymaganiaNonogram = [[[2,1,1],[2,2],[2,1,1],[1,2,1]],[2,[1,1],[2,1],[1,1],[1,1],1,4]]
# wymaganiaNonogram = [[[1,1],3,1,[1,1]],[[2,1],2,[2,1]]]
# wymaganiaNonogram = [[[1,2],[2,1],[2],[1,1],[2]],[[2,1],[2,1],[1,1,1],[2,1]]]
# wymaganiaNonogram = [[[2,1],[2,1,1],[2,1,1],[3,2],[2,1],[8],[2,1],[1,2]],[[1,1],[3,2],[2,4],[1,3,1],[2,1],[1,1],[1,4,1],[1,1,2]]]

# rozwiazanieNonogram =  [[0, 1, 0, 0, 1, 0, 0], [0, 0, 1, 0, 0, 1, 0], [0, 1, 0, 1, 1, 0, 1], [1, 0, 0, 1, 0, 1, 1]]
# rozwiazanieNonogram = [[0,0,0],[0,1,1],[1,0,0],[0,1,0]]

# poprawne_rozwiazanieNonogram =  [[0, 1, 1, 0, 1, 0, 1], [0, 0, 1, 1, 0, 1, 1], [1, 1, 0, 0, 1, 0, 1], [1, 0, 1, 1, 0, 0, 1]]
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

# print(zRozwiazanieDoBinarna(rozwiazanieNonogram))

def pelnyPrzeglad(wymagania):
    najlepszy_cel = float('inf')
    najlepsze_rozwiazanie = None
    squared = len(wymagania[0]) * len(wymagania[1])
    ilosc_mozliwosci = 2 ** squared
    for x in range(ilosc_mozliwosci):
        biezace_rozwiazanie = zamianaBinarna(wymagania, x)
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
            if(len(stos_odwiedzonych) != 0):
                sprawdzane_rozwiazanie = zamianaBinarna(wymagania, stos_odwiedzonych[len(stos_odwiedzonych)-1])
                stos_odwiedzonych.pop(len(stos_odwiedzonych)-1)
                sasiedzi.clear()
                # print("Cofam sie!")
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

# print(algorytmTabu(wymaganiaNonogram, losoweRozwiazanie(wymaganiaNonogram), max_dl_tabu = 1000000, iteracje = 10000))

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
        # delta mniejsze od 0 znaczy ze jest lepszym rozwiazaniem
        delta = nowy_cel - obecny_cel
        
        # Akceptacja nowego rozwiązania
        # Jezeli rozwiazanie jest lepsze to odrazu akceptujemy
        # Jezeli rozwiazanie nie jest lepsze to akceptujemy je z prawdopodobienstwem e^(-delta / T)
        # Jak delta jest wysoka to mała szansa na akceptacje
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

# wizualizacjaRozwiazania(poprawne_rozwiazanieNonogram, wymaganiaNonogram)

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
# Selekcja rankingowa?
# Prawdopodobieństwo selekcji osobnika wyznacza się na podstawie jego rangi, w tym przypadku waga czyli 1/wynik
# 1e-6 = 0.000001, dodajemy by uniknąć dzielenia przez zero
def selekcja(populacja, wyniki, liczba_rodzicow):
    wybrani = random.choices(populacja, weights=[1/(wynik + 1e-6) for _, wynik in wyniki], k=liczba_rodzicow)
    return wybrani

# Selekcja elitarna
# def selekcja(populacja, wyniki, liczba_rodzicow):
#     # Sortujemy wyniki po najlepszych
#     wyniki.sort(key=lambda x: x[1])
#     # Bierzemy pierwsze <liczba_rodzicow> osobnikow
#     wybrani = wyniki[:liczba_rodzicow]
#     # Usuwamy wynik rozwiazania z ostatecznych wybranych by móc je dalej przepuścić
#     wybrani = [osobnik for osobnik, _ in wybrani[:liczba_rodzicow]]

#     return wybrani

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

        # Elita czyli przenoszenie najlepszego osobnika do nowej populacji
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
        # koncowa_populacja = [osobnik for osobnik in populacja]
        # print(f"Pokolenie {pokolenie}: Wyniki populacji: {koncowy_wynik_populacji}")

        # Warunki zakończenia algorytmu
        if warunek_zakonczenia == 'liczba_iteracji' and pokolenie >= liczba_pokolen - 1:
            print("koniec z powodu liczby iteracji")
            break
        elif warunek_zakonczenia == 'minimalna_wartosc' and najlepszy_wynik <= 0:
            print("koniec z powodu minimalnej wartości")
            break

    return najlepszy_osobnik, najlepszy_wynik


def parse_arguments():
    parser = argparse.ArgumentParser(description='Wybierz algorytm')
    subparsers = parser.add_subparsers(dest='algorytm', help='Wybierz algorytm by odpalić')

    # Parser dla celu
    parser_cel = subparsers.add_parser('cel', help='Cel')
    parser_cel.add_argument('--wymagania', type=str, default="wymagania", help='Wymagania nonogramu')
    parser_cel.add_argument('--plik', type=str, default="plik", help='Sczytaj wymagania z pliku')
    parser_cel.add_argument('--rozwiazanie', type=str, default="losowe", help='Przykladowe rozwiazanie nonogramu')
    parser_cel.add_argument('--wizualizacja', type=str, default='False', help='Wizualizacja wyniku True/False')

    # Parser dla sąsiedztwa losowego
    parser_sasiedztwo_losowe = subparsers.add_parser('sasiedztwo_losowe', help='Sąsiedztwo losowe')
    parser_sasiedztwo_losowe.add_argument('--rozwiazanie', type=str, default="losowe", help='Przykladowe rozwiazanie nonogramu')

    # Parser dla sąsiedztwa
    parser_sasiedztwo = subparsers.add_parser('sasiedztwo', help='Sąsiedztwo')
    parser_sasiedztwo.add_argument('--rozwiazanie', type=str, default="losowe", help='Przykladowe rozwiazanie nonogramu')
    parser_sasiedztwo.add_argument('--x', type=int, default=0, help='Który index ma być zmieniony')

    # Parser dla losowego rozwiązania
    parser_losowe_rozwiazanie = subparsers.add_parser('losowe_rozwiazanie', help='Losowe rozwiązanie')
    parser_losowe_rozwiazanie.add_argument('--wymagania', type=str, default="wymagania", help='Wymagania nonogramu')
    parser_losowe_rozwiazanie.add_argument('--plik', type=str, default="plik", help='Sczytaj wymagania z pliku')
    parser_losowe_rozwiazanie.add_argument('--wizualizacja', type=str, default='False', help='Wizualizacja wyniku True/False')

    # Parser dla pełnego przeglądu
    parser_pelny_przeglad = subparsers.add_parser('pelny_przeglad', help='Pełny przegląd')
    parser_pelny_przeglad.add_argument('--wymagania', type=str, default="wymagania", help='Wymagania nonogramu')
    parser_pelny_przeglad.add_argument('--plik', type=str, default="plik", help='Sczytaj wymagania z pliku')
    parser_pelny_przeglad.add_argument('--wizualizacja', type=str, default='False', help='Wizualizacja wyniku True/False')

    # Parser dla wspinaczki klasycznej
    parser_wspinaczkowy_klasyczny = subparsers.add_parser('wspinaczkowy_klasyczny', help='Wspinaczkowy klasyczny')
    parser_wspinaczkowy_klasyczny.add_argument('--rozwiazanie', type=str, default="losowe", help='Przykladowe rozwiazanie nonogramu')
    parser_wspinaczkowy_klasyczny.add_argument('--wymagania', type=str, default="wymagania", help='Wymagania nonogramu')
    parser_wspinaczkowy_klasyczny.add_argument('--plik', type=str, default="plik", help='Sczytaj wymagania z pliku')
    parser_wspinaczkowy_klasyczny.add_argument('--wizualizacja', type=str, default='False', help='Wizualizacja wyniku True/False')

    # Parser dla tablicy tabu
    parser_tablica_tabu = subparsers.add_parser('tablica_tabu', help='Tablica tabu')
    parser_tablica_tabu.add_argument('--rozwiazanie', type=str, default="losowe", help='Przykladowe rozwiazanie nonogramu')
    parser_tablica_tabu.add_argument('--wymagania', type=str, default="wymagania", help='Wymagania nonogramu')
    parser_tablica_tabu.add_argument('--plik', type=str, default="plik", help='Sczytaj wymagania z pliku')
    parser_tablica_tabu.add_argument('--max_dl_tabu', type=int, default=100, help='Maksymalna długość tablicy tabu')
    parser_tablica_tabu.add_argument('--iteracje', type=int, default=10000, help='Maksymalna ilość iteracji')
    parser_tablica_tabu.add_argument('--wizualizacja', type=str, default='False', help='Wizualizacja wyniku True/False')

    # Parser dla symulowane wyzarzanie
    parser_symulowane_wyzarzanie = subparsers.add_parser('symulowane_wyzarzanie', help='Symulowane wyzarzanie')
    parser_symulowane_wyzarzanie.add_argument('--rozwiazanie', type=str, default="losowe", help='Przykladowe rozwiazanie nonogramu')
    parser_symulowane_wyzarzanie.add_argument('--wymagania', type=str, default="wymagania", help='Wymagania nonogramu')
    parser_symulowane_wyzarzanie.add_argument('--plik', type=str, default="plik", help='Sczytaj wymagania z pliku')
    parser_symulowane_wyzarzanie.add_argument('--T_0', type=float, default=100, help='Temperatura wstępna')
    parser_symulowane_wyzarzanie.add_argument('--alpha', type=float, default=0.95, help='Współczynnik schładzania')
    parser_symulowane_wyzarzanie.add_argument('--T_min', type=float, default=0.01, help='Minimalna temperatura')
    parser_symulowane_wyzarzanie.add_argument('--max_iter', type=int, default=10000, help='Maksymalna ilość iteracji')
    parser_symulowane_wyzarzanie.add_argument('--wizualizacja', type=str, default='False', help='Wizualizacja wyniku True/False')

    # Parser dla wizualizacji rozwiazania
    parser_wizualizacja_rozwiazania = subparsers.add_parser('wizualizacja_rozwiazania', help='Wizualizacja rozwiazania')
    parser_wizualizacja_rozwiazania.add_argument('--rozwiazanie', type=str, default="losowe", help='Przykladowe rozwiazanie nonogramu')
    parser_wizualizacja_rozwiazania.add_argument('--wymagania', type=str, default="wymagania", help='Wymagania nonogramu')
    parser_wizualizacja_rozwiazania.add_argument('--plik', type=str, default="plik", help='Sczytaj wymagania z pliku')

    # Parser dla algorytm genetyczny
    parser_algorytm_genetyczny = subparsers.add_parser('algorytm_genetyczny', help='Algorytm genetyczny')
    parser_algorytm_genetyczny.add_argument('--wymagania', type=str, default="wymagania", help='Wymagania nonogramu')
    parser_algorytm_genetyczny.add_argument('--plik', type=str, default="plik", help='Sczytaj wymagania z pliku')
    parser_algorytm_genetyczny.add_argument('--rozmiar_populacji', type=int, default=100, help='Maksymalny rozmiar populacji')
    parser_algorytm_genetyczny.add_argument('--liczba_pokolen', type=int, default=1000, help='Maksymalna liczba pokolen')
    parser_algorytm_genetyczny.add_argument('--wspolczynnik_krzyzowania', type=float, default=0.9, help='Współczynnik aktywacji krzyzowania')
    parser_algorytm_genetyczny.add_argument('--wspolczynnik_mutacji', type=float, default=0.1, help='Współczynnik aktywacji mutacji')
    parser_algorytm_genetyczny.add_argument('--metoda_krzyzowania', type=str, default="jednopunktowe", help='Wybór metody krzyzowania: jednopunktowe/dwupunktowe')
    parser_algorytm_genetyczny.add_argument('--metoda_mutacji', type=str, default="losowa", help='Wybór metody mutacji: losowa/swap')
    parser_algorytm_genetyczny.add_argument('--warunek_zakonczenia', type=str, default="liczba_iteracji", help='Wybór warunku zakonczenia')
    parser_algorytm_genetyczny.add_argument('--elita', type=int, default=0, help='Ilość elity')
    parser_algorytm_genetyczny.add_argument('--wizualizacja', type=str, default='False', help='Wizualizacja wyniku True/False')

    return parser.parse_args()

args = parse_arguments()

if args.algorytm == 'cel':
    # python project.py cel --wymagania '[[[1,1],3,1,[1,1]],[[2,1],2,[2,1]]]' --rozwiazanie '[[0,0,0],[0,1,1],[1,0,0],[0,1,0]]' --plik /Users/kamilpowierza/Desktop/wymagania.txt 
    if(args.wymagania == "wymagania"):
        wymagania = czytaj_wymagania_z_pliku("wymagania.txt")
    else:
        wymagania = json.loads(args.wymagania)
    if(args.plik != "plik"):
        wymagania = czytaj_wymagania_z_pliku(args.plik)
    if(args.rozwiazanie == "losowe"):
        rozwiazanie = losoweRozwiazanie(wymagania)
    else:
        rozwiazanie = json.loads(args.rozwiazanie)

    wynik = cel(wymagania, rozwiazanie)
    print(wynik)
    if(args.wizualizacja == "True"):
        wizualizacjaRozwiazania(rozwiazanie, wymagania)

elif args.algorytm == 'sasiedztwo_losowe':
    # python project.py sasiedztwo_losowe --rozwiazanie '[[0,0,0],[0,1,1],[1,0,0],[0,1,0]]'
    if(args.rozwiazanie == "losowe"):
        rozwiazanie = losoweRozwiazanie(czytaj_wymagania_z_pliku('wymagania.txt'))
    else:
        rozwiazanie = json.loads(args.rozwiazanie)
    print(bliskieSasiedztwoLosowe(rozwiazanie))
    
elif args.algorytm == 'sasiedztwo':
    # python project.py sasiedztwo --rozwiazanie '[[0,0,0],[0,1,1],[1,0,0],[0,1,0]]' --x 2
    if(args.rozwiazanie == "losowe"):
        rozwiazanie = losoweRozwiazanie(czytaj_wymagania_z_pliku('wymagania.txt'))
    else:
        rozwiazanie = json.loads(args.rozwiazanie)
    x = args.x
    print(bliskieSasiedztwo(rozwiazanie, x))

elif args.algorytm == 'losowe_rozwiazanie':
    # python project.py losowe_rozwiazanie --wymagania '[[[1,1],3,1,[1,1]],[[2,1],2,[2,1]]]' --plik /Users/kamilpowierza/Desktop/wymagania.txt 
    if(args.wymagania == "wymagania"):
        wymagania = czytaj_wymagania_z_pliku("wymagania.txt")
    else:
        wymagania = json.loads(args.wymagania)

    if(args.plik != "plik"):
        wymagania = czytaj_wymagania_z_pliku(args.plik)

    wynik = losoweRozwiazanie(wymagania)
    print(wynik)
    if(args.wizualizacja == "True"):
        wizualizacjaRozwiazania(wynik, wymagania)

elif args.algorytm == 'pelny_przeglad':
    # python project.py pelny_przeglad --wymagania '[[[1,1],3,1,[1,1]],[[2,1],2,[2,1]]]' --plik /Users/kamilpowierza/Desktop/wymagania.txt 
    if(args.wymagania == "wymagania"):
        wymagania = czytaj_wymagania_z_pliku("wymagania.txt")
    else:
        wymagania = json.loads(args.wymagania)
    if(args.plik != "plik"):
        wymagania = czytaj_wymagania_z_pliku(args.plik)

    wynik = pelnyPrzeglad(wymagania)
    print(wynik)
    if(args.wizualizacja == "True"):
        wizualizacjaRozwiazania(wynik, wymagania)

elif args.algorytm == 'wspinaczkowy_klasyczny':
    # python project.py wspinaczkowy_klasyczny --rozwiazanie '[[0,0,0],[0,1,1],[1,0,0],[0,1,0]]' --wymagania '[[[1,1],3,1,[1,1]],[[2,1],2,[2,1]]]' --plik /Users/kamilpowierza/Desktop/wymagania.txt 
    if(args.wymagania == "wymagania"):
        wymagania = czytaj_wymagania_z_pliku("wymagania.txt")
    else:
        wymagania = json.loads(args.wymagania)
    if(args.plik != "plik"):
        wymagania = czytaj_wymagania_z_pliku(args.plik)
    if(args.rozwiazanie == "losowe"):
        rozwiazanie = losoweRozwiazanie(wymagania)
    else:
        rozwiazanie = json.loads(args.rozwiazanie)

    wynik = wspinaczkowyKlasyczny(wymagania, rozwiazanie)
    print(wynik)
    if(args.wizualizacja == "True"):
        wizualizacjaRozwiazania(wynik[0], wymagania)
    
elif args.algorytm == 'tablica_tabu':
    # python project.py tablica_tabu --rozwiazanie '[[0,0,0],[0,1,1],[1,0,0],[0,1,0]]' --wymagania '[[[1,1],3,1,[1,1]],[[2,1],2,[2,1]]]' --plik /Users/kamilpowierza/Desktop/wymagania.txt --max_dl_tabu 100000 --iteracje 20000 --wizualizacja True
    if(args.wymagania == "wymagania"):
        wymagania = czytaj_wymagania_z_pliku("wymagania.txt")
    else:
        wymagania = json.loads(args.wymagania)
    if(args.plik != "plik"):
        wymagania = czytaj_wymagania_z_pliku(args.plik)
    if(args.rozwiazanie == "losowe"):
        rozwiazanie = losoweRozwiazanie(wymagania)
    else:
        rozwiazanie = json.loads(args.rozwiazanie)
    
    max_dl_tabu = args.max_dl_tabu
    iteracje = args.iteracje

    wynik = algorytmTabu(wymaganiaNonogram, rozwiazanie, max_dl_tabu, iteracje)
    print(wynik)
    if(args.wizualizacja == "True"):
        wizualizacjaRozwiazania(wynik[0], wymagania)

elif args.algorytm == 'symulowane_wyzarzanie':
    # python project.py symulowane_wyzarzanie --rozwiazanie '[[0,0,0],[0,1,1],[1,0,0],[0,1,0]]' --wymagania '[[[1,1],3,1,[1,1]],[[2,1],2,[2,1]]]' --plik /Users/kamilpowierza/Desktop/wymagania.txt --T_0 100 --alpha 0.999 --T_min 0.01 --max_iter 10000
    if(args.wymagania == "wymagania"):
        wymagania = czytaj_wymagania_z_pliku("wymagania.txt")
    else:
        wymagania = json.loads(args.wymagania)
    if(args.plik != "plik"):
        wymagania = czytaj_wymagania_z_pliku(args.plik)
    if(args.rozwiazanie == "losowe"):
        rozwiazanie = losoweRozwiazanie(wymagania)
    else:
        rozwiazanie = json.loads(args.rozwiazanie)

    T_0 = args.T_0
    alpha = args.alpha
    T_min = args.T_min
    max_iter = args.max_iter

    wynik = symulowaneWyzarzanie(wymagania, rozwiazanie, T_0, alpha, T_min, max_iter)
    print(wynik)
    if(args.wizualizacja == "True"):
        wizualizacjaRozwiazania(wynik[0], wymagania)

elif args.algorytm == 'wizualizacja_rozwiazania':
    # python project.py wizualizacja_rozwiazania --rozwiazanie '[[0,0,0],[0,1,1],[1,0,0],[0,1,0]]' --wymagania '[[[1,1],3,1,[1,1]],[[2,1],2,[2,1]]]' --plik /Users/kamilpowierza/Desktop/wymagania.txt
    if(args.wymagania == "wymagania"):
        wymagania = czytaj_wymagania_z_pliku("wymagania.txt")
    else:
        wymagania = json.loads(args.wymagania)
    if(args.plik != "plik"):
        wymagania = czytaj_wymagania_z_pliku(args.plik)
    if(args.rozwiazanie == "losowe"):
        rozwiazanie = losoweRozwiazanie(wymagania)
    else:
        rozwiazanie = json.loads(args.rozwiazanie)

    wizualizacjaRozwiazania(rozwiazanie, wymagania)

elif args.algorytm == 'algorytm_genetyczny':
    # python project.py algorytm_genetyczny --wymagania '[[[1,1],3,1,[1,1]],[[2,1],2,[2,1]]]' --plik /Users/kamilpowierza/Desktop/wymagania.txt --rozmiar_populacji 100 --liczba_pokolen 1000 --wspolczynnik_krzyzowania 0.9 --wspolczynnik_mutacji 0.1 --metoda_krzyzowania 'jednopunktowe' --metoda_mutacji 'losowa' --warunek_zakonczenia 'liczba_iteracji' --elita 1
    if(args.wymagania == "wymagania"):
        wymagania = czytaj_wymagania_z_pliku("wymagania.txt")
    else:
        wymagania = json.loads(args.wymagania)
    if(args.plik != "plik"):
        wymagania = czytaj_wymagania_z_pliku(args.plik)

    rozmiar_populacji = args.rozmiar_populacji
    liczba_pokolen = args.liczba_pokolen
    wspolczynnik_krzyzowania = args.wspolczynnik_krzyzowania
    wspolczynnik_mutacji = args.wspolczynnik_mutacji
    metoda_krzyzowania = args.metoda_krzyzowania
    metoda_mutacji = args.metoda_mutacji
    warunek_zakonczenia = args.warunek_zakonczenia
    elita = args.elita

    najlepsze_rozwiazanie, najlepszy_wynik = algorytm_genetyczny(
        wymagania,
        rozmiar_populacji = 100,
        liczba_pokolen = 1000,
        wspolczynnik_krzyzowania = 0.9,
        wspolczynnik_mutacji = 0.1,
        metoda_krzyzowania = 'jednopunktowe',
        metoda_mutacji = 'losowa',
        warunek_zakonczenia = 'liczba_iteracji',
        elita = 1
    )
    print(najlepsze_rozwiazanie)
    if(args.wizualizacja == "True"):
        wizualizacjaRozwiazania(najlepsze_rozwiazanie, wymagania)

else:
    print("Nie poprawny algorytm")
