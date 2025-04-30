import { API_URL } from './config';

export const getRaports = async () => {
  const response = await fetch(`${API_URL}/raports/`);
  return await response.json();
};

export const createRaport = async (formData) => {
  const token = localStorage.getItem('access_token');
  const response = await fetch(`${API_URL}/new_raport/`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`
    },
    body: formData
  });
  return await response.json();
};