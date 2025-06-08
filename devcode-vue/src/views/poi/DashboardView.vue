<template>
  <main id="main" class="main">
    <!-- Botones flotantes (se mostrarán encima del iframe) -->
    <button-float-component-vue class="float-buttons" />
    
    <!-- Iframe de Power BI -->
    <iframe
      :src="powerBiUrl"
      frameborder="0"
      allowfullscreen
      class="powerbi-iframe"
    ></iframe>
  </main>
</template>

<script setup>
import ButtonFloatComponentVue from '../../components/widgets/ButtonFloatComponent.vue'; // Ajusta la ruta según tu estructura

const powerBiUrl = "https://app.powerbi.com/view?r=eyJrIjoiODU5YjQ1ZGMtZjBjZi00NTA3LWJiM2YtMTBjN2VmYjcyMGZhIiwidCI6Ijc5MDVjMWZjLTkzM2MtNDUyYS04YjgzLWIyZTU2NDU1ZDE2YSIsImMiOjR9";
</script>

<style scoped>
.main {
  position: fixed;
  top: 100px;
  left: 0;
  right: 0;
  bottom: 00PX;
  margin: 0;
  padding: 0;
  overflow: hidden;
}

.powerbi-iframe {
  width: 100%;
  height: 98%;
  border: none;
  display: block;
}
.float-buttons{
  top:0px !important;
}
/* Opcional: Ocultar posibles barras de desplazamiento */
body {
  overflow: hidden;
  margin: 0;
  padding: 0;
}
</style>