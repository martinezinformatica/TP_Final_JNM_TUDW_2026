import axios from 'axios'

const api = axios.create({
  baseURL: 'http://localhost:8000/api/'
})


api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)


api.interceptors.response.use(
  (response) => {
    return response
  },
  async (error) => {
    const originalRequest = error.config
    
    if (error.response && error.response.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true 

      try {
        const refreshToken = localStorage.getItem('refresh')
        
        if (refreshToken) {
            const response = await axios.post('http://localhost:8000/api/token/refresh/', {
            refresh: refreshToken
          })

          const nuevoAccessToken = response.data.access
          
          localStorage.setItem('access', nuevoAccessToken)
         
          originalRequest.headers.Authorization = `Bearer ${nuevoAccessToken}`
         
          return api(originalRequest)
        }
      } catch (refreshError) {
        localStorage.removeItem('access')
        localStorage.removeItem('refresh')      
      
      }
    }

    
    return Promise.reject(error)
  }
)

export default api