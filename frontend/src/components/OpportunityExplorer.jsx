import React, { useState } from 'react';
import { Search, ExternalLink, ChevronDown, ChevronUp, CheckCircle, AlertCircle, Clock } from 'lucide-react';
import { searchOpportunities, analyzeEligibility } from '../services/api';

function OpportunityExplorer({ profile, opportunities, setOpportunities }) {
  const [searchQuery, setSearchQuery] = useState('');
  const [searching, setSearching] = useState(false);
  const [analyzing, setAnalyzing] = useState({});
  const [analyses, setAnalyses] = useState({});
  const [expandedOpp, setExpandedOpp] = useState(null);

  const handleSearch = async (e) => {
    e.preventDefault();
    if (!searchQuery.trim()) return;

    setSearching(true);
    try {
      const result = await searchOpportunities(searchQuery);
      setOpportunities(result.opportunities);
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
      <h2>Discover Opportunities</h2>
      <p className="subtitle">Search for real opportunities from across the web</p>

      {/* Search Bar */}
      <form onSubmit={handleSearch} className="search-form">
        <div className="search-input-group">
          <Search className="search-icon" />
          <input
            type="text"
            placeholder="Search for hackathons, internships, fellowships..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            disabled={searching}
          />
          <button type="submit" disabled={searching} className="btn btn-primary">
            {searching ? 'Searching...' : 'Search'}
          </button>
        </div>
      </form>

      {/* Quick Search Suggestions */}
      <div className="quick-searches">
        <span className="label">Quick searches:</span>
        {['AI hackathon', 'software internship', 'student fellowship', 'coding competition'].map(term => (
          <button
            key={term}
            className="quick-search-btn"
            onClick={() => {
              setSearchQuery(term);
              searchOpportunities(term).then(result => setOpportunities(result.opportunities));
            }}
          >
            {term}
          </button>
        ))}
      </div>

      {/* Results */}
      {opportunities.length > 0 && (
        <div className="opportunities-list">
          <h3>{opportunities.length} Opportunities Found</h3>

          {opportunities.map((opp) => {
            const analysis = analyses[opp.opportunity_id];
            const isExpanded = expandedOpp === opp.opportunity_id;
            const isAnalyzing = analyzing[opp.opportunity_id];

            return (
              <div key={opp.opportunity_id} className="opportunity-card">
                <div className="opp-header">
                  <div className="opp-main-info">
                    <h4>{opp.title}</h4>
                    <p className="opp-organizer">{opp.organizer}</p>
                    <div className="opp-meta">
                      <span className="opp-type">{opp.type}</span>
                      {opp.deadline && (
                        <span className="opp-deadline">Deadline: {opp.deadline}</span>
                      )}
                    </div>
                  </div>
                  <div className="opp-actions">
                    {analysis ? (
                      <div className="analysis-summary">
                        {getStatusBadge(analysis.eligibility_status)}
                        <div className="confidence-score">
                          <span className={`confidence-value confidence-${getConfidenceColor(analysis.confidence_score)}`}>
                            {analysis.confidence_score}%
                          </span>
                          <span className="confidence-label">confidence</span>
                        </div>
                      </div>
                    ) : (
                      <button
                        className="btn btn-primary"
                        onClick={() => handleAnalyze(opp.opportunity_id)}
                        disabled={isAnalyzing}
                      >
                        {isAnalyzing ? 'Analyzing...' : 'Check Eligibility'}
                      </button>
                    )}
                  </div>
                </div>

                <p className="opp-snippet">{opp.snippet}</p>

                <div className="opp-footer">
                  <a 
                    href={opp.link} 
                    target="_blank" 
                    rel="noopener noreferrer"
                    className="btn btn-text"
                  >
                    <ExternalLink className="icon-sm" />
                    View Details
                  </a>

                  {analysis && (
                    <button
                      className="btn btn-text"
                      onClick={() => setExpandedOpp(isExpanded ? null : opp.opportunity_id)}
                    >
                      {isExpanded ? (
                        <>
                          <ChevronUp className="icon-sm" />
                          Hide Analysis
                        </>
                      ) : (
                        <>
                          <ChevronDown className="icon-sm" />
                          Show Detailed Analysis
                        </>
                      )}
                    </button>
                  )}
                </div>

                {/* Expanded Analysis */}
                {analysis && isExpanded && (
                  <div className="analysis-details">
                    {/* Simple Explanation */}
                    <div className="analysis-section">
                      <h5>📋 Summary</h5>
                      <p className="explanation">{analysis.explanation_simple}</p>
                    </div>

                    {/* What You Have */}
                    {analysis.reasons_met && analysis.reasons_met.length > 0 && (
                      <div className="analysis-section">
                        <h5>✅ What You Have</h5>
                        <ul className="reasons-list reasons-met">
                          {analysis.reasons_met.map((reason, idx) => (
                            <li key={idx}>
                              <CheckCircle className="icon-sm" />
                              {reason}
                            </li>
                          ))}
                        </ul>
                      </div>
                    )}

                    {/* What's Missing */}
                    {analysis.reasons_not_met && analysis.reasons_not_met.length > 0 && (
                      <div className="analysis-section">
                        <h5>❌ What's Missing</h5>
                        <ul className="reasons-list reasons-not-met">
                          {analysis.reasons_not_met.map((reason, idx) => (
                            <li key={idx}>
                              <AlertCircle className="icon-sm" />
                              {reason}
                            </li>
                          ))}
                        </ul>
                      </div>
                    )}

                    {/* Skills to Develop */}
                    {analysis.missing_skills && analysis.missing_skills.length > 0 && (
                      <div className="analysis-section">
                        <h5>🎯 Skills to Develop</h5>
                        <div className="skill-tags">
                          {analysis.missing_skills.map((skill, idx) => (
                            <span key={idx} className="skill-tag skill-missing">
                              {skill}
                            </span>
                          ))}
                        </div>
                      </div>
                    )}

                    {/* Next Steps (CORE DIFFERENTIATOR) */}
                    {analysis.next_steps && analysis.next_steps.length > 0 && (
                      <div className="analysis-section next-steps-section">
                        <h5>🚀 Your Path Forward</h5>
                        <p className="next-steps-intro">
                          Here's how you can become eligible:
                        </p>
                        <div className="next-steps-list">
                          {analysis.next_steps.map((step, idx) => (
                            <div key={idx} className="next-step-card">
                              <div className="step-number">{idx + 1}</div>
                              <div className="step-content">
                                <h6>{step.action}</h6>
                                <p className="step-reason">{step.reason}</p>
                                <span className="step-time">
                                  <Clock className="icon-xs" />
                                  {step.time_estimate}
                                </span>
                              </div>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                )}
              </div>
            );
          })}
        </div>
      )}

      {opportunities.length === 0 && !searching && (
        <div className="empty-state">
          <Search className="icon-lg" />
          <h3>No opportunities yet</h3>
          <p>Search for opportunities to get started</p>
        </div>
      )}
    </div>
  );
}

export default OpportunityExplorer;
