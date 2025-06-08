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
                  <input type="text" id="username" v-model="username" @input="handleLowerCASE" class="form-control"
                    placeholder="Usuario" required />
                </div>
              </div>
              <div class="mb-3">
                <label for="password" class="form-label">Contraseña</label>
                <div class="input-group">
                  <span class="input-group-text">
                    <i class="fas fa-lock"></i>
                  </span>
                  <input :type="showPassword ? 'text' : 'password'" id="password" v-model="password"
                    class="form-control" placeholder="Contraseña" required />
                  <button class="btn btn-outline-secondary" type="button" @click="toggleShowPassword">
                    <i :class="showPassword ? 'far fa-eye-slash' : 'far fa-eye'"></i>
                  </button>
                </div>
              </div>
              <div class="text-center">
                <button type="submit" class="btn btn-primary">
                  <i class="fas fa-sign-in-alt"></i> Ingresar
                </button>
              </div>
            </form>
          </div>
          <!-- Fila inferior con borde morado -->
          <div class="card-footer border-top text-center">
            <small>Gestión Administrativa V.1</small>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { api } from '@/components/services/auth_axios';

const username = ref('')
const password = ref('')
const errorMessage = ref('')
const showPassword = ref(false)
const router = useRouter()

const toggleShowPassword = () => {
  showPassword.value = !showPassword.value
}

const handleLowerCASE = (event) => {
  const targetField = event.target.id;
  if (targetField === 'username') {
    username.value = event.target.value.toLowerCase();
  } else if (targetField === 'password') {
    password.value = event.target.value.toLowerCase();
  }
};

const handleSubmit = async () => {
  try {
    const response = await api.post('user/login/', {
      username: username.value,
      password: password.value,
    });

    console.log('Respuesta del backend:', response.data);

    const { access, refresh, is_superuser, is_staff, group, acceso_poi } = response.data;

    if (!access) {
      errorMessage.value = 'No se recibió token de acceso.';
      return;
    }

    // Store the access token and user data
    localStorage.setItem('auth_token', access);

    if (refresh) {
      localStorage.setItem('refreshToken', refresh);
    }

    localStorage.setItem('is_superuser', is_superuser ? 'true' : 'false');
    localStorage.setItem('is_staff', is_staff ? 'true' : 'false');
    localStorage.setItem('acceso_poi', acceso_poi ? 'true' : 'false');
    localStorage.setItem('dependencia_id', response.data.dependencia_id)

    if (group) {
      localStorage.setItem('group', group);
    }

    username.value = '';
    password.value = '';

    router.push('/dashboard');

  } catch (error) {
    if (error.response && error.response.status === 403) {
      errorMessage.value = error.response.data.detail || 'Su cuenta aún no cuenta con acceso al sistema.';
    }
    else if (error.response && error.response.data && error.response.data.detail) {
      errorMessage.value = error.response.data.detail;
    }
    else {
      errorMessage.value = 'Error en el servidor. Por favor intente nuevamente.';
    }
    console.error('Error:', error);
  }
};
</script>

<style scoped>
.card-footer {
  border-bottom: 5px solid #6f42c1;
}

/* Estilo opcional para el botón del ojo */
.btn-outline-secondary {
  border-color: #ced4da;
  border-left: 0;
}
</style>