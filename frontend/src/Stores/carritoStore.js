import { defineStore } from 'pinia'

export const useCarritoStore = defineStore('carrito', {
  state: () => ({
    mesaId: null,
    mesaSeleccionada: false,
    items: []
  }),
  actions: {
    setMesa(numero) {
      this.mesaId = numero
      this.mesaSeleccionada = true
    },
    resetMesa() {
      this.mesaId = null
      this.mesaSeleccionada = false
      this.items = [] 
    },
    agregarProducto(producto) {
      this.items.push({ 
        id: producto.id, 
        nombre: producto.nombre, 
        precio: parseFloat(producto.precio) 
      })
    },
    quitarProducto(index) {
      this.items.splice(index, 1)
    },
    limpiarCarrito() {
      this.items = []
    }
  },
  getters: {
    totalPedido: (state) => {
      return state.items.reduce((acc, item) => acc + item.precio, 0).toFixed(2)
    },
    cantidadItems: (state) => state.items.length
  }
})