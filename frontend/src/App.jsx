import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, useLocation } from 'react-router-dom';
import LandingPage from './components/LandingPage';
import Auth from './components/Auth';
import ProfileBuilder from './components/ProfileBuilder';
import OpportunityExplorer from './components/OpportunityExplorer';
import Dashboard from './components/Dashboard';
import './App.css';

function AppContent() {
  const [currentProfile, setCurrentProfile] = useState(null);
  const [opportunities, setOpportunities] = useState([]);
  const location = useLocation();
  
  const isLandingOrAuth = location.pathname === '/' || location.pathname === '/auth' || location.pathname === '/dashboard';

  return (
    <div className="App">
      {/* Header - Hide on landing, auth, and dashboard pages */}
      {!isLandingOrAuth && (
        <header className="app-header">
          <div className="container">
            <h1 className="app-title">
              <span className="gradient-text">ORBIT</span>
            </h1>
            <p className="app-subtitle">
              Opportunity Reasoning & Bridging Intelligence Tool
            </p>
            <p className="app-tagline">
              AI-Powered Opportunity Intelligence
            </p>
          </div>
        </header>
      )}

      {/* Main Content */}
      <main className={isLandingOrAuth ? "app-main-full" : "app-main"}>
        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route path="/auth" element={<Auth />} />
          <Route 
            path="/dashboard" 
            element={
              <Dashboard 
                profile={currentProfile}
                setProfile={setCurrentProfile}
                opportunities={opportunities}
                setOpportunities={setOpportunities}
              />
            } 
          />
          <Route 
            path="/profile" 
            element={
              <ProfileBuilder 
                onProfileCreated={setCurrentProfile}
              />
            } 
          />
          <Route 
            path="/opportunities" 
            element={
              <OpportunityExplorer 
                profile={currentProfile}
                opportunities={opportunities}
                setOpportunities={setOpportunities}
              />
            } 
          />
        </Routes>
      </main>

      {/* Footer - Hide on landing and auth pages */}
      {!isLandingOrAuth && (
        <footer className="app-footer">
          <div className="container">
            <p>
              Powered by <strong>Gemini AI</strong> • <strong>Google Search</strong> • <strong>Firebase</strong>
            </p>
            <p className="text-sm">
              Built for students achieving their dreams
            </p>
          </div>
        </footer>
      )}
    </div>
  );
}

function App() {
  return (
    <Router>
      <AppContent />
    </Router>
  );
}

export default App;
