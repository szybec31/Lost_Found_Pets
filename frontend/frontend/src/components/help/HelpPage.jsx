import React from 'react';
import './HelpPage.css';

const HelpPage = () => {
  return (
    <div className="help-container">
      <h1>Jak skutecznie zgłaszać zaginięcie lub znalezienie zwierzęcia</h1>

      <section>
        <h2>1. Co zawrzeć w ogłoszeniu?</h2>
        <ul>
          <li><strong>Imię i gatunek</strong> – np. pies, kot.</li>
          <li><strong>Rasa, umaszczenie, znaki szczególne</strong> – np. obroża, blizny, kolor.</li>
          <li><strong>Gdzie i kiedy</strong> zwierzę zaginęło lub zostało znalezione.</li>
          <li><strong>Kontakt</strong> – numer telefonu lub e-mail.</li>
        </ul>
      </section>

      <section>
        <h2>2. Jak zrobić dobre zdjęcie?</h2>
        <ul>
          <li>Zdjęcie w świetle dziennym, najlepiej z przodu.</li>
          <li>Zbliżenie na twarz lub sylwetkę zwierzęcia.</li>
          <li>Dodaj więcej niż jedno zdjęcie, jeśli to możliwe.</li>
        </ul>
      </section>

      <section>
        <h2>3. Znalazłeś zwierzę?</h2>
        <p>Jeśli znalazłeś zwierzę, które wygląda na zagubione:</p>
        <ul>
          <li>Sprawdź, czy ma adresatkę, chip lub tatuaż.</li>
          <li>Zgłoś je do weterynarza lub schroniska – mają skanery chipów.</li>
          <li>Dodaj ogłoszenie na stronie jako <strong>„Znalezione”</strong>.</li>
        </ul>
      </section>

      <p className="footer-note">
        Twoje zgłoszenie może pomóc komuś odzyskać ukochanego pupila 💚
      </p>
    </div>
  );
};

export default HelpPage;
