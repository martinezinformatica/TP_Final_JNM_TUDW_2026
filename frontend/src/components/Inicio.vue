<template>
  <div class="inicio-container">
    <div class="card-horizontal-inicio">
      <div class="col-foto">
        <img src="../assets/patio_mystic.jpg" alt="Natural Mystic Cervecería" />
        <div class="borde-decorativo"></div>
      </div>

      <div class="col-texto">
        <div class="encabezado">
          <h1>Bienvenidos</h1>
          <p class="subtitulo">NATURAL MYSTIC</p>
          <div class="divisor-mystic"></div>
        </div>

        <div class="bloque-contenido">
          <p>
            Donde la pureza del agua y la fuerza del grano se encuentran en cada
            pinta.
          </p>
          <p>
            Disfrutá de nuestra selección artesanal minuciosamente cuidada,
            directo en tu mesa.
          </p>
        </div>

        <div class="cierre-mystic">
          <h3 class="eslogan">"Artesanal por naturaleza."</h3>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.inicio-container {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 60px 20px;
  font-family: "Roboto Mono", monospace;
  color: white;
  width: 100%;
}

.card-horizontal-inicio {
  display: flex;
  flex-wrap: wrap;
  max-width: 850px;
  width: 100%;
  background: #1a1a1a;
  border: 1px solid #c5a059;
  border-radius: 15px;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.6);
}

.col-foto {
  flex: 0 0 350px;
  position: relative;
  max-height: 450px;
  overflow: hidden;
}

.col-foto img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.borde-decorativo {
  position: absolute;
  top: 15px;
  left: 15px;
  right: 15px;
  bottom: 15px;
  border: 1px dashed #c5a059;
  opacity: 0.2;
  pointer-events: none;
}

.col-texto {
  flex: 1;
  padding: 45px;
  text-align: left;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  background: #111111;
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
  font-size: 0.85rem;
  margin-top: 5px;
  letter-spacing: 1px;
}

.divisor-mystic {
  width: 50px;
  height: 3px;
  background: #c5a059;
  margin: 20px 0;
}

.bloque-contenido p {
  color: #ccc;
  line-height: 1.6;
  font-size: 0.95rem;
  margin-bottom: 15px;
}

.eslogan {
  font-style: italic;
  color: #c5a059;
  margin: 0;
  font-size: 1.05rem;
  letter-spacing: 0.5px;
}

@media (max-width: 750px) {
  .card-horizontal-inicio {
    flex-direction: column;
  }
  .col-foto {
    flex: none;
    width: 100%;
    height: 220px;
  }
  .col-texto {
    padding: 30px 25px;
  }
}
</style>
