import axios from 'axios';

const rawBaseUrl =
  import.meta.env.VITE_API_BASE_URL ||
  (typeof window !== 'undefined' && window.location.hostname.includes('vercel.app')
    ? 'https://sih-paimana.onrender.com/api'
    : '/api');

const trimmedBase = rawBaseUrl.trim().replace(/\/+$/, '');
export const API_BASE_URL = trimmedBase.endsWith('/api') ? trimmedBase : `${trimmedBase}/api`;

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 45000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Attach JWT if present
api.interceptors.request.use((config) => {
  try {
    const token = localStorage.getItem('paimana_auth_token');
    if (token && token !== 'demo-jwt-sovereign-session') {
      config.headers.Authorization = `Bearer ${token}`;
    }
  } catch {}
  return config;
});

export const getRiskReportExportUrl = () => {
  return `${API_BASE_URL}/export/risk-report`;
};

export const getDashboardSummary = async () => {
  const res = await api.get('/dashboard/summary');
  return res.data;
};

export const getProjects = async (params = {}) => {
  const res = await api.get('/projects', { params });
  return res.data;
};

export const getProjectDetail = async (projectId) => {
  const res = await api.get(`/projects/${projectId}`);
  return res.data;
};

export const deleteProject = async (projectId) => {
  const res = await api.delete(`/projects/${projectId}`);
  return res.data;
};

export const clearAllProjects = async () => {
  const res = await api.delete('/projects');
  return res.data;
};

export const getAlerts = async (params = {}) => {
  const res = await api.get('/alerts', { params });
  return res.data;
};

export const getAlertCount = async (params = {}) => {
  const res = await api.get('/alerts/count', { params });
  return res.data;
};

export const reviewAlert = async (alertId) => {
  const res = await api.post(`/alerts/${alertId}/review`);
  return res.data;
};

export const getModelMetrics = async () => {
  const res = await api.get('/models/metrics');
  return res.data;
};

export const queryAIAssistant = async (question, contextProjectId = null) => {
  const res = await api.post('/assistant/query', {
    question,
    context_project_id: contextProjectId,
  });
  return res.data;
};

export const getFilterOptions = async () => {
  const res = await api.get('/filters/options');
  return res.data;
};

export const importReportFiles = async (files, referenceMonth = null) => {
  const formData = new FormData();
  const fileList = Array.isArray(files) ? files : [files];
  fileList.forEach((file) => {
    formData.append('files', file);
  });
  if (referenceMonth) {
    formData.append('reference_month', referenceMonth);
  }
  const res = await api.post('/import/report', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
    timeout: 0, // No client-side timeout limit
  });
  return res.data;
};

export const importReportFile = importReportFiles;

export const loginOfficer = async (email, password) => {
  const res = await api.post('/auth/login', { email, password });
  return res.data;
};

export const registerOfficer = async (userData) => {
  const res = await api.post('/auth/register', userData);
  return res.data;
};

export const getAuthProfiles = async () => {
  const res = await api.get('/auth/profiles');
  return res.data;
};

export const getCurrentUser = async () => {
  const res = await api.get('/auth/me');
  return res.data;
};

export const getAdminUsers = async () => {
  const res = await api.get('/admin/users');
  return res.data;
};

export const createAdminUser = async (officerData) => {
  const res = await api.post('/admin/users', officerData);
  return res.data;
};

export const toggleUserStatus = async (userId, isActive = null) => {
  const payload = isActive !== null ? { is_active: isActive } : {};
  const res = await api.patch(`/admin/users/${userId}/status`, payload);
  return res.data;
};

export default api;


