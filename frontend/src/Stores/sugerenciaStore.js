import { defineStore } from 'pinia'

export const useSugerenciaStore = defineStore('sugerencia', {
  state: () => ({
    comentarios: [
      { calificacion: 4, texto: 'La mejor IPA de Roca.' },
      { calificacion: 3, texto: 'Muy buena atención.' },
      { calificacion: 2, texto: 'Las papas estaban un poco frías.' }
    ]
  }),
  actions: {
    agregarSugerencia(nueva) {
      this.comentarios.push(nueva)
    }
  },
  getters: {   
    ultimasTres: (state) => state.comentarios.slice(-3).reverse()
  }
})