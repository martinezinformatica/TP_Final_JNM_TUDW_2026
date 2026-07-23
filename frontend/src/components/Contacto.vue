<template>
  <div class="contacto-container">
    <div class="card-horizontal-contacto">
      <div class="col-formulario">
        <h1>Contacto</h1>
        <p class="subtitulo">
          Dejanos tu mensaje y nos comunicamos a la brevedad.
        </p>
        <div class="divisor-mystic"></div>

        <div class="grupo-input">
          <label class="label-mystic">Nombre </label>
          <input
            v-model="formulario.nombre"
            type="text"
            placeholder="Tu nombre"
            class="input-mystic"
          />
        </div>

        <div class="grupo-input">
          <label class="label-mystic">Correo Electronico</label>
          <input
            v-model="formulario.email"
            type="email"
            placeholder="ejemplo@correo.com"
            class="input-mystic"
          />
        </div>

        <div class="grupo-input">
          <label class="label-mystic">Mensaje</label>
          <textarea
            v-model="formulario.mensaje"
            placeholder="Escribi tu mensaje aqui..."
            class="textarea-mystic"
          ></textarea>
        </div>

        <button @click="enviarMensaje" class="btn-mystic-full">
          ENVIAR MENSAJE
        </button>
      </div>

      <div class="col-info">
        <h2 class="dorado-texto">Nuestra Ubicacion</h2>

        <div class="mapa-imagen-contenedor">
          <div class="mapa-imagen-fondo"></div>
          <div class="mapa-overlay-oscuro"></div>

          <a
            href="https://www.google.com/maps?q=Natural+Mystic+General+Roca"
            target="_blank"
            class="marcador-birra-absoluto"
            title="Ver en Google Maps"
          >
            <span class="emoji-birra">🍺</span>
            <span class="cartel-bar">NATURAL MYSTIC</span>
          </a>
        </div>

        <div class="info-bloque">
          <strong>DIRECCIÓN</strong>
          <p>General Roca (Fiske Menuco), Rio Negro</p>
        </div>

        <div class="info-bloque">
          <strong>HORARIOS</strong>
          <p>Martes a Domingos — 18:00 a 02:00 hs</p>
        </div>

        <div class="info-bloque">
          <strong>NUESTRAS REDES</strong>
          <div class="redes-links">
            <a href="https://instagram.com" target="_blank" class="link-mystic"
              >INSTAGRAM</a
            >
            <span class="separador">//</span>
            <a href="https://facebook.com" target="_blank" class="link-mystic"
              >FACEBOOK</a
            >
            <span class="separador">//</span>
            <a href="https://wa.me" target="_blank" class="link-mystic"
              >WHATSAPP</a
            >
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";

const formulario = ref({
  nombre: "",
  email: "",
  mensaje: "",
});

const enviarMensaje = () => {
  if (
    !formulario.value.nombre.trim() ||
    !formulario.value.email.trim() ||
    !formulario.value.mensaje.trim()
  ) {
    return alert("Por favor, completa todos los campos antes de enviar.");
  }

  alert(
    `¡Gracias ${formulario.value.nombre}! Tu mensaje fue enviado con exito.`,
  );

  formulario.value = {
    nombre: "",
    email: "",
    mensaje: "",
  };
};
</script>

<style scoped>
.contacto-container {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 40px 20px;
  font-family: "Roboto Mono", monospace;
  color: white;
}

.card-horizontal-contacto {
  display: flex;
  flex-wrap: wrap;
  max-width: 1000px;
  width: 100%;
  background: #1a1a1a;
  border: 1px solid #c5a059;
  border-radius: 15px;
  overflow: hidden;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.5);
}

.col-formulario {
  flex: 1.2;
  padding: 40px;
  text-align: left;
}

.col-info {
  flex: 1;
  padding: 40px;
  background: #111;
  border-left: 1px solid #333;
  text-align: left;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

h1 {
  color: #c5a059;
  text-transform: uppercase;
  letter-spacing: 3px;
  font-size: 1.8rem;
  margin: 0;
}

.subtitulo {
  color: #888;
  font-size: 0.9rem;
  margin-top: 5px;
}

.dorado-texto {
  color: #c5a059;
  font-size: 1.2rem;
  margin-bottom: 20px;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.divisor-mystic {
  width: 50px;
  height: 3px;
  background: #c5a059;
  margin: 20px 0;
}

.grupo-input {
  margin-bottom: 20px;
}

.label-mystic {
  color: #ccc;
  display: block;
  margin-bottom: 8px;
  font-weight: bold;
  font-size: 0.85rem;
  text-transform: uppercase;
}

.input-mystic {
  width: 100%;
  padding: 12px;
  background: #000;
  border: 1px solid #333;
  color: white;
  border-radius: 6px;
  box-sizing: border-box;
}
.input-mystic:focus,
.textarea-mystic:focus {
  border-color: #c5a059;
  outline: none;
}

.textarea-mystic {
  width: 100%;
  height: 120px;
  background: #000;
  color: #ccc;
  border: 1px solid #333;
  border-radius: 6px;
  padding: 15px;
  font-family: "Roboto Mono", monospace;
  box-sizing: border-box;
  resize: none;
}

.btn-mystic-full {
  width: 100%;
  background: #2a2a2a;
  border: 1px solid #c5a059;
  color: #ffffff;
  padding: 15px;
  font-family: "Roboto Mono", monospace;
  font-weight: bold;
  cursor: pointer;
  transition: 0.3s;
  letter-spacing: 1px;
  margin-top: 10px;
}
.btn-mystic-full:hover {
  background: #c5a059;
  color: #000000;
}

.mapa-imagen-contenedor {
  position: relative;
  width: 100%;
  height: 180px;
  border: 1px solid #c5a059;
  border-radius: 8px;
  overflow: hidden;
  margin-bottom: 25px;
  box-shadow: inset 0 0 20px rgba(0, 0, 0, 0.8);
}

.mapa-imagen-fondo {
  width: 100%;
  height: 100%;
  background-image: url("../assets/mapa.jpg");
  background-size: cover;
  background-position: center;
  filter: brightness(85%);
}

.mapa-overlay-oscuro {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(26, 26, 26, 0.1);
  pointer-events: none;
}

.marcador-birra-absoluto {
  position: absolute;
  top: 48%;
  left: 49%;
  transform: translate(-50%, -50%);
  display: flex;
  flex-direction: column;
  align-items: center;
  z-index: 2;
  text-decoration: none;
  cursor: pointer;
}

.emoji-birra {
  font-size: 2.2rem;
  filter: drop-shadow(0 0 10px rgba(197, 160, 89, 0.8));
  animation: rebote-suave 1.5s infinite alternate ease-in-out;
}

.cartel-bar {
  background: #111111;
  color: #c5a059;
  font-size: 0.7rem;
  font-weight: bold;
  padding: 4px 8px;
  border: 1px solid #c5a059;
  border-radius: 4px;
  margin-top: 5px;
  letter-spacing: 1px;
  white-space: nowrap;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.9);
}

@keyframes rebote-suave {
  from {
    transform: translateY(0);
  }
  to {
    transform: translateY(-6px);
  }
}

.info-bloque {
  margin-bottom: 20px;
}
.info-bloque strong {
  color: #888;
  font-size: 0.75rem;
  letter-spacing: 1px;
  display: block;
  margin-bottom: 5px;
}
.info-bloque p {
  margin: 0;
  color: #fff;
  font-size: 0.95rem;
}

.redes-links {
  display: flex;
  gap: 10px;
  align-items: center;
  margin-top: 5px;
}
.link-mystic {
  color: #c5a059;
  text-decoration: none;
  font-weight: bold;
  font-size: 0.85rem;
  transition: 0.2s;
}
.link-mystic:hover {
  color: #ffffff;
  text-decoration: underline;
}
.separador {
  color: #333;
  font-size: 0.8rem;
}

@media (max-width: 850px) {
  .card-horizontal-contacto {
    flex-direction: column;
  }
  .col-info {
    border-left: none;
    border-top: 1px solid #333;
    gap: 20px;
  }
}
</style>
