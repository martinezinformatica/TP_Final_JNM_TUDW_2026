<template>
  <div id="app">
    <nav class="navbar">
      <div class="logo">NATURAL MYSTIC</div>
      <div class="menu">
        <button
          v-for="item in menuItems"
          :key="item.id"
          @click="navegarA(item.id)"
          :class="['nav-btn', { activo: seccionActual === item.id }]"
        >
          {{ item.nombre }}
        </button>
      </div>
    </nav>

    <main class="main-content">
      <Inicio v-if="seccionActual === 'inicio'" />
      <Sugerencias v-if="seccionActual === 'sugerencias'" />
      <Nosotros v-if="seccionActual === 'nosotros'" />
      <Contacto v-if="seccionActual === 'contacto'" />

      <template v-if="seccionActual === 'carta'">
        <div v-if="!authStore.isAuthenticated" class="card-mystic-login">
          <h2 class="subtitulo-login">INGRESO CLIENTE</h2>

          <div v-if="!authStore.esperandoCodigo">
            <p>
              Ingresá tu teléfono para recibir tu código de acceso por WhatsApp
              y notificaciones.
            </p>
            <input
              v-model="telefonoInput"
              type="tel"
              placeholder="Ej: 2984123456"
              class="input-login"
            />
            <button @click="solicitarCodigo" class="btn-login">
              SOLICITAR CÓDIGO
            </button>
          </div>

          <div v-else>
            <p>Ingresá el código de 8 dígitos enviado a tu WhatsApp.</p>
            <input
              v-model="codigoInput"
              type="text"
              maxlength="8"
              placeholder="Código de 8 dígitos"
              class="input-login"
            />
            <button @click="verificarCodigo" class="btn-login">
              VERIFICAR CÓDIGO
            </button>
            <button
              @click="authStore.esperandoCodigo = false"
              class="btn-login btn-volver"
            >
              VOLVER
            </button>
          </div>
        </div>
        <CartaDigital v-else />
      </template>

      <template v-if="seccionActual === 'cocina'">
        <div
          v-if="!authStore.isCocina && !authStore.isAdmin"
          class="card-mystic-login"
        >
          <h2 class="subtitulo-login">ACCESO A COCINA</h2>
          <input
            v-model="usernameInput"
            type="text"
            placeholder="Usuario"
            class="input-login"
          />
          <input
            v-model="passwordInput"
            type="password"
            placeholder="Contraseña"
            class="input-login"
          />
          <button @click="ingresarPersonal('cocina')" class="btn-login">
            INGRESAR
          </button>
        </div>
        <Cocina v-else />
      </template>

      <template v-if="seccionActual === 'admin'">
        <div v-if="!authStore.isAdmin" class="card-mystic-login">
          <h2 class="subtitulo-login">PANEL DE ADMINISTRACIÓN</h2>
          <input
            v-model="usernameInput"
            type="text"
            placeholder="Usuario"
            class="input-login"
          />
          <input
            v-model="passwordInput"
            type="password"
            placeholder="Contraseña"
            class="input-login"
          />
          <button @click="ingresarPersonal('admin')" class="btn-login">
            INGRESAR
          </button>
        </div>
        <Administrador v-else />
      </template>
    </main>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useAuthStore } from "./stores/auth.js";
import Inicio from "./components/Inicio.vue";
import CartaDigital from "./components/CartaDigital.vue";
import Sugerencias from "./components/Sugerencias.vue";
import Nosotros from "./components/Nosotros.vue";
import Contacto from "./components/Contacto.vue";
import Cocina from "./components/Cocina.vue";
import Administrador from "./components/Admin.vue";

const authStore = useAuthStore();
const seccionActual = ref("carta");

const telefonoInput = ref("");
const codigoInput = ref("");
const usernameInput = ref("");
const passwordInput = ref("");

const menuItems = [
  { id: "inicio", nombre: "Inicio" },
  { id: "carta", nombre: "Pedir" },
  { id: "nosotros", nombre: "Nosotros" },
  { id: "sugerencias", nombre: "Voz de Nosotros" },
  { id: "contacto", nombre: "Contacto" },
  { id: "cocina", nombre: "Cocina" },
  { id: "admin", nombre: "Administrador" },
];

const limpiarFormularios = () => {
  usernameInput.value = "";
  passwordInput.value = "";
  telefonoInput.value = "";
  codigoInput.value = "";
};

const navegarA = (id) => {
  seccionActual.value = id;
  limpiarFormularios();
};

const solicitarCodigo = async () => {
  if (!telefonoInput.value.trim()) {
    alert("Por favor, ingresá un número de teléfono válido.");
    return;
  }
  try {
    await authStore.solicitarCodigoCliente(telefonoInput.value);
  } catch (error) {
    alert("Error al solicitar el código. Verificá el número.");
  }
};

const verificarCodigo = async () => {
  if (codigoInput.value.trim().length !== 8) {
    alert("El código debe tener exactamente 8 dígitos.");
    return;
  }
  try {
    await authStore.verificarCodigoCliente(codigoInput.value);
  } catch (error) {
    alert("Código incorrecto, vencido o inválido.");
  }
};

const ingresarPersonal = async (rolRequerido) => {
  if (!usernameInput.value.trim() || !passwordInput.value.trim()) {
    alert("Completá todos los campos.");
    return;
  }
  try {
    await authStore.login(usernameInput.value, passwordInput.value);

    if (rolRequerido === "admin" && !authStore.isAdmin) {
      alert("Tu usuario no tiene permisos de Administrador.");
      authStore.logout();
    }
  } catch (error) {
    alert("Credenciales incorrectas. Verificá tu usuario y contraseña.");
  }
};

const cerrarSesion = () => {
  authStore.logout();
  seccionActual.value = "carta";
  limpiarFormularios();
};
</script>

<style>
@import url("https://fonts.googleapis.com/css2?family=Roboto+Mono:wght@400;700&display=swap");

body {
  margin: 0;
  background-color: #121212;
  font-family: "Roboto Mono", monospace;
  color: #ccc;
}

.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 2rem;
  background: #000;
  border-bottom: 2px solid #c5a059;
  position: sticky;
  top: 0;
  z-index: 1000;
}

.logo {
  color: #c5a059;
  font-weight: bold;
  font-size: 1.5rem;
  letter-spacing: 3px;
}

.nav-btn {
  background: none;
  border: 1px solid transparent;
  color: #c5a059;
  margin-left: 10px;
  padding: 8px 15px;
  cursor: pointer;
  text-transform: uppercase;
  font-family: "Roboto Mono", monospace;
  font-weight: bold;
  border-radius: 4px;
  transition: all 0.3s;
}

.nav-btn:hover,
.nav-btn.activo {
  border: 1px solid #c5a059;
  box-shadow: 0 0 10px rgba(197, 160, 89, 0.5);
}

.main-content {
  display: flex;
  justify-content: center;
  padding: 40px 20px;
}

.card-mystic-login {
  background: #1a1a1a;
  border: 1px solid #c5a059;
  padding: 40px;
  border-radius: 12px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.5);
  text-align: center;
  max-width: 400px;
  width: 100%;
}

.subtitulo-login {
  color: #c5a059;
  margin-bottom: 25px;
  font-size: 1.4rem;
  letter-spacing: 2px;
}

.input-login {
  width: 100%;
  padding: 12px;
  margin: 10px 0;
  background: #000;
  border: 1px solid #333;
  color: white;
  border-radius: 6px;
  box-sizing: border-box;
  font-family: "Roboto Mono", monospace;
  text-align: center;
}

.input-login:focus {
  outline: none;
  border-color: #c5a059;
}

.btn-login {
  width: 100%;
  background: #2a2a2a;
  border: 1px solid #c5a059;
  color: #ffffff;
  padding: 12px;
  cursor: pointer;
  transition: 0.3s;
  font-weight: bold;
  margin-top: 15px;
  font-family: "Roboto Mono", monospace;
}

.btn-login:hover {
  background: #c5a059;
  color: #000;
}

.btn-volver {
  background: #000;
  border-color: #333;
  color: #777;
  font-size: 0.85rem;
  padding: 8px;
}

.btn-volver:hover {
  background: #111;
  color: #fff;
  border-color: #666;
}
</style>
