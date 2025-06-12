import React, { useState } from 'react';
import './ChangePassword.css';

const BASE_URL = 'http://127.0.0.1:8000';

const ChangePassword = () => {
  const [oldPassword, setOldPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');

  const handleChangePassword = async (e) => {
    e.preventDefault();
    setMessage('');
    setError('');

    const token = localStorage.getItem('access_token');
    if (!token) {
      setError('Brak tokenu. Zaloguj się ponownie.');
      return;
    }

    try {
      const response = await fetch(`${BASE_URL}/change_password/`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          old_password: oldPassword,
          new_password: newPassword,
        }),
      });

      const data = await response.json();

      if (response.ok) {
        setMessage(data.detail);
        setOldPassword('');
        setNewPassword('');
      } else {
        setError(data.detail || 'Błąd podczas zmiany hasła.');
      }
    } catch (err) {
      console.error(err);
      setError('Wystąpił błąd sieci.');
    }
  };

  return (
    <div className="change-password-container">
      <h2>Zmiana hasła</h2>
      <form onSubmit={handleChangePassword} className="change-password-form">
        <label>
          Stare hasło:
          <input
            type="password"
            value={oldPassword}
            onChange={(e) => setOldPassword(e.target.value)}
            required
          />
        </label>
        <label>
          Nowe hasło:
          <input
            type="password"
            value={newPassword}
            onChange={(e) => setNewPassword(e.target.value)}
            required
          />
        </label>
        <button type="submit">Zmień hasło</button>
      </form>
      {message && <p className="success">{message}</p>}
      {error && <p className="error">{error}</p>}
    </div>
  );
};

export default ChangePassword;
