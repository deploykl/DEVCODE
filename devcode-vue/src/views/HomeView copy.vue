<template>
  <main class="container py-3">
    <header class="text-center header-background">
      <h1>Plataforma Local</h1>
      <div class="decorative-line"></div>
      <p>Gestión de proyectos y seguimiento institucional</p>
    </header>
    <!-- Example row of columns -->
    <hr>
    <div class="container">
      <div class="row align-items-center">
        <div class="col-md-7 d-flex justify-content-center">
          <img src="@/assets/img/home/portada1.png" alt="Your Image" class="img-fluid per-img">
        </div>
        <div class="col-md-5">
          <div class="row">
            <div class="col-md-6">
              <div class="card shadow border-primary mb-3">
                <img src="@/assets/img/poi/poi.png" alt="Plataforma POI"
                  class="card-img-top rounded-top img-fluid w-25 mx-auto">
                <div class="card-body text-center">
                  <h5 class="card-title">Sistema de Seguimiento Institucional</h5>
                  <p class="card-text">DGOS - DIEM - DIMON</p>
                  <!-- Botón con ícono de Font Awesome -->
                  <router-link :to="{ name: 'login' }" class="btn btn-success btn-sm rounded-circle">
                    <i class="fas fa-paper-plane"></i>
                  </router-link>
                </div>
              </div>
              <div class="card shadow border-primary mb-3">
                <img src="@/assets/img/home/control.png" alt="Plataforma POI"
                  class="card-img-top rounded-top img-fluid w-25 mx-auto">
                <div class="card-body text-center">
                  <h5 class="card-title">Control DGOS</h5>
                  <p class="card-text">Módulos de reporte</p>
                  <!-- Botón con ícono de Font Awesome -->
                  <router-link :to="{ name: 'control-login' }" class="btn btn-success btn-sm rounded-circle">
                    <i class="fas fa-paper-plane"></i>
                  </router-link>
                </div>
              </div>
              <div class="card shadow border-primary mb-1">
                <img src="@/assets/img/home/notas.png" alt="Plataforma POI"
                  class="card-img-top rounded-top img-fluid w-25 mx-auto">
                <div class="card-body text-center">
                  <h5 class="card-title">SGD - Pendientes</h5>
                  <p class="card-text">DGOS - DIEM - DIMON</p>
                  <!-- Botón con ícono de Font Awesome -->
                  <router-link :to="{ name: 'sgd-pendientes' }" class="btn btn-success btn-sm rounded-circle">
                    <i class="fas fa-paper-plane"></i>
                  </router-link>
                </div>
              </div>
            </div>
            <div class="col-md-6">
              <div class="card shadow border-primary mb-3">
                <img src="@/assets/img/presupuesto.png" alt="Plataforma POI"
                  class="card-img-top rounded-top img-fluid w-25 mx-auto">
                <div class="card-body text-center">
                  <h5 class="card-title">Gasto Diario <br class="py-2">DGOS DIEM</h5>
                  <p class="card-text">BI Presupuesto</p>
                  <!-- Botón con ícono de Font Awesome -->
                  <a href="https://app.powerbi.com/view?r=eyJrIjoiMTg2NjhjNTktMTBkMC00ODUyLTlmNzgtYTJjNjM0NTBmNTViIiwidCI6Ijc5MDVjMWZjLTkzM2MtNDUyYS04YjgzLWIyZTU2NDU1ZDE2YSIsImMiOjR9"
                    target="_blank" class="btn btn-success btn-sm rounded-circle">
                    <i class="fas fa-paper-plane"></i>
                  </a>
                </div>
              </div>
              <div class="card shadow border-primary mb-3">
                <img src="@/assets/img/zoom/zoom.png" alt="Plataforma POI"
                  class="card-img-top rounded-top img-fluid w-25 mx-auto">
                <div class="card-body text-center">
                  <h5 class="card-title">En desarrollo</h5>
                  <p class="card-text">Próximamente disponible.</p>
                  <!-- Botón con ícono de Font Awesome -->
                  <a class="btn btn-success btn-sm rounded-circle">
                    <i class="fas fa-paper-plane"></i>
                  </a>
                </div>
              </div>
              <div class="card shadow border-primary mb-3">
                <img src="@/assets/img/desarollo.png" alt="Plataforma POI"
                  class="card-img-top rounded-top img-fluid w-25 mx-auto">
                <div class="card-body text-center">
                  <h5 class="card-title">En desarrollo</h5>
                  <p class="card-text">Próximamente disponible.</p>
                  <!-- Botón con ícono de Font Awesome -->
                  <a class="btn btn-success btn-sm rounded-circle">
                    <i class="fas fa-paper-plane"></i>
                  </a>
                </div>
              </div>
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
          <p class="mb-0">&copy; {{ currentYear }} - Desarrollado por el área de TI de la DGOS</p>
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

.card-title {
  font-family: 'Roboto', sans-serif;
  font-size: 0.9rem;
}

.card-text {
  font-family: 'Lato', sans-serif;
  color: #867d7d;
  font-size: 0.7rem;
  /* Tamaño más pequeño para el texto */
}

.btn-lg {
  transition: all 0.3s ease-in-out;
}

.btn-lg:hover {
  background-color: #0a9f58;
  transform: translateY(-3px);
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
  filter: drop-shadow(10px 5px 10px rgb(168, 162, 151))
}
</style>