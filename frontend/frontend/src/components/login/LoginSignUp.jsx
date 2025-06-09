import React, { useState } from 'react';
import './LoginSignUp.css';
import { Link, useNavigate } from 'react-router-dom';

import user_icon from '../assets/person.png';
import email_icon from '../assets/email.png';
import password_icon from '../assets/password.png';

const LoginSignUp = () => {
  const [action, setAction] = useState("Login");
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    first_name: '',
    last_name: '',
    phone: ''
  });

  const navigate = useNavigate();

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: name === "phone" ? Number(value) : value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      if (action === "Sign Up") {
        const res = await fetch("http://127.0.0.1:8000/new_user/", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(formData),
        });

        const data = await res.json();

        if (res.ok) {
          alert("Rejestracja zakończona! Sprawdź email.");
          setAction("Login");
        } else {
          alert(data.detail || "Rejestracja nie powiodła się.");
        }

      } else {
        const res = await fetch("http://127.0.0.1:8000/login/", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            email: formData.email,
            password: formData.password
          }),
        });

        const data = await res.json();

        if (res.ok) {
          alert("Kod weryfikacyjny został wysłany na email.");
          navigate("/confirm-code/", { state: { email: formData.email } });
        } else {
          alert(data.detail || "Logowanie nie powiodło się.");
        }
      }
    } catch (error) {
      console.error("Błąd:", error);
      alert("Coś poszło nie tak.");
    }
  };

  const toggleAction = () => {
    setAction(prev => (prev === "Login" ? "Sign Up" : "Login"));
  };

  return (
    <div className='container'>
      <Link to="/" className="back-button">Back</Link>
      <div className="header">
        <div className="text">{action}</div>
        <div className="underline"></div>
      </div>
      <form className="inputs" onSubmit={handleSubmit}>
        {action === "Sign Up" && (
          <>
            <div className="input">
              <img src={user_icon} alt="" />
              <input
                type="text"
                name="first_name"
                placeholder="First Name"
                onChange={handleChange}
                required
              />
            </div>
            <div className="input">
              <img src={user_icon} alt="" />
              <input
                type="text"
                name="last_name"
                placeholder="Last Name"
                onChange={handleChange}
                required
              />
            </div>
            <div className="input">
              <img src={user_icon} alt="" />
              <input
                type="text"
                name="phone"
                placeholder="Phone"
                onChange={handleChange}
                required
              />
            </div>
          </>
        )}
        <div className="input">
          <img src={email_icon} alt="" />
          <input
            type="email"
            name="email"
            placeholder="Email"
            onChange={handleChange}
            required
          />
        </div>
        <div className="input">
          <img src={password_icon} alt="" />
          <input
            type="password"
            name="password"
            placeholder="Password"
            onChange={handleChange}
            required
          />
        </div>

        {action === "Login" && (
          <div className="forgot-password">
            Forgot Password?<span> Click Here</span>
          </div>
        )}

        <button
          className="submit"
          style={{ margin: '20px auto', width: '480px' }}
          type="submit"
        >
          {action === "Login" ? "Login" : "Sign Up"}
        </button>
      </form>

      <div className="toggle-action">
        {action === "Login"
          ? "Don't have an account? "
          : "Already have an account? "}
        <span className="auth-toggle-link" onClick={toggleAction}>
          {action === "Login" ? "Sign Up" : "Login"}
        </span>
      </div>
    </div>
  );
};

export default LoginSignUp;
