/**
 * Gamification Helper - Track user actions and update points/tasks
 */

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000/api';

/**
 * Track a gamification action
 * @param {string} action - Action type (search_opportunity, check_eligibility, etc.)
 * @param {object} metadata - Additional data about the action
 */
export const trackAction = async (action, metadata = {}) => {
  try {
    const userId = localStorage.getItem('user_id');
    if (!userId) {
      console.warn('No user_id found, skipping gamification tracking');
      return null;
    }

    const response = await fetch(`${API_URL}/gamification/action`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        user_id: userId,
        action,
        metadata
      })
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    console.log(`✓ Tracked action: ${action}`, data);
    return data;
  } catch (error) {
    console.error('Failed to track gamification action:', error);
    return null;
  }
};

/**
 * Track search action
 */
export const trackSearch = (query) => trackAction('search_opportunity', { query });

/**
 * Track eligibility check
 */
export const trackEligibilityCheck = (opportunityId, score) => 
  trackAction('check_eligibility', { opportunity_id: opportunityId, confidence_score: score });

/**
 * Track save to tracker
 */
export const trackSaveToTracker = (opportunityId, opportunityTitle) => 
  trackAction('save_to_tracker', { opportunity_id: opportunityId, title: opportunityTitle });

/**
 * Track application submission
 */
export const trackApplication = (opportunityId, eligibilityScore) => 
  trackAction('apply_submitted', { opportunity_id: opportunityId, eligibility_score: eligibilityScore });

/**
 * Track chat message
 */
export const trackChatMessage = (messageLength) => 
  trackAction('chat_message', { message_length: messageLength });

/**
 * Track status update
 */
export const trackStatusUpdate = (applicationId, status) => 
  trackAction('status_update', { application_id: applicationId, status });

/**
 * Track profile update
 */
export const trackProfileUpdate = () => trackAction('profile_update');

/**
 * Update login streak
 */
export const updateLoginStreak = async () => {
  try {
    const userId = localStorage.getItem('user_id');
    if (!userId) return null;

    const response = await fetch(`${API_URL}/gamification/streak/${userId}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      }
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    console.log('✓ Updated login streak', data);
    return data;
  } catch (error) {
    console.error('Failed to update login streak:', error);
    return null;
  }
};
