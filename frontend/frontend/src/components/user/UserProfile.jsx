import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './UserProfile.css';

const BASE_URL = 'http://127.0.0.1:8000';

const UserProfile = () => {
  const [userInfo, setUserInfo] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const navigate = useNavigate(); 

  useEffect(() => {
    const token = localStorage.getItem('access_token');

    if (!token) {
      setError('Brak tokenu. Zaloguj się ponownie.');
      setLoading(false);
      return;
    }

    fetch(`${BASE_URL}/user_info/`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
    })
      .then((res) => {
        if (!res.ok) throw new Error('Nie udało się pobrać danych użytkownika.');
        return res.json();
      })
      .then((data) => {
        setUserInfo(data);
        setLoading(false);
      })
      .catch((err) => {
        console.error(err);
        setError('Błąd ładowania profilu użytkownika.');
        setLoading(false);
      });
  }, []);

  if (loading) return <p>Ładowanie profilu...</p>;
  if (error) return <p style={{ color: 'red' }}>{error}</p>;

  return (
    <div className="profile-container">
      <h2>Twój profil</h2>
      <div className="profile-card">
        <p><strong>Email:</strong> {userInfo.email}</p>
        <p><strong>Imię:</strong> {userInfo.first_name}</p>
        <p><strong>Nazwisko:</strong> {userInfo.last_name}</p>
        <p><strong>Telefon:</strong> {userInfo.phone}</p>
        <p><strong>Data rejestracji:</strong> {new Date(userInfo.date_joined).toLocaleString()}</p>
      </div>

      <button
        className="change-password-button"
        onClick={() => navigate('/change-password')}
      >
        Zmień hasło
      </button>
    </div>
  );
};

export default UserProfile;
