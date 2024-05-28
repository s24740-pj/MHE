# Rozwiązywanie Nonogramu za pomocą Algorytmów Optymalizacyjnych

## Czym jest Nonogram?
Nonogram to łamigłówka logiczna, w której zadaniem jest wypełnienie krat na prostokątnej siatce w taki sposób, aby odkryć ukryty obrazek. Rozwiązanie opiera się na liczbach umieszczonych przy wierszach i kolumnach siatki, które określają, ile kolejnych kratek w danym wierszu lub kolumnie powinno być zaznaczone. 

## Problem Optymalizacyjny
Projekt ten skupia się na zastosowaniu i badaniu różnych algorytmów optymalizacyjnych do rozwiązywania nonogramów. Celem jest znalezienie takiego układu zaznaczeń, które spełnią wszystkie wymagane liczby dla wierszy i kolumn, przy jednoczesnej optymalizacji wybranej funkcji celu.

## Obsługiwane Typy Plansz
Projekt obsługuje rozwiązywanie nonogramów o dowolnych wymiarach prostokątnych. Znaczy to, że algorytmy są zaprojektowane, by radzić sobie z planszami o różnych rozmiarach, od małych do dużych i bardziej złożonych układów.

## Wymagania dla Wierszy i Kolumn
W projekcie rozróżniamy dwa typy wymagań dla wierszy i kolumn:

1. **Pojedyncze liczby**: Każde wymaganie przedstawione jako pojedyncza liczba całkowita określa łączną liczbę zaznaczonych pól w danym wierszu lub kolumnie. Jest to podstawowa forma wymagań, która nie uwzględnia rozdzielenia zaznaczeń na oddzielne grupy.

2. **Złożone wymagania**: Projekt obsługuje również wymagania składające się z kilku liczb, np. `[2, 2, 2]`, co oznacza, że w danym wierszu lub kolumnie powinny znaleźć się trzy oddzielne grupy po dwa zaznaczenia każda, rozdzielone co najmniej jednym pustym polem. Taka funkcjonalność pozwala na bardziej szczegółowe definiowanie wymagań i rozwiązywanie skomplikowanych nonogramów.

### Przykładowe wymaganie `Nonogramu`
[[`[2,1,1]`,`[2,2]`,`[2,1,1]`,`[1,2,1]`],[`2`,`[1,1]`,`[2,1]`,`[1,1]`,`[1,1]`,`1`,`4`]]

## O projekcie
Projekt ten eksploruje zastosowanie algorytmów optymalizacyjnych do rozwiązywania nonogramów - łamigłówek logicznych polegających na wypełnianiu krat na prostokątnej siatce w celu odkrycia ukrytego obrazka. Kluczem do rozwiązania jest interpretacja liczb wskazujących, ile kolejnych kratek w danym wierszu lub kolumnie ma być zaznaczone.

W ramach projektu zaimplementowano algorytmy zdolne do obsługi nonogramów o różnych rozmiarach i wymiarach, począwszy od małych plansz, aż po większe i bardziej skomplikowane układy. Co więcej, projekt nie ogranicza się tylko do prostych wymagań, w których liczby wskazują na łączną liczbę zaznaczonych pól w wierszu lub kolumnie, ale radzi sobie również z bardziej złożonymi wymaganiami.

Złożone wymagania, takie jak oddzielne grupy zaznaczonych pól wyrażone przez sekwencje liczb (np. `[2, 2, 2]`), są w pełni obsługiwane. Oznacza to, że algorytmy są w stanie rozpoznać i zastosować wymogi dotyczące konkretnych grup zaznaczeń, oddzielonych co najmniej jednym pustym polem, zapewniając tym samym większą dokładność i elastyczność w generowaniu rozwiązań.

## Wymagania wstępne

Aby uruchomić projekt, potrzebujesz Pythona w wersji 3.x oraz dostępu do następujących bibliotek:

- `random` - używana do generowania losowych rozwiązań i wyborów w algorytmach. Jest częścią standardowej biblioteki Pythona, więc nie wymaga dodatkowej instalacji.
- `math` - wykorzystywana do operacji matematycznych, takich jak zaokrąglanie liczb.
- `json` - używana do odczytywania i zapisywania danych w formacie JSON, co pozwala na łatwe wczytywanie wymagań nonogramu z pliku tekstowego.

Nie ma potrzeby instalowania dodatkowych pakietów poza standardowym środowiskiem Pythona.

# Czytanie wymagań z pliku
Funkcja `czytaj_wymagania_z_pliku` wczytuje wymagania nonogramu z pliku tekstowego. Otwiera plik o podanej ścieżce, odczytuje jego zawartość jako JSON i zwraca w formie odpowiedniej do dalszego przetwarzania.
```python
def czytaj_wymagania_z_pliku(file_path):
    ...
    return wymagania
```

## Przykład działania
```python
wymaganiaNonogram = czytaj_wymagania_z_pliku('wymagania.txt')
```

# Funkcja Celu

### Funkcja znajdz_grupy
Funkcja `znajdz_grupy` przyjmuje jako argument pojedynczą linię (wiersz lub kolumnę) z rozwiązania nonogramu. Jej zadaniem jest analiza tej linii w celu zidentyfikowania i zwrócenia wszystkich ciągłych grup zaznaczeń (jedynek) znajdujących się w linii. Każda grupa to seria sąsiadujących ze sobą zaznaczeń, oddzielonych od innych grup co najmniej jednym pustym polem (zerem).
```python
def znajdz_grupy(linia):
    ...
    return grupy
```
### Funkcja porownaj_z_wymaganiami
Funkcja `porownaj_z_wymaganiami` porównuje zidentyfikowane grupy zaznaczeń z oczekiwanymi grupami zaznaczeń określonymi w wymaganiach nonogramu dla danej linii (wiersza lub kolumny). Na podstawie tej analizy funkcja oblicza i zwraca kary za niezgodności między rzeczywistymi grupami zaznaczeń a tymi określonymi w wymaganiach, uwzględniając zarówno liczbę i długość grup, jak i ich kolejność.
```python
def porownaj_z_wymaganiami(grupy, wymaganie):
    ...
    return kara
```
### Funkcja Celu
Funkcja celu ocenia, jak blisko dane rozwiązanie jest do spełnienia wszystkich wymagań nonogramu. Im mniejsza wartość funkcji celu, tym lepsze rozwiązanie.
```python
def cel(wymagania, rozwiazanie):
    ...
    return kara
```
## Przykład działania
```python
print(cel(wymaganiaNonogram, rozwiazanieNonogram))
```
### Wyniki działania funkcji celu
```
30+ = słabe/niepoprawne
..
0 = w pełni poprawne
```

# Metoda Sąsiedztwa Losowo
Metoda ta generuje "bliskie sąsiedztwo" bieżącego rozwiązania, co pozwala na eksplorację przestrzeni rozwiązań w poszukiwaniu lepszego ułożenia na podstawie losowości, która wskazuje na zmianę kolejnego pola na zaznaczone bądź odwrotnie.

```python
def bliskieSasiedztwoLosowe(rozwiazanie):
    ...
    return rozwiazanie
```
## Przykład działania
```python
for x in range(10000):
    nowe_rozwiazanie = bliskieSasiedztwoLosowe(rozwiazanieNonogram.copy())
    wynik_celu = cel(wymaganiaNonogram, nowe_rozwiazanie)
    if wynik_celu <= 16:
        print(nowe_rozwiazanie, " Ocena: ", wynik_celu)
```
### Wyniki działania funkcji bliskiego losowego sąsiedztwa
```
[[0, 1, 0, 1, 1, 0, 1], [0, 0, 1, 0, 0, 1, 1], [1, 0, 0, 1, 1, 0, 1], [1, 1, 1, 0, 1, 0, 1]]  Ocena:  10
[[0, 1, 1, 1, 1, 0, 1], [0, 0, 1, 0, 0, 1, 1], [1, 0, 0, 1, 1, 0, 1], [1, 1, 1, 0, 1, 0, 1]]  Ocena:  15
[[0, 1, 1, 1, 1, 0, 1], [0, 0, 1, 0, 0, 1, 1], [1, 0, 0, 1, 0, 0, 1], [1, 1, 1, 0, 1, 0, 1]]  Ocena:  13
[[0, 1, 0, 1, 0, 1, 0], [0, 0, 1, 1, 0, 0, 1], [0, 1, 0, 0, 1, 0, 1], [1, 0, 1, 1, 0, 0, 1]]  Ocena:  13
[[1, 0, 1, 0, 0, 0, 1], [1, 1, 0, 0, 1, 0, 0], [1, 0, 1, 1, 0, 1, 0], [0, 1, 0, 1, 1, 0, 1]]  Ocena:  16
...
```

# Metoda Sąsiedztwa
Metoda ta generuje "bliskie sąsiedztwo" bieżącego rozwiązania, co pozwala na eksplorację przestrzeni rozwiązań w poszukiwaniu lepszego ułożenia na podstawie wartości x, która wskazuje na zmianę kolejnego pola na zaznaczone bądź odwrotnie.

```python
def bliskieSasiedztwo(rozwiazanie, x):
    ...
    return nowe_rozwiazanie
```
## Przykład działania
```python
print(rozwiazanieNonogram)
print(bliskieSasiedztwo(rozwiazanieNonogram, 1))
```
### Wyniki działania funkcji bliskiego sąsiedztwa
```
[[0, 1, 0, 0, 1, 0, 0], [0, 0, 1, 0, 0, 1, 0], [0, 1, 0, 1, 1, 0, 1], [1, 0, 0, 1, 0, 1, 1]]
[[0, 0, 0, 0, 1, 0, 0], [0, 0, 1, 0, 0, 1, 0], [0, 1, 0, 1, 1, 0, 1], [1, 0, 0, 1, 0, 1, 1]]
```

# Generowanie Losowego Rozwiązania
Funkcja ta tworzy całkowicie losowe układanie zaznaczeń na planszy, na podstawie wymagań, co jest użyteczne jako punkt startowy dla algorytmów optymalizacyjnych.

```python
def losoweRozwiazanie(wymagania):
    ...
    return rozwiazanie
```
## Przykład działania
```python
print(losoweRozwiazanie(wymaganiaNonogram))
```
### Wyniki działania funkcji losowego rozwiązania
```
[[1, 0, 1, 1, 1, 1, 1], [0, 1, 0, 1, 0, 1, 0], [0, 0, 0, 0, 1, 1, 1], [1, 1, 1, 0, 0, 1, 0]]
```

# Algorytm Pełnego Przeglądu
Algorytm pełnego przeglądu (brute force) generuje wszystkie możliwe konfiguracje planszy i ocenia je, aby znaleźć najlepsze rozwiązanie. Na bieżąco informuje o procesie szukania.

```python
def pelnyPrzeglad(rozwiazanie):
    ...
    return najlepsze_rozwiazanie
```
## Przykład działania
```python
print(pelnyPrzeglad(wymaganiaNonogram))
```
### Wyniki działania funkcji pełnego przeglądu
```
0 / 268435456
500000 / 268435456
...
110000000 / 268435456
110500000 / 268435456
111000000 / 268435456
111500000 / 268435456
111604441 / 268435456  Ocena:  0  Rozwiazanie:  [[0, 1, 1, 0, 1, 0, 1], [0, 0, 1, 1, 0, 1, 1], [1, 1, 0, 0, 1, 0, 1], [1, 0, 1, 1, 0, 0, 1]]
return: [[0, 1, 1, 0, 1, 0, 1], [0, 0, 1, 1, 0, 1, 1], [1, 1, 0, 0, 1, 0, 1], [1, 0, 1, 1, 0, 0, 1]]
```

# Algorytm Wspinaczkowy Klasyczny
Algorytm wspinaczkowy to metoda heurystyczna, która iteracyjnie poprawia rozwiązanie, wybierając najlepsze dostępne "sąsiedztwo" bieżącego stanu.

```python
def wspinaczkowyKlasyczny(wymagania, rozwiazanie):
    ...
    return najlepsze_rozwiazanie, najlepszy_wynik
```
## Przykład działania
```python
print(wspinaczkowyKlasyczny(wymaganiaNonogram, rozwiazanieNonogram))
```
### Wyniki działania funkcji wspinaczki klasycznej
```
[[0, 1, 0, 1, 1, 0, 0], [0, 0, 1, 0, 0, 1, 0], [0, 1, 0, 1, 1, 0, 1], [1, 0, 0, 1, 0, 1, 1]] 28
[[0, 1, 0, 1, 1, 0, 1], [0, 0, 1, 0, 0, 1, 0], [0, 1, 0, 1, 1, 0, 1], [1, 0, 0, 1, 0, 1, 1]] 24
[[0, 1, 0, 1, 1, 0, 1], [0, 0, 1, 0, 0, 1, 1], [0, 1, 0, 1, 1, 0, 1], [1, 0, 0, 1, 0, 1, 1]] 19
[[0, 1, 0, 1, 1, 0, 1], [0, 0, 1, 0, 0, 1, 1], [1, 1, 0, 1, 1, 0, 1], [1, 0, 0, 1, 0, 1, 1]] 17
[[0, 1, 0, 1, 1, 0, 1], [0, 0, 1, 0, 0, 1, 1], [1, 1, 0, 0, 1, 0, 1], [1, 0, 0, 1, 0, 1, 1]] 15
[[0, 1, 0, 1, 1, 0, 1], [0, 0, 1, 0, 0, 1, 1], [1, 1, 0, 0, 1, 0, 1], [1, 0, 1, 1, 0, 1, 1]] 9
[[0, 1, 0, 1, 1, 0, 1], [0, 0, 1, 0, 0, 1, 1], [1, 1, 0, 0, 1, 0, 1], [1, 0, 1, 1, 0, 0, 1]] 4
return: ([[0, 1, 0, 1, 1, 0, 1], [0, 0, 1, 0, 0, 1, 1], [1, 1, 0, 0, 1, 0, 1], [1, 0, 1, 1, 0, 0, 1]], 4)
```

# Algorytm Tabu
Algorytm Tabu jest heurystycznym algorytmem optymalizacyjnym, który unika `utknięcia w lokalnych minimach` poprzez pamiętanie ostatnio odwiedzonych rozwiązań i zakazując ich ponownego odwiedzania przez pewien czas. Algorytm rozpoczyna od początkowego rozwiązania, generuje sąsiadów bieżącego rozwiązania, ocenia ich jakość, a następnie wybiera najlepszego sąsiada, który nie znajduje się na liście `Tabu`. Jeśli nie można znaleźć dopuszczalnych sąsiadów, `algorytm cofa się` do ostatniego odwiedzonego punktu. Proces jest kontynuowany przez określoną liczbę iteracji lub do znalezienia optymalnego rozwiązania. Lista `Tabu` ma ograniczoną długość, co pozwala na ponowne odwiedzanie starszych rozwiązań po ich usunięciu z listy.

```python
def algorytmTabu(wymagania, rozwiazanie, max_dl_tabu, iteracje):
    ...
    if(najlepszy_wynik == 0):
        return rozwiazanie
    ...
    for i in range(iteracje):
        if(len(sasiedzi) == 0):
            if(najlepszy_sasiad[1] == 0):
                return najlepszy_sasiad, i
    ...
    return najlepsze_rozwiazanie_globalne, cel(wymagania,najlepsze_rozwiazanie_globalne)
```
## Przykład działania
```python
print(algorytmTabu(wymaganiaNonogram, losoweRozwiazanie(wymaganiaNonogram), max_dl_tabu = 1000000, iteracje = 1000000))
```

### Wyniki działania algorytmu Tabu
```
0  /  1000000 0.0 %
2000  /  1000000 0.2 %
4000  /  1000000 0.4 %
6000  /  1000000 0.6 %
8000  /  1000000 0.8 %
10000  /  1000000 1.0 %
([[[0, 0, 1, 1, 0, 0, 1, 0], [0, 1, 1, 0, 1, 0, 0, 1], [1, 1, 0, 0, 1, 0, 1, 0], [0, 1, 1, 1, 0, 0, 1, 1], [0, 0, 1, 1, 0, 0, 1, 0], [1, 1, 1, 1, 1, 1, 1, 1], [0, 1, 1, 0, 0, 0, 0, 1], [0, 0, 0, 1, 0, 1, 1, 0]], 0], 10304)
```

# Algorytm Symulowanego Wyżarzania
Algorytm symulowanego wyżarzania (Simulated Annealing) jest heurystycznym algorytmem optymalizacyjnym inspirowanym procesem wyżarzania metali, stosowanym do znajdowania globalnego minimum funkcji celu. Rozpoczyna od losowego rozwiązania i wysokiej temperatury, które następnie jest stopniowo chłodzone zgodnie z funkcją `T = T_0 * α^k`, gdzie `T_0` to początkowa temperatura, `α` to współczynnik chłodzenia `(0 < α < 1)`, a `k` to liczba iteracji. W każdej iteracji generuje nowe rozwiązanie, akceptując je bezwarunkowo, jeśli jest lepsze, lub z pewnym prawdopodobieństwem zależnym od temperatury i różnicy wartości funkcji celu, jeśli jest gorsze. Proces kontynuowany jest, aż temperatura spadnie poniżej minimalnej wartości `T_min` lub osiągnięta zostanie maksymalna liczba iteracji, a najlepsze znalezione rozwiązanie jest zwracane.

```python
def symulowaneWyzarzanie(wymagania, poczatkowe_rozwiazanie, T_0, alpha, T_min, max_iter):
    ...
    return najlepsze_rozwiazanie, najlepszy_cel
```

## Przykład działania
```python
print(symulowaneWyzarzanie(wymaganiaNonogram, losoweRozwiazanie(wymaganiaNonogram), T_0=100, alpha=0.9999, T_min=0.01, max_iter=10000))
```
### Przykładowe wyniki działania funkcji Symulowanego Wyżarzania
```
([[0, 0, 1, 0], [1, 1, 1, 0], [0, 1, 1, 0], [1, 0, 1, 0], [1, 0, 1, 0]], 6)
([[0, 1, 0, 1], [1, 1, 0, 0], [1, 1, 0, 0], [0, 0, 0, 0], [0, 0, 1, 1]], 14)
([[0, 1, 0, 1], [0, 1, 0, 1], [1, 1, 0, 1], [0, 0, 0, 0], [0, 1, 0, 0]], 14)
([[0, 0, 1, 0], [0, 0, 1, 0], [0, 1, 0, 1], [0, 0, 0, 0], [1, 0, 0, 1]], 8)
([[0, 1, 0, 0], [0, 0, 1, 1], [1, 0, 1, 1], [1, 1, 0, 1], [0, 0, 0, 0]], 2)
```
