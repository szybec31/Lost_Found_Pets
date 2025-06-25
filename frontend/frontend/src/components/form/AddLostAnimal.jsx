import React, { useState } from 'react';
import axios from 'axios';
import './AddLostAnimal.css';
import { useNavigate } from 'react-router-dom';


const AddLostAnimal = () => {
  const [animalType, setAnimalType] = useState('');
  const [description, setDescription] = useState('');
  const [images, setImages] = useState(null);
  const [raportType, setRaportType] = useState('');
  const [district, setDistrict] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();

    const formData = new FormData();
    formData.append('raport_type', String(raportType));
formData.append('animal_type', String(animalType));
    formData.append('description', description);
    if (district) formData.append('district', district);

    if (images && images.length > 0) {
      for (let i = 0; i < images.length; i++) {
        formData.append('uploaded_images', images[i]);
      }
    }

    const token = localStorage.getItem('access_token');

    try {
      const response = await axios.post('http://127.0.0.1:8000/new_raport/', formData, {
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'multipart/form-data',
        },
      });

      alert('Zgłoszenie dodane!');
      console.log('Odpowiedź:', response.data);

      setAnimalType('');
      setDescription('');
      setImages(null);
      setRaportType('');
      setDistrict('');
      navigate('/');
    } catch (error) {
      console.error('Błąd przy dodawaniu zgłoszenia:', error.response?.data || error);
      alert('Wystąpił błąd podczas dodawania zgłoszenia.');
    }
  };

  return (
    <div className="form-container">
      <h2>Dodaj zgłoszenie (Zaginione / Znalezione)</h2>
      <form onSubmit={handleSubmit}>
        <select value={raportType} onChange={(e) => setRaportType(e.target.value)} required>
          <option value="">-- Wybierz typ zgłoszenia --</option>
          <option value="Lost">Zaginione</option>
          <option value="Found">Znalezione</option>
        </select>

        <select value={animalType} onChange={(e) => setAnimalType(e.target.value)} required>
          <option value="">-- Wybierz zwierzę --</option>
          <option value="Dog">Pies</option>
          <option value="Cat">Kot</option>
        </select>

        <textarea
          placeholder="Opis"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          required
        />

        <input
          type="text"
          placeholder="Lokalizacja"
          value={district}
          onChange={(e) => setDistrict(e.target.value)}
        />

        <input
          type="file"
          accept="image/*"
          multiple
          onChange={(e) => setImages(e.target.files)}
        />

        <button type="submit">Wyślij</button>
      </form>
    </div>
  );
};

export default AddLostAnimal;
