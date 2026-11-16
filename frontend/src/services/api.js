import axios from 'axios';

// Create Axios client with base URL pointing to /api
const apiClient = axios.create({
  baseURL: '/api',
  timeout: 15000,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const api = {
  // Overview
  getOverview: async () => {
    const res = await apiClient.get('/overview');
    return res.data;
  },

  // Destinations
  getDestinations: async (params = {}) => {
    const res = await apiClient.get('/destinations', { params });
    return res.data;
  },

  getDestinationSpotlight: async (name) => {
    const res = await apiClient.get(`/destinations/spotlight/${encodeURIComponent(name)}`);
    return res.data;
  },

  getRankings: async (topN = 15) => {
    const res = await apiClient.get('/destinations/rankings', { params: { top_n: topN } });
    return res.data;
  },

  getMapMarkers: async (params = {}) => {
    const res = await apiClient.get('/destinations/map', { params });
    return res.data;
  },

  getTypologyImpact: async () => {
    const res = await apiClient.get('/destinations/typology-impact');
    return res.data;
  },

  // Demand Analysis
  getLongitudinalDemand: async () => {
    const res = await apiClient.get('/demand/longitudinal');
    return res.data;
  },

  getStatewiseDemand: async (topN = 12, sortBy = 'Total Visits') => {
    const res = await apiClient.get('/demand/statewise', {
      params: { top_n: topN, sort_by: sortBy },
    });
    return res.data;
  },

  getVisitorComposition: async () => {
    const res = await apiClient.get('/demand/composition');
    return res.data;
  },

  // Seasonal Analysis
  getQuarterlyTrends: async () => {
    const res = await apiClient.get('/seasonal/quarterly');
    return res.data;
  },

  getSeasonalBreakdown: async () => {
    const res = await apiClient.get('/seasonal/breakdown');
    return res.data;
  },

  getSeasonalSummary: async () => {
    const res = await apiClient.get('/seasonal/summary');
    return res.data;
  },

  // Weather & Tourism
  getTemperatureAnalysis: async () => {
    const res = await apiClient.get('/weather/temperature');
    return res.data;
  },

  getRainfallAnalysis: async () => {
    const res = await apiClient.get('/weather/rainfall');
    return res.data;
  },

  getCorrelationMatrix: async () => {
    const res = await apiClient.get('/weather/correlation');
    return res.data;
  },

  // ML Prediction
  getMLMetrics: async () => {
    const res = await apiClient.get('/ml/metrics');
    return res.data;
  },

  predictDemand: async (payload) => {
    const res = await apiClient.post('/ml/predict', payload);
    return res.data;
  },

  // Destination Clustering
  getClusteringOverview: async () => {
    const res = await apiClient.get('/clustering/overview');
    return res.data;
  },

  getClusteringEvaluation: async () => {
    const res = await apiClient.get('/clustering/evaluation');
    return res.data;
  },

  getClusterProfiles: async () => {
    const res = await apiClient.get('/clustering/profiles');
    return res.data;
  },

  getClusterMembers: async (clusterName = null) => {
    const res = await apiClient.get('/clustering/members', {
      params: clusterName ? { cluster_name: clusterName } : {},
    });
    return res.data;
  },

  // Recommendations
  getClusterStrategies: async () => {
    const res = await apiClient.get('/recommendations/strategies');
    return res.data;
  },

  getDecongestionRecommendations: async () => {
    const res = await apiClient.get('/recommendations/decongestion');
    return res.data;
  },

  getWeatherRecommendations: async () => {
    const res = await apiClient.get('/recommendations/weather');
    return res.data;
  },

  getSeasonalRecommendations: async () => {
    const res = await apiClient.get('/recommendations/seasonal');
    return res.data;
  },

  filterRecommendations: async (payload) => {
    const res = await apiClient.post('/recommendations/filter', payload);
    return res.data;
  },

  // Metadata & Filters
  getHealth: async () => {
    const res = await apiClient.get('/meta/health');
    return res.data;
  },

  getFilters: async () => {
    const res = await apiClient.get('/meta/filters');
    return res.data;
  },
};

export default api;
