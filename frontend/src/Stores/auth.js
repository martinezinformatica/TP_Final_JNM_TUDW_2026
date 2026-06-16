import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import api from '../api.js'; 

export const useAuthStore = defineStore('auth', () => {
  const accessToken = ref(localStorage.getItem('access') || null);
  const refreshToken = ref(localStorage.getItem('refresh') || null);
  const userRole = ref(localStorage.getItem('role') || null); 
  const userTelefono = ref(localStorage.getItem('telefono') || null);
  const esperandoCodigo = ref(false);

  const isAuthenticated = computed(() => !!accessToken.value);  
  const isAdmin = computed(() => userRole.value === 'admin');
  const isCocina = computed(() => userRole.value === 'cocina');
  const isCliente = computed(() => userRole.value === 'cliente');

  async function login(username, password) {
    try {
      const response = await api.post('auth/login/', { username, password });
      
      accessToken.value = response.data.access;
      refreshToken.value = response.data.refresh;
      userRole.value = response.data.role;
      userTelefono.value = response.data.telefono || null;

      localStorage.setItem('access', response.data.access);
      localStorage.setItem('refresh', response.data.refresh);
      localStorage.setItem('role', response.data.role);
      if (response.data.telefono) {
        localStorage.setItem('telefono', response.data.telefono);
      }
      return true;
    } catch (error) {
      console.error("Error en el login:", error);
      throw error;
    }
  }

  async function solicitarCodigoCliente(telefono) {
    try {
      await api.post('auth/solicitar-codigo/', { telefono });
      esperandoCodigo.value = true;
      userTelefono.value = telefono;
      return true;
    } catch (error) {
      console.error("Error al solicitar codigo:", error);
      throw error;
    }
  }

  async function verificarCodigoCliente(codigo) {
    try {
      const response = await api.post('auth/verificar-codigo/', { 
        telefono: userTelefono.value, 
        codigo: codigo 
      });
      
      accessToken.value = response.data.access;
      userRole.value = 'cliente';

      localStorage.setItem('access', response.data.access);
      localStorage.setItem('role', 'cliente');
      localStorage.setItem('telefono', userTelefono.value);
      
      esperandoCodigo.value = false;
      return true;
    } catch (error) {
      console.error("Error al verificar codigo:", error);
      throw error;
    }
  }

  function logout() {
    accessToken.value = null;
    refreshToken.value = null;
    userRole.value = null;
    userTelefono.value = null;
    esperandoCodigo.value = false;

    localStorage.removeItem('access');
    localStorage.removeItem('refresh');
    localStorage.removeItem('role');
    localStorage.removeItem('telefono');
  }

  return { 
    accessToken, 
    refreshToken, 
    userRole, 
    userTelefono,
    esperandoCodigo,
    isAuthenticated, 
    isAdmin, 
    isCocina, 
    isCliente,
    login, 
    solicitarCodigoCliente,
    verificarCodigoCliente,
    logout 
  };
});