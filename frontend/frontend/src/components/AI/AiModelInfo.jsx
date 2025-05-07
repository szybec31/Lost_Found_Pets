import React from 'react';
import { Link, Navigate } from 'react-router-dom';
import './AiModelInfo.css';

const AiModelInfo = () => {
  const isLoggedIn = localStorage.getItem('access_token') !== 'false';

  if (!isLoggedIn) {
    return (
      <div className="ai-restricted">
        <h2>Dostęp zabroniony</h2>
        <p>Ta strona jest dostępna tylko dla zalogowanych użytkowników.</p>
        <Link to="/login" className="login-button">Zaloguj się</Link>
      </div>
    );
  }

  return (
    <div className="ai-container">
      <h1>Model AI do rozpoznawania zwierząt</h1>
      <p>
        Nasz model AI wykorzystuje sieci neuronowe do porównywania zdjęć zgłoszonych zwierząt.
        Dzięki analizie cech fizycznych (kształt pyska, umaszczenie, rozstaw oczu), system potrafi
        dopasować podobne zgłoszenia do siebie. Pomaga to w szybszym odnajdywaniu zaginionych pupili.
      </p>
      <h3>Jak działa model?</h3>
      <ul>
        <li>Analizuje zdjęcie dodane w zgłoszeniu</li>
        <li>Wydobywa cechy obrazu (embedding)</li>
        <li>Porównuje z istniejącymi wpisami w bazie</li>
        <li>Podaje potencjalne dopasowania z najwyższym prawdopodobieństwem</li>
      </ul>
      <p>Model został wytrenowany na bazie tysięcy zdjęć zwierząt i jest stale udoskonalany.</p>
    </div>
  );
};

export default AiModelInfo;
