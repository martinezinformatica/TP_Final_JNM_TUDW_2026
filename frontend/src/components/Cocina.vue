<template>
  <div class="cocina-container">
    <h1 class="titulo-brillante">GESTIÓN DE COCINA</h1>

    <div class="cocina-layout">
      <div class="card-mystic seccion-mapa">
        <h2 class="subtitulo">Plano del Salón</h2>
        <div class="salon-grid">
          <div
            @click="abrirMesa(1)"
            class="mesa-fija m-top-left"
            :class="claseMesa(1)"
          >
            <span class="num">Mesa 1</span>
            <span class="lbl">{{ textoEstadoMesa(1) }}</span>
          </div>

          <div
            @click="abrirMesa(2)"
            class="mesa-fija m-top-right"
            :class="claseMesa(2)"
          >
            <span class="num">Mesa 2</span>
            <span class="lbl">{{ textoEstadoMesa(2) }}</span>
          </div>

          <div
            @click="abrirMesa(5)"
            class="mesa-fija m-centro"
            :class="claseMesa(5)"
          >
            <span class="num">Mesa 5</span>
            <span class="lbl">{{ textoEstadoMesa(5) }}</span>
          </div>

          <div
            @click="abrirMesa(3)"
            class="mesa-fija m-bottom-left"
            :class="claseMesa(3)"
          >
            <span class="num">Mesa 3</span>
            <span class="lbl">{{ textoEstadoMesa(3) }}</span>
          </div>

          <div
            @click="abrirMesa(4)"
            class="mesa-fija m-bottom-right"
            :class="claseMesa(4)"
          >
            <span class="num">Mesa 4</span>
            <span class="lbl">{{ textoEstadoMesa(4) }}</span>
          </div>
        </div>
      </div>

      <!-- PANEL DERECHO: ALERTAS DE STOCK -->
      <div class="card-mystic seccion-stock">
        <h2 class="subtitulo">Alertas de Stock</h2>
        <div class="lista-stock">
          <div
            v-for="prod in topStockBajo"
            :key="prod.id"
            class="item-stock"
            :class="{ 'alerta-critica': prod.stock <= 5 }"
          >
            <span>{{ prod.nombre }}</span>
            <strong>Cant: {{ prod.stock }}</strong>
          </div>
        </div>
      </div>
    </div>

    <div v-if="mesaSeleccionada" class="overlay-popup">
      <div class="card-mystic popup-contenido position-relative">
        <div
          v-if="comunicandoCliente"
          class="cartel-comunicando animate-fade-in"
        >
          <div class="whatsapp-icon-mystic">
            <span class="burbuja-icono">💬</span>
          </div>
          <h3 class="texto-comunicando">PEDIDO LISTO</h3>
          <p class="subtexto-comunicando">
            Se generó la alerta para el pedido
            <strong class="resaltado-oro">#{{ idPedidoEntregado }}</strong> de
            la <strong>Mesa {{ mesaSeleccionada }}</strong
            >.
          </p>
          <div class="divisor-mystic-interno"></div>
          <button @click="confirmarEnvioNotificacion" class="btn-enviar-aviso">
            ENVIAR AVISO DE RETIRO (WHATSAPP)
          </button>
        </div>

        <h2 class="subtitulo">Detalle Mesa {{ mesaSeleccionada }}</h2>

        <div v-if="!pedidoDeMesa(mesaSeleccionada)" class="sin-datos">
          No hay pedidos activos para esta mesa.
        </div>

        <div v-else>
          <ul class="lista-items-cocina">
            <li
              v-for="item in pedidoDeMesa(mesaSeleccionada).items"
              :key="item.id"
            >
              <span class="cant">{{ item.cantidad }}x</span>
              <span class="name">{{ item.nombre_producto }}</span>
              <small v-if="item.observacion" class="obs"
                >({{ item.observacion }})</small
              >
            </li>
          </ul>

          <button
            @click="procesarPedido(pedidoDeMesa(mesaSeleccionada))"
            class="btn-amarillo-cocina"
          >
            {{
              pedidoDeMesa(mesaSeleccionada).estado === "NUE"
                ? "EMPEZAR PREPARACIÓN"
                : "MARCAR COMO ENTREGADO"
            }}
          </button>
        </div>

        <button @click="cerrarPopup" class="btn-cerrar">CERRAR PANEL</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import api from "../api.js";

const pedidos = ref([]);
const productos = ref([]);
const mesaSeleccionada = ref(null);
const comunicandoCliente = ref(false);
const idPedidoEntregado = ref(null);

const cargarDatos = async () => {
  try {
    const resPedidos = await api.get("pedidos/");
    pedidos.value = resPedidos.data;

    const resProd = await api.get("productos/");
    productos.value = resProd.data;
  } catch (e) {
    console.error("Error al sincronizar datos de cocina", e);
  }
};

const pedidoDeMesa = (numMesa) => {
  return pedidos.value.find((p) => {
    const numeroMesaActual = p.mesa?.numero || p.mesa;
    return (
      Number(numeroMesaActual) === Number(numMesa) &&
      (p.estado === "NUE" || p.estado === "PRE")
    );
  });
};

const claseMesa = (numMesa) => {
  const p = pedidoDeMesa(numMesa);
  if (!p) return "mesa-vacia";
  if (p.estado === "NUE") return "mesa-nueva";
  if (p.estado === "PRE") return "mesa-preparando";
  return "mesa-vacia";
};

const textoEstadoMesa = (numMesa) => {
  const p = pedidoDeMesa(numMesa);
  if (!p) return "VACÍA";
  if (p.estado === "NUE") return "NUEVO PEDIDO";
  if (p.estado === "PRE") return "EN COCINA";
  return "VACÍA";
};

const topStockBajo = computed(() => {
  return [...productos.value].sort((a, b) => a.stock - b.stock).slice(0, 5);
});

const abrirMesa = (numMesa) => {
  mesaSeleccionada.value = numMesa;
};

const cerrarPopup = () => {
  mesaSeleccionada.value = null;
  comunicandoCliente.value = false;
};

const procesarPedido = async (pedido) => {
  try {
    if (pedido.estado === "PRE") {
      idPedidoEntregado.value = pedido.id;

      await api.post(`pedidos/${pedido.id}/avanzar_estado/`);
      await cargarDatos();
      comunicandoCliente.value = true;
    } else {
      await api.post(`pedidos/${pedido.id}/avanzar_estado/`);
      await cargarDatos();
      cerrarPopup();
    }
  } catch (e) {
    alert("Error al actualizar el estado del pedido.");
    comunicandoCliente.value = false;
  }
};

const confirmarEnvioNotificacion = () => {
  comunicandoCliente.value = false;
  idPedidoEntregado.value = null;
  cerrarPopup();
};

onMounted(cargarDatos);
</script>

<style scoped>
.cocina-container {
  padding: 40px;
  max-width: 1200px;
  margin: 0 auto;
  color: white;
  font-family: "Roboto Mono", monospace;
}
.titulo-brillante {
  color: #c5a059;
  text-transform: uppercase;
  letter-spacing: 4px;
  text-align: center;
  margin-bottom: 40px;
}
.subtitulo {
  color: #c5a059;
  margin-bottom: 20px;
  font-size: 1.1rem;
  border-bottom: 1px solid #333;
  padding-bottom: 5px;
  text-transform: uppercase;
}

.card-mystic {
  background: #1a1a1a;
  border: 1px solid #c5a059;
  padding: 25px;
  border-radius: 12px;
}

.cocina-layout {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 30px;
}

.salon-grid {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  grid-template-rows: 1fr 1fr 1fr;
  gap: 20px;
  height: 450px;
  position: relative;
  padding: 10px;
}

.mesa-fija {
  background: #0a0a0a;
  border: 1px solid #333;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
  box-sizing: border-box;
  padding: 15px;
}
.mesa-fija:hover {
  transform: scale(1.02);
}

.mesa-fija .num {
  font-weight: bold;
  font-size: 1.2rem;
  color: #888;
}
.mesa-fija .lbl {
  font-size: 0.75rem;
  margin-top: 5px;
  color: #444;
}

.m-top-left {
  grid-column: 1;
  grid-row: 1;
}
.m-top-right {
  grid-column: 3;
  grid-row: 1;
}
.m-centro {
  grid-column: 2;
  grid-row: 2;
}
.m-bottom-left {
  grid-column: 1;
  grid-row: 3;
}
.m-bottom-right {
  grid-column: 3;
  grid-row: 3;
}

.mesa-vacia {
  border-color: #333;
  background: #0a0a0a;
}

.mesa-nueva {
  border-color: #c5a059;
  background: #2a2a2a;
  box-shadow: 0 0 15px rgba(197, 160, 89, 0.3);
}
.mesa-nueva .num {
  color: #ffffff;
}
.mesa-nueva .lbl {
  color: #ff4444;
  font-weight: bold;
}

.mesa-preparando {
  border-color: #c5a059;
  background: #1a1a1a;
  box-shadow: 0 0 15px rgba(197, 160, 89, 0.5);
}
.mesa-preparando .num {
  color: #c5a059;
}
.mesa-preparando .lbl {
  color: #ffffff;
  font-weight: bold;
}

.lista-stock {
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.item-stock {
  display: flex;
  justify-content: space-between;
  background: #2a2a2a;
  padding: 12px;
  border-radius: 6px;
  border: 1px solid #c5a059;
  color: #ffffff;
  font-size: 0.9rem;
}
.alerta-critica {
  color: #ff4444;
}

.overlay-popup {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 0.85);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 999;
}
.popup-contenido {
  width: 100%;
  max-width: 460px;
  text-align: center;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.7);
}

.lista-items-cocina {
  list-style: none;
  padding: 0;
  margin: 20px 0;
  text-align: left;
}
.lista-items-cocina li {
  padding: 10px 0;
  border-bottom: 1px solid #222;
  font-size: 1.1rem;
}
.lista-items-cocina .cant {
  color: #c5a059;
  font-weight: bold;
  margin-right: 15px;
}
.lista-items-cocina .obs {
  display: block;
  color: #777;
  font-size: 0.85rem;
  font-style: italic;
}

.btn-amarillo-cocina {
  width: 100%;
  background: #2a2a2a;
  border: 1px solid #c5a059;
  color: #ffffff;
  padding: 14px;
  cursor: pointer;
  font-weight: bold;
  letter-spacing: 1px;
  transition: 0.2s;
  margin-bottom: 15px;
}
.btn-amarillo-cocina:hover {
  background: #c5a059;
  color: #000000;
}

.btn-cerrar {
  background: #2a2a2a;
  border: 1px solid #c5a059;
  color: #ffffff;
  padding: 8px 16px;
  cursor: pointer;
  font-size: 0.8rem;
  border-radius: 4px;
  transition: 0.2s;
}
.btn-cerrar:hover {
  background: #c5a059;
  color: #000000;
}
.sin-datos {
  padding: 20px;
  color: #666;
  font-style: italic;
}
.position-relative {
  position: relative;
  overflow: hidden;
}

.cartel-comunicando {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: #111111;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  z-index: 10;
  padding: 30px;
  box-sizing: border-box;
}

.whatsapp-icon-mystic {
  width: 60px;
  height: 60px;
  border: 2px solid #c5a059;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(197, 160, 89, 0.05);
  box-shadow: 0 0 15px rgba(197, 160, 89, 0.2);
  margin-bottom: 10px;
}

.burbuja-icono {
  font-size: 1.8rem;
}

.texto-comunicando {
  color: #c5a059;
  letter-spacing: 3px;
  font-size: 1.3rem;
  margin: 10px 0 15px 0;
  text-shadow: 0 0 10px rgba(197, 160, 89, 0.3);
  font-weight: bold;
}

.subtexto-comunicando {
  color: #dddddd;
  font-size: 0.95rem;
  line-height: 1.5;
  margin: 0;
}

.resaltado-oro {
  color: #c5a059;
  font-weight: bold;
}

.subtexto-comunicando strong {
  color: #fff;
}

.divisor-mystic-interno {
  width: 85%;
  height: 1px;
  background: #252525;
  margin: 25px 0;
}

.btn-enviar-aviso {
  width: 100%;
  background: #1a1a1a;
  border: 1px solid #c5a059;
  color: #ffffff;
  padding: 14px;
  font-family: "Roboto Mono", monospace;
  font-weight: bold;
  cursor: pointer;
  letter-spacing: 1px;
  transition: 0.2s;
  border-radius: 4px;
}

.btn-enviar-aviso:hover {
  background: #c5a059;
  color: #000000;
}

.animate-fade-in {
  animation: fadeIn 0.2s ease-in-out forwards;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: scale(0.97);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}
</style>
