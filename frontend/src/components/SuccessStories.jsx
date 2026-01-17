import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './SuccessStories.css';

const SuccessStories = () => {
  const [stories, setStories] = useState([]);
  const [peerInsights, setPeerInsights] = useState(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('stories'); // 'stories' or 'insights'

  useEffect(() => {
    fetchSuccessStories();
    fetchPeerInsights();
  }, []);

  const fetchSuccessStories = async () => {
    try {
      const userId = localStorage.getItem('user_id');
      const response = await axios.get(`http://localhost:5000/api/success-stories?user_id=${userId}&limit=5`);
      
      if (response.data.success) {
        setStories(response.data.stories);
      }
    } catch (error) {
      console.error('Error fetching success stories:', error);
    }
  };

  const fetchPeerInsights = async () => {
    try {
      const userId = localStorage.getItem('user_id');
      const response = await axios.get(`http://localhost:5000/api/peer-insights?user_id=${userId}`);
      
      if (response.data.success) {
        setPeerInsights(response.data.insights);
      }
      setLoading(false);
    } catch (error) {
      console.error('Error fetching peer insights:', error);
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div style={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        minHeight: '60vh',
        gap: '24px'
      }}>
        <div style={{
          width: '60px',
          height: '60px',
          border: '4px solid #f3f4f6',
          borderTop: '4px solid #4F46E5',
          borderRadius: '50%',
          animation: 'spin 1s linear infinite'
        }}></div>
        <p style={{
          fontSize: '18px',
          color: '#64748b',
          fontWeight: '500',
          animation: 'fadeIn 0.5s ease-in'
        }}>Loading inspirational content...</p>
        <style>{`
          @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
          }
          @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
          }
        `}</style>
      </div>
    );
  }

  return (
    <div className="success-stories-container">
      <div className="stories-header">
        <h2>🌟 Growth & Inspiration</h2>
        <p>Learn from peers who transformed their careers</p>
      </div>

      <div className="tab-navigation">
        <button 
          className={`tab-btn ${activeTab === 'stories' ? 'active' : ''}`}
          onClick={() => setActiveTab('stories')}
        >
          📖 Success Stories
        </button>
        <button 
          className={`tab-btn ${activeTab === 'insights' ? 'active' : ''}`}
          onClick={() => setActiveTab('insights')}
        >
          📊 Peer Insights
        </button>
      </div>

      {activeTab === 'stories' && (
        <div className="stories-grid">
          {stories.map((story, index) => (
            <div key={story.id} className="story-card">
              <div className="story-header">
                <div className="story-avatar">{story.name[0]}</div>
                <div>
                  <h3>{story.name}</h3>
                  <p className="story-college">{story.college}</p>
                  {story.is_real && <span className="real-badge">✓ Real User</span>}
                </div>
              </div>

              <div className="story-timeline">
                <div className="timeline-item">
                  <span className="timeline-label">Started</span>
                  <p>{story.initial_state}</p>
                </div>
                <div className="timeline-arrow">→</div>
                <div className="timeline-item">
                  <span className="timeline-label">Learned</span>
                  <div className="skills-list">
                    {story.skills_learned.map((skill, i) => (
                      <span key={i} className="skill-badge">{skill}</span>
                    ))}
                  </div>
                </div>
                <div className="timeline-arrow">→</div>
                <div className="timeline-item">
                  <span className="timeline-label">Achieved</span>
                  <p className="achievement-text">{story.achievement}</p>
                </div>
              </div>

              <div className="story-stats">
                <div className="stat">
                  <span className="stat-icon">⏱️</span>
                  <span>{story.time_period}</span>
                </div>
                <div className="stat">
                  <span className="stat-icon">⭐</span>
                  <span>{story.points_earned} pts</span>
                </div>
              </div>

              <div className="story-action">
                <strong>Key Action:</strong>
                <p>{story.key_action}</p>
              </div>
            </div>
          ))}
        </div>
      )}

      {activeTab === 'insights' && peerInsights && (
        <div className="insights-section">
          <div className="your-stats-card">
            <h3>📈 Your Current Standing</h3>
            <div className="stats-row">
              <div className="stat-box">
                <span className="stat-value">{peerInsights.your_stats.points}</span>
                <span className="stat-label">Points</span>
              </div>
              <div className="stat-box">
                <span className="stat-value">{peerInsights.your_stats.streak}</span>
                <span className="stat-label">Day Streak</span>
              </div>
              <div className="stat-box">
                <span className="stat-value">{peerInsights.your_stats.achievements}</span>
                <span className="stat-label">Achievements</span>
              </div>
            </div>
          </div>

          <div className="peer-comparison">
            <h3>👥 Peer Comparison</h3>
            <div className="comparison-grid">
              <div className="comparison-card">
                <h4>Your College Average</h4>
                <div className="comparison-stats">
                  <div><strong>{peerInsights.peer_averages.same_college.points}</strong> points</div>
                  <div><strong>{peerInsights.peer_averages.same_college.streak}</strong> day streak</div>
                  <div><strong>{peerInsights.peer_averages.same_college.achievements}</strong> achievements</div>
                </div>
                <p className="peer-count">{peerInsights.peer_averages.college_peers} students</p>
              </div>
              <div className="comparison-card">
                <h4>All Peers Average</h4>
                <div className="comparison-stats">
                  <div><strong>{peerInsights.peer_averages.all_peers.points}</strong> points</div>
                  <div><strong>{peerInsights.peer_averages.all_peers.streak}</strong> day streak</div>
                  <div><strong>{peerInsights.peer_averages.all_peers.achievements}</strong> achievements</div>
                </div>
                <p className="peer-count">{peerInsights.peer_averages.total_peers} total users</p>
              </div>
            </div>
          </div>

          <div className="growth-insights">
            <h3>💡 How to Grow - Healthy Competition</h3>
            <div className="insights-list">
              {peerInsights.insights.map((insight, index) => (
                <div key={index} className={`insight-card ${insight.status}`}>
                  <div className="insight-icon">{insight.icon}</div>
                  <div className="insight-content">
                    <h4>{insight.message}</h4>
                    <p className="motivation">{insight.motivation}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="recommendations">
            <h3>🎯 Your Action Plan</h3>
            <div className="recommendations-list">
              {peerInsights.recommendations.map((rec, index) => (
                <div key={index} className="recommendation-card">
                  <div className="rec-header">
                    <span className={`priority-badge ${rec.priority}`}>{rec.priority.toUpperCase()}</span>
                    <span className="rec-category">{rec.category}</span>
                  </div>
                  <h4>{rec.action}</h4>
                  <div className="rec-footer">
                    <span className="rec-impact">💥 {rec.impact}</span>
                    <span className="rec-time">⏱️ {rec.time}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default SuccessStories;
