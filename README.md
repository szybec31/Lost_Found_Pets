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
5. Uruchom aplikację:
    
- Dla serwera lokalnego:
   ```
    python manage.py runserver
   ```
- Dla serwera publicznego: należy zmienić adres na publiczny w pliku address.js
   ```
    python manage.py runserver 0.0.0.0:8000
   ```