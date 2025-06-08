<template>
  <div class="container">
    <div class="d-flex justify-content-center align-items-center min-vh-100">
      <div class="login-box">
        <div class="card shadow-lg p-4" style="max-width: 600px; width: 100%;">
          <div class="card-body">
            <!-- Fila superior con enlace a la izquierda y una imagen a la derecha -->
            <div class="d-flex justify-content-between align-items-center mb-4">
              <img src="@/assets/img/login/logo.png" alt="Imagen" class="img-fluid"
                style="max-width: 100%; height: auto;" />
            </div>

            <!-- Mostrar mensaje de error -->
            <div v-if="errorMessage" class="alert alert-danger text-center mb-4" role="alert">
              {{ errorMessage }}
            </div>

            <form @submit.prevent="handleSubmit">
              <div class="mb-3">
                <label for="username" class="form-label">Nombre de usuario</label>
                <div class="input-group">
                  <span class="input-group-text">
                    <i class="fas fa-user"></i>
                  </span>
                  <input type="text" id="username" v-model="username" @input="handleUsernameInput" class="form-control"
                    placeholder="Usuario" required />
                </div>
              </div>
              <div class="mb-3">
                <label for="password" class="form-label">Contraseña</label>
                <div class="input-group">
                  <span class="input-group-text">
                    <i class="fas fa-lock"></i>
                  </span>
                  <input type="password" id="password" v-model="password" class="form-control" placeholder="Contraseña"
                    required />
                </div>
              </div>
              <div class="text-center">
                <button type="submit" class="btn btn-primary custom-blue">
                  <i class="fas fa-sign-in-alt"></i> Ingresar
                </button>
              </div>
            </form>
          </div>
          <!-- Fila inferior con borde morado -->
          <div class="card-footer border-top text-center">
            <small>Aplicativo CTL v.0.1</small>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>


<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { api, getAuthToken } from '@/components/services/auth_axios';
import { toLowerCase } from '@/assets/js/validation.js'

const username = ref('')
const password = ref('')
const errorMessage = ref('')
const router = useRouter()

// Maneja la entrada del nombre de usuario
const handleUsernameInput = (event) => {
  username.value = toLowerCase(event.target.value)
}

const handleSubmit = async () => {
  try {
    const response = await api.post('user/login/', {
      username: username.value,
      password: password.value,
    });

    // Validar que haya un token de acceso antes de redirigir
    const { access, refresh, is_superuser, is_staff, group } = response.data;

    if (access) {
      localStorage.setItem('auth_token', access);
      localStorage.setItem('refreshToken', refresh || ''); // Manejo opcional de refresh token
      localStorage.setItem('is_superuser', is_superuser ? 'true' : 'false');
      localStorage.setItem('is_staff', is_staff ? 'true' : 'false');
      localStorage.setItem('group', group || 'No definido');

      // Si todo está correcto, redirigir al dashboard
      router.push('/modulos/materiales');
    } else {
      // Manejo del error si no se recibe el token
      errorMessage.value = 'No se recibió token de acceso.';
    }
  } catch (error) {
    // Si hay error en la autenticación, mostrar mensaje y no redirigir
    if (error.response && error.response.data && error.response.data.detail) {
      errorMessage.value = error.response.data.detail;
    } else {
      errorMessage.value = 'Servidor deshabilitado. Por favor contactar con el ingeniero de sistemas.';
    }
    console.error('Error en la autenticación:', error);
  }
};



</script>


<style scoped>
/* Estilo para el borde morado en la parte inferior de la tarjeta */
.card-footer {
  border-bottom: 5px solid #3e6a86;
  /* Morado */
}
.custom-blue {
  background-color: #3e6a86 !important;
  border-color: #3e6a86 !important;
}

</style>