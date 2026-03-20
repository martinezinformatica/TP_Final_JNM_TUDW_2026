<template>
  <div id="app">
    <nav class="navbar">
      <div class="logo">NATURAL MYSTIC</div>
      <div class="menu">
        <button @click="seccionActual = 'inicio'">Inicio</button>
        <button @click="seccionActual = 'carta'">Pedir</button>
        <button @click="seccionActual = 'nosotros'">Nosotros</button>
        <button @click="seccionActual = 'sugerencias'">Voz de nosotros</button>
        <button @click="seccionActual = 'contacto'">Contacto</button>
      </div>
    </nav>

    <main class="main-content">
      
      <section v-if="seccionActual === 'inicio'">
        <div class="card-simple">
          <h1>Bienvenidos</h1>
          <p>Esta es la página principal de la cervecería.</p>
        </div>
      </section>

      <CartaDigital v-if="seccionActual === 'carta'" />

      <section v-if="seccionActual === 'nosotros'">
        <div class="card-simple">
          <h1>Quiénes Somos</h1>
          <p>Historia de Natural Mystic en General Roca.</p>
        </div>
      </section>

      <section v-if="seccionActual === 'sugerencias'">
        <div class="card-simple">
          <h1>Voz de nosotros</h1>
          <p>Sección para dejar comentarios y ver los últimos 3.</p>
        </div>
      </section>

      <section v-if="seccionActual === 'contacto'">
        <div class="card-simple">
          <h1>Contacto</h1>
          <p>📍 Dirección y Redes Sociales.</p>
        </div>
      </section>

    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import CartaDigital from './components/CartaDigital.vue'

// Variable que controla qué bloque se muestra
const seccionActual = ref('inicio')
</script>

<style>
/* Estética Base Muy Simple */
body {
  margin: 0;
  font-family: Arial, sans-serif;
  background-color: #1a1a1a;
  color: white;
}

.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 2rem;
  background-color: #000;
  border-bottom: 1px solid #333;
}

.logo {
  font-weight: bold;
  font-size: 1.2rem;
  color: #c5a059;
}

.menu button {
  background: none;
  border: none;
  color: white;
  margin-left: 15px;
  cursor: pointer;
  padding: 5px 10px;
}

.menu button:hover {
  color: #c5a059;
}

.main-content {
  padding: 20px;
}

.card-simple {
  background: #222;
  padding: 40px;
  border-radius: 8px;
  text-align: center;
  margin-top: 20px;
}
</style>