import React, { useState, useRef, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import './MenuDropdown.css';

const MenuDropdown = () => {
  const [isOpen, setIsOpen] = useState(false);
  const menuRef = useRef();
  const navigate = useNavigate();

  const toggleMenu = () => setIsOpen(prev => !prev);

  const isLoggedIn = !!localStorage.getItem('access_token');

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('user_email');
    setIsOpen(false);
    navigate('/login');
  };

  const handleLogin = () => {
    setIsOpen(false);
    navigate('/login');
  };

  useEffect(() => {
    const handleClickOutside = (e) => {
      if (menuRef.current && !menuRef.current.contains(e.target)) {
        setIsOpen(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  return (
    <div className="menu-dropdown" ref={menuRef}>
      <button className="dots-button" onClick={toggleMenu}>⋮</button>
      {isOpen && (
        <div className="menu-content">
          <Link to="/" onClick={() => setIsOpen(false)}>Strona główna</Link>
          <Link to="/reports" onClick={() => setIsOpen(false)}>Zgłoszenia</Link>
          <Link to="/profile" onClick={() => setIsOpen(false)}>Profil</Link>
          <Link to="/help" onClick={() => setIsOpen(false)}>Pomoc</Link>

          {isLoggedIn ? (
            <button onClick={handleLogout} className="logout-button">Wyloguj się</button>
          ) : (
            <button onClick={handleLogin} className="logout-button">Zaloguj się</button>
          )}
        </div>
      )}
    </div>
  );
};

export default MenuDropdown;
