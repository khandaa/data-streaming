import React, { useState, useEffect } from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';

// Components
import Navbar from './components/Navbar';
import Sidebar from './components/Sidebar';
import Footer from './components/Footer';

// Pages
import Dashboard from './pages/Dashboard';
import StreamingStatus from './pages/StreamingStatus';
import Topics from './pages/Topics';
import StreamingApps from './pages/StreamingApps';
import AdminLogin from './pages/AdminLogin';
import AdminDashboard from './pages/AdminDashboard';
import Help from './pages/Help';

// Styles
import './App.css';

const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
  },
});

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [sidebarOpen, setSidebarOpen] = useState(true);

  // Check if user is logged in
  useEffect(() => {
    const user = localStorage.getItem('user');
    if (user) {
      setIsLoggedIn(true);
    }
  }, []);

  const handleLogin = (user) => {
    localStorage.setItem('user', JSON.stringify(user));
    setIsLoggedIn(true);
  };

  const handleLogout = () => {
    localStorage.removeItem('user');
    setIsLoggedIn(false);
  };

  const toggleSidebar = () => {
    setSidebarOpen(!sidebarOpen);
  };

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <div className="app">
        <Navbar 
          toggleSidebar={toggleSidebar} 
          isLoggedIn={isLoggedIn} 
          onLogout={handleLogout} 
        />
        <div className="content-container">
          <Sidebar open={sidebarOpen} />
          <main className={`main-content ${sidebarOpen ? 'sidebar-open' : ''}`}>
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/status" element={<StreamingStatus />} />
              <Route path="/topics" element={<Topics />} />
              <Route path="/apps" element={<StreamingApps />} />
              <Route path="/help" element={<Help />} />
              <Route 
                path="/admin/login" 
                element={
                  isLoggedIn ? 
                    <Navigate to="/admin/dashboard" replace /> : 
                    <AdminLogin onLogin={handleLogin} />
                } 
              />
              <Route 
                path="/admin/dashboard" 
                element={
                  isLoggedIn ? 
                    <AdminDashboard /> : 
                    <Navigate to="/admin/login" replace />
                } 
              />
              <Route path="*" element={<Navigate to="/" replace />} />
            </Routes>
          </main>
        </div>
        <Footer />
      </div>
    </ThemeProvider>
  );
}

export default App;
