import { API_URL } from './config';

export const getUserInfo = async () => {
  const token = localStorage.getItem('access_token');
  const response = await fetch(`${API_URL}/user_info/`, {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  });
  return await response.json();
};

export const changePassword = async (oldPassword, newPassword) => {
  const token = localStorage.getItem('access_token');
  const response = await fetch(`${API_URL}/change_password/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify({
      old_password: oldPassword,
      new_password: newPassword
    })
  });
  return await response.json();
};