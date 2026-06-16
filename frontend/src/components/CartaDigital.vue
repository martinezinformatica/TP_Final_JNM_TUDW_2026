<template>
  <div class="carta-container">
    <div v-if="carritoStore.mesaSeleccionada" class="posavasos-mesa">
      <div class="mesa-info">
        <span class="label">MESA</span>
        <span class="numero">{{ carritoStore.mesaId }}</span>
      </div>
      <button
        @click="ejecutarCerrarMesa"
        class="btn-salir-mesa"
        title="Cerrar Mesa / Salir"
      >
        SALIR
      </button>
    </div>

    <div v-if="!carritoStore.mesaSeleccionada" class="pantalla-inicio-centrada">
      <div class="card-mystic-base card-mesa-selector">
        <h1 class="titulo-brillante">La Pizarra</h1>
        <p class="subtitulo-carta">General Roca • Pedí directamente a cocina</p>
        <div class="divisor-mystic centro"></div>
        <h2>Bienvenido</h2>
        <p class="bajada-bienvenida">
          Por favor, seleccioná tu mesa para comenzar:
        </p>

        <div class="mesas-grid">
          <button
            v-for="n in [1, 2, 3, 4, 5]"
            :key="n"
            @click="carritoStore.setMesa(n)"
            :class="['btn-mesa', { seleccionado: carritoStore.mesaId === n }]"
          >
            Mesa {{ n }}
          </button>
        </div>
      </div>
    </div>

    <div v-else class="layout-principal">
      <div class="columnas-wrap">
        <section class="productos-seccion">
          <h1 class="titulo-pizarra">La Pizarra</h1>
          <p class="subtitulo-pizarra">Elegí tus pintas y comida artesanal.</p>
          <div class="divisor-mystic"></div>

          <div class="productos-grid">
            <div v-for="p in productos" :key="p.id" class="producto-card">
              <div class="producto-info">
                <h3>{{ p.nombre }}</h3>
                <p class="precio">{{ formatearPrecio(p.precio) }}</p>

                <p
                  class="stock"
                  :class="{ 'sin-stock': obtenerStockDisponible(p) <= 0 }"
                >
                  {{
                    obtenerStockDisponible(p) > 0
                      ? `Disponible`
                      : "No disponible"
                  }}
                </p>
              </div>

              <button
                @click="carritoStore.agregarProducto(p)"
                :disabled="obtenerStockDisponible(p) <= 0"
                class="btn-agregar-producto"
              >
                {{ obtenerStockDisponible(p) > 0 ? "+ AGREGAR" : "AGOTADO" }}
              </button>
            </div>
          </div>
        </section>

        <aside v-if="carritoStore.items.length > 0" class="carrito-panel">
          <h2 class="dorado-texto">Tu Pedido</h2>
          <div class="divisor-rustico"></div>

          <ul class="lista-carrito">
            <li v-for="(item, index) in carritoStore.items" :key="index">
              <div class="item-linea">
                <span class="nombre-item">{{ item.nombre }}</span>
                <span class="precio-item">{{
                  formatearPrecio(item.precio)
                }}</span>
              </div>
              <button
                @click="carritoStore.quitarProducto(index)"
                class="btn-quitar-item"
              >
                ✕ QUITAR
              </button>
            </li>
          </ul>

          <div class="total-seccion">
            <p class="total-label">TOTAL</p>
            <p class="total-monto">
              {{ formatearPrecio(carritoStore.totalPedido) }}
            </p>
          </div>

          <button @click="enviarPedidoFinal" class="btn-confirmar-pedido">
            ENVIAR A COCINA
          </button>
        </aside>
      </div>
    </div>

    <div v-if="mostrarModalExito" class="overlay-popup-mystic">
      <div class="card-mystic-modal popup-exito-contenido animate-fade-in">
        <div class="icono-exito-oro">
          <span class="burbuja-icono">✓</span>
        </div>
        <h2 class="titulo-modal-oro">¡PEDIDO PROCESADO!</h2>
        <p class="mensaje-modal-texto">
          El pedido
          <strong class="resaltado-oro">#{{ idPedidoCreado }}</strong> fue
          enviado con éxito a la cocina.
        </p>
        <div class="divisor-mystic-modal"></div>
        <button @click="cerrarModalExito" class="btn-modal-aceptar">
          ACEPTAR
        </button>
      </div>
    </div>

    <div v-if="mostrarModalError" class="overlay-popup-mystic">
      <div
        class="card-mystic-modal popup-exito-contenido animate-fade-in error-borde"
      >
        <div class="icono-error-rojo">
          <span class="burbuja-icono">✕</span>
        </div>
        <h2 class="titulo-modal-rojo">ERROR</h2>
        <p class="mensaje-modal-texto">{{ mensajeError }}</p>
        <div class="divisor-mystic-modal un-rojo"></div>
        <button @click="mostrarModalError = false" class="btn-modal-aceptar">
          CERRAR
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import api from "../api.js";
import { useCarritoStore } from "../stores/carritoStore";
import { useAuthStore } from "../stores/auth.js";

const carritoStore = useCarritoStore();
const authStore = useAuthStore();
const productos = ref([]);
const mostrarModalExito = ref(false);
const idPedidoCreado = ref(null);
const mostrarModalError = ref(false);
const mensajeError = ref("");
const ejecutarCerrarMesa = () => {
  if (confirm("¿Deseas cerrar la mesa y salir del sistema?")) {
    carritoStore.limpiarCarrito();
    carritoStore.resetMesa();
    authStore.logout();
    window.location.reload();
  }
};

const fetchProductos = async () => {
  try {
    const response = await api.get("productos/");
    productos.value = response.data;
  } catch (error) {
    console.error("Error conectando con la API desde la Carta");
  }
};

const obtenerStockDisponible = (producto) => {
  if (!producto) return 0;
  const cantidadEnCarrito = carritoStore.items.filter(
    (item) => item.id === producto.id,
  ).length;
  return producto.stock - cantidadEnCarrito;
};

const enviarPedidoFinal = async () => {
  const tieneItemsSinStock = carritoStore.items.some((item) => {
    const prodOriginal = productos.value.find((p) => p.id === item.id);
    return !prodOriginal || prodOriginal.stock <= 0;
  });

  if (tieneItemsSinStock) {
    mensajeError.value =
      "Uno de los productos de tu pedido se quedó sin stock. Modificá el carrito antes de enviar.";
    mostrarModalError.value = true;
    await fetchProductos();
    return;
  }
  const itemsAgrupados = [];
  carritoStore.items.forEach((item) => {
    const yaExiste = itemsAgrupados.find((i) => i.producto === item.id);
    if (yaExiste) {
      yaExiste.cantidad += 1;
    } else {
      itemsAgrupados.push({
        producto: item.id,
        cantidad: 1,
        observacion: "",
      });
    }
  });
  const payload = {
    mesa: carritoStore.mesaId,
    items: itemsAgrupados,
  };
  try {
    const res = await api.post("pedidos/", payload);

    idPedidoCreado.value = res.data.id;
    mostrarModalExito.value = true;

    carritoStore.limpiarCarrito();
    await fetchProductos();
  } catch (error) {
    if (error.response && error.response.status === 400) {
      mensajeError.value =
        "Error: Algunos productos elegidos superan el stock disponible actual de la barra.";
    } else {
      mensajeError.value =
        "Ocurrió un problema al enviar el pedido a la cocina. Intente nuevamente.";
    }
    mostrarModalError.value = true;
    await fetchProductos();
  }
};

const formatearPrecio = (valor) => {
  if (!valor) return "$0";
  const entero = Math.floor(Number(valor));
  return new Intl.NumberFormat("es-AR", {
    style: "currency",
    currency: "ARS",
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
  }).format(entero);
};

const cerrarModalExito = () => {
  mostrarModalExito.value = false;
  idPedidoCreado.value = null;
};

onMounted(fetchProductos);
</script>

<style scoped>
.carta-container {
  width: 100vw;
  max-width: 1250px;
  margin: 0 auto;
  position: relative;
  padding: 20px;
  font-family: "Roboto Mono", monospace;
  color: white;
  box-sizing: border-box;
}

.posavasos-mesa {
  position: absolute;
  top: 0px;
  right: 20px;
  background: #111;
  border: 2px solid #c5a059;
  width: 85px;
  height: 85px;
  border-radius: 50%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  box-shadow:
    0 4px 15px rgba(0, 0, 0, 0.6),
    0 0 10px rgba(197, 160, 89, 0.2);
  z-index: 10;
  padding: 5px;
  box-sizing: border-box;
}

.mesa-info {
  text-align: center;
  line-height: 1;
  margin-top: 4px;
}
.mesa-info .label {
  font-size: 0.5rem;
  color: #888;
  display: block;
  font-weight: bold;
  letter-spacing: 1px;
}
.mesa-info .numero {
  font-size: 1.4rem;
  color: #c5a059;
  font-weight: bold;
}

.btn-salir-mesa {
  background: #c5a059;
  border: 1px solid #000;
  color: #000;
  font-family: "Roboto Mono", monospace;
  font-size: 0.65rem;
  font-weight: bold;
  padding: 2px 8px;
  cursor: pointer;
  border-radius: 10px;
  margin-top: 4px;
  transition: all 0.2s ease;
}

.btn-salir-mesa:hover {
  background: #ffffff;
  box-shadow: 0 0 8px rgba(255, 255, 255, 0.6);
}

.pantalla-inicio-centrada {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 60vh;
  width: 100%;
}

.card-mystic-base {
  background: #1a1a1a;
  border: 1px solid #c5a059;
  padding: 45px;
  border-radius: 12px;
}

.card-mesa-selector {
  text-align: center;
  max-width: 500px;
  width: 100%;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
}

.titulo-brillante {
  color: #c5a059;
  text-transform: uppercase;
  letter-spacing: 4px;
  margin: 0 0 5px 0;
  font-size: 1.8rem;
}

.subtitulo-carta {
  color: #888;
  font-size: 0.85rem;
  margin-bottom: 20px;
}

.card-mesa-selector h2 {
  font-size: 1.3rem;
  text-transform: uppercase;
  letter-spacing: 1px;
  margin-top: 10px;
}

.bajada-bienvenida {
  color: #ccc;
  font-size: 0.95rem;
}

.mesas-grid {
  display: flex;
  gap: 15px;
  margin-top: 35px;
  justify-content: center;
  flex-wrap: wrap;
}

.btn-mesa {
  background: #2a2a2a;
  border: 1px solid #c5a059;
  color: #ffffff;
  padding: 12px 22px;
  font-family: "Roboto Mono", monospace;
  font-weight: bold;
  cursor: pointer;
  border-radius: 6px;
  transition: 0.3s;
}
.btn-mesa:hover,
.btn-mesa.seleccionado {
  background: #c5a059;
  color: #000000;
}

.layout-principal {
  width: 100%;
}

.columnas-wrap {
  display: flex;
  gap: 30px;
  align-items: flex-start;
  width: 100%;
}

.productos-seccion {
  flex: 1;
  width: 100%;
  text-align: left;
}

.titulo-pizarra {
  color: #c5a059;
  text-transform: uppercase;
  letter-spacing: 3px;
  font-size: 1.8rem;
  margin: 0;
}

.subtitulo-pizarra {
  color: #888;
  font-size: 0.9rem;
  margin-top: 5px;
}

.divisor-mystic {
  width: 50px;
  height: 3px;
  background: #c5a059;
  margin: 20px 0;
}
.divisor-mystic.centro {
  margin: 20px auto;
}

.productos-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 20px;
  width: 100%;
}

.producto-card {
  background: #000000;
  border: 1px solid #222;
  border-radius: 8px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  transition: 0.2s;
}
.producto-card:hover {
  border-color: #c5a059;
}

.producto-info {
  padding: 20px;
  text-align: left;
}
.producto-info h3 {
  color: #fff;
  font-size: 1.05rem;
  margin: 0 0 10px 0;
  letter-spacing: 0.5px;
}
.precio {
  color: #c5a059;
  font-size: 1.3rem;
  font-weight: bold;
  margin: 0;
}
.stock {
  font-size: 0.75rem;
  color: #666;
  margin: 8px 0 0 0;
}
.sin-stock {
  color: #ff4444 !important;
  font-weight: bold;
}

.btn-agregar-producto {
  width: 100%;
  background: #1a1a1a;
  border: none;
  border-top: 1px solid #222;
  color: #c5a059;
  padding: 14px;
  font-family: "Roboto Mono", monospace;
  font-weight: bold;
  cursor: pointer;
  transition: 0.2s;
  letter-spacing: 0.5px;
}
.btn-agregar-producto:hover:not(:disabled) {
  background: #c5a059;
  color: #000000;
}
.btn-agregar-producto:disabled {
  color: #ff4444;
  background: #150505;
  border-top: 1px solid #301010;
  cursor: not-allowed;
}

.carrito-panel {
  flex: 0 0 340px;
  background: #111111;
  border: 1px solid #c5a059;
  padding: 30px 25px;
  border-radius: 12px;
  position: sticky;
  top: 100px;
  text-align: left;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.4);
}

.dorado-texto {
  color: #c5a059;
  font-size: 1.2rem;
  margin: 0 0 15px 0;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.divisor-rustico {
  width: 40px;
  height: 2px;
  background: #c5a059;
  margin-bottom: 20px;
}

.lista-carrito {
  list-style: none;
  padding: 0;
  margin: 0;
  max-height: 240px;
  overflow-y: auto;
}
.lista-carrito li {
  padding: 12px 0;
  border-bottom: 1px solid #222;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.item-linea {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.nombre-item {
  color: #fff;
  font-size: 0.9rem;
}
.precio-item {
  color: #c5a059;
  font-weight: bold;
  font-size: 0.95rem;
}

.btn-quitar-item {
  background: transparent;
  border: none;
  color: #ff4444;
  font-size: 0.75rem;
  cursor: pointer;
  text-align: left;
  padding: 0;
  font-family: "Roboto Mono", monospace;
}
.btn-quitar-item:hover {
  text-decoration: underline;
}

.total-seccion {
  margin-top: 25px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.total-label {
  color: #888;
  font-size: 0.85rem;
  font-weight: bold;
  letter-spacing: 1px;
  margin: 0;
}
.total-monto {
  font-size: 1.6rem;
  color: #fff;
  font-weight: bold;
  margin: 0;
}

.btn-confirmar-pedido {
  width: 100%;
  margin-top: 25px;
  background: #2a2a2a;
  border: 1px solid #c5a059;
  color: #ffffff;
  padding: 15px;
  font-family: "Roboto Mono", monospace;
  font-weight: bold;
  cursor: pointer;
  letter-spacing: 1px;
  transition: 0.3s;
}
.btn-confirmar-pedido:hover {
  background: #c5a059;
  color: #000000;
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
  max-width: 440px;
  text-align: center;
}

.error-borde {
  border-color: #ff4444 !important;
  box-shadow:
    0 10px 30px rgba(0, 0, 0, 0.8),
    0 0 15px rgba(255, 68, 68, 0.1) !important;
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

.icono-error-rojo {
  width: 60px;
  height: 60px;
  border: 2px solid #ff4444;
  color: #ff4444;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 20px auto;
  background: rgba(255, 68, 68, 0.05);
  box-shadow: 0 0 15px rgba(255, 68, 68, 0.2);
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
}

.titulo-modal-rojo {
  color: #ff4444;
  font-size: 1.3rem;
  letter-spacing: 3px;
  margin: 10px 0 15px 0;
  font-weight: bold;
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
.divisor-mystic-modal.un-rojo {
  background: rgba(255, 68, 68, 0.2);
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

@media (max-width: 950px) {
  .columnas-wrap {
    flex-direction: column;
    gap: 30px;
  }
  .carrito-panel {
    flex: none;
    width: 100%;
    position: static;
  }
  .posavasos-mesa {
    position: fixed;
    top: auto;
    bottom: 20px;
    right: 20px;
  }
}
</style>
