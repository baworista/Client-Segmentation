## Segmentacja klientów sklepu on-line

Twoim cele  jest segmentacja klientów sklepu internetowego przy użyciu metody RMF (Recency > Monetary Value > Frequency).

Źródłowy zbiór danych dostępny jest pod adresem: https://archive.ics.uci.edu/ml/datasets/online+retail

Znaczenie kolumn:

**InvoiceNo**: Numer faktury. Nominalnie, 6-cio cyfrowy numer integralny, jednoznacznie przypisany do każdej transakcji. Jeżeli kod ten zaczyna się od litery "c", oznacza to, że transakcja została anulowana.

**StockCode**: Kod produktu (pozycji). Nominalnie, 5-cyfrowy numer integralny, niepowtarzalnie przypisany do każdego odrębnego produktu.

**Description**: Nazwa produktu (pozycji). Nominalna.

**Quantity**: Ilości każdego produktu (pozycji) na transakcję. Numeryczne.

**InvoiceDate**: Data i godzina wystawienia faktury. Numeryczne, dzień i godzina wygenerowania każdej transakcji.

**UnitPrice**: Cena jednostkowa. Numeryczna, cena produktu za jednostkę w funtach szterlingach.

**CustomerID**: Numer klienta. Nominalny, 5-cyfrowy numer integralny, jednoznacznie przypisany do każdego klienta.

**Country**: Nazwa kraju. Nominalna, nazwa kraju, w którym przebywa każdy klient.

## Strategia

1. Wyczyść dane
   1. Numer faktury: usuń wszystkie rekordy zaczynające się od "c" (czyli: anulowane)
   2. Usuń niepotrzebne kolumny: StockCode, Description, Country

2. Przygotuj dane
   1. Utwórz kolumnę Recency: liczba dni od daty wystawienia faktury do 30.12.2011 (koniec roku)
      1. Uważaj na Data Sampling!
   2. Utwórz kolumnę Monetary: oblicz wartość zamówienia mnożąc Ilość przez Cenę jednostkową.
   3. Zgrupuj Zbiór danych tak, aby uzyskać pojedynczy wpis dla każdego z klientów
   
3. Stwórz segmentację
   1. Użyj Lab > ML Clustering do segmentacji swoich klientów
   2. Poeksperymentuj z różnymi algorytmami i ich hiper-parametrami
   3. Dla najlepszego algorytmu: **zinterpretuj znaczenie klastrów**
   4. Wdróż najlepszy model i zastosuj do zbioru danych



