import { useState, useEffect } from 'react';
import {
  LineChart, Line, BarChart, Bar, PieChart, Pie, Cell,
  XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer
} from 'recharts';
import { TrendingUp, TrendingDown } from 'lucide-react';
import './AnalyticsDashboard.css';
import './AnalyticsKPI.css';

const COLORS = ['#2563eb', '#f97316', '#06b6d4', '#10b981', '#8b5cf6'];

function AnalyticsDashboard({ userId }) {
  const [analytics, setAnalytics] = useState(null);
  const [leaderboardStats, setLeaderboardStats] = useState(null);
  const [insights, setInsights] = useState([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('overview');

  useEffect(() => {
    fetchAnalytics();
  }, [userId]);

  const fetchAnalytics = async () => {
    try {
      setLoading(true);
      const apiUrl = import.meta.env.VITE_API_URL;

      // Fetch all analytics data
      const [analyticsRes, leaderboardRes, insightsRes] = await Promise.all([
        fetch(`${apiUrl}/analytics/${userId}`),
        fetch(`${apiUrl}/analytics/leaderboard/${userId}`),
        fetch(`${apiUrl}/analytics/insights/${userId}`)
      ]);

      if (analyticsRes.ok) {
        const data = await analyticsRes.json();
        setAnalytics(data);
      }

      if (leaderboardRes.ok) {
        const data = await leaderboardRes.json();
        setLeaderboardStats(data);
      }

      if (insightsRes.ok) {
        const data = await insightsRes.json();
        setInsights(data);
      }
    } catch (error) {
      console.error('Error fetching analytics:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="analytics-loading">Loading analytics...</div>;
  }

  if (!analytics) {
    return <div className="analytics-error">No analytics data available</div>;
  }

  const stats = analytics.statistics;
  const peerComparison = analytics.peer_comparison;

  // Prepare data for charts
  const statusData = [
    { name: 'Pending', value: stats.pending },
    { name: 'Under Review', value: stats.under_review },
    { name: 'Accepted', value: stats.accepted },
    { name: 'Rejected', value: stats.rejected }
  ].filter(item => item.value > 0);

  const categoryData = Object.entries(stats.categories).map(([name, value]) => ({
    name: name.charAt(0).toUpperCase() + name.slice(1),
    value
  }));

  const monthlyTrendData = Object.entries(stats.monthly_trend).map(([month, count]) => ({
    month: new Date(month + '-01').toLocaleDateString('default', { month: 'short' }),
    applications: count
  }));

  const comparisonData = peerComparison ? [
    {
      metric: 'Points',
      You: stats.total_points,
      Average: peerComparison.avg_points
    },
    {
      metric: 'Applications',
      You: stats.total_applications,
      Average: peerComparison.avg_applications
    }
  ] : [];

  return (
    <div className="analytics-dashboard">
      <div className="analytics-header">
        <h2>📊 Analytics Dashboard</h2>
        <p className="analytics-subtitle">Track your progress and compare with peers</p>
      </div>

      {/* Insights Section */}
      {insights.length > 0 && (
        <div className="insights-section">
          {insights.map((insight, idx) => (
            <div key={idx} className={`insight-card insight-${insight.type}`}>
              <span className="insight-icon">{insight.icon}</span>
              <p>{insight.message}</p>
            </div>
          ))}
        </div>
      )}

      {/* Tabs */}
      <div className="analytics-tabs">
        <button
          className={activeTab === 'overview' ? 'active' : ''}
          onClick={() => setActiveTab('overview')}
        >
          Overview
        </button>
        <button
          className={activeTab === 'ranking' ? 'active' : ''}
          onClick={() => setActiveTab('ranking')}
        >
          Rankings
        </button>
        <button
          className={activeTab === 'activity' ? 'active' : ''}
          onClick={() => setActiveTab('activity')}
        >
          Activity
        </button>
      </div>

      {/* Overview Tab */}
      {activeTab === 'overview' && (
        <div className="analytics-content">
          {/* KPI Cards Grid - PRODUCTION DESIGN */}
          <div className="kpi-grid">
            {/* Total Applications */}
            <div className="kpi-card primary">
              <div className="kpi-header">
                <div className="kpi-icon">📝</div>
                <div className="kpi-trend positive">
                  <TrendingUp size={12} />
                  <span>+{Math.round((stats.total_applications / 30) * 100)}%</span>
                </div>
              </div>
              <div className="kpi-body">
                <div className="kpi-value">{stats.total_applications}</div>
                <div className="kpi-label">Total Applications</div>
                <div className="kpi-subtitle">All time activity</div>
              </div>
            </div>

            {/* Acceptance Rate */}
            <div className="kpi-card success">
              <div className="kpi-header">
                <div className="kpi-icon">✅</div>
                <div className="kpi-trend positive">
                  <TrendingUp size={12} />
                  <span>+5%</span>
                </div>
              </div>
              <div className="kpi-body">
                <div className="kpi-value">{stats.acceptance_rate}%</div>
                <div className="kpi-label">Acceptance Rate</div>
                <div className="kpi-subtitle">
                  {stats.acceptance_rate > 50 ? 'Above average' : 'Room for growth'}
                </div>
              </div>
            </div>

            {/* Avg Eligibility Score */}
            <div className="kpi-card cyan">
              <div className="kpi-header">
                <div className="kpi-icon">🎯</div>
                <div className="kpi-trend neutral">
                  <span>--</span>
                </div>
              </div>
              <div className="kpi-body">
                <div className="kpi-value">{stats.avg_eligibility_score}%</div>
                <div className="kpi-label">Avg Match Score</div>
                <div className="kpi-subtitle">Quality targeting</div>
              </div>
            </div>

            {/* Login Streak */}
            <div className="kpi-card orange">
              <div className="kpi-header">
                <div className="kpi-icon">🔥</div>
                <div className="kpi-trend positive">
                  <span>{stats.login_streak} days</span>
                </div>
              </div>
              <div className="kpi-body">
                <div className="kpi-value">{stats.login_streak}</div>
                <div className="kpi-label">Day Streak</div>
                <div className="kpi-subtitle">Keep it up!</div>
              </div>
            </div>
          </div>

          {/* Charts Section */}
          <div className="analytics-charts">
            {/* Application Status Pie Chart */}
            <div className="chart-card">
              <h3 className="chart-title">Application Status</h3>
              <ResponsiveContainer width="100%" height={250}>
                <PieChart>
                  <Pie
                    data={statusData}
                    cx="50%"
                    cy="50%"
                    labelLine={false}
                    label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                    outerRadius={80}
                    fill="#8884d8"
                    dataKey="value"
                  >
                    {statusData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            </div>

            {/* Monthly Trend Line Chart */}
            <div className="chart-card">
              <h3>Monthly Trend</h3>
              <ResponsiveContainer width="100%" height={250}>
                <LineChart data={monthlyTrendData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="month" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Line
                    type="monotone"
                    dataKey="applications"
                    stroke="#8884d8"
                    strokeWidth={2}
                    dot={{ r: 5 }}
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* Charts Row 2 */}
          <div className="charts-row">
            {/* Category Distribution Bar Chart */}
            {categoryData.length > 0 && (
              <div className="chart-card">
                <h3>Applications by Category</h3>
                <ResponsiveContainer width="100%" height={250}>
                  <BarChart data={categoryData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="name" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Bar dataKey="value" fill="#0088FE" />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            )}

            {/* Peer Comparison */}
            {peerComparison && (
              <div className="chart-card">
                <h3>You vs Peers</h3>
                <ResponsiveContainer width="100%" height={250}>
                  <BarChart data={comparisonData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="metric" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Bar dataKey="You" fill="#00C49F" />
                    <Bar dataKey="Average" fill="#FFBB28" />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Rankings Tab - PRODUCTION LEADERBOARD */}
      {activeTab === 'ranking' && leaderboardStats && (
        <div className="rankings-content">
          {/* Your Rank Card */}
          <div className="your-rank-card">
            <div className="rank-content">
              <div className="rank-badge">#{leaderboardStats.user_rank}</div>
              <div className="rank-details">
                <div className="rank-position">
                  #{leaderboardStats.user_rank} out of {leaderboardStats.total_users} users
                </div>
                <div className="rank-subtitle">
                  Top {(100 - leaderboardStats.percentile).toFixed(0)}% • Keep pushing!
                </div>
              </div>
              <div className="rank-points">
                <div className="points-value">{stats.total_points}</div>
                <div className="points-label">Points</div>
              </div>
            </div>
          </div>

          {/* Leaderboard Section */}
          <div className="leaderboard-section">
            <div className="leaderboard-header">
              <h3 className="leaderboard-title">Leaderboard Position</h3>
            </div>
            
            <div className="leaderboard-list">
              {leaderboardStats.surrounding_users.map((user) => (
                <div
                  key={user.rank}
                  className={`leaderboard-item ${user.is_current_user ? 'current-user' : ''} ${
                    user.rank === 1 ? 'rank-1' : user.rank === 2 ? 'rank-2' : user.rank === 3 ? 'rank-3' : ''
                  }`}
                >
                  <div className="leaderboard-rank">
                    {user.rank <= 3 ? (user.rank === 1 ? '🥇' : user.rank === 2 ? '🥈' : '🥉') : user.rank}
                  </div>
                  <div className="leaderboard-user">
                    <div className="user-name">{user.name}</div>
                    {user.college && <div className="user-college">{user.college}</div>}
                  </div>
                  <div className="leaderboard-score">{user.points}</div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Activity Tab */}
      {activeTab === 'activity' && (
        <div className="activity-content">
          <h3>Recent Activity</h3>
          <div className="activity-timeline">
            {analytics.timeline.map((event, idx) => (
              <div key={idx} className="timeline-item">
                <div className="timeline-icon">{event.icon}</div>
                <div className="timeline-content">
                  <p className="timeline-action">{event.action}</p>
                  <p className="timeline-time">
                    {new Date(event.timestamp).toLocaleDateString()} at{' '}
                    {new Date(event.timestamp).toLocaleTimeString()}
                  </p>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

export default AnalyticsDashboard;
