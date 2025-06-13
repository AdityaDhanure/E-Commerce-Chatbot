import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'
import { AuthProvider } from './AuthContext'; 
import { BrowserRouter as Router } from 'react-router-dom';

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <Router> {/* Wrap your App component with Router for routing */}
      <AuthProvider> {/* Wrap your App component with AuthProvider */}
        <App />
      </AuthProvider>
    </Router>
  </StrictMode>,
)
