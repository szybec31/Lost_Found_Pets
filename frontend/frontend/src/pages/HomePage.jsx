import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import './HomePage.css';

const HomePage = () => {
  const navigate = useNavigate();
  const isLoggedIn = localStorage.getItem('access_token') !== 'false';

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    navigate('/');
  };

  return (
    <div className="home-container">

      <header className="home-header">
        <h1>Lost Found Pets</h1>
        <p></p>
      </header>

      <main className="home-main">
        <section className="home-welcome">
          <h2>Witamy w LostFoundPets!</h2>
          <h3>Znajdź swojego pupila lub pomóż odnaleźć czyjegoś</h3>
          <p>
            To platforma umożliwiająca szybkie zgłaszanie zaginionych lub znalezionych zwierząt.
            Nasz system wykorzystuje sztuczną inteligencję do analizy zdjęć i porównywania zgłoszeń.
          </p>
        </section>

        <section className="home-actions">
          <div className="action-card">
            <h3>Przeglądaj zgłoszenia</h3>
            <p>Sprawdź, czy ktoś dodał już podobne zgłoszenie.</p>
            <Link to="/reports" className="action-button">Zobacz</Link>
          </div>

          <div className="action-card">
            <h3>O modelu AI</h3>
            <p>Dowiedz się, jak działa nasze rozpoznawanie zwierząt.</p>
            <Link to="/ai-model" className="action-button">Zobacz</Link>
          </div>

          <div className={`action-card ${!isLoggedIn ? 'disabled' : ''}`}>
            <h3>Dodaj zgłoszenie</h3>
            <p>Zgłoś zaginięcie lub znalezienie zwierzęcia.</p>
            <Link to="/add" className="action-button">Dodaj</Link>
          </div>

          <div className={`action-card ${!isLoggedIn ? 'disabled' : ''}`}>
            <h3>Twój profil</h3>
            <p>Zarządzaj swoimi zgłoszeniami i danymi.</p>
            <Link to="/profile" className="action-button">Profil</Link>
          </div>
        </section>

        {!isLoggedIn && (
          <div className="login-prompt">
            <p>Aby skorzystać z funkcjonalności, zaloguj się lub zarejestruj.</p>
            <Link to="/login" className="login-button">Zaloguj się / Zarejestruj</Link>
          </div>
        )}
      </main>

      <footer className="home-footer">
        <p>&copy; 2025 LostFoundPets</p>
        <p>Projekt stworzony w ramach pracy Projektu Zespołowego</p>
      </footer>
    </div>
  );
};

export default HomePage;
