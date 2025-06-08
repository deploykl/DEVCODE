<template>
  <main id="main" class="main">
    <iframe
      :src="powerBiUrl"
      width="100%"
      height="100%"
      frameborder="0"
      allowFullScreen="true"
    ></iframe>
  </main>
</template>

<script setup>
const powerBiUrl =
  "https://app.powerbi.com/view?r=eyJrIjoiYjgwZjdiMmYtYmUyYS00MzQ5LTk4NDItZDgwNTk3YTk3ZjU5IiwidCI6Ijc5MDVjMWZjLTkzM2MtNDUyYS04YjgzLWIyZTU2NDU1ZDE2YSIsImMiOjR9";
</script>

<style scoped>
/* Ajustar para que el iframe tenga un margen superior de 200px */
.main {
  position: fixed;
  top: 80px; /* Espacio arriba */
  left: 0;
  right: 0;
  bottom: 0; /* Ajustado para no cortar contenido */
  margin: 0;
  padding: 0;
  overflow: hidden;
}

/* Ajustar el iframe para que ocupe toda el área disponible */
iframe {
  width: 100%;
  height: calc(100vh - 100px); /* Resta los 200px de espacio superior */
}
</style>
