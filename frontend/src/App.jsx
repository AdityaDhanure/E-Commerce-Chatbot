import React, {useEffect} from 'react'; 
import { BrowserRouter as Router, Routes, Route, Link, useNavigate } from 'react-router-dom'; 
import ChatbotPage from '../pages/ChatbotPage.jsx';
import LoginPage from '../pages/LoginPage.jsx';
import ProductSearchPage from '../pages/ProductSearchPage.jsx';
import { useAuth } from './AuthContext.jsx'; 
import './CSS-files/App.css'; 

function App() {
  const { isAuthenticated, user, logout } = useAuth(); 
  const navigate = useNavigate(); 

  useEffect(() => {
    if (!isAuthenticated && window.location.pathname !== '/login') {
      navigate('/login');
    }
  }, [isAuthenticated, navigate]); 

  const handleLogout = () => {
    logout(); 
  };

  return (
    <>
      <div className="App">
        <header className="App-header">
          <nav>
            <Link to="/">Chatbot</Link> | <Link to="/products">Products</Link> |
            {isAuthenticated ? (
              <>
                {/* Display username and Logout button when authenticated */}
                <span> Hello, {user ? user.username : 'User'} !</span> 
                <button onClick={handleLogout} className="logout-button">Logout</button>
              </>
            ) : (
              <>
                {/* Display Guest and Login button when not authenticated */}
                <span> Hello, Guest !</span> 
                <button onClick={() => navigate('/login')} className="login-button"> Login</button>
              </>
            )}
          </nav>
          <h1>E-commerce Sales Chatbot</h1>
        </header>
        <main>
          <Routes>
            <Route path="/" element={<ChatbotPage />} />
            <Route path="/login" element={<LoginPage />} />
            <Route path="/products" element={<ProductSearchPage />} />
          </Routes>
        </main>
      </div>
    </>
  );
}

export default App;