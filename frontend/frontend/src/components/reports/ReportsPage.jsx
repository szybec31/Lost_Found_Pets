import React, { useEffect, useState } from 'react';
import './ReportsPage.css'; // opcjonalny styl

const ReportsPage = () => {
  const [reports, setReports] = useState([]);
  const [filter, setFilter] = useState('all');

  useEffect(() => {
    fetch('/api/reports') // podmień na swój endpoint
      .then((res) => res.json())
      .then((data) => setReports(data))
      .catch((err) => console.error(err));
  }, []);

  const filteredReports = reports.filter(report => {
    if (filter === 'all') return true;
    return report.status === filter;
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
            <img src={report.imageUrl} alt={report.name} />
            <h3>{report.name}</h3>
            <p>{report.description}</p>
            <p>Status: <strong>{report.status}</strong></p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ReportsPage;
