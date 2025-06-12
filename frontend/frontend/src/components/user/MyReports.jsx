import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './MyReports.css';

const BASE_URL = 'http://127.0.0.1:8000';

const MyReports = () => {
  const [reports, setReports] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem('access_token');

    if (!token) {
      setError('Brak tokenu. Zaloguj się ponownie.');
      setLoading(false);
      return;
    }

    fetch(`${BASE_URL}/user_raports/`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${token}`,
      },
    })
      .then((res) => {
        if (!res.ok) {
          throw new Error('Nie udało się pobrać zgłoszeń użytkownika.');
        }
        return res.json();
      })
      .then((data) => {
        setReports(data);
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message);
        setLoading(false);
      });
  }, []);

  if (loading) return <p>Ładowanie zgłoszeń...</p>;
  if (error) return <p>Błąd: {error}</p>;

  return (
    <div className="my-reports-container">
      <h2>Moje zgłoszenia</h2>
      {reports.length === 0 ? (
        <p>Brak zgłoszeń</p>
      ) : (
        <div className="reports-list">
          {reports.map((report) => (
            <div key={report.id} className="report-card">
              {report.images && report.images.length > 0 && (
                <img
                  src={BASE_URL + report.images[0].image}
                  alt={`Zgłoszenie ${report.id}`}
                />
              )}

              <h3>{report.animal_type}</h3>
              <p><strong>Typ:</strong> {report.raport_type}</p>
              <p><strong>Data:</strong> {new Date(report.date_added).toLocaleString()}</p>
              <p><strong>Opis:</strong> {report.description}</p>

              <button onClick={() => navigate(`/raport/${report.id}`)}>
                Szczegóły
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default MyReports;
