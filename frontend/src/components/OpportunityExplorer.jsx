import React, { useState, useEffect } from 'react';
import { Search, ExternalLink, ChevronDown, ChevronUp, CheckCircle, AlertCircle, Clock, Bookmark } from 'lucide-react';
import { searchOpportunities, analyzeEligibility, getPersonalizedSuggestions } from '../services/api';
import { trackSearch, trackEligibilityCheck, trackSaveToTracker } from '../utils/gamification';
import './OpportunityCard.css';
import './EligibilityAnalysis.css';

function OpportunityExplorer({ profile, opportunities, setOpportunities }) {
  const [searchQuery, setSearchQuery] = useState('');
  const [searching, setSearching] = useState(false);
  const [analyzing, setAnalyzing] = useState({});
  const [analyses, setAnalyses] = useState({});
  const [expandedOpp, setExpandedOpp] = useState(null);
  const [saving, setSaving] = useState({});
  const [quickSearches, setQuickSearches] = useState(['AI hackathon', 'software internship', 'student fellowship', 'coding competition']);

  // Fetch personalized suggestions when profile loads
  useEffect(() => {
    if (profile?.profile_id) {
      getPersonalizedSuggestions(profile.profile_id)
        .then(data => {
          if (data.suggestions && data.suggestions.length > 0) {
            // Take first 4-5 suggestions for quick search
            setQuickSearches(data.suggestions.slice(0, 4));
          }
        })
        .catch(err => {
          console.log('Could not fetch personalized suggestions, using defaults:', err);
        });
    }
  }, [profile?.profile_id]);

  const handleSaveToTracker = async (opportunity) => {
    const oppId = opportunity.opportunity_id;
    setSaving(prev => ({ ...prev, [oppId]: true }));
    
    try {
      // Get userId - prefer localStorage, but fallback to profile if needed
      // This ensures consistency across the app
      let userId = localStorage.getItem('user_id');
      
      // If no user_id in localStorage, check if we have profile data
      if (!userId && profile) {
        // Use profile.user_id if available, otherwise profile_id
        userId = profile.user_id || profile.profile_id;
        // Store it in localStorage for future use
        if (userId) {
          localStorage.setItem('user_id', userId);
        }
      }
      
      if (!userId) {
        alert('❌ Please log in to save opportunities');
        setSaving(prev => ({ ...prev, [oppId]: false }));
        return;
      }
      
      console.log('💾 Saving with user_id:', userId);
      
      const analysis = analyses[oppId];
      const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:5000';
      
      console.log('API URL:', apiUrl);
      console.log('Saving to tracker:', {
        user_id: userId,
        opportunity_title: opportunity.title,
        opportunity_link: opportunity.link
      });
      
      // Test backend connectivity first
      try {
        const healthCheck = await fetch(`${apiUrl}/health`, { 
          method: 'GET',
          signal: AbortSignal.timeout(5000)
        });
        if (!healthCheck.ok) {
          throw new Error('Backend server is not responding');
        }
      } catch (healthErr) {
        console.error('Backend health check failed:', healthErr);
        alert('❌ Cannot connect to backend server. Please ensure:\n1. Backend is running (python app.py in backend folder)\n2. Server is on http://localhost:5000\n3. No firewall blocking the connection');
        setSaving(prev => ({ ...prev, [oppId]: false }));
        return;
      }
      
      const response = await fetch(`${apiUrl}/applications`, {
        method: 'POST',
        headers: { 
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        },
        body: JSON.stringify({
          user_id: userId,
          opportunity_title: opportunity.title,
          opportunity_link: opportunity.link,
          deadline: opportunity.deadline || 'Not specified',
          eligibility_score: analysis?.confidence_score || null,
          priority: 'medium',
          notes: ''
        }),
        signal: AbortSignal.timeout(10000) // 10 second timeout
      });
      
      const data = await response.json();
      
      if (response.ok) {
        console.log('✅ Saved successfully:', data);
        alert('✅ Saved to Application Tracker! Check the tracker tab.');
        
        // Track save to tracker for gamification
        trackSaveToTracker(oppId, opportunity.title);
      } else {
        console.error('❌ Save failed:', data);
        throw new Error(data.error || `Server error: ${response.status}`);
      }
    } catch (err) {
      console.error('Save error:', err);
      if (err.name === 'TimeoutError') {
        alert('❌ Request timeout. Backend server may be slow or not running.');
      } else if (err.message.includes('fetch')) {
        alert('❌ Network error: Cannot connect to backend.\nPlease check:\n• Backend server is running\n• No firewall blocking localhost:5000');
      } else {
        alert(`❌ Failed to save: ${err.message}`);
      }
    } finally {
      setSaving(prev => ({ ...prev, [oppId]: false }));
    }
  };

  const handleSearch = async (e) => {
    e.preventDefault();
    if (!searchQuery.trim()) return;

    setSearching(true);
    try {
      const result = await searchOpportunities(searchQuery);
      setOpportunities(result.opportunities);
      
      // Track search action for gamification
      trackSearch(searchQuery);
    } catch (err) {
      console.error('Search failed:', err);
      alert('Failed to search opportunities');
    } finally {
      setSearching(false);
    }
  };

  const handleAnalyze = async (opportunityId) => {
    setAnalyzing(prev => ({ ...prev, [opportunityId]: true }));
    
    try {
      const result = await analyzeEligibility(profile.profile_id, opportunityId);
      setAnalyses(prev => ({
        ...prev,
        [opportunityId]: result
      }));
      
      // Track eligibility check for gamification
      if (result?.confidence_score !== undefined) {
        trackEligibilityCheck(opportunityId, result.confidence_score);
      }
    } catch (err) {
      console.error('Analysis failed:', err);
      console.error('Error details:', err.response?.data);
      const errorMessage = err.response?.data?.error || 'Failed to analyze eligibility';
      alert(errorMessage);
    } finally {
      setAnalyzing(prev => ({ ...prev, [opportunityId]: false }));
    }
  };

  const getStatusBadge = (status) => {
    const badges = {
      'Eligible': { icon: CheckCircle, color: 'green', text: 'Eligible' },
      'Partially Eligible': { icon: Clock, color: 'yellow', text: 'Partially Eligible' },
      'Not Yet Eligible': { icon: AlertCircle, color: 'red', text: 'Not Yet Eligible' }
    };

    const badge = badges[status] || badges['Partially Eligible'];
    const Icon = badge.icon;

    return (
      <div className={`status-badge status-${badge.color}`}>
        <Icon className="icon-sm" />
        {badge.text}
      </div>
    );
  };

  const getConfidenceColor = (score) => {
    if (score >= 80) return 'green';
    if (score >= 50) return 'yellow';
    return 'red';
  };

  return (
    <div className="opportunity-explorer">
      {/* Hero Section */}
      <div style={{
        textAlign: 'center',
        padding: '48px 0 32px',
        animation: 'fadeInUp 0.8s ease-out'
      }}>
        <h2 style={{
          fontSize: '42px',
          fontWeight: '800',
          background: 'linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%)',
          WebkitBackgroundClip: 'text',
          WebkitTextFillColor: 'transparent',
          backgroundClip: 'text',
          marginBottom: '12px',
          letterSpacing: '-0.02em'
        }}>
          Discover Opportunities
        </h2>
        <p style={{
          fontSize: '18px',
          color: '#64748b',
          fontWeight: '500',
          maxWidth: '600px',
          margin: '0 auto'
        }}>
          Search for real opportunities from across the web
        </p>
      </div>

      {/* Fancy Search Bar */}
      <form onSubmit={handleSearch} style={{
        maxWidth: '1500px',
        margin: '0 auto 32px',
        animation: 'fadeInUp 0.8s ease-out 0.2s both'
      }}>
        <div style={{
          position: 'relative',
          background: 'white',
          borderRadius: '20px',
          padding: '10px',
          boxShadow: '0 10px 40px rgba(79, 70, 229, 0.15), 0 0 0 1px rgba(79, 70, 229, 0.1)',
          transition: 'all 0.3s ease',
          border: '2px solid transparent'
        }}
        onFocus={(e) => {
          e.currentTarget.style.boxShadow = '0 20px 60px rgba(79, 70, 229, 0.25), 0 0 0 2px #4F46E5';
          e.currentTarget.style.borderColor = '#4F46E5';
        }}
        onBlur={(e) => {
          e.currentTarget.style.boxShadow = '0 10px 40px rgba(79, 70, 229, 0.15), 0 0 0 1px rgba(79, 70, 229, 0.1)';
          e.currentTarget.style.borderColor = 'transparent';
        }}>
          <div style={{
            display: 'flex',
            alignItems: 'center',
            gap: '14px'
          }}>
            <Search style={{
              marginLeft: '14px',
              width: '26px',
              height: '26px',
              color: '#4F46E5',
              flexShrink: 0
            }} />
            <input
              type="text"
              placeholder="Search for hackathons, internships, fellowships, competitions..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              disabled={searching}
              style={{
                flex: 1,
                border: 'none',
                outline: 'none',
                fontSize: '17px',
                padding: '18px 14px',
                background: 'transparent',
                color: '#0f172a',
                fontWeight: '500'
              }}
            />
            <button 
              type="submit" 
              disabled={searching}
              style={{
                padding: '16px 32px',
                background: 'linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%)',
                color: 'white',
                border: 'none',
                borderRadius: '14px',
                fontSize: '16px',
                fontWeight: '700',
                cursor: searching ? 'not-allowed' : 'pointer',
                transition: 'all 0.3s ease',
                boxShadow: '0 4px 15px rgba(79, 70, 229, 0.3)',
                opacity: searching ? 0.6 : 1,
                minWidth: '140px'
              }}
              onMouseOver={(e) => {
                if (!searching) {
                  e.currentTarget.style.transform = 'translateY(-2px)';
                  e.currentTarget.style.boxShadow = '0 8px 25px rgba(79, 70, 229, 0.4)';
                }
              }}
              onMouseOut={(e) => {
                e.currentTarget.style.transform = 'translateY(0)';
                e.currentTarget.style.boxShadow = '0 4px 15px rgba(79, 70, 229, 0.3)';
              }}>
              {searching ? 'Searching...' : 'Search'}
            </button>
          </div>
        </div>
      </form>

      {/* Quick Search Suggestions - Enhanced */}
      <div style={{
        maxWidth: '900px',
        margin: '0 auto 48px',
        textAlign: 'center',
        animation: 'fadeInUp 0.8s ease-out 0.3s both'
      }}>
        <span style={{
          fontSize: '14px',
          color: '#94a3b8',
          fontWeight: '600',
          textTransform: 'uppercase',
          letterSpacing: '0.8px',
          marginRight: '16px'
        }}>Quick searches:</span>
        <div style={{
          display: 'inline-flex',
          gap: '12px',
          flexWrap: 'wrap',
          justifyContent: 'center',
          marginTop: '12px'
        }}>
          {quickSearches.map(term => (
            <button
              key={term}
              onClick={() => {
                setSearchQuery(term);
                searchOpportunities(term).then(result => setOpportunities(result.opportunities));
              }}
              style={{
                padding: '12px 24px',
                background: 'linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%)',
                border: '2px solid #e2e8f0',
                borderRadius: '12px',
                fontSize: '15px',
                fontWeight: '600',
                color: '#475569',
                cursor: 'pointer',
                transition: 'all 0.3s ease',
                boxShadow: '0 2px 8px rgba(0, 0, 0, 0.05)'
              }}
              onMouseOver={(e) => {
                e.currentTarget.style.background = 'linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%)';
                e.currentTarget.style.color = 'white';
                e.currentTarget.style.borderColor = '#4F46E5';
                e.currentTarget.style.transform = 'translateY(-2px)';
                e.currentTarget.style.boxShadow = '0 8px 20px rgba(79, 70, 229, 0.3)';
              }}
              onMouseOut={(e) => {
                e.currentTarget.style.background = 'linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%)';
                e.currentTarget.style.color = '#475569';
                e.currentTarget.style.borderColor = '#e2e8f0';
                e.currentTarget.style.transform = 'translateY(0)';
                e.currentTarget.style.boxShadow = '0 2px 8px rgba(0, 0, 0, 0.05)';
              }}>
              {term}
            </button>
          ))}
        </div>
      </div>

      {/* Results */}
      {opportunities.length > 0 && (
        <div className="opportunities-grid">
          <h3 style={{ marginBottom: '24px', fontSize: '1.5rem', fontWeight: 700 }}>
            {opportunities.length} Opportunities Found
          </h3>

          {opportunities.map((opp) => {
            const analysis = analyses[opp.opportunity_id];
            const isExpanded = expandedOpp === opp.opportunity_id;
            const isAnalyzing = analyzing[opp.opportunity_id];

            return (
              <div key={opp.opportunity_id} className="opportunity-card">
                {/* Card Header */}
                <div className="opp-header">
                  <div className="opp-title-section">
                    <h4 className="opp-title">{opp.title}</h4>
                    <div className="opp-meta">
                      <span className="opp-type">{opp.type}</span>
                      {opp.deadline && (
                        <span className="opp-deadline">
                          <Clock size={12} />
                          {opp.deadline}
                        </span>
                      )}
                    </div>
                  </div>
                </div>

                {/* Analysis Quick Summary (if analyzed) */}
                {analysis && (
                  <div className="opp-analysis-quick">
                    <div className="quick-score">
                      <div className="quick-score-value">{analysis.confidence_score}%</div>
                      <div className="quick-score-label">Match</div>
                    </div>
                    <div className="quick-status">
                      <div className={`status-badge-inline ${analysis.eligibility_status.replace(/_/g, '-')}`}>
                        {analysis.eligibility_status === 'eligible' && '✅ Eligible'}
                        {analysis.eligibility_status === 'partially_eligible' && '⚠️ Partially'}
                        {analysis.eligibility_status === 'not_eligible' && '❌ Not Eligible'}
                      </div>
                    </div>
                  </div>
                )}

                {/* Card Body */}
                <div className="opp-body">
                  <p className="opp-snippet">{opp.snippet}</p>
                </div>

                {/* Card Footer - Actions */}
                <div className="opp-footer">
                  <a 
                    href={opp.link} 
                    target="_blank" 
                    rel="noopener noreferrer"
                    className="opp-link"
                  >
                    <ExternalLink size={16} />
                    View Details
                  </a>

                  {!analysis ? (
                    <button
                      className="btn btn-primary"
                      onClick={() => handleAnalyze(opp.opportunity_id)}
                      disabled={isAnalyzing}
                    >
                      {isAnalyzing ? 'Analyzing...' : 'Check Eligibility'}
                    </button>
                  ) : null}

                  <button
                    className="btn btn-action"
                    onClick={() => handleSaveToTracker(opp)}
                    disabled={saving[opp.opportunity_id]}
                  >
                    <Bookmark size={16} />
                    {saving[opp.opportunity_id] ? 'Saving...' : 'Save'}
                  </button>

                  {analysis && (
                    <button
                      className="btn btn-ghost"
                      onClick={() => setExpandedOpp(isExpanded ? null : opp.opportunity_id)}
                    >
                      {isExpanded ? (
                        <>
                          <ChevronUp size={16} />
                          Hide Analysis
                        </>
                      ) : (
                        <>
                          <ChevronDown size={16} />
                          Show Analysis
                        </>
                      )}
                    </button>
                  )}
                </div>

                {/* Expanded Analysis - PRODUCTION UI */}
                {/* Expanded Analysis - PRODUCTION UI */}
                {analysis && isExpanded && (
                  <div className="analysis-details-premium">
                    {/* SCORE HERO - THE FOCAL POINT */}
                    <div className="analysis-score-hero">
                      <div className="score-primary">
                        <div>
                          <div className="score-number">
                            {analysis.confidence_score}<span className="score-percent">%</span>
                          </div>
                          <div className="score-label">Match Score</div>
                        </div>
                      </div>
                      
                      <div className="score-status">
                        <div className={`status-badge-large ${analysis.eligibility_status.replace(/_/g, '-')}`}>
                          {analysis.eligibility_status === 'eligible' && '✅ Eligible'}
                          {analysis.eligibility_status === 'partially_eligible' && '⚠️ Partially Eligible'}
                          {analysis.eligibility_status === 'not_eligible' && '❌ Not Eligible'}
                        </div>
                      </div>
                    </div>

                    {/* Summary Section */}
                    {analysis.explanation_simple && (
                      <div className="analysis-summary-section">
                        <div className="summary-section-title">Analysis Summary</div>
                        <p className="summary-text">{analysis.explanation_simple}</p>
                      </div>
                    )}

                    {/* REQUIREMENTS BREAKDOWN - CLEAR VISUAL SEPARATION */}
                    <div className="requirements-breakdown">
                      {/* ✅ What You Have */}
                      {analysis.reasons_met && analysis.reasons_met.length > 0 && (
                        <div className="requirement-section met">
                          <div className="requirement-header">
                            <div className="requirement-icon">✓</div>
                            <h4 className="requirement-title">✅ Requirements Met</h4>
                          </div>
                          <ul className="requirement-list">
                            {analysis.reasons_met.map((reason, idx) => (
                              <li key={idx} className="requirement-item">
                                <span className="requirement-item-icon">✓</span>
                                <span>{reason}</span>
                              </li>
                            ))}
                          </ul>
                        </div>
                      )}

                      {/* ❌ Missing Requirements */}
                      {analysis.reasons_not_met && analysis.reasons_not_met.length > 0 && (
                        <div className="requirement-section missing">
                          <div className="requirement-header">
                            <div className="requirement-icon">✗</div>
                            <h4 className="requirement-title">❌ Missing Requirements</h4>
                          </div>
                          <ul className="requirement-list">
                            {analysis.reasons_not_met.map((reason, idx) => (
                              <li key={idx} className="requirement-item">
                                <span className="requirement-item-icon">✗</span>
                                <span>{reason}</span>
                              </li>
                            ))}
                          </ul>
                        </div>
                      )}
                    </div>

                    {/* ROADMAP SECTION - NUMBERED STEPS */}
                    {analysis.next_steps && analysis.next_steps.length > 0 && (
                      <div className="roadmap-section">
                        <div className="roadmap-header">
                          <h3 className="roadmap-title">🎯 Your Path to Eligibility</h3>
                          <p className="roadmap-subtitle">Follow these steps to improve your match score</p>
                        </div>
                        
                        <div className="roadmap-steps">
                          {analysis.next_steps.map((step, idx) => (
                            <div key={idx} className="roadmap-step">
                              <div className="step-number">{idx + 1}</div>
                              <div className="step-content">
                                <h5 className="step-title">{step.action || step.title || 'Action Step'}</h5>
                                <p className="step-description">{step.reason || step.description || ''}</p>
                                {step.time_estimate && (
                                  <div className="step-meta">
                                    <div className="step-time">
                                      <Clock size={14} />
                                      <span>{step.time_estimate}</span>
                                    </div>
                                  </div>
                                )}
                              </div>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}

                    {/* Action Footer */}
                    <div className="analysis-action-footer">
                      <div className="footer-message">
                        <div className="footer-title">Ready to take action?</div>
                        <p className="footer-text">Save this opportunity and track your progress</p>
                      </div>
                      <div className="footer-actions">
                        <button
                          className="btn btn-action"
                          onClick={() => handleSaveToTracker(opp)}
                          disabled={saving[opp.opportunity_id]}
                        >
                          <Bookmark size={16} />
                          {saving[opp.opportunity_id] ? 'Saving...' : 'Save to Tracker'}
                        </button>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}

export default OpportunityExplorer;
