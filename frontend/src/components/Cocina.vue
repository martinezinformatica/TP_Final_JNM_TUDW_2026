<template>
  <div class="cocina-container">
    <header class="cocina-header">
      <h1 class="titulo-brillante">GESTIÓN DE COCINA</h1>
      <button @click="ejecutarLogout" class="btn-cerrar-sesion">
        CERRAR SESIÓN
      </button>
    </header>
    <div class="linea-divisoria-header"></div>

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
    <div v-if="mesaSeleccionada" class="overlay-popup-mystic">
      <div
        v-if="comunicandoCliente"
        class="card-mystic-modal popup-exito-contenido animate-fade-in"
      >
        <div class="icono-exito-oro">
          <span class="burbuja-icono">💬</span>
        </div>
        <h2 class="titulo-modal-oro">PEDIDO LISTO</h2>
        <p class="mensaje-modal-texto">
          Se generó la notificación para la
          <strong class="resaltado-oro">Mesa {{ mesaSeleccionada }}</strong
          >: "Tu pedido
          <strong class="resaltado-oro">#{{ idPedidoEntregado }}</strong> está
          listo en barra".
        </p>
        <div class="divisor-mystic-modal"></div>
        <button @click="confirmarEnvioNotificacion" class="btn-modal-aceptar">
          ENVIAR AVISO DE RETIRO (WHATSAPP)
        </button>
      </div>

      <div
        v-else
        class="card-mystic-modal popup-exito-contenido animate-fade-in"
      >
        <h2 class="titulo-modal-oro">Detalle Mesa {{ mesaSeleccionada }}</h2>

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
            class="btn-modal-aceptar"
          >
            {{
              pedidoDeMesa(mesaSeleccionada).estado === "NUE"
                ? "EMPEZAR PREPARACIÓN"
                : "MARCAR COMO ENTREGADO"
            }}
          </button>
        </div>

        <div class="divisor-mystic-modal"></div>
        <button @click="cerrarPopup" class="btn-cerrar-volver">
          VOLVER AL PLANO
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import api from "../api.js";
import { useAuthStore } from "../stores/auth.js";

const pedidos = ref([]);
const productos = ref([]);
const mesaSeleccionada = ref(null);
const comunicandoCliente = ref(false);
const idPedidoEntregado = ref(null);

const authStore = useAuthStore();

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

const ejecutarLogout = () => {
  if (confirm("¿Seguro que deseas cerrar sesión en el panel de Cocina?")) {
    authStore.logout();
    window.location.reload();
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

.cocina-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.titulo-brillante {
  color: #c5a059;
  text-transform: uppercase;
  letter-spacing: 4px;
  margin: 0;
  font-size: 2rem;
  font-weight: bold;
}

.btn-cerrar-sesion {
  background: transparent;
  border: 1px solid #c5a059;
  color: #c5a059;
  padding: 10px 20px;
  font-family: "Roboto Mono", monospace;
  font-weight: bold;
  font-size: 0.9rem;
  cursor: pointer;
  border-radius: 4px;
  transition: all 0.3s ease;
  letter-spacing: 1px;
}
.btn-cerrar-sesion:hover {
  background: #c5a059;
  color: #000000;
  box-shadow: 0 0 10px rgba(197, 160, 89, 0.4);
}

.linea-divisoria-header {
  width: 100%;
  height: 1px;
  background: #333;
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
  border: 1px solid #333;
  color: #ffffff;
  font-size: 0.9rem;
}
.alerta-critica {
  color: #ff4444;
  border-color: rgba(255, 68, 68, 0.4);
}

.overlay-popup-mystic {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 0.85);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
}

.card-mystic-modal {
  background: #111111;
  border: 2px solid #c5a059;
  padding: 35px 25px;
  border-radius: 12px;
  box-shadow:
    0 10px 30px rgba(0, 0, 0, 0.8),
    0 0 15px rgba(197, 160, 89, 0.2);
}

.popup-exito-contenido {
  width: 90%;
  max-width: 460px;
  text-align: center;
}

.icono-exito-oro {
  width: 60px;
  height: 60px;
  border: 2px solid #c5a059;
  color: #c5a059;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 20px auto;
  background: rgba(197, 160, 89, 0.05);
  box-shadow: 0 0 15px rgba(197, 160, 89, 0.2);
}

.burbuja-icono {
  font-size: 1.6rem;
  font-weight: bold;
}

.titulo-modal-oro {
  color: #c5a059;
  font-size: 1.3rem;
  letter-spacing: 3px;
  margin: 10px 0 15px 0;
  text-shadow: 0 0 10px rgba(197, 160, 89, 0.3);
  font-weight: bold;
  text-transform: uppercase;
}

.mensaje-modal-texto {
  color: #dddddd;
  font-size: 0.95rem;
  line-height: 1.5;
  margin: 0 0 20px 0;
}

.resaltado-oro {
  color: #c5a059;
  font-weight: bold;
}

.divisor-mystic-modal {
  width: 85%;
  height: 1px;
  background: #252525;
  margin: 25px auto;
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

.sin-datos {
  padding: 20px;
  color: #666;
  font-style: italic;
}

.btn-modal-aceptar {
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
.btn-modal-aceptar:hover {
  background: #c5a059;
  color: #000000;
}

.btn-cerrar-volver {
  background: transparent;
  border: 1px solid #444;
  color: #888;
  padding: 10px 20px;
  font-family: "Roboto Mono", monospace;
  cursor: pointer;
  font-size: 0.8rem;
  border-radius: 4px;
  transition: 0.2s;
  letter-spacing: 1px;
}
.btn-cerrar-volver:hover {
  border-color: #c5a059;
  color: #fff;
}

.animate-fade-in {
  animation: modalFadeIn 0.2s ease-in-out forwards;
}

@keyframes modalFadeIn {
  from {
    opacity: 0;
    transform: scale(0.97);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

@media (max-width: 850px) {
  .cocina-layout {
    grid-template-columns: 1fr;
  }
  .cocina-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 15px;
  }
  .btn-cerrar-sesion {
    width: 100%;
  }
}
</style>
