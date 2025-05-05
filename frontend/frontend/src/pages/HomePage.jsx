import React from 'react';
import { Link } from 'react-router-dom';
import './HomePage.css';

const HomePage = () => {
    const isLoggedIn = localStorage.getItem('access_token') !== 'false';

    return(
        <div className="home-container">
          <header className="home-header">
            <h1>Lost Found Pets</h1>
            <p>Znajdź swojego pupila lub pomóż odnaleźć czyjegoś</p>
            {!isLoggedIn && (
              <div className="header-login-button">
                <Link to="/login" className="login-button">Zaloguj się</Link>
              </div>
            )}
          </header>
    
          <main className="home-main">
            <section className="home-welcome">
              <h2>Witamy w LostFoundPets!</h2>
              <p>
                To platforma umożliwiająca szybkie zgłaszanie zaginionych lub znalezionych zwierząt.
                Nasz system wykorzystuje sztuczną inteligencję do analizy zdjęć i porównywania zgłoszeń.
              </p>
            </section>
    
            <section className="home-actions">
              {isLoggedIn ? (
                <>
                  <div className="action-card">
                    <h3>Dodaj zgłoszenie</h3>
                    <p>Zgłoś zaginięcie lub znalezienie zwierzęcia.</p>
                    <Link to="/add" className="action-button">Dodaj</Link>
                  </div>
    
                  <div className="action-card">
                    <h3>Przeglądaj zgłoszenia</h3>
                    <p>Sprawdź, czy ktoś już dodał podobne zgłoszenie.</p>
                    <Link to="/reports" className="action-button">Zobacz</Link>
                  </div>
    
                  <div className="action-card">
                    <h3>Twój profil</h3>
                    <p>Zarządzaj swoimi zgłoszeniami i danymi.</p>
                    <Link to="/profile" className="action-button">Profil</Link>
                  </div>
                </>
              ) : (
                <div className="login-prompt">
                  <p>Aby dodać zgłoszenie lub przeglądać zgłoszenia, musisz się zalogować.</p>
                  <Link to="/login" className="login-button">Zaloguj się / Zarejestruj</Link>
                </div>
              )}
            </section>
          </main>

            <footer className="home-footer">
                <p>&copy; 2025 LostFoundPets</p>
                <p>Projekt stworzony w ramach pracy Projektu Zespołowego</p>
            </footer>
        </div>
    );
};

export default HomePage;