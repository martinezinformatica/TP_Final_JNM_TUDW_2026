<template>
  <div id="app">
    <nav class="navbar">
      <div class="logo">NATURAL MYSTIC</div>
      <div class="menu">
        <button
          v-for="item in menuItems"
          :key="item.id"
          @click="seccionActual = item.id"
          :class="['nav-btn', { activo: seccionActual === item.id }]"
        >
          {{ item.nombre }}
        </button>
      </div>
    </nav>

    <main class="main-content">
      <Inicio v-if="seccionActual === 'inicio'" />
      <CartaDigital v-if="seccionActual === 'carta'" />
      <Sugerencias v-if="seccionActual === 'sugerencias'" />
      <Nosotros v-if="seccionActual === 'nosotros'" />
      <Contacto v-if="seccionActual === 'contacto'" />
      <Cocina v-if="seccionActual === 'cocina'" />
      <Administrador v-if="seccionActual === 'admin'" />
    </main>
  </div>
</template>

<script setup>
import { ref } from "vue";
import Inicio from "./components/Inicio.vue";
import CartaDigital from "./components/CartaDigital.vue";
import Sugerencias from "./components/Sugerencias.vue";
import Nosotros from "./components/Nosotros.vue";
import Contacto from "./components/Contacto.vue";
import Cocina from "./components/Cocina.vue";
import Administrador from "./components/Admin.vue";

const seccionActual = ref("carta");

const menuItems = [
  { id: "inicio", nombre: "Inicio" },
  { id: "carta", nombre: "Pedir" },
  { id: "nosotros", nombre: "Nosotros" },
  { id: "sugerencias", nombre: "Voz de Nosotros" },
  { id: "contacto", nombre: "Contacto" },
  { id: "cocina", nombre: "Cocina" },
  { id: "admin", nombre: "Administrador" },
];
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
</style>
