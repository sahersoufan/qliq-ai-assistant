import axios from 'axios';

// Create an axios instance with default config
const api = axios.create({
  baseURL: 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Health check
export const checkHealth = async () => {
  try {
    const response = await api.get('/health');
    return response.data;
  } catch (error) {
    console.error('Health check failed:', error);
    throw error;
  }
};

// Onboarding
export const onboardUser = async (message) => {
  try {
    const response = await api.post('/onboard', { message });
    return response.data;
  } catch (error) {
    console.error('Onboarding failed:', error);
    throw error;
  }
};

// Ask a question
export const askQuestion = async (query) => {
  try {
    const response = await api.post('/ask', { query });
    return response.data;
  } catch (error) {
    console.error('Question failed:', error);
    throw error;
  }
};

// Get recommendations
export const getRecommendations = async (userId, topK = 5) => {
  try {
    const response = await api.get(`/recommendations/${userId}?top_k=${topK}`);
    return response.data;
  } catch (error) {
    console.error('Recommendations failed:', error);
    throw error;
  }
};

// Get metrics
export const getMetrics = async () => {
  try {
    const response = await api.get('/metrics');
    return response.data;
  } catch (error) {
    console.error('Metrics failed:', error);
    throw error;
  }
};

// Compare classifiers
export const compareClassifiers = async () => {
  try {
    const response = await api.get('/classifier-compare');
    return response.data;
  } catch (error) {
    console.error('Classifier comparison failed:', error);
    throw error;
  }
};

export default api;