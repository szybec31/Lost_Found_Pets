import React from 'react';
import './UserProfile.css';

const UserProfile = () => {
  const userEmail = localStorage.getItem('user_email') || 'example@email.com';

  return (
    <div className="profile-container">
      <h2>Twój profil</h2>
      <div className="profile-card">
        <p><strong>Email:</strong> {userEmail}</p>
        <p><strong>Typ konta:</strong> Użytkownik</p>
        <p><strong>Liczba zgłoszeń:</strong> 0 (placeholder)</p>
      </div>
    </div>
  );
};

export default UserProfile;