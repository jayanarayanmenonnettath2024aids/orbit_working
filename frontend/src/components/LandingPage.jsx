import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Sparkles, TrendingUp, Target, Zap, ArrowRight, Users, Award, BarChart } from 'lucide-react';

function LandingPage() {
  const navigate = useNavigate();

  return (
    <div className="landing-page">
      {/* Hero Section */}
      <section className="hero-section">
        <div className="hero-content">
          <div className="hero-badge">
            <Sparkles size={16} />
            <span>AI-Powered Career Intelligence</span>
          </div>
          
          <h1 className="hero-title">
            Discover Opportunities
            <span className="gradient-text"> That Match You</span>
          </h1>
          
          <p className="hero-description">
            Never face "Not Eligible" without knowing why. Get AI-powered insights, 
            personalized guidance, and actionable steps to reach your goals.
          </p>
          
          <div className="hero-buttons">
            <button className="btn-primary-large" onClick={() => navigate('/auth')}>
              Get Started
              <ArrowRight size={20} />
            </button>
            <button className="btn-secondary-large" onClick={() => navigate('/auth')}>
              Sign In
            </button>
          </div>
          
          <div className="hero-stats">
            <div className="stat-item">
              <div className="stat-number">10K+</div>
              <div className="stat-label">Opportunities</div>
            </div>
            <div className="stat-item">
              <div className="stat-number">95%</div>
              <div className="stat-label">Accuracy</div>
            </div>
            <div className="stat-item">
              <div className="stat-number">24/7</div>
              <div className="stat-label">AI Support</div>
            </div>
          </div>
        </div>
        
        <div className="hero-illustration">
          <div className="floating-card card-1">
            <Target size={24} />
            <div className="card-text">Smart Matching</div>
          </div>
          <div className="floating-card card-2">
            <TrendingUp size={24} />
            <div className="card-text">Career Growth</div>
          </div>
          <div className="floating-card card-3">
            <Zap size={24} />
            <div className="card-text">Instant Analysis</div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="features-section">
        <div className="section-header">
          <h2>Why Choose ORBIT?</h2>
          <p>Powered by cutting-edge AI to transform your career journey</p>
        </div>
        
        <div className="features-grid">
          <div className="feature-card">
            <div className="feature-icon icon-primary">
              <Target size={28} />
            </div>
            <h3>Smart Opportunity Matching</h3>
            <p>AI analyzes your profile and matches you with the perfect opportunities based on your skills and goals.</p>
          </div>
          
          <div className="feature-card">
            <div className="feature-icon icon-secondary">
              <BarChart size={28} />
            </div>
            <h3>Real-Time Eligibility Analysis</h3>
            <p>Get instant feedback on your eligibility with detailed explanations and confidence scores.</p>
          </div>
          
          <div className="feature-card">
            <div className="feature-icon icon-tertiary">
              <TrendingUp size={28} />
            </div>
            <h3>Personalized Roadmap</h3>
            <p>Receive step-by-step guidance on how to become eligible for your dream opportunities.</p>
          </div>
          
          <div className="feature-card">
            <div className="feature-icon icon-accent">
              <Award size={28} />
            </div>
            <h3>Resume Enhancement</h3>
            <p>Get AI-powered suggestions to improve your resume and increase your success rate.</p>
          </div>
          
          <div className="feature-card">
            <div className="feature-icon icon-success">
              <Zap size={28} />
            </div>
            <h3>Instant Insights</h3>
            <p>Lightning-fast analysis powered by Google's Gemini AI for accurate results.</p>
          </div>
          
          <div className="feature-card">
            <div className="feature-icon icon-info">
              <Users size={28} />
            </div>
            <h3>Community Support</h3>
            <p>Join thousands of students and professionals achieving their career goals.</p>
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section className="how-it-works-section">
        <div className="section-header">
          <h2>How It Works</h2>
          <p>Three simple steps to unlock your potential</p>
        </div>
        
        <div className="steps-container">
          <div className="step-card">
            <div className="step-number">1</div>
            <div className="step-content">
              <h3>Create Your Profile</h3>
              <p>Upload your resume or manually enter your skills, education, and experience. AI parses your resume automatically.</p>
            </div>
          </div>
          
          <div className="step-connector"></div>
          
          <div className="step-card">
            <div className="step-number">2</div>
            <div className="step-content">
              <h3>Discover Opportunities</h3>
              <p>Real-time search across web for hackathons, internships, fellowships, competitions, and scholarships with smart deadline filtering.</p>
            </div>
          </div>
          
          <div className="step-connector"></div>
          
          <div className="step-card">
            <div className="step-number">3</div>
            <div className="step-content">
              <h3>Get AI Analysis</h3>
              <p>Receive detailed eligibility breakdown with match score, requirements met/missing, and numbered roadmap steps to improve.</p>
            </div>
          </div>
        </div>
        
        <div className="additional-features">
          <h3>More Features</h3>
          <div>
            <div>
              <div>📊</div>
              <h4>Application Tracker</h4>
              <p>Track applications with status updates: Applied, Under Review, Accepted, Rejected</p>
            </div>
            <div>
              <div>🎮</div>
              <h4>Gamification</h4>
              <p>Earn points, unlock achievements, maintain streaks, complete daily/weekly tasks</p>
            </div>
            <div>
              <div>📈</div>
              <h4>Analytics & Rankings</h4>
              <p>View stats, acceptance rate, leaderboards, and peer comparisons</p>
            </div>
            <div>
              <div>🤖</div>
              <h4>AI Chatbot</h4>
              <p>24/7 AI assistant with web scraping, context-aware career guidance</p>
            </div>
            <div>
              <div>🏆</div>
              <h4>Success Stories</h4>
              <p>Get inspired by peers who improved skills and got accepted</p>
            </div>
            <div>
              <div>💡</div>
              <h4>Peer Insights</h4>
              <p>Compare your progress with college and platform averages</p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="cta-section">
        <div className="cta-content">
          <h2>Ready to Transform Your Career?</h2>
          <p>Join thousands of students finding their perfect opportunities</p>
          <button className="btn-cta" onClick={() => navigate('/auth')}>
            Start Your Journey
            <ArrowRight size={24} />
          </button>
        </div>
      </section>
    </div>
  );
}

export default LandingPage;
