import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import api from '../api.js';

export const useAuthStore = defineStore('auth', () => {

  const accessToken  = ref(localStorage.getItem('access')   || null);
  const refreshToken = ref(localStorage.getItem('refresh')  || null);
  const userRole     = ref(localStorage.getItem('role')     || null);
  const userTelefono = ref(localStorage.getItem('telefono') || null);  
  const esperandoCodigo = ref(false);  
  const esperandoPassword = ref(false); 
  const rolDetectado = ref(null);

  const isAuthenticated = computed(() => !!accessToken.value);
  const isAdmin         = computed(() => userRole.value === 'admin');
  const isCocina        = computed(() => userRole.value === 'cocina');
  const isCliente       = computed(() => userRole.value === 'cliente');
  const isPersonal      = computed(() => isAdmin.value || isCocina.value);

  function _guardarSesion({ access, refresh, role }) {
    accessToken.value  = access;
    refreshToken.value = refresh || null;
    userRole.value     = role;

    localStorage.setItem('access', access);
    localStorage.setItem('role', role);
    if (refresh)            localStorage.setItem('refresh', refresh);
    if (userTelefono.value) localStorage.setItem('telefono', userTelefono.value);
  }

  async function iniciarLogin(telefono) {
    try {
      userTelefono.value = telefono;
      const response = await api.post('auth/login-unificado/', { telefono });

      if (response.data.tipo === 'personal') {
        rolDetectado.value      = response.data.role;
        esperandoPassword.value = true;
        return 'personal';
      } else {
        rolDetectado.value    = 'cliente';
        esperandoCodigo.value = true;
        return 'cliente';
      }
    } catch (error) {
      throw error;
    }
  }

  async function verificarCodigoCliente(codigo) {
    try {
      const response = await api.post('auth/verificar-codigo/', {
        telefono: userTelefono.value,
        codigo,
      });
      _guardarSesion(response.data);
      esperandoCodigo.value = false;
      rolDetectado.value    = null;
      return true;
    } catch (error) {
      throw error;
    }
  }

  async function verificarPasswordPersonal(password) {
    try {
      const response = await api.post('auth/login/', {
        username: userTelefono.value,
        password,
      });
      _guardarSesion(response.data);
      esperandoPassword.value = false;
      rolDetectado.value      = null;
      return true;
    } catch (error) {
      throw error;
    }
  }

  function resetearLogin() {
    esperandoCodigo.value   = false;
    esperandoPassword.value = false;
    rolDetectado.value      = null;
    userTelefono.value      = null;
  }

  async function logout(mesaIdDesdeFrontend = null) {   
    const mesaId = mesaIdDesdeFrontend || localStorage.getItem('mesa_id');    
    if (mesaId) {
      try {
        await api.patch(`mesas/${mesaId}/`, {
          esta_libre: true,
          cliente_telefono: ""
        });       
      } catch (err) {
        console.error("No se pudo liberar la mesa en el servidor:", err);
      }
    } else {
      console.warn("ALERTA: No se cerro la sesion.");
    }

    
    accessToken.value       = null;
    refreshToken.value      = null;
    userRole.value          = null;
    userTelefono.value      = null;
    esperandoCodigo.value   = false;
    esperandoPassword.value = false;
    rolDetectado.value      = null;

    localStorage.removeItem('access');
    localStorage.removeItem('refresh');
    localStorage.removeItem('role');
    localStorage.removeItem('telefono');
    localStorage.removeItem('mesa_id');
  }

  return {
    accessToken,
    refreshToken,
    userRole,
    userTelefono,
    esperandoCodigo,
    esperandoPassword,
    rolDetectado,
    isAuthenticated,
    isAdmin,
    isCocina,
    isCliente,
    isPersonal,
    iniciarLogin,
    verificarCodigoCliente,
    verificarPasswordPersonal,
    resetearLogin,
    logout
  };
});