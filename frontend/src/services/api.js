import axios from 'axios';

// Define a URL base da API usando as variáveis de ambiente
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

// Cria uma instância do axios
const api = axios.create({
  baseURL: API_BASE_URL,
});

// Adiciona um "interceptor" que anexa o token de autenticação em cada requisição
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export default api;