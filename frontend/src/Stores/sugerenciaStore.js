import { defineStore } from 'pinia'

export const useSugerenciaStore = defineStore('sugerencia', {
  state: () => ({
    comentarios: [
      { calificacion: '😍', texto: 'La mejor IPA de Roca.' },
      { calificacion: '🙂', texto: 'Muy buena atención.' },
      { calificacion: '😐', texto: 'Las papas estaban un poco frías.' }
    ]
  }),
  actions: {
    agregarSugerencia(nueva) {
      this.comentarios.push(nueva)
    }
  },
  getters: {
    ultimasTres: (state) => {
           return state.comentarios.slice(-3).reverse()
    }
  }
})