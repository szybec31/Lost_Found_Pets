import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import './ConfirmCode.css';

const ConfirmCode = () => {
  const [code, setCode] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleVerify = async () => {
    if (!code || code.length > 10) {
      setError('Kod jest wymagany');
      return;
    }

    try {
      const res = await axios.post('http://localhost:8000/confirm-code/', {
        code: code.trim()
      });

      if (res.data.access && res.data.refresh) {
        localStorage.setItem('access_token', res.data.access);
        localStorage.setItem('refresh_token', res.data.refresh);

        alert('Weryfikacja zakończona sukcesem!');
        navigate('/');
      } else {
        setError('Niepoprawna odpowiedź z serwera');
      }
    } catch (err) {
      console.error(err);
      setError('Niepoprawny kod lub błąd serwera');
    }
  };

  return (
    <div className="container">
      <h2>Weryfikacja kodu</h2>
      <p>Wpisz kod weryfikacyjny otrzymany na e-mail.</p>

      <input
        type="text"
        maxLength="10"
        placeholder="Wpisz kod"
        value={code}
        onChange={(e) => setCode(e.target.value)}
      />
      <button onClick={handleVerify}>Zweryfikuj</button>

      {error && <p style={{ color: 'red' }}>{error}</p>}
    </div>
  );
};

export default ConfirmCode;
