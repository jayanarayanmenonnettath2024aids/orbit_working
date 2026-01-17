import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { User, Mail, Lock, Eye, EyeOff } from 'lucide-react';
import { registerUser, loginUser } from '../services/api';
import './Auth.css';

function Auth() {
  const navigate = useNavigate();
  const [isLogin, setIsLogin] = useState(true);
  const [showPassword, setShowPassword] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: ''
  });

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    console.log('🔐 Auth attempt:', { isLogin, email: formData.email });

    try {
      let result;
      
      if (isLogin) {
        // Login flow
        console.log('📡 Calling loginUser API...');
        result = await loginUser(formData.email, formData.password);
        console.log('✅ Login result:', result);
      } else {
        // Registration flow
        if (!formData.name) {
          setError('Please enter your name');
          setLoading(false);
          return;
        }
        console.log('📡 Calling registerUser API...');
        result = await registerUser(formData.email, formData.password, formData.name);
        console.log('✅ Register result:', result);
      }
      
      // Store session data
      if (result.session_token && result.user_id) {
        console.log('💾 Storing session data...');
        localStorage.setItem('session_token', result.session_token);
        localStorage.setItem('user_id', result.user_id);
        localStorage.setItem('user_email', result.email);
        localStorage.setItem('user_name', result.name || formData.email.split('@')[0]);
        
        console.log('🚀 Navigating to dashboard...');
        // Navigate to dashboard immediately
        navigate('/dashboard');
      } else {
        console.error('❌ Invalid response:', result);
        throw new Error('Invalid server response');
      }
      
    } catch (err) {
      console.error('❌ Authentication error:', err);
      console.error('❌ Error details:', { message: err.message, response: err.response, request: err.request });
      setError(err.message || 'Authentication failed. Please try again.');
      setLoading(false);
    }
  };

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  return (
    <div className="auth-page">
      <div className="auth-split-container">
        {/* Left Brand Panel */}
        <div className="auth-brand-panel">
          <div className="brand-content">
            <div className="brand-logo">
              <span className="logo-letter">O</span>
              <div className="logo-pulse"></div>
            </div>
            <h1 className="brand-title">ORBIT</h1>
            <p className="brand-subtitle">Your AI-powered career companion for discovering and achieving opportunities</p>
            
            <div className="brand-features">
              <div className="brand-feature">
                <div className="feature-icon-wrapper">
                  <div className="feature-icon">🤖</div>
                </div>
                <div className="feature-content">
                  <h3>AI-Powered Matching</h3>
                  <p>Smart algorithms find opportunities that match your profile</p>
                </div>
              </div>
              <div className="brand-feature">
                <div className="feature-icon-wrapper">
                  <div className="feature-icon">📊</div>
                </div>
                <div className="feature-content">
                  <h3>Real-Time Analysis</h3>
                  <p>Get instant insights on your eligibility and chances</p>
                </div>
              </div>
              <div className="brand-feature">
                <div className="feature-icon-wrapper">
                  <div className="feature-icon">🎯</div>
                </div>
                <div className="feature-content">
                  <h3>Personalized Guidance</h3>
                  <p>Receive tailored advice to improve your applications</p>
                </div>
              </div>
              <div className="brand-feature">
                <div className="feature-icon-wrapper">
                  <div className="feature-icon">🚀</div>
                </div>
                <div className="feature-content">
                  <h3>10,000+ Opportunities</h3>
                  <p>Access scholarships, grants, and career opportunities</p>
                </div>
              </div>
            </div>
            
            <div className="brand-stats">
              <div className="brand-stat">
                <div className="stat-number">10K+</div>
                <div className="stat-text">Opportunities</div>
              </div>
              <div className="stat-divider"></div>
              <div className="brand-stat">
                <div className="stat-number">5K+</div>
                <div className="stat-text">Active Users</div>
              </div>
              <div className="stat-divider"></div>
              <div className="brand-stat">
                <div className="stat-number">95%</div>
                <div className="stat-text">Success Rate</div>
              </div>
            </div>
          </div>
        </div>

        {/* Right Form Panel */}
        <div className="auth-form-panel">
          <div className="form-content">
            {/* Form Header */}
            <div className="form-header">
              <h2 className="form-title">{isLogin ? 'Welcome Back!' : 'Create Account'}</h2>
              <p className="form-subtitle">
                {isLogin 
                  ? 'Sign in to continue your journey' 
                  : 'Join thousands achieving their goals'}
              </p>
            </div>

            {/* Tabs */}
            <div className="auth-tabs">
              <button 
                type="button"
                className={`auth-tab ${isLogin ? 'active' : ''}`}
                onClick={() => setIsLogin(true)}
              >
                Sign In
              </button>
              <button 
                type="button"
                className={`auth-tab ${!isLogin ? 'active' : ''}`}
                onClick={() => setIsLogin(false)}
              >
                Sign Up
              </button>
            </div>

            {/* Form */}
            <form onSubmit={handleSubmit} className="auth-form">
              {error && (
                <div className="form-error">
                  {error}
                </div>
              )}
              
              {!isLogin && (
                <div className="form-group">
                  <label htmlFor="name" className="form-label form-label-required">
                    Full Name
                  </label>
                  <div className="input-wrapper">
                    <User size={18} className="input-icon" />
                    <input
                      type="text"
                      id="name"
                      name="name"
                      className="form-input"
                      placeholder="e.g., Sarah Johnson"
                      value={formData.name}
                      onChange={handleChange}
                      required={!isLogin}
                      autoComplete="name"
                    />
                  </div>
                </div>
              )}

              <div className="form-group">
                <label htmlFor="email" className="form-label form-label-required">
                  Email Address
                </label>
                <div className="input-wrapper">
                  <Mail size={18} className="input-icon" />
                  <input
                    type="email"
                    id="email"
                    name="email"
                    className="form-input"
                    placeholder="your.email@example.com"
                    value={formData.email}
                    onChange={handleChange}
                    required
                    autoComplete="email"
                  />
                </div>
              </div>

              <div className="form-group">
                <label htmlFor="password" className="form-label form-label-required">
                  Password
                </label>
                <div className="input-wrapper">
                  <Lock size={18} className="input-icon" />
                  <input
                    type={showPassword ? 'text' : 'password'}
                    id="password"
                    name="password"
                    className="form-input"
                    placeholder={isLogin ? 'Enter your password' : 'Create a strong password (min. 8 characters)'}
                    value={formData.password}
                    onChange={handleChange}
                    required
                    minLength={isLogin ? undefined : 8}
                    autoComplete={isLogin ? 'current-password' : 'new-password'}
                    style={{ paddingRight: '50px' }}
                  />
                  <button
                    type="button"
                    className="password-toggle"
                    onClick={() => setShowPassword(!showPassword)}
                    tabIndex="-1"
                    aria-label={showPassword ? 'Hide password' : 'Show password'}
                  >
                    {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
                  </button>
                </div>
              </div>

              {/* Remember Me & Forgot Password */}
              {isLogin && (
                <div className="form-options">
                  <label className="checkbox-label">
                    <input type="checkbox" className="checkbox-input" />
                    <span className="checkbox-text">Remember me</span>
                  </label>
                  <a href="#" className="forgot-link" onClick={(e) => e.preventDefault()}>
                    Forgot Password?
                  </a>
                </div>
              )}

              <button type="submit" className="auth-submit" disabled={loading}>
                {loading ? (
                  <>
                    <div className="spinner"></div>
                    {isLogin ? 'Signing In...' : 'Creating Account...'}
                  </>
                ) : (
                  <>
                    {isLogin ? 'Sign In' : 'Create Account'}
                  </>
                )}
              </button>
            </form>

            {/* Footer Link */}
            <div className="form-footer">
              {isLogin ? (
                <>
                  Don't have an account?{' '}
                  <a href="#" className="footer-link" onClick={(e) => { e.preventDefault(); setIsLogin(false); }}>
                    Sign up free
                  </a>
                </>
              ) : (
                <>
                  Already have an account?{' '}
                  <a href="#" className="footer-link" onClick={(e) => { e.preventDefault(); setIsLogin(true); }}>
                    Sign in
                  </a>
                </>
              )}
            </div>

            {/* Trust Badges */}
            <div className="trust-badges">
              <div className="trust-badge">
                <span className="badge-icon">🔒</span>
                <span className="badge-text">Secure & Encrypted</span>
              </div>
              <div className="trust-badge">
                <span className="badge-icon">⚡</span>
                <span className="badge-text">2-Min Setup</span>
              </div>
              <div className="trust-badge">
                <span className="badge-icon">✓</span>
                <span className="badge-text">Free Forever</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Auth;
