<template>
  <div class="nosotros-container">
    <div class="card-horizontal-nosotros">
      <div class="col-texto">
        <h1>Nosotros</h1>
        <p class="subtitulo">Conocé la historia detrás de la mística.</p>
        <div class="divisor-mystic"></div>

        <div class="bloque-historia">
          <p>
            En el corazón de General Roca (Fiske Menuco), nació
            <strong>Natural Mystic</strong> como un refugio para los amantes de
            la buena cerveza artesanal y las charlas eternas. No somos solo un
            bar; somos un punto de encuentro donde se cruzan la cultura local,
            la música con identidad y las mejores recetas de la zona.
          </p>
          <p>
            Nuestra propuesta combina pizarras con estilos de cerveza
            minuciosamente seleccionados y una cocina rústica pero con un
            carácter único, pensada para acompañar cada pinta de la mejor
            manera.
          </p>
        </div>
      </div>

      <div class="col-pilares">
        <h2 class="dorado-texto">Nuestra Esencia</h2>

        <div class="pilar-item">
          <span class="pilar-icono"></span>
          <div class="pilar-info">
            <strong>Cerveza Artesanal</strong>
            <p>
              Variedades locales y de la región seleccionadas por su pureza y
              sabor.
            </p>
          </div>
        </div>

        <div class="pilar-item">
          <span class="pilar-icono"></span>
          <div class="pilar-info">
            <strong>Música & Cultura</strong>
            <p>
              Un ambiente sonoro diseñado para desconectar y disfrutar del
              momento.
            </p>
          </div>
        </div>

        <div class="pilar-item">
          <span class="pilar-icono"></span>
          <div class="pilar-info">
            <strong>La Mística</strong>
            <p>
              Esa atmósfera oscura, dorada y rústica donde el tiempo pasa más
              lento.
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.nosotros-container {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 40px 20px;
  font-family: "Roboto Mono", monospace;
  color: white;
}

.card-horizontal-nosotros {
  display: flex;
  flex-wrap: wrap;
  max-width: 1000px;
  width: 100%;
  background: #1a1a1a;
  border: 1px solid #c5a059;
  border-radius: 15px;
  overflow: hidden;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.5);
}

.col-texto {
  flex: 1.2;
  padding: 40px;
  text-align: left;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.col-pilares {
  flex: 1;
  padding: 40px;
  background: #111;
  border-left: 1px solid #333;
  text-align: left;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
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
  letter-spacing: 1px;
}

.divisor-mystic {
  width: 50px;
  height: 3px;
  background: #c5a059;
  margin: 20px 0;
}

.bloque-historia p {
  color: #ccc;
  line-height: 1.6;
  font-size: 0.95rem;
  margin-bottom: 20px;
}

.bloque-historia strong {
  color: #c5a059;
}

.btn-mystic-link {
  display: block;
  text-align: center;
  text-decoration: none;
  background: #2a2a2a;
  border: 1px solid #c5a059;
  color: #ffffff;
  padding: 15px;
  font-family: "Roboto Mono", monospace;
  font-weight: bold;
  cursor: pointer;
  transition: 0.3s;
  letter-spacing: 1px;
  margin-top: 10px;
}

.btn-mystic-link:hover {
  background: #c5a059;
  color: #000000;
}

.pilar-item {
  display: flex;
  gap: 15px;
  margin-bottom: 25px;
  align-items: flex-start;
}

.pilar-icono {
  font-size: 1.5rem;
  background: #c5a059;
  padding: 8px;
  border-radius: 6px;
  border: 1px solid #333;
}

.pilar-info strong {
  color: #fff;
  font-size: 0.95rem;
  display: block;
  margin-bottom: 5px;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.pilar-info p {
  margin: 0;
  color: #888;
  font-size: 0.85rem;
  line-height: 1.4;
}

@media (max-width: 850px) {
  .card-horizontal-nosotros {
    flex-direction: column;
  }
  .col-pilares {
    border-left: none;
    border-top: 1px solid #333;
    gap: 20px;
  }
}
</style>
