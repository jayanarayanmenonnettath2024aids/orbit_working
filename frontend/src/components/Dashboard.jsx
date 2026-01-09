import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import ProfileBuilder from './ProfileBuilder';
import OpportunityExplorer from './OpportunityExplorer';
import { FileText, Search, Sparkles } from 'lucide-react';

function Dashboard({ profile, setProfile, opportunities, setOpportunities }) {
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState('profile');

  return (
    <div className="dashboard">
      <div className="container">
        {/* Welcome Section */}
        <div className="welcome-section">
          <h2 className="welcome-title">
            <Sparkles className="icon" />
            Welcome to Your Opportunity Journey
          </h2>
          <p className="welcome-text">
            This system doesn't just tell you if you're eligible—it shows you the path to become eligible.
          </p>
        </div>

        {/* Tab Navigation */}
        <div className="tab-nav">
          <button
            className={`tab-button ${activeTab === 'profile' ? 'active' : ''}`}
            onClick={() => setActiveTab('profile')}
          >
            <FileText className="icon-sm" />
            Step 1: Build Your Profile
          </button>
          <button
            className={`tab-button ${activeTab === 'explore' ? 'active' : ''}`}
            onClick={() => setActiveTab('explore')}
            disabled={!profile}
          >
            <Search className="icon-sm" />
            Step 2: Explore Opportunities
          </button>
        </div>

        {/* Tab Content */}
        <div className="tab-content">
          {activeTab === 'profile' && (
            <ProfileBuilder 
              onProfileCreated={(newProfile) => {
                setProfile(newProfile);
                setActiveTab('explore');
              }}
              existingProfile={profile}
            />
          )}

          {activeTab === 'explore' && profile && (
            <OpportunityExplorer 
              profile={profile}
              opportunities={opportunities}
              setOpportunities={setOpportunities}
            />
          )}
        </div>

        {/* Info Cards */}
        <div className="info-cards">
          <div className="info-card">
            <h3>🎯 What Makes This Different?</h3>
            <ul>
              <li>Real opportunities from Google Search</li>
              <li>AI-powered eligibility analysis using Gemini</li>
              <li>Clear explanations, not just yes/no</li>
              <li>Actionable guidance to become eligible</li>
            </ul>
          </div>

          <div className="info-card">
            <h3>🚀 How It Works</h3>
            <ol>
              <li>Create your profile (resume or manual)</li>
              <li>Search for opportunities</li>
              <li>Get AI analysis of your eligibility</li>
              <li>Follow personalized guidance to improve</li>
            </ol>
          </div>

          <div className="info-card">
            <h3>💡 Our Philosophy</h3>
            <p>
              We believe eligibility is a journey, not a gate. 
              Every "not yet eligible" comes with a roadmap to get there.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
