const API_URL = 'http://127.0.0.1:8000';

export const registerUser = async (userData) => {
  try {
    const response = await fetch(`${API_URL}/new_user/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(userData)
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.message || 'Registration failed');
    }

    return await response.json();
  } catch (error) {
    console.error('Registration error:', error);
    throw error;
  }
};

export const login = async (email, password) => {
  try {
    const response = await fetch('http://127.0.0.1:8000/login/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        email: email.trim(),
        password: password.trim()
      }),
    });

    const data = await response.json();

    if (!response.ok) {
      return { success: false, detail: data.detail || 'Login failed' };
    }

    return {
      success: true,
      access: data.access,
      refresh: data.refresh,
    };
  } catch (error) {
    console.error('Login error:', error);
    return { success: false, detail: 'Network error' };
  }
};
