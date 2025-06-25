import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import axios from 'axios';
import './ReportDetail.css';

const BASE_URL = 'http://127.0.0.1:8000';

const ReportDetail = () => {
  const { id } = useParams();
  const [report, setReport] = useState(null);
  const [error, setError] = useState(null);
  const [similarReports, setSimilarReports] = useState([]);
  const [loadingSimilar, setLoadingSimilar] = useState(false);
  const [compareError, setCompareError] = useState(null);
  const [linkSuccess, setLinkSuccess] = useState(null);
  const [linkError, setLinkError] = useState(null);

  const token = localStorage.getItem('access_token');

  useEffect(() => {
    axios.get(`${BASE_URL}/user_raport/${id}/`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })
  .then(response => {
    console.log("Raport z API:", response.data);
    setReport(response.data);
  })
  .catch(err => {
    console.error("Błąd podczas pobierania szczegółów:", err);
    setError('Nie udało się pobrać szczegółów.');
  });
  }, [id, token]);

  const handleCompare = async () => {
  setLoadingSimilar(true);
  setCompareError(null);
  setSimilarReports([]);

  try {
    const res = await axios.get(`${BASE_URL}/user_raport/${id}/?compare=true`, {
      headers: { Authorization: `Bearer ${token}` },
    });

    console.log("Odpowiedź z API:", res.data); 


    if (Array.isArray(res.data.comparison_results) && res.data.comparison_results.length > 0) {
      const enrichedSimilarReports = res.data.comparison_results.map(item => ({
        ...item,
        raport_type: item.raport_type || 'Unknown',
        animal_type: item.animal_type || 'Unknown',
        date_added: item.date_added || new Date().toISOString(),
        similarity: item.similarity ?? null
      }));
      
      setSimilarReports(enrichedSimilarReports.slice(0, 3));
    } else {
      setCompareError('Brak podobnych zgłoszeń.');
    }
  } catch (err) {
    console.error("Błąd porównywania:", err.response?.data || err);
    setCompareError(err.response?.data?.message || 'Nie udało się znaleźć podobnych zgłoszeń.');
  } finally {
    setLoadingSimilar(false);
  }
};


  const handleLinkRaports = async (matchedId) => {
    setLinkSuccess(null);
    setLinkError(null);

    try {
      const response = await axios.post(`${BASE_URL}/link-raports/`, {
        raport_id_1: id,
        raport_id_2: matchedId,
      }, {
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      });

      setLinkSuccess(response.data.message || 'Pomyślnie połączono zgłoszenia');
    } catch (err) {
      console.error("Błąd podczas łączenia:", err);
      const msg = err.response?.data?.error || "Nie udało się połączyć zgłoszeń.";
      setLinkError(msg);
    }
  };

  if (error) return <div className="error-message">{error}</div>;
  if (!report) return <div>Ładowanie...</div>;

  console.log("Dane raportu:", report);

  return (
    <div className="report-detail-container">
      {report.is_owner && (
        <Link to={`/raport/${id}/edit`} className="edit-button">
          Edytuj zgłoszenie
        </Link>
      )}
      <h2>Szczegóły zgłoszenia</h2>
      <div className="report-info">
        <p><strong>ID:</strong> {report.id}</p>
        <p><strong>Typ:</strong> {report.raport_type}</p>
        <p><strong>Zwierzę:</strong> {report.animal_type}</p>
        <p><strong>Numer kontaktowy:</strong> {report.user.phone}</p>
        <p><strong>Opis:</strong> {report.description || 'Brak opisu'}</p>
        <p><strong>Email kontaktowy:</strong> {report.user.email}</p>
                <p><strong>Data:</strong> {new Date(report.date_added).toLocaleString()}</p>
      </div>

      {report.images && report.images.length > 0 && (
        <div className="image-gallery">
          <h3>Zdjęcia:</h3>
          <div className="images-grid">
            {report.images.map((img) => (
              <div key={img.id} className="image-container">
                <img src={img.image} alt="Zdjęcie zgłoszenia" />
              </div>
            ))}
          </div>
        </div>
      )}

      <div className="report-actions">

        <button 
          onClick={handleCompare} 
          className="compare-button"
          disabled={loadingSimilar}
        >
          {loadingSimilar ? 'Wyszukiwanie...' : 'Znajdź podobne'}
        </button>
      </div>

      {loadingSimilar && <p className="loading-message">Szukam podobnych zgłoszeń...</p>}
      {compareError && <p className="error-message">{compareError}</p>}
      {linkSuccess && <p className="success-message">{linkSuccess}</p>}
      {linkError && <p className="error-message">{linkError}</p>}

      {similarReports.length > 0 && (
        <div className="similar-reports">
          <h3>Podobne zgłoszenia:</h3>
          <div className="similar-grid">
            {similarReports.map((rep) => (
              <div key={`${rep.id}-${rep.image}`} className="similar-card">
                <img src={`${BASE_URL}${rep.image}`} alt="Podobne zgłoszenie" />
                <div className="similar-info">
                  <p><strong>ID raportu:</strong> {rep.id}</p>
                  <p><strong>Typ:</strong> {rep.raport_type}</p>
                  <p><strong>Zwierzę:</strong> {rep.animal_type}</p>
                  <p><strong>Podobieństwo:</strong> {rep.similarity ? `${rep.similarity.toFixed(2)}%` : 'Brak danych'}</p>
                  <p><strong>Data:</strong> {new Date(rep.date_added).toLocaleDateString()}</p>
                </div>
                <div className="similar-actions">
                  <Link to={`/raport/${rep.id}`} className="details-button">Zobacz szczegóły</Link>
                  <button 
                    onClick={() => handleLinkRaports(rep.id)} 
                    className="link-button"
                  >
                    Połącz zgłoszenia
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default ReportDetail;