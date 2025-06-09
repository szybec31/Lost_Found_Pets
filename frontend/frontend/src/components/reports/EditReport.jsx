import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import './EditReport.css'

console.log('Komponent EditRaport działa!');

const EditRaport = () => {
  const { id } = useParams();
  const navigate = useNavigate();

  const [formState, setFormState] = useState({
    raport_type: '',
    animal_type: '',
    description: '',
    district: '',
  });

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchRaport = async () => {
      try {
        const res = await fetch(`http://localhost:8000/user_raport/${id}/`, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('access_token')}`,
          },
        });

        if (!res.ok) throw new Error('Nie udało się pobrać danych raportu.');

        const data = await res.json();

        setFormState({
          raport_type: data.raport_type,
          animal_type: data.animal_type,
          description: data.description,
          district: data.district || '',
        });

        setLoading(false);
      } catch (err) {
        setError(err.message);
        setLoading(false);
      }
    };

    fetchRaport();
  }, [id]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormState((prev) => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const patchRes = await fetch(`http://localhost:8000/update_user_raport/${id}/`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${localStorage.getItem('access_token')}`,
        },
        body: JSON.stringify(formState),
      });

      if (!patchRes.ok) {
        alert('Błąd podczas aktualizacji.');
        return;
      }

      alert('Zgłoszenie zostało zaktualizowane.');
      navigate('/user_reports/');
    } catch (err) {
      alert('Błąd połączenia.');
      console.error(err);
    }
  };

  if (loading) return <p>Ładowanie...</p>;
  if (error) return <p>{error}</p>;

  return (
    <div className="edit-raport-container">
      <h2>Edytuj Zgłoszenie</h2>
      <form onSubmit={handleSubmit} className="edit-raport-form">
        <label>
          Typ zgłoszenia:
          <select name="raport_type" value={formState.raport_type} onChange={handleChange}>
            <option value="Lost">Zaginione</option>
            <option value="Found">Znalezione</option>
          </select>
        </label>

        <label>
          Zwierzę:
          <select name="animal_type" value={formState.animal_type} onChange={handleChange}>
            <option value="Cat">Kot</option>
            <option value="Dog">Pies</option>
          </select>
        </label>

        <label>
          Dzielnica:
          <input type="text" name="district" value={formState.district} onChange={handleChange} />
        </label>

        <label>
          Opis:
          <textarea name="description" value={formState.description} onChange={handleChange} rows="4" />
        </label>

        <button type="submit" className="submit">Zapisz zmiany</button>
      </form>
    </div>
  );
};

export default EditRaport;
