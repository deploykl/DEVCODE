<template>
  <!-- Contenedor para los botones -->
  <div class="btn-container">

    <!-- Botón de retroceso -->
    <button 
      class="btn btn-warning btn-float btn-back" 
      @click="goBack"
      :disabled="isOnActividades">
      <i class="fas fa-arrow-left"></i> <!-- Ícono de Font Awesome -->
    </button>

    <!-- Botón de inicio -->
    <router-link :to="{ name: 'actividades' }" class="btn-link">
      <button class="btn btn-success btn-float">
        <i class="fas fa-home"></i> <!-- Ícono de Font Awesome -->
      </button>
    </router-link>
    
    <!-- Botón de avance -->
    <button class="btn btn-info btn-float btn-forward" @click="goForward">
      <i class="fas fa-arrow-right"></i> <!-- Ícono de Font Awesome -->
    </button>
  </div>
</template>

<script setup>
import { useRouter, useRoute } from 'vue-router';
import { computed } from 'vue';

const router = useRouter();
const route = useRoute();

// Función para ir hacia atrás en el historial
const goBack = () => {
  if (!isOnActividades.value) {
    router.go(-1); // Navega a la página anterior si no estás en 'actividades'
  }
};

// Función para ir hacia adelante en el historial
const goForward = () => {
  router.go(1); // Navega a la siguiente página en el historial
};

// Computed que verifica si estamos en la ruta 'actividades'
const isOnActividades = computed(() => {
  return route.name === 'actividades';
});
</script>

<style scoped>
.btn-container {
  position: relative;
  display: flex;
  flex-direction: row;
  gap: 8px;
}

.btn-link {
  display: flex;
}

.btn-float {
  border-radius: 50%;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 25px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  cursor: pointer;
  transition: all 0.3s ease;
  border: 2px solid #fff;
}

.btn-float:disabled {
  cursor: not-allowed; /* Mostrar el cursor de no permitido cuando está deshabilitado */
  opacity: 0.5; /* Reducir opacidad cuando está deshabilitado */
}

.btn-float:hover {
  background-color: #fff;
  color: #333;
  border: 2px solid #333;
}

.btn-back {
  background-color: #9c3e32;
  color: #fff;
}

.btn-forward {
  background-color: #14517a;
  color: #fff;
}

.btn-back:hover {
  background-color: #fff;
  color: #9c3e32;
}

.btn-forward:hover {
  background-color: #fff;
  color: #3498db;
}
</style>
