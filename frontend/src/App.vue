<template>
  <div id="app">
    <nav class="navbar">
      <div class="logo">NATURAL MYSTIC</div>
      <div class="menu">
        <button
          v-for="item in menuItemsVisibles"
          :key="item.id"
          @click="navegarA(item.id)"
          :class="['nav-btn', { activo: seccionActual === item.id }]"
        >
          {{ item.nombre }}
        </button>
        <button
          v-if="authStore.isAuthenticated"
          @click="cerrarSesion"
          class="nav-btn btn-logout"
        >
          SALIR
        </button>
      </div>
    </nav>

    <main class="main-content">
      <Inicio v-if="seccionActual === 'inicio'" />
      <Sugerencias v-if="seccionActual === 'sugerencias'" />
      <Nosotros v-if="seccionActual === 'nosotros'" />
      <Contacto v-if="seccionActual === 'contacto'" />

      <template v-if="seccionActual === 'carta'">
        <LoginUnificado v-if="!authStore.isAuthenticated" @navegar="navegarA" />
        <CartaDigital v-else />
      </template>

      <template v-if="seccionActual === 'cocina'">
        <LoginUnificado
          v-if="!authStore.isCocina && !authStore.isAdmin"
          @navegar="navegarA"
        />
        <Cocina v-else />
      </template>

      <template v-if="seccionActual === 'admin'">
        <LoginUnificado v-if="!authStore.isAdmin" @navegar="navegarA" />
        <Administrador v-else />
      </template>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, watch } from "vue";
import { useAuthStore } from "./stores/auth.js";
import { useCarritoStore } from "./stores/carritoStore.js";
import Inicio from "./components/Inicio.vue";
import CartaDigital from "./components/CartaDigital.vue";
import Sugerencias from "./components/Sugerencias.vue";
import Nosotros from "./components/Nosotros.vue";
import Contacto from "./components/Contacto.vue";
import Cocina from "./components/Cocina.vue";
import Administrador from "./components/Admin.vue";
import LoginUnificado from "./components/LoginUnificado.vue";

const authStore = useAuthStore();
const carritoStore = useCarritoStore();

const seccionActual = ref("carta");

watch(
  () => authStore.userRole,
  (nuevoRol) => {
    if (nuevoRol === "admin") seccionActual.value = "admin";
    if (nuevoRol === "cocina") seccionActual.value = "cocina";
    if (nuevoRol === "cliente") seccionActual.value = "carta";
  },
  { immediate: true },
);

const todosLosItems = [
  {
    id: "inicio",
    nombre: "Inicio",
    roles: ["publico", "cliente", "cocina", "admin"],
  },
  {
    id: "carta",
    nombre: "Pedir",
    roles: ["publico", "cliente", "cocina", "admin"],
  },
  {
    id: "nosotros",
    nombre: "Nosotros",
    roles: ["publico", "cliente", "cocina", "admin"],
  },
  {
    id: "sugerencias",
    nombre: "Voz de Nosotros",
    roles: ["publico", "cliente", "cocina", "admin"],
  },
  {
    id: "contacto",
    nombre: "Contacto",
    roles: ["publico", "cliente", "cocina", "admin"],
  },
  { id: "cocina", nombre: "Cocina", roles: ["cocina", "admin"] },
  { id: "admin", nombre: "Administrador", roles: ["admin"] },
];

const menuItemsVisibles = computed(() => {
  const rol = authStore.userRole || "publico";
  return todosLosItems.filter((item) => item.roles.includes(rol));
});

const navegarA = (id) => {
  seccionActual.value = id;
};

const cerrarSesion = async () => {
  if (confirm("¿Seguro que deseas cerrar la sesión?")) {
    try {
      const mesaIdALiberar =
        carritoStore.mesaId || localStorage.getItem("mesa_id");

      await authStore.logout(mesaIdALiberar);

      carritoStore.limpiarCarrito();
      carritoStore.resetMesa();
      seccionActual.value = "carta";
    } catch (err) {
      console.error("Error durante el cierre de sesion:", err);
    }
  }
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

input[type="number"]::-webkit-inner-spin-button,
input[type="number"]::-webkit-outer-spin-button {
  -webkit-appearance: none;
  margin: 0;
}
input[type="number"] {
  -moz-appearance: textfield;
  appearance: textfield;
}

::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}
::-webkit-scrollbar-track {
  background: #121212;
}
::-webkit-scrollbar-thumb {
  background: #c5a059;
  border-radius: 3px;
}
::-webkit-scrollbar-thumb:hover {
  background: #e5c079;
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

.btn-logout {
  color: #8a8a8a;
  margin-left: 20px;
  border-left: 1px solid #2a2a2a;
  padding-left: 20px;
  border-radius: 0;
  letter-spacing: 2px;
}

.btn-logout:hover {
  color: #000;
  background: #c5a059;
  border-color: #c5a059;
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

.btn-login:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.btn-login:disabled:hover {
  background: #2a2a2a;
  color: #ffffff;
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

@media (max-width: 768px) {
  .navbar {
    flex-direction: column;
    gap: 15px;
    padding: 1rem;
  }

  .menu {
    flex-wrap: wrap;
    justify-content: center;
    width: 100%;
  }

  .nav-btn {
    font-size: 0.85rem;
    padding: 6px 12px;
  }
}
</style>
