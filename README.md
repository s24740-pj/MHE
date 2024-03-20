# Rozwiązywanie Nonogramu za pomocą Algorytmów Optymalizacyjnych

## Czym jest Nonogram?
Nonogram to łamigłówka logiczna, w której gracz wypełnia kratki na prostokątnej siatce, aby odkryć ukryty obrazek, opierając się na liczbach podanych na bokach siatki. Liczby te wskazują, ile kolejnych kratek w danym wierszu lub kolumnie ma być zaznaczone. Cel polega na odkryciu obrazka, dokładnie interpretując te wskazówki.

## Problem Optymalizacyjny
Projekt dotyczy implementacji i eksploracji różnych algorytmów optymalizacyjnych do rozwiązywania nonogramów. Zadanie optymalizacyjne polega na znalezieniu takiego ułożenia zaznaczeń, które spełnia wszystkie wymagania numeryczne dla wierszy i kolumn, optymalizując przy tym określoną funkcję celu.

## Informacje Dodatkowe

W tym projekcie skupiamy się na rozwiązywaniu nonogramów o rozmiarze planszy 5x5, gdzie wymagania dla każdego wiersza i kolumny są przedstawione jako pojedyncze liczby całkowite. Oznacza to, że każde wymaganie wskazuje na łączną liczbę zaznaczonych pól w danym wierszu lub kolumnie, bez rozróżnienia na oddzielne grupy zaznaczonych pól.

## Przykład planszy:
=1 2 4 2 1<br />
0 _ _ _ _ _<br />
1 _ _ x _ _<br />
1 _ _ x _ _<br />
3 _ x x x _<br />
5 x x x x x<br />

## O projekcie

W powyższym przykładzie, wymagania dla wierszy i kolumn są reprezentowane przez pojedyncze liczby. To uproszczenie ma kluczowe znaczenie dla działania implementowanych algorytmów optymalizacyjnych. Projekt jest stricte dostosowany do tego typu wymagań i na obecnym etapie nie obsługuje nonogramów z bardziej złożonymi wymaganiami, takimi jak oddzielne grupy zaznaczonych pól (np. `2 i 2`). Jednakże, dla prostych przypadków, gdzie wymagania mogą być zinterpretowane jako suma oddzielnych grup zaznaczonych pól (np. traktowanie `2 i 2` jako `4`), algorytmy te mogą nadal generować poprawne rozwiązania. Należy jednak pamiętać, że takie uproszczenie może nie zawsze prowadzić do oczekiwanego rozwiązania w przypadku bardziej złożonych nonogramów.

## Wymagania wstępne

Aby uruchomić projekt, potrzebujesz Pythona w wersji 3.x oraz dostępu do następujących bibliotek:

- `random` - używana do generowania losowych rozwiązań i wyborów w algorytmach. Jest częścią standardowej biblioteki Pythona, więc nie wymaga dodatkowej instalacji.
- `math` - wykorzystywana do operacji matematycznych, takich jak zaokrąglanie liczb. Tak jak `random`, jest częścią standardowej biblioteki Pythona.

Nie ma potrzeby instalowania dodatkowych pakietów poza standardowym środowiskiem Pythona.


# Funkcja Celu
Funkcja celu ocenia, jak blisko dane rozwiązanie jest do spełnienia wszystkich wymagań nonogramu. Im mniejsza wartość funkcji celu, tym lepsze rozwiązanie.

```python
def cel(wymagania, rozwiazanie):
    # Implementacja funkcji celu
    return kara

print(cel(wymaganiaNonogram, rozwiazanieNonogram))
```
### Wyniki działania funkcji celu
14 - słabe<br />
..<br />
0 - w pełni poprawne<br />

# Metoda Sąsiedztwa Losowo
Metoda ta generuje "bliskie sąsiedztwo" bieżącego rozwiązania, co pozwala na eksplorację przestrzeni rozwiązań w poszukiwaniu lepszego ułożenia na podstawie losowości, która wskazuje na zmianę kolejnego pola na zaznaczone bądź odwrotnie.

```python
def bliskieSasiedztwoLosowe(rozwiazanie):
    # Implementacja generowania bliskiego sąsiedztwa losowego
    return rozwiazanie

for x in range(10000):
    nowe_rozwiazanie = bliskieSasiedztwoLosowe(rozwiazanieNonogram.copy())
    wynik_celu = cel(wymaganiaNonogram, nowe_rozwiazanie)
    if wynik_celu <= 8:
        print(nowe_rozwiazanie, " Ocena: ", wynik_celu)
```
### Wyniki działania funkcji celu
[[0, 0, 1, 1, 0], [0, 0, 0, 0, 0], [0, 0, 1, 0, 0], [0, 1, 1, 1, 0], [0, 1, 1, 0, 1]]  Ocena:  6<br />
[[0, 0, 1, 1, 0], [0, 0, 0, 0, 0], [0, 0, 1, 0, 0], [0, 0, 1, 1, 0], [0, 1, 1, 0, 1]]  Ocena:  8<br />
...<br />

# Metoda Sąsiedztwa
Metoda ta generuje "bliskie sąsiedztwo" bieżącego rozwiązania, co pozwala na eksplorację przestrzeni rozwiązań w poszukiwaniu lepszego ułożenia na podstawie wartości x, która wskazuje na zmianę kolejnego pola na zaznaczone bądź odwrotnie.

```python
def bliskieSasiedztwo(rozwiazanie, x):
    # Implementacja generowania bliskiego sąsiedztwa
    return nowe_rozwiazanie

print(rozwiazanieNonogram)
print(bliskieSasiedztwo(rozwiazanieNonogram, 1))
```
### Wyniki działania funkcji bliskiego sąsiedztwa
[[0, 1, 0, 1, 0], [0, 0, 0, 0, 0], [0, 1, 1, 1, 0], [0, 1, 0, 1, 1], [0, 1, 1, 1, 1]]<br />
[[0, 0, 0, 1, 0], [0, 0, 0, 0, 0], [0, 1, 1, 1, 0], [0, 1, 0, 1, 1], [0, 1, 1, 1, 1]]<br />

# Generowanie Losowego Rozwiązania
Funkcja ta tworzy całkowicie losowe układanie zaznaczeń na planszy, co jest użyteczne jako punkt startowy dla algorytmów optymalizacyjnych.

```python
def losoweRozwiazanie(rozwiazanie):
    # Implementacja generowania losowego rozwiązania
    return rozwiazanie

print(losoweRozwiazanie(wymaganiaNonogram))
```
### Wyniki działania funkcji losowego rozwiązania
[[0, 1, 0, 0, 0], [0, 1, 1, 1, 1], [0, 0, 1, 1, 0], [1, 0, 0, 0, 0], [0, 0, 0, 0, 0]]

# Algorytm Pełnego Przeglądu
Algorytm pełnego przeglądu (brute force) generuje wszystkie możliwe konfiguracje planszy i ocenia je, aby znaleźć najlepsze rozwiązanie. Na bieżąco informuje o procesie szukania.

```python
def pelnyPrzeglad(rozwiazanie):
    # Implementacja algorytmu pełnego przeglądu
    return najlepsze_rozwiazanie

print(pelnyPrzeglad(wymaganiaNonogram))
```
### Wyniki działania funkcji pełnego przeglądu
0 / 33554432<br />
135647 / 33554432  Ocena:  0  Rozwiazanie:  [[0, 0, 0, 0, 0], [0, 0, 1, 0, 0], [0, 0, 1, 0, 0], [0, 1, 1, 1, 0], [1, 1, 1, 1, 1]]<br />
1000000 / 33554432 <br />
2000000 / 33554432<br />
3000000 / 33554432<br />
...<br />

# Algorytm Wspinaczkowy Klasyczny
Algorytm wspinaczkowy to metoda heurystyczna, która iteracyjnie poprawia rozwiązanie, wybierając najlepsze dostępne "sąsiedztwo" bieżącego stanu.

```python
def wspinaczkowyKlasyczny(wymagania, rozwiazanie):
    # Implementacja klasycznego algorytmu wspinaczkowego klasycznego
    return rozwiazanie_najlepsze, najlepszy_wynik
```
### Wyniki działania funkcji wspinaczki klasycznej
[[0, 0, 0, 1, 0], [0, 0, 0, 0, 0], [0, 1, 1, 1, 0], [0, 1, 0, 1, 1], [0, 1, 1, 1, 1]] 12<br />
[[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 1, 1, 1, 0], [0, 1, 0, 1, 1], [0, 1, 1, 1, 1]] 10<br />
[[0, 0, 0, 0, 0], [1, 0, 0, 0, 0], [0, 1, 1, 1, 0], [0, 1, 0, 1, 1], [0, 1, 1, 1, 1]] 8<br />
[[0, 0, 0, 0, 0], [1, 0, 0, 0, 0], [0, 0, 1, 1, 0], [0, 1, 0, 1, 1], [0, 1, 1, 1, 1]] 6<br />
[[0, 0, 0, 0, 0], [1, 0, 0, 0, 0], [0, 0, 1, 0, 0], [0, 1, 0, 1, 1], [0, 1, 1, 1, 1]] 4<br />
([[0, 0, 0, 0, 0], [1, 0, 0, 0, 0], [0, 0, 1, 0, 0], [0, 1, 0, 1, 1], [0, 1, 1, 1, 1]], 4)<br />