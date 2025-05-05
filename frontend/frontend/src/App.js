import './App.css';
import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import HomePage from './pages/HomePage';
import LoginSignUp from './components/login/LoginSignUp';
import AddLostAnimal from './components/form/AddLostAnimal';
import UserProfile from './components/user/UserProfile'; 

  function App() {
    return (
      <div className="App">
       <Router>
        //dla weryfikacji poprawności działania
        <nav>
          <Link to="/">Home</Link> | 
          <Link to="/add">Dodaj zwierzę</Link> | 
          <Link to="/profile">Profil</Link>
        </nav>

        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/login" element={<LoginSignUp />} />
          <Route path="/add" element={<AddLostAnimal />} />
          <Route path="/profile" element={<UserProfile />} />
        </Routes>
      </Router>
      </div>
    );
  }

export default App;
