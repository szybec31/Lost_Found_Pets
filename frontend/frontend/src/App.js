import './App.css';
import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import LoginSignUp from './components/login/LoginSignUp';
import ConfirmCode from './components/login/ConfirmCode';
import HomePage from './pages/HomePage';
import AddLostAnimal from './components/form/AddLostAnimal';
import UserProfile from './components/user/UserProfile';
import MyReports from './components/user/MyReports';
import AiModelInfo from './components/AI/AiModelInfo';
import ReportsPage from './components/reports/ReportsPage';
import RaportDetails from './components/reports/ReportDetail';
import ProtectedRoute from './components/login/ProtectedRoute';
import MenuDropdown from './components/menu/MenuDropdown';
import HelpPage from './components/help/HelpPage';
import ChangePassword from './components/user/ChangePassword';
import EditRaport from './components/reports/EditReport';
import SimilarRaports from './components/reports/ReportDetail'

function App() {
  return (
    <div className="page-layout">
      <Router>
        <header>
        <nav className="main-navbar">
          <Link to="/" className="logo">Lost & Found Pets</Link>
          <MenuDropdown />
        </nav>
        </header>
        <main className="page-content">
          <Routes>
            <Route path="/help" element={<HelpPage />} />
            <Route path="/login" element={<LoginSignUp />} />
            <Route path="/confirm-code/" element={<ConfirmCode />} />
            <Route path="/" element={<HomePage />} />
            <Route path="/ai-model" element={<AiModelInfo />} />
            <Route path="/reports" element={<ReportsPage />} />
            <Route path="/user_reports/" element={<MyReports />} />
            <Route path="/raport/:id" element={<RaportDetails />} />
            <Route path="/raport/:id/similar" element={<SimilarRaports />} />
            <Route
              path="/raport/:id/edit"
              element={
                <ProtectedRoute>
                  <EditRaport />
                </ProtectedRoute>
              }
            />
            <Route
              path="/change-password"
              element={
                <ProtectedRoute>
                  <ChangePassword />
                </ProtectedRoute>
              }
            />
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
        </main>

        <footer className="home-footer">
          <p>&copy; 2025 LostFoundPets</p>
          <p>Projekt stworzony w ramach pracy Projektu Zespołowego</p>
        </footer>
      </Router>
    </div>
  );
}

export default App;
