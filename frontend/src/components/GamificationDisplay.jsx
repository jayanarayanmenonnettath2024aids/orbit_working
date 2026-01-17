import { useState, useEffect } from 'react';
import './GamificationDisplay.css';

function GamificationDisplay({ 
  userId,
  showTasks: showTasksProp,
  setShowTasks: setShowTasksProp,
  showAchievements: showAchievementsProp,
  setShowAchievements: setShowAchievementsProp,
  showLeaderboard: showLeaderboardProp,
  setShowLeaderboard: setShowLeaderboardProp,
  leaderboardData
}) {
  const [gamification, setGamification] = useState(null);
  const [showAchievements, setShowAchievements] = useState(showAchievementsProp || false);
  const [showLeaderboard, setShowLeaderboard] = useState(showLeaderboardProp || false);
  const [showTasks, setShowTasks] = useState(showTasksProp || false);
  const [leaderboard, setLeaderboard] = useState(leaderboardData || []);
  const [showSeparator, setShowSeparator] = useState(false);

  // Use parent setters if provided, otherwise use local state
  const handleShowTasks = (value) => {
    if (setShowTasksProp) setShowTasksProp(value);
    else setShowTasks(value);
  };

  const handleShowAchievements = (value) => {
    if (setShowAchievementsProp) setShowAchievementsProp(value);
    else setShowAchievements(value);
  };

  const handleShowLeaderboard = (value) => {
    if (setShowLeaderboardProp) setShowLeaderboardProp(value);
    else setShowLeaderboard(value);
  };

  // Sync props to local state
  useEffect(() => {
    if (showTasksProp !== undefined) setShowTasks(showTasksProp);
  }, [showTasksProp]);

  useEffect(() => {
    if (showAchievementsProp !== undefined) setShowAchievements(showAchievementsProp);
  }, [showAchievementsProp]);

  useEffect(() => {
    if (showLeaderboardProp !== undefined) setShowLeaderboard(showLeaderboardProp);
  }, [showLeaderboardProp]);

  useEffect(() => {
    if (leaderboardData) setLeaderboard(leaderboardData);
  }, [leaderboardData]);

  useEffect(() => {
    fetchGamification();
  }, [userId]);

  const fetchGamification = async () => {
    try {
      const apiUrl = import.meta.env.VITE_API_URL;
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
      const apiUrl = import.meta.env.VITE_API_URL;
      const response = await fetch(`${apiUrl}/gamification/leaderboard?user_id=${userId}&top=10`);
      if (response.ok) {
        const data = await response.json();
        setLeaderboard(data.leaderboard || data);
        setShowSeparator(data.show_separator || false);
        handleShowLeaderboard(true);
      }
    } catch (error) {
      console.error('Error fetching leaderboard:', error);
    }
  };

  if (!gamification) {
    return null;
  }

  const rarityColors = {
    common: '#94a3b8',
    uncommon: '#22c55e',
    rare: '#3b82f6',
    epic: '#a855f7',
    legendary: '#eab308'
  };

  return (
    <>
      {/* Disclaimer Banner */}
      <div className="gamification-disclaimer">
        <span className="disclaimer-icon">⚠️</span>
        <span className="disclaimer-text">
          <strong>Fair Play Policy:</strong> Earn points through genuine actions. Cheating or gaming the system may result in point deduction or account suspension.
        </span>
      </div>

      {/* Compact Gamification Bar */}
      <div className="gamification-bar">
        <div className="gami-level" title={`Level ${gamification.level}: ${gamification.level_name}`}>
          <span className="level-icon">{gamification.level_icon}</span>
          <span className="level-text">Lv.{gamification.level}</span>
        </div>

        <div className="gami-points" title="Total Points">
          <span className="points-icon">⭐</span>
          <span className="points-text">{gamification.total_points}</span>
        </div>

        <div className="gami-progress" title={`${gamification.progress_to_next}% to next level`}>
          <div className="progress-bar">
            <div
              className="progress-fill"
              style={{ 
                width: `${gamification.progress_to_next}%`,
                background: gamification.level_color || '#6366f1'
              }}
            />
          </div>
          {gamification.next_level && (
            <span className="next-level">{gamification.next_level.name}</span>
          )}
        </div>

        <div className="gami-streak" title={`${gamification.login_streak} day streak`}>
          <span className="streak-icon">🔥</span>
          <span className="streak-text">{gamification.login_streak}</span>
        </div>

        <button className="gami-tasks-btn" onClick={() => handleShowTasks(true)}>
          <span>✅</span>
          <span>Tasks</span>
        </button>

        <button className="gami-achievements-btn" onClick={() => handleShowAchievements(true)}>
          <span>🏆</span>
          <span>{gamification.achievements_count}</span>
        </button>

        <button className="gami-leaderboard-btn" onClick={fetchLeaderboard}>
          <span>📊</span>
          <span>Ranks</span>
        </button>
      </div>

      {/* Tasks Modal */}
      {showTasks && (
        <div className="modal-overlay" onClick={() => handleShowTasks(false)}>
          <div className="modal-content large" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h2>✅ Daily & Weekly Tasks</h2>
              <button className="modal-close" onClick={() => handleShowTasks(false)}>×</button>
            </div>
            
            <div className="tasks-section">
              <h3 className="tasks-heading">📅 Daily Tasks (Reset at Midnight)</h3>
              <div className="tasks-list">
                {gamification.daily_tasks?.map((task) => (
                  <div key={task.id} className={`task-card ${task.completed ? 'completed' : ''}`}>
                    <div className="task-header">
                      <div className="task-title">{task.title}</div>
                      {task.completed && <span className="task-badge">✓ Completed</span>}
                    </div>
                    <div className="task-description">{task.description}</div>
                    <div className="task-progress">
                      <div className="task-progress-bar">
                        <div 
                          className="task-progress-fill"
                          style={{ width: `${task.percentage}%` }}
                        />
                      </div>
                      <span className="task-progress-text">
                        {task.progress}/{task.target}
                      </span>
                    </div>
                    <div className="task-reward">+{task.points} pts</div>
                  </div>
                ))}
              </div>

              <h3 className="tasks-heading">📆 Weekly Tasks (Reset on Monday)</h3>
              <div className="tasks-list">
                {gamification.weekly_tasks?.map((task) => (
                  <div key={task.id} className={`task-card ${task.completed ? 'completed' : ''}`}>
                    <div className="task-header">
                      <div className="task-title">{task.title}</div>
                      {task.completed && <span className="task-badge">✓ Completed</span>}
                    </div>
                    <div className="task-description">{task.description}</div>
                    <div className="task-progress">
                      <div className="task-progress-bar">
                        <div 
                          className="task-progress-fill weekly"
                          style={{ width: `${task.percentage}%` }}
                        />
                      </div>
                      <span className="task-progress-text">
                        {task.progress}/{task.target}
                      </span>
                    </div>
                    <div className="task-reward weekly">+{task.points} pts</div>
                  </div>
                ))}
              </div>

              <div className="tasks-stats">
                <div className="stat-item">
                  <div className="stat-value">{gamification.tasks_completed_total}</div>
                  <div className="stat-label">Tasks Completed</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Achievements Modal */}
      {showAchievements && (
        <div className="modal-overlay" onClick={() => handleShowAchievements(false)}>
          <div className="modal-content large" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h2>🏆 Achievements</h2>
              <button className="modal-close" onClick={() => handleShowAchievements(false)}>×</button>
            </div>
            <div className="achievements-grid">
              {gamification.achievements.map((achievement) => (
                <div 
                  key={achievement.id} 
                  className="achievement-card earned"
                  style={{ borderColor: rarityColors[achievement.rarity] || '#6366f1' }}
                >
                  <div className="achievement-icon">{achievement.icon}</div>
                  <div className="achievement-name">{achievement.name}</div>
                  <div className="achievement-desc">{achievement.description}</div>
                  <div className="achievement-rarity" style={{ color: rarityColors[achievement.rarity] }}>
                    {achievement.rarity?.toUpperCase()}
                  </div>
                  <div className="achievement-points">+{achievement.points} pts</div>
                </div>
              ))}
              {gamification.achievements.length === 0 && (
                <p className="no-achievements">No achievements yet. Complete tasks and explore opportunities to earn badges!</p>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Leaderboard Modal */}
      {showLeaderboard && (
        <div className="modal-overlay" onClick={() => handleShowLeaderboard(false)}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h2>📊 Global Leaderboard</h2>
              <button className="modal-close" onClick={() => handleShowLeaderboard(false)}>×</button>
            </div>
            <div className="leaderboard-list">
              {leaderboard.map((user, idx) => (
                <>
                  {/* Show separator before current user if they're not in top 10 */}
                  {showSeparator && idx === 10 && (
                    <div key="separator" className="leaderboard-separator">
                      <span>• • •</span>
                    </div>
                  )}
                  <div
                    key={user.user_id}
                    className={`leaderboard-item ${user.user_id === userId ? 'current-user' : ''} ${idx < 3 ? 'top-3' : ''}`}
                  >
                    <div className="lb-rank">
                      {idx === 0 && '🥇'}
                      {idx === 1 && '🥈'}
                      {idx === 2 && '🥉'}
                      {idx > 2 && `#${user.rank}`}
                    </div>
                    <div className="lb-info">
                      <div className="lb-name">{user.name}</div>
                      <div className="lb-level">
                        {user.level_icon} {user.level_name} • {user.achievements_count} achievements
                      </div>
                    </div>
                    <div className="lb-points">{user.points} pts</div>
                  </div>
                </>
              ))}
            </div>
          </div>
        </div>
      )}
    </>
  );
}

export default GamificationDisplay;
