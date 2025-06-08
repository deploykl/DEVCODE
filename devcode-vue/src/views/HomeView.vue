<template>
  <main class="container py-3">
    <header>
      <div class="d-flex justify-content-between align-items-center py-2">
        <img src="@/assets/img/login/logo.png" alt="Logo" class="img-fluid logo">
        <a class="btn btn-primary px-4" href="/login">
          <i class="bi bi-box-arrow-in-right"></i> Login
        </a>
      </div>
    </header>
    <!-- Example row of columns -->
    <hr>
    <div class="container">
      <div class="row align-items-center">
        <div class="col-md-7 d-flex justify-content-center">
          <img src="@/assets/img/home/portada3.png" alt="Your Image" class="img-fluid per-img">
        </div>
        <div class="col-md-5">
          <h1 class="text-center">Herramienta de Gestión Administrativa</h1>
          <p class="text-center text-justify">La Herramienta de Gestión Administrativa de la DGOS integra la
            planificación operativa, presupuesto, gestión de personal, control patrimonial y almacenamiento de
            materiales, optimizando recursos y procesos para una gestión eficiente y orientada a resultados en la
            institución.</p>
          <!-- Botón con ícono de Font Awesome -->

        </div>
      </div>
    </div>
  </main>
  <footer class="footer">
    <div class="container">
      <div class="row">
        <div class="col-md-6">
          <p class="mb-0">
            &copy; {{ currentYear }} - Desarrollado por el área de TI de la DGOS<br>
            Desarrollo por <strong>Mg. Ing. Luis Ángel Salas Laza</strong>,<br> Modelado por <strong>Lic. Katty Ramirez
              Vela</strong>
          </p>
        </div>
        <div class="col-md-6 text-right">
          <p class="mb-0">Tecnologías utilizadas:
            <span class="me-2 badge bg-primary text-light"><i class="fab fa-python me-2"></i> Python</span>
            <span class="me-2 badge bg-secondary text-light"><i class="fab fa-python me-2"></i> Django</span>
            <span class="me-2 badge bg-info text-light"><i class="fas fa-layer-group me-2"></i> REST API</span>
            <span class="me-2 badge bg-success text-light"><i class="fab fa-js me-2"></i> Vue.js</span>
            <span class="me-2 badge bg-warning text-dark"><i class="fas fa-database me-2"></i> SQL Server</span>
          </p>
        </div>
      </div>
    </div>
  </footer>

</template>

<script setup>
const currentYear = new Date().getFullYear();
</script>

<style scoped>
.bg-header {
  background-color: #083758;
}

header {
  width: 100%;
}

.logo {
  width: auto;
  /* Permite que la imagen mantenga su tamaño original */
  height: auto;
  /* Evita que se distorsione */
  max-width: none;
  /* Elimina cualquier restricción de tamaño */
}

.card-title {
  font-family: 'Roboto', sans-serif;
  font-size: 0.9rem;
}

.card-text {
  font-family: 'Lato', sans-serif;
  color: #867d7d;
  font-size: 0.7rem;
}

.btn-lg {
  transition: all 0.3s ease-in-out;
}

.btn-lg:hover {
  background-color: #0a9f58;
  transform: translateY(-3px);
}

.text-justify {
  text-align: justify;
}

main {
  display: grid;
  grid-template-rows: auto 1fr auto;
}

/* Fondo con degradado suave */
.header-background {
  background: linear-gradient(135deg, #6a9ac4, #3d6d9a);
  padding: 1rem 1rem;
  color: #ffffff;
  border-radius: 10px;
}

/* Estilos para el título principal */
.header-background h1 {
  font-family: 'Georgia', serif;
  font-weight: 700;
  font-size: 2.5rem;
  margin-bottom: 0.5rem;
}

/* Estilos para el subtítulo */
.header-background p {
  font-family: 'Arial', sans-serif;
  font-size: 1.2rem;
  color: #e0e0e0;
  font-weight: 300;
  margin-bottom: 0;
}

/* Línea divisoria decorativa */
.decorative-line {
  width: 60px;
  height: 3px;
  background-color: #ffffff;
  margin: 0.5rem auto;
  border-radius: 5px;
}

.per-img {
  filter: drop-shadow(10px 5px 10px rgb(168, 162, 151));
}

.logo {
  max-width: 700px;
  /* Ancho máximo de 500px */
  width: 100%;
  /* Se ajusta automáticamente en pantallas más pequeñas */
  height: auto;
  /* Mantiene la proporción original */
}


.header-background h1 {
  font-family: 'Georgia', serif;
  font-weight: 700;
  font-size: 2.2rem;
  /* Reducido ligeramente para mejor balance */
  margin-bottom: 0;
  line-height: 1.2;
}

.header-background .btn-primary {
  padding: 0.5rem 1.5rem;
  font-size: 1.1rem;
}
</style>
