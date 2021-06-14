# Zaawansowana wyszukiwarka nieruchomości

## Opis

Zaawansowana wyszukiwarka nieruchomości pozwala na znalezienie mieszkań oraz domów na wielu
portalach na raz. Po podaniu parametrów wyszukiwania aplikacja wyśle zapytania do popularnych portali
ogłoszeniowych z nieruchomościami i zwróci scalone wyniki.

## Konfiguracja

Wymagania

- python3
- chrome webdriver

Instalacja wymaganych pakietów

`pip install -r requirements.txt`

Stworzenie bazy danych

`./manage.py migrate`

Załadowanie danych

`./manage.py loaddata cities.json`

`./manage.py loaddata websites.json`

Instalacja Webdriver

https://chromedriver.chromium.org/getting-started

##Serwer

Uruchomienie lokalnego serwera

`./manage.py runserver 8000`

Strona dostępna pod url

http://localhost:8000/