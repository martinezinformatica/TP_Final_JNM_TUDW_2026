<template>
  <div class="card-mystic-login">
    <template v-if="!authStore.esperandoCodigo && !authStore.esperandoPassword">
      <h2 class="subtitulo-login">INGRESO</h2>
      <p class="texto-login">Ingresá tu número de teléfono para continuar.</p>

      <input
        v-model="telefonoInput"
        type="tel"
        placeholder="Ej: 2984123456"
        class="input-login"
        @keyup.enter="iniciarLogin"
      />

      <p v-if="errorMsg" class="error-msg">{{ errorMsg }}</p>

      <button @click="iniciarLogin" class="btn-login">
        {{ cargando ? "VERIFICANDO..." : "CONTINUAR" }}
      </button>
    </template>

    <template v-else-if="authStore.esperandoCodigo">
      <h2 class="subtitulo-login">CÓDIGO WHATSAPP</h2>
      <p class="texto-login">
        Ingresá el código de 8 dígitos enviado al número
        <strong class="telefono-highlight">{{ authStore.userTelefono }}</strong
        >.
      </p>

      <input
        v-model="codigoInput"
        type="text"
        maxlength="8"
        placeholder="Código de 8 dígitos"
        class="input-login"
        @keyup.enter="verificarCodigo"
      />

      <p v-if="errorMsg" class="error-msg">{{ errorMsg }}</p>

      <button @click="verificarCodigo" class="btn-login">
        {{ cargando ? "VERIFICANDO..." : "VERIFICAR CÓDIGO" }}
      </button>

      <button @click="authStore.resetearLogin" class="btn-login btn-volver">
        ← VOLVER
      </button>
    </template>

    <template v-else-if="authStore.esperandoPassword">
      <h2 class="subtitulo-login">
        {{
          authStore.rolDetectado === "admin"
            ? "BUEN DÍA ADMINISTRADOR"
            : "BUEN DÍA COCINERO"
        }}
      </h2>
      <p class="texto-login">Ingresá tu contraseña para continuar.</p>

      <input
        v-model="passwordInput"
        type="password"
        placeholder="Contraseña"
        class="input-login"
        @keyup.enter="verificarPassword"
      />

      <p v-if="errorMsg" class="error-msg">{{ errorMsg }}</p>

      <button @click="verificarPassword" class="btn-login">
        {{ cargando ? "VERIFICANDO..." : "INGRESAR" }}
      </button>

      <button @click="authStore.resetearLogin" class="btn-login btn-volver">
        ← VOLVER
      </button>
    </template>
  </div>
</template>

<script setup>
import { ref, nextTick } from "vue";
import { useAuthStore } from "../stores/auth.js";

const authStore = useAuthStore();
const emit = defineEmits(["navegar"]);

const telefonoInput = ref("");
const codigoInput = ref("");
const passwordInput = ref("");
const cargando = ref(false);
const errorMsg = ref("");

// Paso 1: detectar tipo de usuario
const iniciarLogin = async () => {
  errorMsg.value = "";
  const tel = telefonoInput.value.trim();

  if (!tel) {
    errorMsg.value = "Ingresá un número de teléfono.";
    return;
  }

  cargando.value = true;
  try {
    await authStore.iniciarLogin(tel);
  } catch {
    errorMsg.value = "Error al conectar. Intentá de nuevo.";
  } finally {
    cargando.value = false;
  }
};

// Paso 2a: código WhatsApp para clientes
const verificarCodigo = async () => {
  errorMsg.value = "";
  const cod = codigoInput.value.trim();

  if (cod.length !== 8) {
    errorMsg.value = "El código debe tener exactamente 8 dígitos.";
    return;
  }

  cargando.value = true;
  try {
    await authStore.verificarCodigoCliente(cod);
  } catch {
    errorMsg.value = "Código incorrecto o vencido.";
  } finally {
    cargando.value = false;
  }
};

// Paso 2b: contraseña para cocinero y admin
const verificarPassword = async () => {
  errorMsg.value = "";
  const pass = passwordInput.value;

  if (!pass) {
    errorMsg.value = "Ingresá tu contraseña.";
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
</script>

<style scoped>
.texto-login {
  color: #aaa;
  font-size: 0.9rem;
  margin-bottom: 10px;
  line-height: 1.5;
}

.telefono-highlight {
  color: #c5a059;
}

.error-msg {
  color: #e05555;
  font-size: 0.85rem;
  margin: 6px 0 2px;
  font-family: "Roboto Mono", monospace;
}
</style>
