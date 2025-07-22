import axios from 'axios'

const API_BASE_URL = 'http://localhost:5000'

// Create axios instance with base URL
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Add request interceptor to include auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Add response interceptor to handle token refresh
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true

      try {
        const refreshToken = localStorage.getItem('refresh_token')
        if (refreshToken) {
          const response = await axios.post(`${API_BASE_URL}/api/auth/refresh`, {}, {
            headers: {
              Authorization: `Bearer ${refreshToken}`,
            },
          })

          const { access_token } = response.data
          localStorage.setItem('access_token', access_token)
          api.defaults.headers.common['Authorization'] = `Bearer ${access_token}`
          
          return api(originalRequest)
        }
      } catch (refreshError) {
        // Refresh token failed, redirect to login
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
        localStorage.removeItem('user')
        window.location.href = '/login'
      }
    }

    return Promise.reject(error)
  }
)

export const authAPI = {
  // Register new user
  register: async (userData) => {
    console.log('Register payload:', userData)
    const response = await api.post('/api/auth/register', userData)
    return response.data
  },

  // Login user
  login: async (credentials) => {
    console.log('Login payload:', credentials)
    const response = await api.post('/api/auth/login', credentials)
    return response.data
  },

  // Get user profile
  getProfile: async () => {
    const response = await api.get('/api/auth/profile')
    return response.data
  },

  // Refresh token
  refreshToken: async () => {
    const refreshToken = localStorage.getItem('refresh_token')
    const response = await axios.post(`${API_BASE_URL}/api/auth/refresh`, {}, {
      headers: {
        Authorization: `Bearer ${refreshToken}`,
      },
    })
    return response.data
  },
}

export default api 