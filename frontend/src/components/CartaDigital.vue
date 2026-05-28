<template>
  <div class="carta-container">
    <div v-if="carritoStore.mesaSeleccionada" class="posavasos-mesa">
      <div class="mesa-info">
        <span class="label">MESA</span>
        <span class="numero">{{ carritoStore.mesaId }}</span>
      </div>
      <button
        @click="carritoStore.resetMesa()"
        class="btn-cambiar-mesa"
        title="Cambiar Mesa"
      >
        ✎
      </button>
    </div>

    <div v-if="!carritoStore.mesaSeleccionada" class="pantalla-inicio-centrada">
      <div class="card-mesa-selector">
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
                <p class="precio">${{ p.precio }}</p>
                <p class="stock" :class="{ 'sin-stock': p.stock <= 0 }">
                  {{ p.stock > 0 ? "Disponible" : "Sin Stock" }}
                </p>
              </div>
              <button
                @click="carritoStore.agregarProducto(p)"
                :disabled="p.stock <= 0"
                class="btn-agregar-producto"
              >
                {{ p.stock > 0 ? "+ AGREGAR" : "AGOTADO" }}
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
                <span class="precio-item">${{ item.precio }}</span>
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
            <p class="total-monto">${{ carritoStore.totalPedido }}</p>
          </div>

          <button @click="enviarPedidoFinal" class="btn-confirmar-pedido">
            ENVIAR A COCINA
          </button>
        </aside>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";
import { useCarritoStore } from "../stores/carritoStore";

const carritoStore = useCarritoStore();
const productos = ref([]);

const fetchProductos = async () => {
  try {
    const response = await axios.get("http://localhost:8000/api/productos/");
    productos.value = response.data;
  } catch (error) {
    console.error("Error conectando con Django");
  }
};

const enviarPedidoFinal = async () => {
  const payload = {
    mesa: carritoStore.mesaId,
    items: carritoStore.items.map((item) => ({
      producto: item.id,
      cantidad: 1,
      observacion: "",
    })),
  };

  try {
    const res = await axios.post("http://localhost:8000/api/pedidos/", payload);
    alert(`¡Pedido #${res.data.id} enviado con éxito!`);
    carritoStore.limpiarCarrito();
    await fetchProductos();
  } catch (error) {
    alert("Error enviando pedido");
  }
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
  width: 75px;
  height: 75px;
  border-radius: 50%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  box-shadow:
    0 4px 15px rgba(0, 0, 0, 0.6),
    0 0 10px rgba(197, 160, 89, 0.2);
  z-index: 10;
}

.mesa-info {
  text-align: center;
  line-height: 1.1;
}
.mesa-info .label {
  font-size: 0.55rem;
  color: #888;
  display: block;
  font-weight: bold;
  letter-spacing: 1px;
}
.mesa-info .numero {
  font-size: 1.6rem;
  color: #c5a059;
  font-weight: bold;
}

.btn-cambiar-mesa {
  position: absolute;
  bottom: -2px;
  right: -2px;
  background: #c5a059;
  border: 1px solid #111;
  color: #000;
  border-radius: 50%;
  width: 26px;
  height: 26px;
  cursor: pointer;
  font-size: 0.85rem;
  font-weight: bold;
  display: flex;
  justify-content: center;
  align-items: center;
  transition: 0.2s;
}
.btn-cambiar-mesa:hover {
  background: #ffffff;
  transform: scale(1.1);
}

.pantalla-inicio-centrada {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 60vh;
  width: 100%;
}

.card-mesa-selector {
  background: #1a1a1a;
  padding: 45px;
  border-radius: 15px;
  border: 1px solid #c5a059;
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
}

.btn-agregar-producto {
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
  color: #444;
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
}
</style>
