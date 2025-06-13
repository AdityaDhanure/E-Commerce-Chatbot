import React, { useState } from 'react';
import axios from 'axios'; 
import { useNavigate } from 'react-router-dom';
import '../src/CSS-files/LoginPage.css'; 
import { useAuth } from '../src/AuthContext.jsx'; 

function LoginPage() {
  const navigate = useNavigate();
  const { login } = useAuth();

  // State for Login Form
  const [loginUsername, setLoginUsername] = useState('');
  const [loginPassword, setLoginPassword] = useState('');
  const [loginError, setLoginError] = useState('');

  // State for Signup Form
  const [registerUsername, setRegisterUsername] = useState('');
  const [registerEmail, setRegisterEmail] = useState('');
  const [registerPassword, setRegisterPassword] = useState('');
  const [registerConfirmPassword, setRegisterConfirmPassword] = useState('');
  const [registerError, setRegisterError] = useState('');
  const [registerSuccess, setRegisterSuccess] = useState('');

  // State to toggle between Login and Signup views
  const [isLoginView, setIsLoginView] = useState(true);

  // --- Handle Login ---
  const handleLogin = async (e) => {
    e.preventDefault();
    setLoginError(''); // Clear previous errors
    try {
      const response = await axios.post('http://127.0.0.1:8000/api/token/', {
        username: loginUsername,
        password: loginPassword,
      });

      // Use the login function from AuthContext to set tokens
      login(response.data.access, response.data.refresh);

      console.log('Login successful, redirecting to home.');
      navigate('/'); // Redirect to home/chatbot page
    } catch (err) {
      console.error('Login error:', err);
      // Check if error response has specific messages
      if (err.response && err.response.data && err.response.data.detail) {
        setLoginError(err.response.data.detail);
      } else {
        setLoginError('Invalid username or password. Please try again.');
      }
    }
  };

  // --- Handle Registration ---
  const handleRegister = async (e) => {
    e.preventDefault();
    setRegisterError(''); // Clear previous errors
    setRegisterSuccess(''); // Clear previous success message

    if (registerPassword !== registerConfirmPassword) {
      setRegisterError('Passwords do not match.');
      return;
    }

    try {
      // Step 1: Register the new user
      const registerResponse = await axios.post('http://127.0.0.1:8000/api/register/', {
        username: registerUsername,
        email: registerEmail,
        password: registerPassword,
        password2: registerConfirmPassword, // Backend expects password2
      });
      console.log('Registration successful:', registerResponse.data);
      setRegisterSuccess('Registration successful! Logging you in...');
      setRegisterError(''); // Clear any previous registration errors

      // Step 2: Automatically log in the newly registered user
      const loginResponse = await axios.post('http://127.0.0.1:8000/api/token/', {
        username: registerUsername,
        password: registerConfirmPassword, // Use the confirmed password for login
      });
      console.log('Auto-login successful after registration:', loginResponse.data);

      // Use the login function from AuthContext to set tokens
      login(loginResponse.data.access, loginResponse.data.refresh);

      // Clear registration form fields
      setRegisterUsername('');
      setRegisterEmail('');
      setRegisterPassword('');
      setRegisterConfirmPassword('');
      
      console.log('Registration and auto-login successful, redirecting to home.');
      navigate('/'); // Redirect to home/chatbot page

    } catch (err) {
      console.error('Registration or auto-login error:', err);
      // Handle different types of registration errors from backend
      if (err.response && err.response.data) {
        const errorData = err.response.data;
        let errorMessage = 'Registration failed. Please check your details.';

        // Prioritize specific error messages
        if (errorData.username) {
          errorMessage = errorData.username[0];
        } else if (errorData.email) {
          errorMessage = errorData.email[0];
        } else if (errorData.password) {
          errorMessage = errorData.password[0];
        } else if (errorData.password2) {
          errorMessage = errorData.password2[0];
        } else if (errorData.detail) { // Catch general token errors if auto-login fails
            errorMessage = errorData.detail;
        }
        setRegisterError(errorMessage);
        setRegisterSuccess(''); // Ensure success message is cleared if there's an error
      } else {
        setRegisterError('An unexpected error occurred during registration.');
        setRegisterSuccess('');
      }
    }
  };

  return (
    <div className="auth-container">
      <div className="auth-toggle">
        <button
          className={`toggle-button ${isLoginView ? 'active' : ''}`}
          onClick={() => setIsLoginView(true)}
        >
          Login
        </button>
        <button
          className={`toggle-button ${!isLoginView ? 'active' : ''}`}
          onClick={() => setIsLoginView(false)}
        >
          Sign Up
        </button>
      </div>

      <div className="auth-form-wrapper">
        {isLoginView ? (
          <div className="auth-form login-form">
            <h2>Login</h2>
            <form onSubmit={handleLogin}>
              <div className="form-group">
                <label htmlFor="login-username">Username:</label>
                <input
                  type="text"
                  id="login-username"
                  value={loginUsername}
                  onChange={(e) => setLoginUsername(e.target.value)}
                  required
                />
              </div>
              <div className="form-group">
                <label htmlFor="login-password">Password:</label>
                <input
                  type="password"
                  id="login-password"
                  value={loginPassword}
                  onChange={(e) => setLoginPassword(e.target.value)}
                  required
                />
              </div>
              {loginError && <p className="error-message">{loginError}</p>}
              <button type="submit" className="submit-button">Login</button>
            </form>
          </div>
        ) : (
          <div className="auth-form register-form">
            <h2>Sign Up</h2>
            <form onSubmit={handleRegister}>
              <div className="form-group">
                <label htmlFor="register-username">Username:</label>
                <input
                  type="text"
                  id="register-username"
                  value={registerUsername}
                  onChange={(e) => setRegisterUsername(e.target.value)}
                  required
                />
              </div>
              <div className="form-group">
                <label htmlFor="register-email">Email:</label>
                <input
                  type="email"
                  id="register-email"
                  value={registerEmail}
                  onChange={(e) => setRegisterEmail(e.target.value)}
                  required
                />
              </div>
              <div className="form-group">
                <label htmlFor="register-password">Password:</label>
                <input
                  type="password"
                  id="register-password"
                  value={registerPassword}
                  onChange={(e) => setRegisterPassword(e.target.value)}
                  required
                />
              </div>
              <div className="form-group">
                <label htmlFor="register-confirm-password">Confirm Password:</label>
                <input
                  type="password"
                  id="register-confirm-password"
                  value={registerConfirmPassword}
                  onChange={(e) => setRegisterConfirmPassword(e.target.value)}
                  required
                />
              </div>
              {registerError && <p className="error-message">{registerError}</p>}
              {registerSuccess && <p className="success-message">{registerSuccess}</p>}
              <button type="submit" className="submit-button">Sign Up</button>
            </form>
          </div>
        )}
      </div>
    </div>
  );
}

export default LoginPage;