<template>
  <!-- HEADER -->
  <header-component-vue :is-staff="true" v-if="showHeader" @toggleAside="toggleAside" />
  <!-- Transición para el aside -->
  <transition name="slide">
    <aside-component-vue v-if="showAside" />
  </transition>
  <!-- NAVIGATION -->
  <page-title-component-vue v-if="showPageTitle" />
  <!-- MAIN CONTENT -->
  <router-view />
  <button-float-component-vue v-if="showButton" />
  <!-- FOOTER -->
  <footer-component-vue v-if="showFooter" />
</template>

<script setup>
import { onMounted, computed, ref } from 'vue';
import { useRoute } from 'vue-router';
import HeaderComponentVue from './components/HeaderComponent.vue';
import FooterComponentVue from './components/FooterComponent.vue';
import AsideComponentVue from './components/AsideComponent.vue';
import PageTitleComponentVue from './components/PageTitleComponent.vue';
import ButtonFloatComponentVue from './components/widgets/ButtonFloatComponent.vue';

// Importa los componentes
const route = useRoute();

// Estado para controlar la visibilidad del aside
const isAsideVisible = ref(true);
const isStaff = ref(false); // Asegúrate de obtener este valor del localStorage o API

// Función para alternar la visibilidad del aside
const toggleAside = () => {
  if (route.name !== 'not-found' && route.path !== '/login' && route.path !== '/') {
    isAsideVisible.value = !isAsideVisible.value;
    
    // Alterna la clase en el body cuando el aside se muestra o se oculta
    if (isAsideVisible.value) {
      document.body.classList.add('sidebar-expanded');
      document.body.classList.remove('sidebar-collapsed');
    } else {
      document.body.classList.remove('sidebar-expanded');
      document.body.classList.add('sidebar-collapsed');
    }
  }
};

// Asegúrate de aplicar la clase adecuada al cargar la págin
onMounted(() => {
  isStaff.value = localStorage.getItem('is_staff') === 'true';

// Colapsar automáticamente si NO es staff
  if (!isStaff.value) {
    isAsideVisible.value = false;
    document.body.classList.add('sidebar-collapsed');
    document.body.classList.remove('sidebar-expanded');
  } else {
    document.body.classList.add('sidebar-expanded');
    document.body.classList.remove('sidebar-collapsed');
  }
});


// Determina si se deben mostrar los componentes
const showHeader = computed(() => route.name !== 'not-found' && route.path !== '/login' && route.path !== '/' && route.path !== '/' && route.path !== '/control/login' && route.path !== '/sgd/pendientes');
const showAside = computed(() => isAsideVisible.value && route.name !== 'not-found' && route.path !== '/login' && route.path !== '/' && route.path !== '/control/login' && route.path !== '/sgd/pendientes');
const showPageTitle = computed(() => route.path !== '/' && route.path !== '/login' && route.name !== 'not-found' && route.path !== '/control/login' && route.path !== '/sgd/pendientes' && route.path !== '/modulos/gasto' && route.path !== '/modulos/dashboard' && route.path !== '/dashboard');
const showFooter = computed(() => route.name !== 'not-found' && route.path !== '/login' && route.path !== '/' && route.path !== '/sgd/pendientes'  && route.path !== '/modulos/dashboard' && route.path !== '/modulos/gasto' && route.path !== '/dashboard');
//const showButton = computed(() => route.name !== 'not-found' && route.path !== '/login' && route.path !== '/');


</script>

<style>
html, body {
  margin: 0;
}
/* Estilos para la transición */
.slide-enter-active, .slide-leave-active {
  transition: transform 0.3s ease, opacity 0.3s ease;
}

.slide-enter, .slide-leave-to /* .slide-leave-active en <2.1.8 */ {
  opacity: 0;
  transform: translateX(-100%);
}

.slide-enter-to, .slide-leave /* .slide-enter-active en <2.1.8 */ {
  opacity: 1;
  transform: translateX(0);
}

</style>
