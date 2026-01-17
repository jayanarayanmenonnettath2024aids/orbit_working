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
import './Dashboard.css';
import './Components.css';

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
    <div className="dashboard" style={{ minHeight: '100vh', background: 'linear-gradient(135deg, #f8fafc 0%, #e8eef7 100%)' }}>
      {/* ============================================
          FANCY HEADER WITH ORBIT BRANDING + WELCOME MESSAGE
          ============================================ */}
      <div style={{
        background: 'linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%)',
        borderBottom: '3px solid rgba(255, 255, 255, 0.2)',
        boxShadow: '0 10px 40px rgba(79, 70, 229, 0.3)',
        position: 'relative',
        overflow: 'hidden'
      }}>
        {/* Animated Background Pattern */}
        <div style={{
          position: 'absolute',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          backgroundImage: `
            radial-gradient(circle at 20% 50%, rgba(255, 255, 255, 0.1) 0%, transparent 50%),
            radial-gradient(circle at 80% 80%, rgba(255, 255, 255, 0.08) 0%, transparent 50%)
          `,
          pointerEvents: 'none'
        }}></div>

        <div style={{
          maxWidth: '1400px',
          margin: '0 auto',
          padding: '48px 32px',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          gap: '48px',
          position: 'relative',
          zIndex: 1
        }}>
          {/* Left: ORBIT Branding */}
          <div style={{
            display: 'flex',
            flexDirection: 'column',
            gap: '12px'
          }}>
            <div style={{
              fontSize: '48px',
              fontWeight: '900',
              color: 'black',
              letterSpacing: '-0.02em',
              lineHeight: 1,
              textShadow: '0 4px 20px rgba(0, 0, 0, 0.2)',
              animation: 'fadeInLeft 0.8s ease-out'
            }}>
              ORBIT
            </div>
            <div style={{
              fontSize: '14px',
              color: 'rgba(255, 255, 255, 0.9)',
              letterSpacing: '0.05em',
              fontWeight: '500',
              animation: 'fadeInLeft 0.8s ease-out 0.1s both'
            }}>
              Opportunity Reasoning & Bridging Intelligence Tool
            </div>
            <div style={{
              fontSize: '13px',
              color: 'rgba(255, 255, 255, 0.8)',
              fontWeight: '400',
              animation: 'fadeInLeft 0.8s ease-out 0.2s both'
            }}>
              AI-Powered Opportunity Intelligence
            </div>
          </div>

          {/* Right: Welcome Message - Only show if profile exists */}
          {profile && (
            <div style={{
              flex: 1,
              maxWidth: '600px',
              animation: 'fadeInRight 0.8s ease-out 0.3s both'
            }}>
              <h1 style={{
                fontSize: '32px',
                fontWeight: '700',
                color: 'white',
                margin: '0 0 12px 0',
                letterSpacing: '-0.02em',
                lineHeight: '1.2',
                textShadow: '0 2px 10px rgba(0, 0, 0, 0.15)'
              }}>
                Welcome to Your Opportunity Journey
              </h1>
              <p style={{
                fontSize: '16px',
                color: 'rgba(255, 255, 255, 0.95)',
                margin: 0,
                lineHeight: '1.6',
                textShadow: '0 1px 5px rgba(0, 0, 0, 0.1)'
              }}>
                This system doesn't just tell you if you're eligible — it shows you the path to become eligible.
              </p>
            </div>
          )}
        </div>
      </div>

      {/* ============================================
          FANCY NAVIGATION BAR WITH GAMIFICATION STATS
          ============================================ */}
      <nav style={{
        position: 'sticky',
        top: 0,
        zIndex: 1000,
        background: 'white',
        borderBottom: '2px solid #e2e8f0',
        boxShadow: '0 4px 20px rgba(0, 0, 0, 0.08)',
        backdropFilter: 'blur(10px)'
      }}>
        <div style={{
          maxWidth: '1400px',
          margin: '0 auto',
          padding: '12px 32px',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          gap: '32px'
        }}>
          {/* Gamification Stats Bar */}
          {profile && gamification && (
            <div style={{ 
              display: 'flex', 
              alignItems: 'center', 
              gap: '24px',
              flex: 1,
              marginLeft: '180px'
            }}>
              {/* Level Badge */}
              <div style={{ 
                display: 'flex', 
                alignItems: 'center', 
                gap: '8px',
                padding: '8px 14px',
                background: 'linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%)',
                borderRadius: '10px',
                border: '1px solid #e2e8f0',
                boxShadow: '0 2px 8px rgba(0, 0, 0, 0.05)'
              }}>
                <span style={{ fontSize: '20px' }}>{gamification.level_icon}</span>
                <div>
                  <div style={{ 
                    fontSize: '9px', 
                    color: '#94a3b8', 
                    fontWeight: '600', 
                    textTransform: 'uppercase', 
                    letterSpacing: '0.8px',
                    marginBottom: '2px'
                  }}>
                    LEVEL
                  </div>
                  <div style={{ fontSize: '13px', color: '#0f172a', fontWeight: '700' }}>
                    Lv.{gamification.level} {gamification.level_name}
                  </div>
                </div>
              </div>

              {/* XP Progress Bar */}
              <div style={{ flex: 1, maxWidth: '280px' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '5px' }}>
                  <span style={{ fontSize: '10px', color: '#94a3b8', fontWeight: '600', textTransform: 'uppercase', letterSpacing: '0.5px' }}>
                    XP PROGRESS
                  </span>
                  <span style={{ fontSize: '11px', color: '#4F46E5', fontWeight: '700' }}>
                    {gamification.progress_to_next}%
                  </span>
                </div>
                <div style={{
                  height: '8px',
                  background: '#f1f5f9',
                  borderRadius: '4px',
                  overflow: 'hidden',
                  boxShadow: 'inset 0 1px 2px rgba(0,0,0,0.08)'
                }}>
                  <div style={{
                    height: '100%',
                    width: `${gamification.progress_to_next}%`,
                    background: 'linear-gradient(90deg, #4F46E5 0%, #7C3AED 100%)',
                    borderRadius: '4px',
                    transition: 'width 0.4s ease',
                    boxShadow: '0 0 8px rgba(79, 70, 229, 0.4)'
                  }} />
                </div>
              </div>

              {/* Points Badge */}
              <div style={{ 
                display: 'flex', 
                alignItems: 'center', 
                gap: '8px',
                padding: '8px 14px',
                background: 'linear-gradient(135deg, #fef3c7 0%, #fde68a 100%)',
                borderRadius: '10px',
                border: '1px solid #fbbf24',
                boxShadow: '0 2px 8px rgba(251, 191, 36, 0.2)'
              }}>
                <span style={{ fontSize: '20px' }}>⭐</span>
                <div>
                  <div style={{ 
                    fontSize: '9px', 
                    color: '#92400e', 
                    fontWeight: '600', 
                    textTransform: 'uppercase', 
                    letterSpacing: '0.8px',
                    marginBottom: '2px'
                  }}>
                    POINTS
                  </div>
                  <div style={{ fontSize: '13px', color: '#92400e', fontWeight: '700' }}>
                    {gamification.total_points}
                  </div>
                </div>
              </div>

              {/* Quick Actions */}
              <div style={{ display: 'flex', gap: '8px', alignItems: 'center' }}>
                <button
                  onClick={() => setShowTasks(true)}
                  style={{
                    padding: '8px 12px',
                    background: '#fef3c7',
                    border: '1px solid #fbbf24',
                    borderRadius: '8px',
                    color: '#92400e',
                    fontSize: '11px',
                    fontWeight: '600',
                    cursor: 'pointer',
                    transition: 'all 0.2s ease',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '6px'
                  }}
                  onMouseOver={(e) => {
                    e.currentTarget.style.background = '#fde68a';
                    e.currentTarget.style.transform = 'translateY(-2px)';
                  }}
                  onMouseOut={(e) => {
                    e.currentTarget.style.background = '#fef3c7';
                    e.currentTarget.style.transform = 'translateY(0)';
                  }}
                >
                  <span style={{ fontSize: '14px' }}>📋</span>
                  Tasks
                </button>

                <button
                  onClick={() => fetchLeaderboard()}
                  style={{
                    padding: '8px 12px',
                    background: '#fef3c7',
                    border: '1px solid #fbbf24',
                    borderRadius: '8px',
                    color: '#92400e',
                    fontSize: '11px',
                    fontWeight: '600',
                    cursor: 'pointer',
                    transition: 'all 0.2s ease',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '6px'
                  }}
                  onMouseOver={(e) => {
                    e.currentTarget.style.background = '#fde68a';
                    e.currentTarget.style.transform = 'translateY(-2px)';
                  }}
                  onMouseOut={(e) => {
                    e.currentTarget.style.background = '#fef3c7';
                    e.currentTarget.style.transform = 'translateY(0)';
                  }}
                >
                  <span style={{ fontSize: '14px' }}>🏆</span>
                  Ranks
                </button>
              </div>
            </div>
          )}

          {/* User Actions */}
          <div style={{ display: 'flex', gap: '12px', alignItems: 'center', flexShrink: 0 }}>
            {profile && (
              <button
                onClick={() => {
                  setShowUpdateProfile(true);
                  setActiveTab('profile');
                }}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '8px',
                  padding: '10px 18px',
                  background: 'linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%)',
                  border: 'none',
                  borderRadius: '10px',
                  color: 'white',
                  fontSize: '13px',
                  fontWeight: '600',
                  cursor: 'pointer',
                  transition: 'all 0.3s ease',
                  boxShadow: '0 4px 12px rgba(79, 70, 229, 0.3)'
                }}
                onMouseOver={(e) => {
                  e.currentTarget.style.transform = 'translateY(-2px)';
                  e.currentTarget.style.boxShadow = '0 6px 20px rgba(79, 70, 229, 0.4)';
                }}
                onMouseOut={(e) => {
                  e.currentTarget.style.transform = 'translateY(0)';
                  e.currentTarget.style.boxShadow = '0 4px 12px rgba(79, 70, 229, 0.3)';
                }}
              >
                <RefreshCw size={14} />
                Update Profile
              </button>
            )}
            <button
              onClick={handleLogout}
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '8px',
                padding: '10px 18px',
                background: 'white',
                border: '2px solid #fee2e2',
                borderRadius: '10px',
                color: '#ef4444',
                fontSize: '13px',
                fontWeight: '600',
                cursor: 'pointer',
                transition: 'all 0.3s ease'
              }}
              onMouseOver={(e) => {
                e.currentTarget.style.background = '#fef2f2';
                e.currentTarget.style.borderColor = '#ef4444';
                e.currentTarget.style.transform = 'translateY(-2px)';
                e.currentTarget.style.boxShadow = '0 4px 12px rgba(239, 68, 68, 0.2)';
              }}
              onMouseOut={(e) => {
                e.currentTarget.style.background = 'white';
                e.currentTarget.style.borderColor = '#fee2e2';
                e.currentTarget.style.transform = 'translateY(0)';
                e.currentTarget.style.boxShadow = 'none';
              }}
            >
              <LogOut size={14} />
              Logout
            </button>
          </div>
        </div>
      </nav>

      {/* ============================================
          FLOATING PAGE NAVIGATION TABS
          ============================================ */}
      {profile && (
        <div style={{
          maxWidth: '1400px',
          margin: '62px auto 0',
          padding: '0 32px',
          display: 'flex',
          justifyContent: 'center'
        }}>
          <div style={{
            display: 'flex',
            gap: '12px',
            padding: '8px',
            background: 'white',
            borderRadius: '16px',
            boxShadow: '0 10px 40px rgba(0, 0, 0, 0.1)',
            border: '1px solid #e2e8f0',
            width: 'fit-content'
          }}>
            <button
              onClick={() => setActiveTab('explore')}
              disabled={!profile}
              style={{
                background: activeTab === 'explore' ? 'linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%)' : 'transparent',
                border: 'none',
                color: activeTab === 'explore' ? 'white' : '#64748b',
                fontSize: '14px',
                fontWeight: '600',
                cursor: profile ? 'pointer' : 'not-allowed',
                opacity: profile ? 1 : 0.5,
                display: 'flex',
                alignItems: 'center',
                gap: '8px',
                padding: '12px 24px',
                borderRadius: '12px',
                transition: 'all 0.3s ease',
                boxShadow: activeTab === 'explore' ? '0 4px 12px rgba(79, 70, 229, 0.3)' : 'none'
              }}
              onMouseOver={(e) => {
                if (profile && activeTab !== 'explore') {
                  e.currentTarget.style.background = '#f8fafc';
                  e.currentTarget.style.color = '#4F46E5';
                }
              }}
              onMouseOut={(e) => {
                if (profile && activeTab !== 'explore') {
                  e.currentTarget.style.background = 'transparent';
                  e.currentTarget.style.color = '#64748b';
                }
              }}
            >
              <Search size={18} />
              Explore
            </button>

            <button
              onClick={() => setActiveTab('tracker')}
              disabled={!profile}
              style={{
                background: activeTab === 'tracker' ? 'linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%)' : 'transparent',
                border: 'none',
                color: activeTab === 'tracker' ? 'white' : '#64748b',
                fontSize: '14px',
                fontWeight: '600',
                cursor: profile ? 'pointer' : 'not-allowed',
                opacity: profile ? 1 : 0.5,
                display: 'flex',
                alignItems: 'center',
                gap: '8px',
                padding: '12px 24px',
                borderRadius: '12px',
                transition: 'all 0.3s ease',
                boxShadow: activeTab === 'tracker' ? '0 4px 12px rgba(79, 70, 229, 0.3)' : 'none'
              }}
              onMouseOver={(e) => {
                if (profile && activeTab !== 'tracker') {
                  e.currentTarget.style.background = '#f8fafc';
                  e.currentTarget.style.color = '#4F46E5';
                }
              }}
              onMouseOut={(e) => {
                if (profile && activeTab !== 'tracker') {
                  e.currentTarget.style.background = 'transparent';
                  e.currentTarget.style.color = '#64748b';
                }
              }}
            >
              <ClipboardList size={18} />
              Tracker
            </button>

            <button
              onClick={() => setActiveTab('analytics')}
              disabled={!profile}
              style={{
                background: activeTab === 'analytics' ? 'linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%)' : 'transparent',
                border: 'none',
                color: activeTab === 'analytics' ? 'white' : '#64748b',
                fontSize: '14px',
                fontWeight: '600',
                cursor: profile ? 'pointer' : 'not-allowed',
                opacity: profile ? 1 : 0.5,
                display: 'flex',
                alignItems: 'center',
                gap: '8px',
                padding: '12px 24px',
                borderRadius: '12px',
                transition: 'all 0.3s ease',
                boxShadow: activeTab === 'analytics' ? '0 4px 12px rgba(79, 70, 229, 0.3)' : 'none'
              }}
              onMouseOver={(e) => {
                if (profile && activeTab !== 'analytics') {
                  e.currentTarget.style.background = '#f8fafc';
                  e.currentTarget.style.color = '#4F46E5';
                }
              }}
              onMouseOut={(e) => {
                if (profile && activeTab !== 'analytics') {
                  e.currentTarget.style.background = 'transparent';
                  e.currentTarget.style.color = '#64748b';
                }
              }}
            >
              <BarChart3 size={18} />
              Analytics
            </button>

            <button
              onClick={() => setActiveTab('success')}
              disabled={!profile}
              style={{
                background: activeTab === 'success' ? 'linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%)' : 'transparent',
                border: 'none',
                color: activeTab === 'success' ? 'white' : '#64748b',
                fontSize: '14px',
                fontWeight: '600',
                cursor: profile ? 'pointer' : 'not-allowed',
                opacity: profile ? 1 : 0.5,
                display: 'flex',
                alignItems: 'center',
                gap: '8px',
                padding: '12px 24px',
                borderRadius: '12px',
                transition: 'all 0.3s ease',
                boxShadow: activeTab === 'success' ? '0 4px 12px rgba(79, 70, 229, 0.3)' : 'none'
              }}
              onMouseOver={(e) => {
                if (profile && activeTab !== 'success') {
                  e.currentTarget.style.background = '#f8fafc';
                  e.currentTarget.style.color = '#4F46E5';
                }
              }}
              onMouseOut={(e) => {
                if (profile && activeTab !== 'success') {
                  e.currentTarget.style.background = 'transparent';
                  e.currentTarget.style.color = '#64748b';
                }
              }}
            >
              <Trophy size={18} />
              Success Stories
            </button>
          </div>
        </div>
      )}

      {/* ============================================
          MAIN CONTENT AREA
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
