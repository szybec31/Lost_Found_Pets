import React, { useState } from 'react'
import './LoginSignUp.css'
import { Link, useNavigate } from 'react-router-dom';
import { registerUser, login } from '../../api/auth';

import user_icon from '../assets/person.png'
import email_icon from '../assets/email.png'
import password_icon from '../assets/password.png'

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
    setFormData({
      ...formData,
      [e.target.name]: e.target.name === "phone" ? Number(e.target.value) : e.target.value
    });
  };

  const handleSubmit = async () => {
    try {
      if (action === "Sign Up") {
        await registerUser(formData);
        await login(formData.email, formData.password);
      } else {
        await login(formData.email, formData.password);
      }
      console.log(formData);
      navigate('/');
    } catch (error) {
      console.error('Error:', error);
      alert(action === "Sign Up" ? 'Registration failed' : 'Login failed');
    }
  };

  const toggleAction = () => {
    setAction(prev => prev === "Login" ? "Sign Up" : "Login");
  };

  return (
    <div className='container'>
      <Link to="/" className="back-button">Back</Link>
      <div className="header">
        <div className="text">{action}</div>
        <div className="underline"></div>
      </div>
      <div className="inputs">
        {action === "Sign Up" && (
          <>
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
          </>
        )}        
        <div className="input">
          <img src={email_icon} alt="" />
          <input 
            type="email" 
            name="email"
            placeholder='Email' 
            onChange={handleChange}
            required
          />
        </div>
        <div className="input">
          <img src={password_icon} alt="" />
          <input 
            type="password" 
            name="password"
            placeholder='Password' 
            onChange={handleChange}
            required
          />
        </div>
      </div>
      
      {action === "Login" && (
        <div className="forgot-password">
          Forgot Password?<span> Click Here</span>
        </div>
      )}
      
      <div 
        className="submit" 
        style={{ margin: '20px auto', width: '480px' }}
        onClick={handleSubmit}
      >
        {action === "Login" ? "Login" : "Sign Up"}
      </div>
      
      <div className="toggle-action">
        {action === "Login" 
          ? "Don't have an account? " 
          : "Already have an account? "}
        <span onClick={toggleAction}>
          {action === "Login" ? "Sign Up" : "Login"}
        </span>
      </div>
    </div>
  );
};

export default LoginSignUp;