import React, { useState } from 'react';
import axios from 'axios';

const AddLostAnimal = () => {
  const [name, setName] = useState('');
  const [desc, setDesc] = useState('');
  const [image, setImage] = useState(null);
  const [type, setType] = useState('lost'); // lost / found

  const handleSubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append('name', name);
    formData.append('description', desc);
    formData.append('type', type);
    formData.append('image', image);

    // konfiguracja endpointu backendu
    await axios.post('http://localhost:8000/new_raport/', formData);

    alert('Zgłoszenie dodane!');
  }

  return (
    <div className="form-container">
      <h2>Add Lost/Found Pet</h2>
      <form onSubmit={handleSubmit}>
        <select value={type} onChange={(e) => setType(e.target.value)}>
          <option value="lost">Lost</option>
          <option value="found">Found</option>
        </select>
        <input type="text" placeholder="Pet Name" onChange={(e) => setName(e.target.value)} required />
        <textarea placeholder="Description" onChange={(e) => setDesc(e.target.value)} required />
        <input type="file" accept="image/*" onChange={(e) => setImage(e.target.files[0])} required />

        <button type="submit">Submit</button>
      </form>
    </div>
  );
};

export default AddLostAnimal;
