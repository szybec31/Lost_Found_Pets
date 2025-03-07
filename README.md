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

5. Uruchom aplikację:
    
- Dla serwera lokalnego:
   ```
    python manage.py runserver
   ```
- Dla serwera publicznego: należy zmienić adres na publiczny w pliku address.js
   ```
    python manage.py runserver 0.0.0.0:8000
   ```