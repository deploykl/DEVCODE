<template>
  <main class="container py-3">
    <header>
      <div class="d-flex justify-content-between align-items-center py-2">
        <img src="@/assets/img/login/logo.png" alt="Logo" class="img-fluid logo">
       
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

         <div class="row row-cols-1 row-cols-md-3 g-4 mt-4">
  <div class="col" v-for="item in modulos" :key="item.texto">
    <a :href="item.ruta" class="btn btn-modulo shadow-sm d-flex flex-column align-items-center justify-content-center text-center w-100 h-100 py-4">
      <i :class="item.icono + ' fs-2 mb-2'"></i>
      <span class="fs-5 fw-semibold">{{ item.texto }}</span>
    </a>
  </div>
</div>

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


const modulos = [
  {
    texto: 'Planeamiento Operativo',
    ruta: '/dashboard',
    icono: 'bi bi-bar-chart-steps', // Representa procesos y planeamiento
    clase: 'btn-outline-primary'
  },
  {
    texto: 'Gasto Diario',
    ruta: '/modulos/gasto',
    icono: 'bi bi-wallet2', // Ícono de billetera más claro
    clase: 'btn-outline-success'
  },
  {
    texto: 'Bienes y Servicios',
    ruta: '/modulos/informatica',
    icono: 'bi bi-box-seam', // Representa productos, bienes almacenados
    clase: 'btn-outline-info'
  },
  {
    texto: 'Informática',
    ruta: '/modulos/informatica',
    icono: 'bi bi-cpu', // Ícono técnico para TI / hardware
    clase: 'btn-outline-info'
  },
  {
    texto: 'Personal',
    ruta: '/modulos/usuarios',
    icono: 'bi bi-person-badge', // Representa claramente empleados/personal
    clase: 'btn-outline-info'
  },
  {
    texto: 'Patrimonio',
    ruta: '/modulos/usuarios',
    icono: 'bi bi-building', // Representa edificios/bienes institucionales
    clase: 'btn-outline-primary'
  }
];

</script>

<style scoped>
.bg-header {
  background-color: #083758;
}
.btn-modulo {
  border: 2px solid var(--bs-border-color);
  border-radius: 12px;
  height: 160px;
  background-color: white;
  transition: all 0.2s ease-in-out;
  font-weight: 500;
  color: #333;
}
.btn-modulo:hover {
  transform: translateY(-4px);
  background-color: #f8f9fa;
  box-shadow: 0 6px 18px rgba(0, 0, 0, 0.1);
  text-decoration: none;
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
