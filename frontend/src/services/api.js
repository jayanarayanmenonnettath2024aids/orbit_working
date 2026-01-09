import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// ============================================================================
// PROFILE API
// ============================================================================

export const parseResume = async (file) => {
  const formData = new FormData();
  formData.append('resume', file);
  
  const response = await api.post('/profile/parse_resume', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  
  return response.data;
};

export const createProfile = async (profileData) => {
  const response = await api.post('/profile/create', profileData);
  return response.data;
};

export const getProfile = async (profileId) => {
  const response = await api.get(`/profile/${profileId}`);
  return response.data;
};

// ============================================================================
// OPPORTUNITY API
// ============================================================================

export const searchOpportunities = async (query, opportunityType = null) => {
  const response = await api.post('/opportunities/search', {
    query,
    opportunity_type: opportunityType,
  });
  return response.data;
};

export const getCachedOpportunities = async (limit = 20, type = null) => {
  const params = new URLSearchParams();
  if (limit) params.append('limit', limit);
  if (type) params.append('type', type);
  
  const response = await api.get(`/opportunities/cached?${params.toString()}`);
  return response.data;
};

export const getOpportunity = async (opportunityId) => {
  const response = await api.get(`/opportunities/${opportunityId}`);
  return response.data;
};

// ============================================================================
// REASONING API (CORE INTELLIGENCE)
// ============================================================================

export const analyzeEligibility = async (profileId, opportunityId) => {
  const response = await api.post('/reasoning/analyze', {
    profile_id: profileId,
    opportunity_id: opportunityId,
  });
  return response.data;
};

export const analyzeBatch = async (profileId, opportunityIds) => {
  const response = await api.post('/reasoning/batch', {
    profile_id: profileId,
    opportunity_ids: opportunityIds,
  });
  return response.data;
};

export const getReasoningResult = async (reasoningId) => {
  const response = await api.get(`/reasoning/results/${reasoningId}`);
  return response.data;
};

// ============================================================================
// UTILITY
// ============================================================================

export const healthCheck = async () => {
  const response = await api.get('/health');
  return response.data;
};

export default api;
