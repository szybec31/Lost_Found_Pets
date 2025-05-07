import './App.css';
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import LoginSignUp from './components/login/LoginSignUp';
import HomePage from './pages/HomePage';
import AddLostAnimal from './components/form/AddLostAnimal';
import UserProfile from './components/user/UserProfile'; 
import AiModelInfo from './components/AI/AiModelInfo';
import ReportsPage from './components/reports/ReportsPage'; 
import ProtectedRoute from './components/login/ProtectedRoute';
import MenuDropdown from './components/menu/MenuDropdown';
import HelpPage from './components/help/HelpPage';

function App() {
  return (
    <div className="App">
      <Router>
        <nav className="main-navbar">
          <h2 className="logo">Lost & Found Pets</h2>
          <MenuDropdown />
        </nav>
        <Routes>
          <Route path="/help" element={<HelpPage />} />
          <Route path="/login" element={<LoginSignUp />} />
          <Route path="/" element={<HomePage />} />
          <Route path="/ai-model" element={<AiModelInfo />} /> {/* Dostępna dla wszystkich */}
          <Route path="/reports" element={<ReportsPage />} />   {/* Dostępna dla wszystkich */}
          <Route
            path="/add"
            element={
              <ProtectedRoute>
                <AddLostAnimal />
              </ProtectedRoute>
            }
          />
          <Route
            path="/profile"
            element={
              <ProtectedRoute>
                <UserProfile />
              </ProtectedRoute>
            }
          />
        </Routes>
      </Router>
    </div>
  );
}

export default App;
