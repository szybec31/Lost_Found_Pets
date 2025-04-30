const API_URL = 'http://127.0.0.1:8000';

export const registerUser = async (userData) => {
  const response = await fetch(`${API_URL}/new_user/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(userData)
  });
  return await response.json();
};

export const login = async (email, password) => {
  const response = await fetch(`${API_URL}/login/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ email, password })
  });
  const data = await response.json();
  localStorage.setItem('access_token', data.access);
  localStorage.setItem('refresh_token', data.refresh);
  return data;
};