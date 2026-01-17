import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import ProfileBuilder from './ProfileBuilder';
import OpportunityExplorer from './OpportunityExplorer';
import ApplicationTracker from './ApplicationTracker';
import AIChatbot from './AIChatbot';
import AnalyticsDashboard from './AnalyticsDashboard';
import GamificationDisplay from './GamificationDisplay';
import SuccessStories from './SuccessStories';
import { Search, ClipboardList, RefreshCw, BarChart3, Trophy, LogOut } from 'lucide-react';
import { updateLoginStreak } from '../utils/gamification';
import { logoutUser } from '../services/api';

function Dashboard({ profile, setProfile, opportunities, setOpportunities }) {
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState('explore');
  const [showUpdateProfile, setShowUpdateProfile] = useState(false);
  const [gamification, setGamification] = useState(null);
  const [showTasks, setShowTasks] = useState(false);
  const [showAchievements, setShowAchievements] = useState(false);
  const [showLeaderboard, setShowLeaderboard] = useState(false);
  const [leaderboard, setLeaderboard] = useState([]);
  
  const userId = localStorage.getItem('user_id') || profile?.profile_id || 'default-user';
  const userName = localStorage.getItem('user_name') || profile?.personal_info?.name || 'there';

  // Fetch gamification data
  useEffect(() => {
    if (profile) {
      fetchGamification();
    }
  }, [userId, profile]);

  const fetchGamification = async () => {
    try {
      const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:5000/api';
      const response = await fetch(`${apiUrl}/gamification/${userId}`);
      if (response.ok) {
        const data = await response.json();
        setGamification(data);
      }
    } catch (error) {
      console.error('Error fetching gamification:', error);
    }
  };

  const fetchLeaderboard = async () => {
    try {
      const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:5000/api';
      const response = await fetch(`${apiUrl}/gamification/leaderboard?user_id=${userId}&top=10`);
      if (response.ok) {
        const data = await response.json();
        setLeaderboard(data.leaderboard || data);
        setShowLeaderboard(true);
      }
    } catch (error) {
      console.error('Error fetching leaderboard:', error);
    }
  };

  const handleLogout = async () => {
    try {
      await logoutUser();
      localStorage.removeItem('session_token');
      localStorage.removeItem('user_id');
      localStorage.removeItem('user_email');
      localStorage.removeItem('user_name');
      localStorage.removeItem('userProfile');
      sessionStorage.clear();
      navigate('/');
    } catch (err) {
      console.error('Logout error:', err);
      localStorage.clear();
      sessionStorage.clear();
      navigate('/');
    }
  };

  useEffect(() => {
    updateLoginStreak();
  }, []);

  useEffect(() => {
    const savedProfile = localStorage.getItem('userProfile');
    if (savedProfile && !profile) {
      try {
        const parsedProfile = JSON.parse(savedProfile);
        setProfile(parsedProfile);
        setActiveTab('explore');
        console.log('✅ Loaded saved profile from localStorage');
      } catch (err) {
        console.error('Failed to parse saved profile:', err);
        localStorage.removeItem('userProfile');
      }
    } else if (!profile) {
      setActiveTab('profile');
    }
  }, []);

  useEffect(() => {
    if (profile) {
      localStorage.setItem('userProfile', JSON.stringify(profile));
      console.log('✅ Profile saved to localStorage');
    }
  }, [profile]);

  return (
    <div className="dashboard" style={{ minHeight: '100vh', background: '#f8fafc' }}>
      {/* ============================================
          1️⃣ GLOBAL TOP NAVBAR (ALWAYS VISIBLE)
          Purpose: Stable navigation, ORBIT identity, user actions
          ============================================ */}
      <nav style={{
        position: 'sticky',
        top: 0,
        zIndex: 1000,
        background: 'white',
        borderBottom: '2px solid #e2e8f0',
        boxShadow: '0 2px 8px rgba(0,0,0,0.05)'
      }}>
        <div style={{
          maxWidth: '1400px',
          margin: '0 auto',
          padding: '14px 32px',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          gap: '32px'
        }}>
          {/* Logo */}
          <div style={{
            fontSize: '26px',
            fontWeight: '800',
            background: 'linear-gradient(135deg, #2563eb 0%, #06b6d4 100%)',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent',
            letterSpacing: '-0.03em',
            cursor: 'pointer',
            flexShrink: 0
          }}>
            ORBIT
          </div>

          {/* Primary Navigation - Center */}
          <div style={{ display: 'flex', gap: '28px', alignItems: 'center', flex: 1, justifyContent: 'center' }}>
            <button
              onClick={() => setActiveTab('explore')}
              disabled={!profile}
              style={{
                background: 'transparent',
                border: 'none',
                color: activeTab === 'explore' ? '#2563eb' : '#64748b',
                fontSize: '14px',
                fontWeight: '600',
                cursor: profile ? 'pointer' : 'not-allowed',
                opacity: profile ? 1 : 0.5,
                display: 'flex',
                alignItems: 'center',
                gap: '6px',
                padding: '10px 4px',
                borderBottom: activeTab === 'explore' ? '3px solid #2563eb' : '3px solid transparent',
                transition: 'all 0.2s ease',
                position: 'relative',
                top: '2px'
              }}
            >
              <Search size={17} />
              Explore
            </button>

            <button
              onClick={() => setActiveTab('tracker')}
              disabled={!profile}
              style={{
                background: 'transparent',
                border: 'none',
                color: activeTab === 'tracker' ? '#2563eb' : '#64748b',
                fontSize: '14px',
                fontWeight: '600',
                cursor: profile ? 'pointer' : 'not-allowed',
                opacity: profile ? 1 : 0.5,
                display: 'flex',
                alignItems: 'center',
                gap: '6px',
                padding: '10px 4px',
                borderBottom: activeTab === 'tracker' ? '3px solid #2563eb' : '3px solid transparent',
                transition: 'all 0.2s ease',
                position: 'relative',
                top: '2px'
              }}
            >
              <ClipboardList size={17} />
              Tracker
            </button>

            <button
              onClick={() => setActiveTab('analytics')}
              disabled={!profile}
              style={{
                background: 'transparent',
                border: 'none',
                color: activeTab === 'analytics' ? '#2563eb' : '#64748b',
                fontSize: '14px',
                fontWeight: '600',
                cursor: profile ? 'pointer' : 'not-allowed',
                opacity: profile ? 1 : 0.5,
                display: 'flex',
                alignItems: 'center',
                gap: '6px',
                padding: '10px 4px',
                borderBottom: activeTab === 'analytics' ? '3px solid #2563eb' : '3px solid transparent',
                transition: 'all 0.2s ease',
                position: 'relative',
                top: '2px'
              }}
            >
              <BarChart3 size={17} />
              Analytics
            </button>

            <button
              onClick={() => setActiveTab('success')}
              disabled={!profile}
              style={{
                background: 'transparent',
                border: 'none',
                color: activeTab === 'success' ? '#2563eb' : '#64748b',
                fontSize: '14px',
                fontWeight: '600',
                cursor: profile ? 'pointer' : 'not-allowed',
                opacity: profile ? 1 : 0.5,
                display: 'flex',
                alignItems: 'center',
                gap: '6px',
                padding: '10px 4px',
                borderBottom: activeTab === 'success' ? '3px solid #2563eb' : '3px solid transparent',
                transition: 'all 0.2s ease',
                position: 'relative',
                top: '2px'
              }}
            >
              <Trophy size={17} />
              Success Stories
            </button>
          </div>

          {/* User Actions - Right */}
          <div style={{ display: 'flex', gap: '8px', alignItems: 'center', flexShrink: 0 }}>
            {profile && (
              <button
                onClick={() => {
                  setShowUpdateProfile(true);
                  setActiveTab('profile');
                }}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '6px',
                  padding: '9px 14px',
                  background: 'white',
                  border: '1.5px solid #e2e8f0',
                  borderRadius: '7px',
                  color: '#64748b',
                  fontSize: '13px',
                  fontWeight: '600',
                  cursor: 'pointer',
                  transition: 'all 0.2s ease'
                }}
                onMouseOver={(e) => {
                  e.currentTarget.style.borderColor = '#2563eb';
                  e.currentTarget.style.color = '#2563eb';
                }}
                onMouseOut={(e) => {
                  e.currentTarget.style.borderColor = '#e2e8f0';
                  e.currentTarget.style.color = '#64748b';
                }}
              >
                <RefreshCw size={13} />
                Update Profile
              </button>
            )}
            <button
              onClick={handleLogout}
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '6px',
                padding: '9px 14px',
                background: 'white',
                border: '1.5px solid #fee2e2',
                borderRadius: '7px',
                color: '#ef4444',
                fontSize: '13px',
                fontWeight: '600',
                cursor: 'pointer',
                transition: 'all 0.2s ease'
              }}
              onMouseOver={(e) => {
                e.currentTarget.style.background = '#fef2f2';
                e.currentTarget.style.borderColor = '#ef4444';
              }}
              onMouseOut={(e) => {
                e.currentTarget.style.background = 'white';
                e.currentTarget.style.borderColor = '#fee2e2';
              }}
            >
              <LogOut size={13} />
              Logout
            </button>
          </div>
        </div>
      </nav>

      {/* ============================================
          2️⃣ DASHBOARD HEADER (INTRO SECTION)
          Purpose: Conceptual anchor - what ORBIT does
          Not a card. Not collapsible. Always visible when logged in.
          ============================================ */}
      {profile && (
        <div style={{
          background: 'linear-gradient(to bottom, #f8fafc 0%, white 100%)',
          borderBottom: '1px solid #e2e8f0',
          padding: '42px 32px 36px'
        }}>
          <div style={{ maxWidth: '1400px', margin: '0 auto' }}>
            <h1 style={{
              fontSize: '34px',
              fontWeight: '700',
              color: '#0f172a',
              margin: '0 0 10px 0',
              letterSpacing: '-0.025em',
              lineHeight: '1.2'
            }}>
              Welcome to Your Opportunity Journey
            </h1>
            <p style={{
              fontSize: '17px',
              color: '#64748b',
              margin: 0,
              lineHeight: '1.65',
              maxWidth: '720px'
            }}>
              This system doesn't just tell you if you're eligible — it shows you the path to become eligible.
            </p>
          </div>
        </div>
      )}

      {/* ============================================
          3️⃣ PROGRESS & STATUS STRIP
          Purpose: Status console - Level, XP, Points, Actions
          Horizontal alignment. No floating elements.
          ============================================ */}
      {profile && gamification && (
        <div style={{
          background: 'white',
          borderBottom: '1px solid #e2e8f0',
          padding: '20px 32px',
          boxShadow: '0 1px 3px rgba(0,0,0,0.03)'
        }}>
          <div style={{
            maxWidth: '1400px',
            margin: '0 auto',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            gap: '40px'
          }}>
            {/* Left Side: Level, XP, Points */}
            <div style={{ display: 'flex', alignItems: 'center', gap: '36px', flex: 1 }}>
              {/* Level Badge */}
              <div style={{ 
                display: 'flex', 
                alignItems: 'center', 
                gap: '10px',
                padding: '10px 16px',
                background: '#f8fafc',
                borderRadius: '10px',
                border: '1px solid #e2e8f0'
              }}>
                <span style={{ fontSize: '24px' }}>{gamification.level_icon}</span>
                <div>
                  <div style={{ 
                    fontSize: '10px', 
                    color: '#94a3b8', 
                    fontWeight: '600', 
                    textTransform: 'uppercase', 
                    letterSpacing: '0.8px',
                    marginBottom: '2px'
                  }}>
                    Level
                  </div>
                  <div style={{ fontSize: '15px', color: '#0f172a', fontWeight: '700' }}>
                    Lv.{gamification.level} {gamification.level_name}
                  </div>
                </div>
              </div>

              {/* XP Progress Bar */}
              <div style={{ flex: 1, maxWidth: '320px' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '7px' }}>
                  <span style={{ fontSize: '11px', color: '#94a3b8', fontWeight: '600', textTransform: 'uppercase', letterSpacing: '0.5px' }}>
                    XP Progress
                  </span>
                  <span style={{ fontSize: '12px', color: '#2563eb', fontWeight: '700' }}>
                    {gamification.progress_to_next}%
                  </span>
                </div>
                <div style={{
                  height: '10px',
                  background: '#f1f5f9',
                  borderRadius: '5px',
                  overflow: 'hidden',
                  boxShadow: 'inset 0 1px 3px rgba(0,0,0,0.08)'
                }}>
                  <div style={{
                    height: '100%',
                    width: `${gamification.progress_to_next}%`,
                    background: 'linear-gradient(90deg, #2563eb 0%, #06b6d4 100%)',
                    borderRadius: '5px',
                    transition: 'width 0.4s ease',
                    boxShadow: '0 0 8px rgba(37, 99, 235, 0.3)'
                  }} />
                </div>
              </div>

              {/* Points Badge */}
              <div style={{ 
                display: 'flex', 
                alignItems: 'center', 
                gap: '10px',
                padding: '10px 16px',
                background: '#fffbeb',
                borderRadius: '10px',
                border: '1px solid #fef3c7'
              }}>
                <span style={{ fontSize: '24px' }}>⭐</span>
                <div>
                  <div style={{ 
                    fontSize: '10px', 
                    color: '#92400e', 
                    fontWeight: '600', 
                    textTransform: 'uppercase', 
                    letterSpacing: '0.8px',
                    marginBottom: '2px'
                  }}>
                    Points
                  </div>
                  <div style={{ fontSize: '15px', color: '#78350f', fontWeight: '700' }}>
                    {gamification.total_points}
                  </div>
                </div>
              </div>
            </div>

            {/* Right Side: Action Buttons */}
            <div style={{ display: 'flex', gap: '10px', flexShrink: 0 }}>
              {/* Streak Button */}
              <button
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '8px',
                  padding: '11px 18px',
                  background: 'linear-gradient(135deg, #fff7ed 0%, #ffedd5 100%)',
                  border: '1.5px solid #fed7aa',
                  borderRadius: '9px',
                  color: '#9a3412',
                  fontSize: '13px',
                  fontWeight: '700',
                  cursor: 'default',
                  boxShadow: '0 1px 3px rgba(0,0,0,0.05)'
                }}
              >
                <span style={{ fontSize: '18px' }}>🔥</span>
                <span>{gamification.login_streak} Day{gamification.login_streak !== 1 ? 's' : ''}</span>
              </button>

              {/* Tasks Button */}
              <button
                onClick={() => setShowTasks(true)}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '8px',
                  padding: '11px 18px',
                  background: 'white',
                  border: '1.5px solid #e2e8f0',
                  borderRadius: '9px',
                  color: '#64748b',
                  fontSize: '13px',
                  fontWeight: '700',
                  cursor: 'pointer',
                  transition: 'all 0.2s ease',
                  boxShadow: '0 1px 3px rgba(0,0,0,0.05)'
                }}
                onMouseOver={(e) => {
                  e.currentTarget.style.borderColor = '#2563eb';
                  e.currentTarget.style.color = '#2563eb';
                  e.currentTarget.style.background = '#f8fafc';
                }}
                onMouseOut={(e) => {
                  e.currentTarget.style.borderColor = '#e2e8f0';
                  e.currentTarget.style.color = '#64748b';
                  e.currentTarget.style.background = 'white';
                }}
              >
                <span style={{ fontSize: '18px' }}>📝</span>
                <span>Tasks</span>
              </button>

              {/* Ranks Button */}
              <button
                onClick={fetchLeaderboard}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '8px',
                  padding: '11px 18px',
                  background: 'white',
                  border: '1.5px solid #e2e8f0',
                  borderRadius: '9px',
                  color: '#64748b',
                  fontSize: '13px',
                  fontWeight: '700',
                  cursor: 'pointer',
                  transition: 'all 0.2s ease',
                  boxShadow: '0 1px 3px rgba(0,0,0,0.05)'
                }}
                onMouseOver={(e) => {
                  e.currentTarget.style.borderColor = '#2563eb';
                  e.currentTarget.style.color = '#2563eb';
                  e.currentTarget.style.background = '#f8fafc';
                }}
                onMouseOut={(e) => {
                  e.currentTarget.style.borderColor = '#e2e8f0';
                  e.currentTarget.style.color = '#64748b';
                  e.currentTarget.style.background = 'white';
                }}
              >
                <span style={{ fontSize: '18px' }}>🏆</span>
                <span>Ranks</span>
              </button>
            </div>
          </div>
        </div>
      )}

      {/* ============================================
          5️⃣ MAIN CONTENT AREA
          Purpose: Focus space for core product - Explore, Tracker, Analytics, Success
          No global alerts. No gamification noise. Clean and calm.
          ============================================ */}
      <div style={{
        maxWidth: '1400px',
        margin: '0 auto',
        padding: '36px 32px',
        minHeight: 'calc(100vh - 400px)'
      }}>
        {activeTab === 'profile' && (
          <ProfileBuilder
            onProfileCreated={(newProfile) => {
              setProfile(newProfile);
              setShowUpdateProfile(false);
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

        {activeTab === 'tracker' && profile && (
          <ApplicationTracker userId={userId} />
        )}

        {activeTab === 'analytics' && profile && (
          <AnalyticsDashboard userId={userId} />
        )}

        {activeTab === 'success' && profile && (
          <SuccessStories />
        )}

        {/* AI Chatbot */}
        {profile && (
          <AIChatbot
            userId={userId}
            context={{ profile: profile }}
          />
        )}
      </div>

      {/* ============================================
          5️⃣ MODALS (Tasks, Achievements, Leaderboard)
          ============================================ */}
      {(showTasks || showAchievements || showLeaderboard) && (
        <GamificationDisplay
          userId={userId}
          showTasks={showTasks}
          setShowTasks={setShowTasks}
          showAchievements={showAchievements}
          setShowAchievements={setShowAchievements}
          showLeaderboard={showLeaderboard}
          setShowLeaderboard={setShowLeaderboard}
          leaderboardData={leaderboard}
        />
      )}
    </div>
  );
}

export default Dashboard;
