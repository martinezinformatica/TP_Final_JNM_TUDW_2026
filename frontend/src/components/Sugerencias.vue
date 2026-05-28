<template>
  <div class="nosotros-container">
    <div class="card-horizontal-sugerencias">
      <div class="col-texto form-section">
        <h1>Voz de Nosotros</h1>
        <p class="subtitulo">Tu opinión ayuda a mejorar la mística.</p>
        <div class="divisor-mystic"></div>

        <label class="label-mystic">¿Cómo fue tu experiencia?</label>
        <div class="vasos-selector">
          <button
            v-for="item in opcionesCalificacion"
            :key="item.valor"
            @click="calificacionSeleccionada = item.valor"
            :class="{ activo: calificacionSeleccionada === item.valor }"
            :title="item.leyenda"
          >
            <span class="vasos-icono">{{ item.icono }}</span>
            <span class="vasos-leyenda">{{ item.leyenda }}</span>
          </button>
        </div>

        <textarea
          v-model="nuevoComentario"
          placeholder="Escribí tu sugerencia aquí..."
          class="textarea-mystic"
        ></textarea>

        <button @click="mandarSugerencia" class="btn-mystic-full">
          PUBLICAR COMENTARIO
        </button>
      </div>

      <div class="col-opiniones">
        <h2 class="dorado-texto">Últimas Opiniones</h2>

        <div v-if="store.ultimasTres.length === 0" class="sin-datos">
          Todavía no hay comentarios.
        </div>

        <div
          v-for="(sug, index) in store.ultimasTres"
          :key="index"
          class="comentario-item"
        >
          <div class="badge-calificacion">
            {{ mostrarVasos(sug.calificacion) }}
          </div>
          <div class="texto-comentario">
            <p>"{{ sug.texto }}"</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useSugerenciaStore } from "../stores/sugerenciaStore";

const store = useSugerenciaStore();
const nuevoComentario = ref("");
const calificacionSeleccionada = ref(null);

const opcionesCalificacion = [
  { valor: 1, icono: "🥃", leyenda: "Vacío" },
  { valor: 2, icono: "🥃🥃", leyenda: "Medio" },
  { valor: 3, icono: "🥃🥃🥃", leyenda: "Lleno" },
  { valor: 4, icono: "🥃🥃🥃🥃", leyenda: "Mystic" },
];

const mostrarVasos = (valorCalificacion) => {
  if (isNaN(valorCalificacion)) return valorCalificacion;
  return "🥃".repeat(valorCalificacion);
};

const mandarSugerencia = () => {
  if (!calificacionSeleccionada.value)
    return alert("Por favor, seleccioná una calificación.");
  if (nuevoComentario.value.trim().length < 5)
    return alert("Escribí un comentario un poco más largo.");

  store.agregarSugerencia({
    calificacion: calificacionSeleccionada.value,
    texto: nuevoComentario.value,
  });

  nuevoComentario.value = "";
  calificacionSeleccionada.value = null;
  alert("¡Gracias por tu comentario!");
};
</script>

<style scoped>
.nosotros-container {
  display: flex;
  flex-wrap: wrap;
  max-width: 1000px;
  width: 100%;
  background: #1a1a1a;
  border: 1px solid #c5a059;
  border-radius: 15px;
  overflow: hidden;
}

.card-horizontal-sugerencias {
  display: flex;
  flex-wrap: wrap;
  max-width: 1000px;
  width: 100%;
  background: #1a1a1a;
  border: 1px solid #c5a059;
  border-radius: 15px;
  overflow: hidden;
}

.col-texto {
  flex: 1.2;
  padding: 40px;
  text-align: left;
}
.col-opiniones {
  flex: 1;
  padding: 40px;
  background: #111;
  border-left: 1px solid #333;
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
  margin-bottom: 25px;
  text-transform: uppercase;
}

.divisor-mystic {
  width: 50px;
  height: 3px;
  background: #c5a059;
  margin: 20px 0;
}

.label-mystic {
  color: #ccc;
  display: block;
  margin-bottom: 15px;
  font-weight: bold;
}

.vasos-selector {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 10px;
  margin-bottom: 25px;
}
.vasos-selector button {
  background: #2a2a2a;
  border: 1px solid #333;
  color: #ffffff;
  border-radius: 6px;
  cursor: pointer;
  padding: 12px 5px;
  transition: 0.3s;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 5px;
}
.vasos-icono {
  font-size: 1.2rem;
  letter-spacing: -2px;
}
.vasos-leyenda {
  font-size: 0.7rem;
  text-transform: uppercase;
  color: #888;
}
.vasos-selector button:hover {
  border-color: #c5a059;
}
.vasos-selector button.activo {
  border-color: #c5a059;
  background: #1a1a1a;
  box-shadow: 0 0 10px rgba(197, 160, 89, 0.3);
}
.vasos-selector button.activo .vasos-leyenda {
  color: #c5a059;
  font-weight: bold;
}

.textarea-mystic {
  width: 100%;
  height: 120px;
  background: #000;
  color: #ccc;
  border: 1px solid #333;
  border-radius: 5px;
  padding: 15px;
  font-family: "Roboto Mono", monospace;
  margin-bottom: 20px;
  resize: none;
}
.textarea-mystic:focus {
  border-color: #c5a059;
  outline: none;
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
}
.btn-mystic-full:hover {
  background: #c5a059;
  color: #000000;
}

.comentario-item {
  background: #1a1a1a;
  padding: 15px;
  border-radius: 5px;
  margin-bottom: 15px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  border-left: 3px solid #c5a059;
}
.badge-calificacion {
  font-size: 1rem;
  letter-spacing: -1px;
  text-align: left;
}
.texto-comentario p {
  margin: 0;
  color: #aaa;
  font-style: italic;
  font-size: 0.9rem;
  text-align: left;
}
.sin-datos {
  color: #555;
  font-style: italic;
  text-align: center;
}

@media (max-width: 850px) {
  .card-horizontal-sugerencias {
    flex-direction: column;
  }
  .col-opiniones {
    border-left: none;
    border-top: 1px solid #333;
  }
  .vasos-selector {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>
