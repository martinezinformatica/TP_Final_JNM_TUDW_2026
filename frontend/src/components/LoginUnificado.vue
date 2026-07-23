<template>
  <div class="card-mystic-login">
    <template v-if="!authStore.esperandoCodigo && !authStore.esperandoPassword">
      <h2 class="subtitulo-login">INGRESO</h2>
      <p class="texto-login">Ingresa tu telefono para continuar.</p>
      <input
        v-model="telefonoInput"
        type="tel"
        placeholder="Ej: 2984123456"
        class="input-login"
        @keyup.enter="iniciarLogin"
      />
      <div v-if="!esNumeroDePersonal" class="contenedor-mesa-select">
        <p class="texto-login">¿En que mesa estas?</p>
        <select v-model="mesaSeleccionada" class="select-login">
          <option value="" disabled>Selecciona tu mesa</option>
          <option v-for="mesa in mesasLibres" :key="mesa.id" :value="mesa.id">
            Mesa {{ mesa.numero }}
          </option>
        </select>
        <p v-if="cargandoMesas" class="texto-cargando-mesas">
          Buscando mesas disponibles...
        </p>
      </div>

      <p v-if="errorMsg" class="error-msg">{{ errorMsg }}</p>

      <button @click="iniciarLogin" :disabled="cargando" class="btn-login">
        {{ cargando ? "VERIFICANDO..." : "CONTINUAR" }}
      </button>
    </template>
    <template v-else-if="authStore.esperandoCodigo">
      <h2 class="subtitulo-login">CODIGO WHATSAPP</h2>
      <p class="texto-login">
        Ingresa el codigo de 8 digitos enviado al Wathsapp
        <strong class="telefono-highlight">{{ authStore.userTelefono }}</strong
        >.
      </p>
      <input
        v-model="codigoInput"
        type="text"
        maxlength="8"
        placeholder="Codigo de 8 digitos"
        class="input-login"
        @keyup.enter="verificarCodigo"
      />
      <p v-if="errorMsg" class="error-msg">{{ errorMsg }}</p>

      <button @click="verificarCodigo" :disabled="cargando" class="btn-login">
        {{ cargando ? "VERIFICANDO..." : "VERIFICAR CODIGO" }}
      </button>

      <button @click="volverAtras" class="btn-login btn-volver">VOLVER</button>
    </template>
    <template v-else-if="authStore.esperandoPassword">
      <h2 class="subtitulo-login">
        {{
          authStore.rolDetectado === "admin"
            ? "BUEN DIA ADMINISTRADOR"
            : "BUEN DIA COCINERO"
        }}
      </h2>
      <p class="texto-login">Ingresa tu contraseña para continuar.</p>

      <input
        v-model="passwordInput"
        type="password"
        placeholder="Contraseña"
        class="input-login"
        @keyup.enter="verificarPassword"
      />

      <p v-if="errorMsg" class="error-msg">{{ errorMsg }}</p>

      <button @click="verificarPassword" :disabled="cargando" class="btn-login">
        {{ cargando ? "VERIFICANDO..." : "INGRESAR" }}
      </button>

      <button @click="volverAtras" class="btn-login btn-volver">VOLVER</button>
    </template>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick } from "vue";
import { useAuthStore } from "../stores/auth.js";
import { useCarritoStore } from "../stores/carritoStore.js";
import api from "../api.js";

const authStore = useAuthStore();
const carritoStore = useCarritoStore();
const emit = defineEmits(["navegar"]);

const telefonoInput = ref("");
const codigoInput = ref("");
const passwordInput = ref("");
const cargando = ref(false);
const errorMsg = ref("");
const mesasLibres = ref([]);
const mesaSeleccionada = ref("");
const cargandoMesas = ref(false);
const NUMEROS_PERSONAL = ["2984333444", "2984111222"];

const esNumeroDePersonal = computed(() => {
  const telLimpio = telefonoInput.value.replace(/\s+/g, "").trim();
  return NUMEROS_PERSONAL.includes(telLimpio);
});

const obtenerMesasLibres = async () => {
  cargandoMesas.value = true;
  try {
    const response = await api.get("mesas/");
    mesasLibres.value = response.data.filter((mesa) => mesa.esta_libre);
  } catch (e) {
    console.error("Error al cargar mesas:", e);
  } finally {
    cargandoMesas.value = false;
  }
};

onMounted(() => {
  obtenerMesasLibres();
});

const iniciarLogin = async () => {
  errorMsg.value = "";
  const tel = telefonoInput.value.trim();

  if (!tel) {
    errorMsg.value = "Ingresa un numero de telefono.";
    return;
  }

  if (!esNumeroDePersonal.value && !mesaSeleccionada.value) {
    errorMsg.value = "Por favor, elegi tu mesa.";
    return;
  }

  cargando.value = true;
  try {
    await authStore.iniciarLogin(tel);
  } catch {
    errorMsg.value = "Error al conectar. Intenta de nuevo.";
  } finally {
    cargando.value = false;
  }
};

const verificarCodigo = async () => {
  errorMsg.value = "";
  const cod = codigoInput.value.trim();

  if (cod.length !== 8) {
    errorMsg.value = "El codigo debe tener 8 digitos.";
    return;
  }

  cargando.value = true;
  try {
    await authStore.verificarCodigoCliente(cod);

    if (!esNumeroDePersonal.value && mesaSeleccionada.value) {
      console.log(mesaSeleccionada.value);

      await api.patch(`mesas/${mesaSeleccionada.value}/`, {
        esta_libre: false,
        cliente_telefono: authStore.userTelefono,
      });

      localStorage.setItem("mesa_id", mesaSeleccionada.value);
      carritoStore.setMesa(Number(mesaSeleccionada.value));
    }
  } catch (err) {
    console.error("Error al ocupar la mesa:", err);
    errorMsg.value = "Código incorrecto o vencido.";
  } finally {
    cargando.value = false;
  }
};

const verificarPassword = async () => {
  errorMsg.value = "";
  const pass = passwordInput.value;

  if (!pass) {
    errorMsg.value = "Ingresa tu contraseña.";
    return;
  }

  cargando.value = true;
  try {
    await authStore.verificarPasswordPersonal(pass);

    await nextTick();
    if (authStore.isAdmin) {
      emit("navegar", "admin");
    } else if (authStore.isCocina) {
      emit("navegar", "cocina");
    }
  } catch {
    errorMsg.value = "Contraseña incorrecta.";
  } finally {
    cargando.value = false;
  }
};

const volverAtras = () => {
  errorMsg.value = "";
  mesaSeleccionada.value = "";
  authStore.resetearLogin();
};
</script>

<style scoped>
.texto-login {
  color: #aaa;
  font-size: 0.9rem;
  margin-top: 15px;
  margin-bottom: 5px;
  line-height: 1.5;
}

.telefono-highlight {
  color: #c5a059;
}

.error-msg {
  color: #e05555;
  font-size: 0.85rem;
  margin: 12px 0 2px;
  font-family: "Roboto Mono", monospace;
}

.contenedor-mesa-select {
  margin-top: 15px;
  text-align: center;
}

.select-login {
  width: 100%;
  padding: 12px;
  margin-top: 8px;
  background: #000;
  border: 1px solid #333;
  color: #c5a059;
  border-radius: 6px;
  box-sizing: border-box;
  font-family: "Roboto Mono", monospace;
  text-align-last: center;
  cursor: pointer;
  transition: border-color 0.3s;
}

.select-login:focus {
  outline: none;
  border-color: #c5a059;
}

.texto-cargando-mesas {
  font-size: 0.75rem;
  color: #666;
  margin-top: 5px;
}
</style>
