<template>
  <div class="admin-container">
    <div class="admin-header">
      <h1 class="titulo-brillante">PANEL DE CONTROL Y ADMINISTRACIÓN</h1>
    </div>

    <div class="forms-grid">
      <div class="card-mystic">
        <h2 class="subtitulo">Nuevo Producto</h2>
        <input
          v-model="nuevoProd.nombre"
          placeholder="Nombre"
          class="input-mystic"
        />
        <input
          v-model="nuevoProd.descripcion"
          placeholder="Descrpcion"
          class="input-mystic"
        />
        <input
          v-model="nuevoProd.precio"
          type="number"
          placeholder="Precio"
          class="input-mystic"
          @focus="limpiarSiCero(nuevoProd, 'precio')"
        />
        <input
          v-model="nuevoProd.stock"
          type="number"
          placeholder="Stock"
          class="input-mystic"
          @focus="limpiarSiCero(nuevoProd, 'stock')"
        />
        <button @click="crearProducto" class="btn-confirmar-pedido">
          CREAR PRODUCTO
        </button>
      </div>

      <div class="card-mystic form-crear-mesa">
        <h2 class="subtitulo">Nueva Mesa</h2>

        <div class="form-group-mystic">
          <input
            v-model="nuevaMesa.numero"
            type="number"
            placeholder="Numero de Mesa"
            class="input-mystic"
            @focus="limpiarSiCero(nuevaMesa, 'numero')"
          />
        </div>

        <div class="form-group-mystic">
          <input
            v-model="nuevaMesa.capacidad"
            type="number"
            min="1"
            placeholder="Cantidad de personas"
            class="input-mystic"
            @focus="limpiarSiCero(nuevaMesa, 'capacidad')"
          />
        </div>

        <div class="form-group-mystic checkbox-mystic-container">
          <label class="checkbox-mystic-label">
            <div class="checkbox-custom-wrapper">
              <input
                v-model="nuevaMesa.esta_libre"
                type="checkbox"
                class="checkbox-mystic-input"
              />
              <span class="checkbox-mystic-box"></span>
            </div>
            <span class="checkbox-mystic-text"
              >¿Iniciar como mesa ocupada?</span
            >
          </label>
        </div>

        <button @click="crearMesa" class="btn-confirmar-pedido">
          AGREGAR MESA
        </button>
      </div>
    </div>

    <div class="listas-paralelo-grid">
      <div class="card-mystic tabla-seccion">
        <h2 class="subtitulo">Lista de Productos</h2>
        <div class="productos-lista contenedor-scrollable">
          <div
            v-for="prod in productos"
            :key="prod.id"
            class="item-producto-admin"
          >
            <div v-if="productoEditandoId !== prod.id" class="info-prod">
              <div class="texto-prod-wrap">
                <span class="nombre">{{ prod.nombre }}</span>
                <span class="detalle"
                  >{{ formatearPrecio(prod.precio) }} | Stock:
                  {{ prod.stock }}</span
                >
              </div>
              <div class="acciones">
                <button
                  @click="iniciarEdicion(prod)"
                  class="btn-accion btn-editar"
                >
                  EDITAR
                </button>
                <button
                  @click="eliminarProducto(prod.id)"
                  class="btn-accion btn-eliminar"
                >
                  ELIMINAR
                </button>
              </div>
            </div>

            <div v-else class="form-edicion-linea">
              <input v-model="prodEditado.nombre" class="input-mystic mini" />
              <input
                v-model="prodEditado.descripcion"
                class="input-mystic mini"
              />
              <input
                v-model="prodEditado.precio"
                type="number"
                class="input-mystic mini"
                @focus="limpiarSiCero(prodEditado, 'precio')"
              />
              <input
                v-model="prodEditado.stock"
                type="number"
                class="input-mystic mini"
                @focus="limpiarSiCero(prodEditado, 'stock')"
              />
              <div class="acciones">
                <button
                  @click="guardarEdicion(prod.id)"
                  class="btn-accion btn-guardar"
                >
                  GUARDAR
                </button>
                <button
                  @click="cancelarEdicion"
                  class="btn-accion btn-cancelar"
                >
                  ✕
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="card-mystic tabla-seccion">
        <h2 class="subtitulo">Top 10 Productos Más Vendidos</h2>
        <div class="productos-lista contenedor-scrollable">
          <div v-if="productosMasVendidos.length === 0" class="sin-datos">
            Esperando registros de ventas...
          </div>
          <div
            v-for="(prod, index) in productosMasVendidos"
            :key="index"
            class="item-producto-admin top-vendido-fila"
          >
            <div class="info-prod">
              <div>
                <span class="medalla-ranking">{{ index + 1 }}°</span>
                <span class="nombre">{{ prod.nombre }}</span>
              </div>
              <span class="badge-ventas"
                >{{ prod.cantidadVendida }} unidades</span
              >
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="card-mystic tabla-seccion historial-bajar">
      <h2 class="subtitulo">Historial de Ventas (Pedidos Entregados)</h2>
      <div v-if="ventas.length === 0" class="sin-datos">
        No hay ventas registradas todavía.
      </div>
      <div v-else class="ventas-lista">
        <div v-for="pedido in ventas" :key="pedido.id" class="card-venta">
          <div class="venta-header">
            <span
              ><strong
                >Mesa {{ pedido.mesa?.numero || pedido.mesa }}</strong
              ></span
            >
            <span class="fecha">{{
              formatearFecha(pedido.fecha_creacion)
            }}</span>
            <span class="total-venta"
              >Total: {{ formatearPrecio(pedido.total) }}</span
            >
          </div>
          <ul class="venta-detalles">
            <li v-for="item in pedido.items" :key="item.id">
              {{ item.cantidad }}x {{ item.nombre_producto }}
            </li>
          </ul>
        </div>

        <div class="paginacion-container">
          <button
            @click="cambiarPagina(paginaActual - 1)"
            :disabled="paginaActual === 1"
            class="btn-paginacion"
          >
            « Anterior
          </button>
          <span class="info-paginas"
            >Página {{ paginaActual }} de {{ totalPaginas }}</span
          >
          <button
            @click="cambiarPagina(paginaActual + 1)"
            :disabled="paginaActual === totalPaginas"
            class="btn-paginacion"
          >
            Siguiente »
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import api from "../api.js";

const nuevoProd = ref({ nombre: "", precio: "", stock: "" });
const nuevaMesa = ref({ numero: null, capacidad: "", esta_libre: false });
const productos = ref([]);
const ventas = ref([]);
const productoEditandoId = ref(null);
const prodEditado = ref({ nombre: "", precio: 0, stock: 0 });
const paginaActual = ref(1);
const totalPaginas = ref(1);

const limpiarSiCero = (objeto, propiedad) => {
  if (objeto[propiedad] === 0 || objeto[propiedad] === "0") {
    objeto[propiedad] = "";
  }
};

const cargarDatos = async () => {
  try {
    const resProd = await api.get("productos/");
    productos.value = resProd.data.results
      ? resProd.data.results
      : resProd.data;
    const resPedidos = await api.get(`pedidos/?page=${paginaActual.value}`);

    let datosPedidos = [];
    if (resPedidos.data.results) {
      datosPedidos = resPedidos.data.results;
      totalPaginas.value = Math.ceil(resPedidos.data.count / 10) || 1;
    } else {
      datosPedidos = resPedidos.data;
      totalPaginas.value = 1;
    }

    const pedidosEntregados = datosPedidos.filter((p) => p.estado === "ENT");

    ventas.value = pedidosEntregados.sort((a, b) => {
      return new Date(b.fecha_creacion) - new Date(a.fecha_creacion);
    });
  } catch (e) {
    console.error("Error al cargar los datos:", e);
  }
};

const cambiarPagina = (nuevaPagina) => {
  if (nuevaPagina >= 1 && nuevaPagina <= totalPaginas.value) {
    paginaActual.value = nuevaPagina;
    cargarDatos();
  }
};

const productosMasVendidos = computed(() => {
  const mapeoProductos = {};
  ventas.value.forEach((pedido) => {
    if (pedido.items) {
      pedido.items.forEach((item) => {
        const nombre = item.nombre_producto;
        const cant = parseInt(item.cantidad) || 0;
        if (mapeoProductos[nombre]) {
          mapeoProductos[nombre] += cant;
        } else {
          mapeoProductos[nombre] = cant;
        }
      });
    }
  });

  return Object.keys(mapeoProductos)
    .map((nombre) => ({
      nombre: nombre,
      cantidadVendida: mapeoProductos[nombre],
    }))
    .sort((a, b) => b.cantidadVendida - a.cantidadVendida)
    .slice(0, 10);
});

const crearProducto = async () => {
  try {
    await api.post("productos/", nuevoProd.value);
    alert("Producto creado con éxito");
    nuevoProd.value = { nombre: "", precio: "", stock: "" };
    cargarDatos();
  } catch (e) {
    alert("Error al crear el producto");
  }
};

const crearMesa = async () => {
  try {
    await api.post("mesas/", nuevaMesa.value);
    alert("Mesa agregada con éxito");
    nuevaMesa.value = { numero: null, capacidad: 4, esta_libre: true };
    cargarDatos();
  } catch (e) {
    alert("Error al crear la mesa.");
  }
};

const iniciarEdicion = (producto) => {
  productoEditandoId.value = producto.id;
  prodEditado.value = { ...producto };
};

const cancelarEdicion = () => {
  productoEditandoId.value = null;
};

const guardarEdicion = async (id) => {
  try {
    await api.put(`productos/${id}/`, prodEditado.value);
    productoEditandoId.value = null;
    cargarDatos();
  } catch (e) {
    alert("Error al editar el producto");
  }
};

const eliminarProducto = async (id) => {
  if (confirm("¿Estas seguro de eliminar este producto?")) {
    try {
      await api.delete(`productos/${id}/`);
      cargarDatos();
    } catch (e) {
      alert("No se pudo eliminar el producto.");
    }
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

const formatearFecha = (fechaStr) => {
  if (!fechaStr) return "";
  const fecha = new Date(fechaStr);
  return (
    fecha.toLocaleDateString() +
    " " +
    fecha.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })
  );
};

onMounted(cargarDatos);
</script>

<style scoped>
.admin-container {
  padding: 40px;
  max-width: 1200px;
  margin: 0 auto;
  color: white;
  font-family: "Roboto Mono", monospace;
}
.admin-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 40px;
  border-bottom: 2px solid #c5a059;
  padding-bottom: 15px;
}
.titulo-brillante {
  color: #c5a059;
  text-transform: uppercase;
  letter-spacing: 4px;
  text-align: left;
  margin: 0;
}
.subtitulo {
  color: #c5a059;
  margin-bottom: 20px;
  font-size: 1.2rem;
  border-bottom: 1px solid #333;
  padding-bottom: 5px;
}
.forms-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 30px;
  margin-bottom: 40px;
}
.form-crear-mesa {
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.form-group-mystic {
  display: flex;
  flex-direction: column;
  gap: 4px;
  text-align: left;
}
.checkbox-mystic-container {
  margin-top: 10px;
  margin-bottom: 10px;
}
.checkbox-mystic-label {
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
  user-select: none;
}
.checkbox-custom-wrapper {
  position: relative;
  width: 20px;
  height: 20px;
}
.checkbox-mystic-input {
  position: absolute;
  opacity: 0;
  cursor: pointer;
  height: 0;
  width: 0;
}
.checkbox-mystic-box {
  position: absolute;
  top: 0;
  left: 0;
  height: 20px;
  width: 20px;
  background-color: #000;
  border: 1px solid #333;
  border-radius: 4px;
  transition: all 0.2s ease-in-out;
}
.checkbox-mystic-label:hover .checkbox-mystic-box {
  border-color: #c5a059;
  box-shadow: 0 0 8px rgba(197, 160, 89, 0.3);
}
.checkbox-mystic-input:checked ~ .checkbox-mystic-box {
  background-color: #c5a059;
  border-color: #c5a059;
  box-shadow: 0 0 10px rgba(197, 160, 89, 0.5);
}
.checkbox-mystic-box:after {
  content: "";
  position: absolute;
  display: none;
  left: 6px;
  top: 2px;
  width: 5px;
  height: 10px;
  border: solid black;
  border-width: 0 2px 2px 0;
  transform: rotate(45deg);
}
.checkbox-mystic-input:checked ~ .checkbox-mystic-box:after {
  display: block;
}
.checkbox-mystic-text {
  color: #cccccc;
  font-size: 0.95rem;
}
.listas-paralelo-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 30px;
}
.contenedor-scrollable {
  max-height: 400px;
  overflow-y: auto;
  padding-right: 5px;
}
.contenedor-scrollable::-webkit-scrollbar {
  width: 6px;
}
.contenedor-scrollable::-webkit-scrollbar-thumb {
  background: #c5a059;
  border-radius: 3px;
}
.contenedor-scrollable::-webkit-scrollbar-track {
  background: #000;
}
.card-mystic {
  background: #1a1a1a;
  border: 1px solid #c5a059;
  padding: 30px;
  border-radius: 12px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.5);
}
.tabla-seccion {
  margin-bottom: 40px;
}
.historial-bajar {
  margin-top: 10px;
}
.input-mystic {
  width: 100%;
  padding: 12px;
  margin: 8px 0;
  background: #000;
  border: 1px solid #333;
  color: white;
  border-radius: 6px;
  box-sizing: border-box;
  font-family: "Roboto Mono", monospace;
  transition: border-color 0.2s;
}
.input-mystic:focus {
  outline: none;
  border-color: #c5a059;
}
.input-mystic[type="number"]::-webkit-outer-spin-button,
.input-mystic[type="number"]::-webkit-inner-spin-button {
  -webkit-appearance: none;
  margin: 0;
}
.input-mystic[type="number"] {
  -moz-appearance: textfield;
  appearance: textfield;
}
.input-mystic.mini {
  width: 80px;
  margin: 0 2px;
  display: inline-block;
  padding: 6px;
  font-size: 0.8rem;
}
.btn-confirmar-pedido {
  width: 100%;
  background: #2a2a2a;
  border: 1px solid #c5a059;
  color: #ffffff;
  padding: 12px;
  cursor: pointer;
  transition: 0.3s;
  font-weight: bold;
  margin-top: 15px;
}
.btn-confirmar-pedido:hover {
  background: #c5a059;
  color: #000;
}
.item-producto-admin {
  border-bottom: 1px solid #222;
  padding: 12px 0;
}
.info-prod {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.texto-prod-wrap {
  display: flex;
  flex-direction: column;
  gap: 4px;
}
.form-edicion-linea {
  display: flex;
  gap: 5px;
  align-items: center;
}
.nombre {
  font-weight: bold;
  color: #fff;
}
.detalle {
  color: #888;
  font-size: 0.9rem;
}
.top-vendido-fila {
  padding: 15px 0;
}
.medalla-ranking {
  color: #c5a059;
  font-weight: bold;
  margin-right: 12px;
  font-size: 1.1rem;
}
.badge-ventas {
  background: #000;
  border: 1px solid #333;
  padding: 4px 10px;
  border-radius: 20px;
  font-size: 0.8rem;
  color: #c5a059;
}
.acciones {
  display: flex;
  gap: 6px;
}
.btn-accion {
  padding: 6px 10px;
  cursor: pointer;
  font-size: 0.72rem;
  font-weight: bold;
  background: #2a2a2a;
  border: 1px solid #c5a059;
  color: #ffffff;
  transition: 0.2s;
}
.btn-accion:hover {
  background: #c5a059;
  color: #000000;
}
.btn-eliminar {
  color: #888888;
  border-color: #333333;
}
.btn-eliminar:hover {
  color: #c5a059;
  background: #000000;
  border-color: #c5a059;
  box-shadow: 0 0 8px rgba(197, 160, 89, 0.4);
}
.sin-datos {
  color: #666;
  font-style: italic;
  text-align: center;
  padding: 20px;
}
.card-venta {
  background: #2a2a2a;
  border-left: 3px solid #c5a059;
  padding: 15px;
  margin-bottom: 15px;
  border-radius: 4px;
}
.venta-header {
  display: flex;
  justify-content: space-between;
  color: #cccccc;
  font-size: 0.95rem;
  margin-bottom: 8px;
}
.fecha {
  color: #777777;
}
.total-venta {
  color: #c5a059;
  font-weight: bold;
}
.venta-detalles {
  list-style-type: none;
  padding-left: 10px;
  font-size: 0.9rem;
  color: #bbbbbb;
}
.paginacion-container {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 20px;
  margin-top: 25px;
  padding-top: 15px;
  border-top: 1px solid #222;
}
.info-paginas {
  color: #888888;
  font-size: 0.9rem;
}
.btn-paginacion {
  background: #000;
  border: 1px solid #333;
  color: #c5a059;
  padding: 8px 16px;
  cursor: pointer;
  font-family: "Roboto Mono", monospace;
  font-weight: bold;
  border-radius: 4px;
  transition: all 0.2s;
}
.btn-paginacion:hover:not(:disabled) {
  border-color: #c5a059;
  box-shadow: 0 0 8px rgba(197, 160, 89, 0.3);
}
.btn-paginacion:disabled {
  color: #444;
  border-color: #222;
  cursor: not-allowed;
  opacity: 0.5;
}

@media (max-width: 900px) {
  .forms-grid,
  .listas-paralelo-grid {
    grid-template-columns: 1fr;
  }
  .admin-header {
    flex-direction: column;
    gap: 15px;
    text-align: center;
  }
  .titulo-brillante {
    text-align: center;
  }
}
</style>
