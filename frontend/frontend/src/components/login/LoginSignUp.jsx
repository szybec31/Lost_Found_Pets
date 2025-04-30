import React, { useState } from 'react'
import './LoginSignUp.css'
import { Link, useNavigate } from 'react-router-dom';
import { registerUser, login } from '../../api/auth';

import user_icon from '../assets/person.png'
import email_icon from '../assets/email.png'
import password_icon from '../assets/password.png'

const LoginSignUp = () => {
  const [action, setAction] = useState("Sign Up");
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    first_name: '',
    last_name: '',
    phone: ''
  });
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async () => {
    try {
      if (action === "Sign Up") {
        await registerUser(formData);
        // Po rejestracji automatyczne logowanie
        await login(formData.email, formData.password);
      } else {
        await login(formData.email, formData.password);
      }
      navigate('/'); // Przekierowanie po udanej autentykacji
    } catch (error) {
      console.error('Error:', error);
      alert(action === "Sign Up" ? 'Registration failed' : 'Login failed');
    }
  };

  return (
    <div className='container'>
      <Link to="/" className="back-button">Back</Link>
      <div className="header">
        <div className="text">{action}</div>
        <div className="underline"></div>
      </div>
      <div className="inputs">
        {action==="Login"?<div></div>:<>
          <div className="input">
            <img src={user_icon} alt="" />
            <input 
              type="text" 
              name="first_name"
              placeholder='First Name' 
              onChange={handleChange}
            />
          </div>
          <div className="input">
            <img src={user_icon} alt="" />
            <input 
              type="text" 
              name="last_name"
              placeholder='Last Name' 
              onChange={handleChange}
            />
          </div>
          <div className="input">
            <img src={user_icon} alt="" />
            <input 
              type="text" 
              name="phone"
              placeholder='Phone' 
              onChange={handleChange}
            />
          </div>
        </>}        
        <div className="input">
          <img src={email_icon} alt="" />
          <input 
            type="email" 
            name="email"
            placeholder='Email' 
            onChange={handleChange}
          />
        </div>
        <div className="input">
          <img src={password_icon} alt="" />
          <input 
            type="password" 
            name="password"
            placeholder='Password' 
            onChange={handleChange}
          />
        </div>
      </div>
      {action==="Sign Up"?<div></div>:<div className="forgot-password">Forgot Password?<span> Click Here</span></div>}
      <div className="submit-container">
        <div 
          className={action==="Login"?"submit gray":"submit"} 
          onClick={()=>{setAction("Sign Up")}}
        >
          Sign Up
        </div>
        <div 
          className={action==="Sign Up"?"submit gray":"submit"} 
          onClick={()=>{setAction("Login")}}
        >
          Login
        </div>
      </div>
      <div 
        className="submit" 
        style={{ margin: '20px auto', width: '480px' }}
        onClick={handleSubmit}
      >
        {action === "Login" ? "Login" : "Sign Up"}
      </div>
    </div>
  );
};

export default LoginSignUp;