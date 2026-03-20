<template>
  <div class="carta-container">
    <h1>🍺 Mi Cervecería - Carta Digital</h1>

    <div v-if="!mesaSeleccionada" class="pantalla-inicio">
      <h2>¡Bienvenido! Seleccioná tu mesa para empezar:</h2>
      <div class="mesas-grid">
        <button v-for="n in [1, 2, 3]" :key="n" @click="seleccionarMesa(n)" class="btn-mesa">
          Mesa {{ n }}
        </button>
      </div>
    </div>

    <div v-else class="layout-principal">
      <div class="header-mesa">
        <p>Estas pidiendo para la <strong>Mesa {{ mesaId }}</strong></p>
        <button @click="mesaSeleccionada = false" class="btn-cambiar">Cambiar Mesa</button>
      </div>

      <div class="main-content">
        <section class="productos-grid">
          <div v-for="p in productos" :key="p.id" class="producto-card">
            <h3>{{ p.nombre }}</h3>
            <p class="precio">${{ p.precio }}</p>
            <p class="stock">Stock: {{ p.stock }}</p>
            <button 
              @click="agregarAlCarrito(p)" 
              :disabled="p.stock <= 0"
              class="btn-agregar"
            >
              {{ p.stock > 0 ? 'Agregar' : 'Sin Stock' }}
            </button>
          </div>
        </section>

        <aside v-if="carrito.length > 0" class="carrito-panel">
          <h2>🛒 Tu Pedido</h2>
          <ul>
            <li v-for="(item, index) in carrito" :key="index">
              {{ item.nombre }} - ${{ item.precio }}
              <button @click="quitarDelCarrito(index)" class="btn-quitar">x</button>
            </li>
          </ul>
          <hr>
          <p class="total">Total: ${{ calcularTotal() }}</p>
          <button @click="confirmarPedido" class="btn-confirmar">🚀 ENVIAR PEDIDO A COCINA</button>
        </aside>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const productos = ref([])
const carrito = ref([])
const loading = ref(true)
const mesaId = ref(null)
const mesaSeleccionada = ref(false)

const seleccionarMesa = (n) => {
  mesaId.value = n
  mesaSeleccionada.value = true
}

const fetchProductos = async () => {
  try {
    const response = await axios.get('http://localhost:8000/api/productos/')
    productos.value = response.data
  } catch (error) {
    alert("Error conectando con Django")
  } finally {
    loading.value = false
  }
}

const agregarAlCarrito = (p) => {
  carrito.value.push({ id: p.id, nombre: p.nombre, precio: p.precio })
}

const quitarDelCarrito = (i) => {
  carrito.value.splice(i, 1)
}

const calcularTotal = () => {
  return carrito.value.reduce((acc, item) => acc + parseFloat(item.precio), 0).toFixed(2)
}

const confirmarPedido = async () => {
  const payload = {
    mesa: mesaId.value,
    items: carrito.value.map(item => ({
      producto: item.id,
      cantidad: 1,
      observacion: ""
    }))
  }

  try {
    const res = await axios.post('http://localhost:8000/api/pedidos/', payload)
    alert(`✅ ¡Pedido #${res.data.id} enviado!`)
    carrito.value = [] // Limpia el carrito después de enviar
    await fetchProductos() // RECARGA EL STOCK DESDE LA BASE DE DATOS
  } catch (error) {
    alert("Error: " + (error.response?.data?.error || "No se pudo enviar"))
  }
}

onMounted(fetchProductos)
</script>

<style scoped>
.carta-container { color: white; padding: 20px; text-align: center; }
.pantalla-inicio { margin-top: 50px; }
.mesas-grid { display: flex; justify-content: center; gap: 20px; margin-top: 20px; }
.btn-mesa { padding: 20px 40px; font-size: 1.5rem; cursor: pointer; background: #3498db; color: white; border: none; border-radius: 10px; }

.header-mesa { background: #333; padding: 10px; margin-bottom: 20px; border-radius: 10px; display: flex; justify-content: space-around; align-items: center; }
.main-content { display: flex; gap: 20px; text-align: left; }
.productos-grid { flex: 2; display: grid; grid-template-columns: repeat(auto-fill, minmax(180px, 1fr)); gap: 15px; }
.producto-card { background: white; color: #333; padding: 15px; border-radius: 10px; text-align: center; }

.carrito-panel { flex: 1; background: #222; padding: 20px; border-radius: 10px; border: 1px solid #444; }
.btn-confirmar { background: #2ecc71; color: white; border: none; padding: 15px; width: 100%; cursor: pointer; font-weight: bold; border-radius: 5px; }
.btn-cambiar { background: #e74c3c; color: white; border: none; padding: 5px 10px; border-radius: 5px; cursor: pointer; }
</style>