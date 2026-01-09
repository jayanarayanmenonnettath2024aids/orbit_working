import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import ProfileBuilder from './components/ProfileBuilder';
import OpportunityExplorer from './components/OpportunityExplorer';
import Dashboard from './components/Dashboard';
import './App.css';

function App() {
  const [currentProfile, setCurrentProfile] = useState(null);
  const [opportunities, setOpportunities] = useState([]);

  return (
    <Router>
      <div className="App">
        {/* Header */}
        <header className="app-header">
          <div className="container">
            <h1 className="app-title">
              🎯 Opportunity Intelligence System
            </h1>
            <p className="app-tagline">
              Never just "Not Eligible" — Always explain why & guide how to improve
            </p>
          </div>
        </header>

        {/* Main Content */}
        <main className="app-main">
          <Routes>
            <Route 
              path="/" 
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

        {/* Footer */}
        <footer className="app-footer">
          <div className="container">
            <p>
              Powered by <strong>Gemini AI</strong> • <strong>Google Search</strong> • <strong>Firebase</strong>
            </p>
            <p className="text-sm">
              Built for students in underserved campuses across India
            </p>
          </div>
        </footer>
      </div>
    </Router>
  );
}

export default App;
