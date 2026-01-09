import React, { useState } from 'react';
import { Upload, Edit, Check, AlertCircle } from 'lucide-react';
import { parseResume, createProfile } from '../services/api';

function ProfileBuilder({ onProfileCreated, existingProfile }) {
  const [mode, setMode] = useState('choose'); // choose, upload, manual
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);
  const [evaluation, setEvaluation] = useState(null);

  // Manual profile state
  const [formData, setFormData] = useState({
    education: {
      degree: '',
      major: '',
      institution: '',
      year: '',
      cgpa_or_percentage: ''
    },
    skills: {
      programming_languages: [],
      frameworks: [],
      tools: [],
      domains: []
    },
    experience: [],
    achievements: [],
    interests: [],
    self_description: ''
  });

  const [skillInput, setSkillInput] = useState({
    programming_languages: '',
    frameworks: '',
    tools: '',
    domains: ''
  });

  const [interestInput, setInterestInput] = useState('');

  const handleResumeUpload = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    if (file.type !== 'application/pdf') {
      setError('Please upload a PDF file');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const result = await parseResume(file);
      
      // Store evaluation if available
      if (result.resume_grade || result.resume_summary) {
        setEvaluation({
          grade: result.resume_grade,
          summary: result.resume_summary,
          strengths: result.strengths || [],
          improvements: result.improvements || []
        });
      }
      
      setSuccess(true);
      setTimeout(() => {
        onProfileCreated(result);
      }, 1500);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to parse resume');
    } finally {
      setLoading(false);
    }
  };

  const handleManualSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const result = await createProfile(formData);
      setSuccess(true);
      setTimeout(() => {
        onProfileCreated(result);
      }, 1500);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to create profile');
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (section, field, value) => {
    setFormData(prev => ({
      ...prev,
      [section]: {
        ...prev[section],
        [field]: value
      }
    }));
  };

  const addSkill = (category) => {
    const value = skillInput[category].trim();
    if (value) {
      setFormData(prev => ({
        ...prev,
        skills: {
          ...prev.skills,
          [category]: [...prev.skills[category], value]
        }
      }));
      setSkillInput(prev => ({ ...prev, [category]: '' }));
    }
  };

  const removeSkill = (category, index) => {
    setFormData(prev => ({
      ...prev,
      skills: {
        ...prev.skills,
        [category]: prev.skills[category].filter((_, i) => i !== index)
      }
    }));
  };

  const addInterest = () => {
    const value = interestInput.trim();
    if (value) {
      setFormData(prev => ({
        ...prev,
        interests: [...prev.interests, value]
      }));
      setInterestInput('');
    }
  };

  if (existingProfile) {
    return (
      <div className="profile-existing">
        <div className="success-message">
          <Check className="icon" />
          <h3>Profile Created Successfully!</h3>
          <p>Profile ID: {existingProfile.profile_id}</p>
        </div>
        <button 
          className="btn btn-secondary"
          onClick={() => window.location.reload()}
        >
          Create New Profile
        </button>
      </div>
    );
  }

  if (mode === 'choose') {
    return (
      <div className="profile-builder">
        <h2>Build Your Profile</h2>
        <p className="subtitle">Choose how you'd like to create your profile:</p>

        <div className="mode-selection">
          <div 
            className="mode-card"
            onClick={() => setMode('upload')}
          >
            <Upload className="icon-lg" />
            <h3>Upload Resume</h3>
            <p>Quick and easy - we'll parse your PDF resume automatically</p>
          </div>

          <div 
            className="mode-card"
            onClick={() => setMode('manual')}
          >
            <Edit className="icon-lg" />
            <h3>Enter Manually</h3>
            <p>Fill in your details step by step</p>
          </div>
        </div>
      </div>
    );
  }

  if (mode === 'upload') {
    return (
      <div className="profile-builder">
        <button 
          className="btn btn-text"
          onClick={() => setMode('choose')}
        >
          ← Back
        </button>

        <h2>Upload Your Resume</h2>
        <p className="subtitle">Upload a PDF resume and we'll extract your information automatically using AI</p>

        <div className="upload-area">
          <input
            type="file"
            id="resume-upload"
            accept="application/pdf"
            onChange={handleResumeUpload}
            disabled={loading}
            style={{ display: 'none' }}
          />
          <label htmlFor="resume-upload" className="upload-label">
            <Upload className="icon-lg" />
            <span>Click to upload PDF</span>
            <span className="text-sm">or drag and drop</span>
          </label>
        </div>

        {loading && (
          <div className="loading-message">
            <div className="spinner"></div>
            <p>Parsing your resume with AI...</p>
          </div>
        )}

        {success && !evaluation && (
          <div className="success-message">
            <Check className="icon" />
            <p>Resume parsed successfully!</p>
          </div>
        )}

        {success && evaluation && (
          <div className="resume-evaluation">
            <div className="evaluation-header">
              <Check className="icon" />
              <h3>Resume Evaluation</h3>
            </div>
            
            <div className="grade-display">
              <div className="grade-badge">{evaluation.grade}</div>
              <p className="grade-summary">{evaluation.summary}</p>
            </div>

            {evaluation.strengths && evaluation.strengths.length > 0 && (
              <div className="feedback-section">
                <h4>✅ Strengths</h4>
                <ul>
                  {evaluation.strengths.map((strength, idx) => (
                    <li key={idx}>{strength}</li>
                  ))}
                </ul>
              </div>
            )}

            {evaluation.improvements && evaluation.improvements.length > 0 && (
              <div className="feedback-section">
                <h4>💡 Areas for Improvement</h4>
                <ul>
                  {evaluation.improvements.map((improvement, idx) => (
                    <li key={idx}>{improvement}</li>
                  ))}
                </ul>
              </div>
            )}

            <p className="redirect-note">Redirecting to opportunities...</p>
          </div>
        )}

        {error && (
          <div className="error-message">
            <AlertCircle className="icon" />
            <p>{error}</p>
          </div>
        )}
      </div>
    );
  }

  if (mode === 'manual') {
    return (
      <div className="profile-builder">
        <button 
          className="btn btn-text"
          onClick={() => setMode('choose')}
        >
          ← Back
        </button>

        <h2>Create Profile Manually</h2>

        <form onSubmit={handleManualSubmit} className="profile-form">
          {/* Education */}
          <div className="form-section">
            <h3>📚 Education</h3>
            <div className="form-grid">
              <input
                type="text"
                placeholder="Degree (e.g., B.Tech, M.Tech)"
                value={formData.education.degree}
                onChange={(e) => handleInputChange('education', 'degree', e.target.value)}
                required
              />
              <input
                type="text"
                placeholder="Major (e.g., Computer Science)"
                value={formData.education.major}
                onChange={(e) => handleInputChange('education', 'major', e.target.value)}
                required
              />
              <input
                type="text"
                placeholder="Institution"
                value={formData.education.institution}
                onChange={(e) => handleInputChange('education', 'institution', e.target.value)}
                required
              />
              <input
                type="text"
                placeholder="Year (e.g., 2nd year, 2024)"
                value={formData.education.year}
                onChange={(e) => handleInputChange('education', 'year', e.target.value)}
                required
              />
              <input
                type="text"
                placeholder="CGPA/Percentage (optional)"
                value={formData.education.cgpa_or_percentage}
                onChange={(e) => handleInputChange('education', 'cgpa_or_percentage', e.target.value)}
              />
            </div>
          </div>

          {/* Skills */}
          <div className="form-section">
            <h3>💻 Skills</h3>
            
            <div className="skill-input-group">
              <label>Programming Languages</label>
              <div className="input-with-button">
                <input
                  type="text"
                  placeholder="e.g., Python, Java, JavaScript"
                  value={skillInput.programming_languages}
                  onChange={(e) => setSkillInput({...skillInput, programming_languages: e.target.value})}
                  onKeyPress={(e) => e.key === 'Enter' && (e.preventDefault(), addSkill('programming_languages'))}
                />
                <button 
                  type="button"
                  onClick={() => addSkill('programming_languages')}
                >
                  Add
                </button>
              </div>
              <div className="skill-tags">
                {formData.skills.programming_languages.map((skill, index) => (
                  <span key={index} className="skill-tag">
                    {skill}
                    <button type="button" onClick={() => removeSkill('programming_languages', index)}>×</button>
                  </span>
                ))}
              </div>
            </div>

            <div className="skill-input-group">
              <label>Frameworks & Libraries</label>
              <div className="input-with-button">
                <input
                  type="text"
                  placeholder="e.g., React, Django, TensorFlow"
                  value={skillInput.frameworks}
                  onChange={(e) => setSkillInput({...skillInput, frameworks: e.target.value})}
                  onKeyPress={(e) => e.key === 'Enter' && (e.preventDefault(), addSkill('frameworks'))}
                />
                <button 
                  type="button"
                  onClick={() => addSkill('frameworks')}
                >
                  Add
                </button>
              </div>
              <div className="skill-tags">
                {formData.skills.frameworks.map((skill, index) => (
                  <span key={index} className="skill-tag">
                    {skill}
                    <button type="button" onClick={() => removeSkill('frameworks', index)}>×</button>
                  </span>
                ))}
              </div>
            </div>
          </div>

          {/* Interests */}
          <div className="form-section">
            <h3>🎯 Interests & Goals</h3>
            <div className="input-with-button">
              <input
                type="text"
                placeholder="e.g., Machine Learning, Web Development"
                value={interestInput}
                onChange={(e) => setInterestInput(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && (e.preventDefault(), addInterest())}
              />
              <button 
                type="button"
                onClick={addInterest}
              >
                Add
              </button>
            </div>
            <div className="skill-tags">
              {formData.interests.map((interest, index) => (
                <span key={index} className="skill-tag">
                  {interest}
                  <button 
                    type="button" 
                    onClick={() => setFormData(prev => ({
                      ...prev,
                      interests: prev.interests.filter((_, i) => i !== index)
                    }))}
                  >
                    ×
                  </button>
                </span>
              ))}
            </div>
          </div>

          {/* Self Description */}
          <div className="form-section">
            <h3>✍️ About You</h3>
            <textarea
              placeholder="Tell us about yourself, your goals, what you're good at..."
              value={formData.self_description}
              onChange={(e) => setFormData({...formData, self_description: e.target.value})}
              rows={4}
            />
          </div>

          {error && (
            <div className="error-message">
              <AlertCircle className="icon" />
              <p>{error}</p>
            </div>
          )}

          <button 
            type="submit" 
            className="btn btn-primary btn-large"
            disabled={loading}
          >
            {loading ? 'Creating Profile...' : 'Create Profile'}
          </button>
        </form>
      </div>
    );
  }

  return null;
}

export default ProfileBuilder;
