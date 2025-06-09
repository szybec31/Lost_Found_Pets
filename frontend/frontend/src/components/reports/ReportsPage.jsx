import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './ReportsPage.css';

const BASE_URL = 'http://127.0.0.1:8000';

const ReportsPage = () => {
  const [reports, setReports] = useState([]);
  const [filter, setFilter] = useState('all');
  const navigate = useNavigate(); 

  useEffect(() => {
    fetch(`${BASE_URL}/raports/`)
      .then((res) => res.json())
      .then((data) => {
        const formatted = data.map((item) => ({
          ...item,
          imageUrl: Array.isArray(item.image)
            ? `${BASE_URL}${item.image[0]}`
            : `${BASE_URL}${item.image}`,
        }));
        setReports(formatted);
      })
      .catch((err) => console.error('Błąd podczas pobierania zgłoszeń:', err));
  }, []);

  const filteredReports = reports.filter((report) => {
    if (filter === 'all') return true;
    if (filter === 'zaginione') return report.raport_type === 'Lost';
    if (filter === 'odnalezione') return report.raport_type === 'Found';
    return true;
  });

  return (
    <div className="reports-container">
      <h2>Zgłoszenia</h2>

      <div className="filter-buttons">
        <button onClick={() => setFilter('all')}>Wszystkie</button>
        <button onClick={() => setFilter('zaginione')}>Zaginione</button>
        <button onClick={() => setFilter('odnalezione')}>Odnalezione</button>
      </div>

      <div className="reports-list">
        {filteredReports.map((report) => (
          <div key={report.id} className="report-card">
            <img
              src={report.imageUrl}
              alt={`Zgłoszenie ${report.id}`}
            />
            <h3>{report.animal_type}</h3>
            <p><strong>Typ:</strong> {report.raport_type}</p>
            <p><strong>Data:</strong> {new Date(report.date_added).toLocaleString()}</p>
            <button onClick={() => navigate(`/raport/${report.id}`)}>
              Szczegóły
            </button>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ReportsPage;
