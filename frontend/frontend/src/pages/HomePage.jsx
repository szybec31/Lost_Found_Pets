import React from 'react';
import { Link } from 'react-router-dom';
import './HomePage.css';

const HomePage = () => {
    const isLoggedIn = localStorage.getItem('access_token');

    return(
        <div className="home-container">
            <header className="home-header">
                <h1>Lost Found Pets</h1>
                <p>memle</p>
                {!isLoggedIn && (
                    <div className="header-login-button">
                        <Link to="/login" className="login-button">Login</Link>
                    </div>
                )}
            </header>

            <main className="home-main">
                {isLoggedIn ? (
                    <div>
                        <h2>Welcome!</h2>
                        <Link to="/reports" className="login-button">View Reports</Link>
                    </div>
                ) : (
                    <Link to="/login" className="login-button">Login / Register</Link>
                )}
            </main>

            <footer className="home-footer">
            </footer>
        </div>
    );
};

export default HomePage;