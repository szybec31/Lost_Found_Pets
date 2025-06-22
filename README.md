# Aplikacja Lost and Found Pets - porównywanie zdjęć zagubionych i znalezionych zwierząt

Projekt został stworzony w oparciu o model MobileNetV2, który służy do konwersji zdjęć przesyłanych przez użytkowników na 1280-elementowe wektory cech. Te wektory są 
następnie porównywane z wykorzystaniem biblioteki FAISS, która oblicza odległości między nimi w celu znalezienia najbardziej podobnych zdjęć w bazie.

Aplikacja ma formę webową - back-end został zrealizowany w Django, a front-end w React.

## Funkcje programu
- Rejestracja i logowanie użytkownika z weryfikacją e-mailową
- Przeglądanie oraz edycja własnego profilu, w tym zmiana hasła
- Dodawanie zgłoszeń o zagubionych lub znalezionych zwierzętach
- Przeglądanie istniejących zgłoszeń
- Filtrowanie zgłoszeń według ich typu (zagubione / znalezione)


## Instalacja i uruchomienie lokalne
1. Sklonuj repozytorium:
   ```
    git clone https://github.com/XSajmonX/Lost_Found_Pets.git
    cd Lost_Found_Pets
   ```
2. Stwórz wirtualne środowisko:
    ```
    python -m venv myenv
    myenv\Scripts\activate       # Dla systemu operacyjnego Windows
    source myenv/bin/activate    # Linux/Mac 
    ```
3. Zainstaluj zależności:
    ```
    pip install -r requirements.txt
    ```
4. Skonfiguruj bazę danych i zmienne środowiskowe.
   ```
   a) Pobierz i zainstaluj MySQL (wersja 8.0.41, web-community):
   https://dev.mysql.com/downloads/file/?id=536787

   b) Otwórz MySQL Command Line Client i utwórz bazę danych:
   CREATE DATABASE lost_found_pets CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

   c) Jeśli masz inne hasło użytkownika root, zaktualizuj `settings.py` w sekcji DATABASES.

   d) Utwórz superużytkownika do panelu admina:
      python manage.py createsuperuser

   e) Wykonaj migracje:
      python manage.py makemigrations
      python manage.py migrate

   f) Uruchom serwer:
      python manage.py runserver

   g) Otwórz przeglądarkę i przejdź do:
      http://localhost:8000/admin

   ```
5. Wyczyść bazę i dodaj dane:
- Usuń wszystki tabele w MySQL Workbench
- W środowisku wirtualnym wykonaj:
```
      python manage.py makemigrations
      python manage.py migrate
```
- Wprowadź skrypyty do bazy Mysql z folderu Add_data:
  - Wartości domyślne 
  - Dane użytkowników
  - Raporty
  - Gotowe zdjęcia do folderu IMG_Database/Animals


## Użyte technologie
- Python – Zapewnienie ogólnego back-endu aplikacji
- Django – Zbudowanie witryny od strony back-endu, przygotowanie API
- React – Zaprojektowanie strony internetowej od strony front-endu
- MySQL – Zbudowanie i zarządzanie bazą danych
- MobileNetV2 - Konwersja zdjęć na wektory cech
- FAISS - Porównywanie wektorów cech

## Środowisko programistyczne
- Python w wersji 3.12
- Django w wersji 5.1.7 lub nowszej
- React w wersji 19.1.0 lub nowszej
- MySQL w wersji 2.2.7 lub nowszej
- Wirtualne środowisko venv

## Struktura projektu
- `app/` - Moduł aplikacji wewnętrznej projektu
    - `ai.py` - Funkcja ekstrakcji wektora cech ze zdjęcia
    - `forms.py` - Formularze do rejestracji użytkownika i zmiany jego danych
    - `generator.py` - Funkcja do generowania kodu wysłanego na maila użytkownika
    - `mail.py` - Funkcja do weryfikowania kodu wysłanego na maila użytkownika
    - `models.py` - Definicje modeli danych używanych w bazie
    - `serializers.py` - Serializatory, używane do konwersji danych między formatami JSON a modelami Django
    - `views.py` - Widoki odpowiedzialne za obsługę żądań HTTP
- `frontend/frontend/` - Folder zawierający wszystkie pliki od front-endu
    - `public/` - Zawiera logo aplikacji 
    - `src/` - Zawiera wszystkie pliki JavaScript i CSS używane we front-endzie
    - `package.json` - Plik konfiguracyjny menedżera pakietów npm
    - `package-lock.json` - Plik automatycznie generowany przez npm
- `Lost_Found_Pets` - Zawiera główną aplikację projektu
    - `settings` - Plik konfiguracyjny projektu
    - `urls` - Konfiguracja tras URL
    - `wsgi.py` – Plik uruchamiania aplikacji w środowisku produkcyjnym
    - `asgi.py` – Konfiguracja dla środowiska ASGI
- `IMG_Database/Animals/` - Zawiera zdjęcie każdego ze zgłoszeń w bazie
- `manage.py` - Narzędzie do zarządzania projektem (np. uruchamianie serwera, migracje bazy danych)
- `requirements.txt` - Plik z listą zależności potrzebnych do uruchomienia projektu
- `.gitignore` - Plik określający, które pliki i foldery mają być pomijane przez Gita


## Autorzy projektu
- Szymon Bęczkowski - Moduł AI i backend
- Piotr Kontny - Moduł AI i backend
- Damian Fajfer - Baza danych i backend
- Oliwier Szczecina - Baza danych i backend
- Piotr Stangred - Frontend i integracja z backendem
- Marcin Obuchowski - Frontend i integracja z backendem






