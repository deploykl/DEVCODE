<template>
  <main id="main" class="main">
    <div class="card">
      <div class="card-body">
        <div class="d-flex justify-content-between align-items-center mb-3">
          <h5 class="card-title mb-0">Inventario de Equipos de Informática</h5>
          <button @click="fetchEquipos" class="btn btn-sm btn-outline-primary">
            <i class="bi bi-arrow-clockwise"></i> Actualizar
          </button>
        </div>

        <!-- Filtros -->
        <div class="row mb-3">
          <div class="col-md-3">
            <input v-model="filters.codigo" @input="applyFilters" type="text" class="form-control form-control-sm" placeholder="Filtrar por código">
          </div>
          <div class="col-md-3">
            <input v-model="filters.descripcion" @input="applyFilters" type="text" class="form-control form-control-sm" placeholder="Filtrar por descripción">
          </div>
          <div class="col-md-3">
            <select v-model="filters.piso" @change="applyFilters" class="form-select form-select-sm">
              <option value="">Todos los pisos</option>
              <option value="1">Piso 1</option>
              <option value="2">Piso 2</option>
              <option value="3">Piso 3</option>
            </select>
          </div>
          <div class="col-md-3">
            <select v-model="filters.estado" @change="applyFilters" class="form-select form-select-sm">
              <option value="">Todos los estados</option>
              <option value="Operativo">Operativo</option>
              <option value="Inoperativo">Inoperativo</option>
              <option value="En reparación">En reparación</option>
            </select>
          </div>
        </div>

        <!-- Tabla de equipos -->
        <div class="table-responsive">
          <table class="table table-striped table-hover table-bordered">
            <thead class="table-dark">
              <tr>
                <th @click="sortBy('codigo')" style="cursor: pointer;">
                  Código <i class="bi bi-arrow-down-up"></i>
                </th>
                <th>Descripción</th>
                <th>Marca/Modelo</th>
                <th>Serie</th>
                <th @click="sortBy('piso')" style="cursor: pointer;">
                  Piso <i class="bi bi-arrow-down-up"></i>
                </th>
                <th>Estado</th>
                <th>Usuario</th>
                <th>Dependencia</th>
                <th>Responsable</th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="equipo in filteredEquipos" :key="equipo.id">
                <td>{{ equipo.codigo }}</td>
                <td>{{ equipo.descripcion }}</td>
                <td>{{ equipo.marca }} {{ equipo.modelo ? `- ${equipo.modelo}` : '' }}</td>
                <td>{{ equipo.serie }}</td>
                <td>{{ equipo.piso }}</td>
                <td>
                  <span :class="`badge bg-${getEstadoBadge(equipo.estado)}`">
                    {{ equipo.estado }}
                  </span>
                </td>
                <td>{{ equipo.usuario }}</td>
                <td>{{ equipo.dependencia }}</td>
                <td>{{ equipo.responsable }}</td>
                <td>
                  <button @click="viewDetails(equipo)" class="btn btn-sm btn-outline-info me-1" title="Ver detalles">
                    <i class="bi bi-eye"></i>
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Paginación -->
        <div class="d-flex justify-content-between align-items-center mt-3">
          <div class="form-text">
            Mostrando {{ filteredEquipos.length }} de {{ equipos.length }} equipos
          </div>
          <nav aria-label="Page navigation">
            <ul class="pagination pagination-sm">
              <li class="page-item" :class="{ disabled: currentPage === 1 }">
                <button class="page-link" @click="prevPage">Anterior</button>
              </li>
              <li class="page-item" v-for="page in totalPages" :key="page" :class="{ active: currentPage === page }">
                <button class="page-link" @click="goToPage(page)">{{ page }}</button>
              </li>
              <li class="page-item" :class="{ disabled: currentPage === totalPages }">
                <button class="page-link" @click="nextPage">Siguiente</button>
              </li>
            </ul>
          </nav>
        </div>

        <!-- Modal de detalles -->
        <div class="modal fade" id="equipoDetailsModal" tabindex="-1" aria-hidden="true">
          <div class="modal-dialog modal-lg">
            <div class="modal-content">
              <div class="modal-header">
                <h5 class="modal-title">Detalles del Equipo</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
              </div>
              <div class="modal-body" v-if="selectedEquipo">
                <div class="row">
                  <div class="col-md-6">
                    <h6>Información del Equipo</h6>
                    <ul class="list-group list-group-flush">
                      <li class="list-group-item"><strong>Código:</strong> {{ selectedEquipo.codigo }}</li>
                      <li class="list-group-item"><strong>Inventario 2023:</strong> {{ selectedEquipo.inv_2023 }}</li>
                      <li class="list-group-item"><strong>Código SBN:</strong> {{ selectedEquipo.cod_sbn }}</li>
                      <li class="list-group-item"><strong>Descripción:</strong> {{ selectedEquipo.descripcion }}</li>
                      <li class="list-group-item"><strong>Marca/Modelo:</strong> {{ selectedEquipo.marca }} {{ selectedEquipo.modelo }}</li>
                      <li class="list-group-item"><strong>Serie:</strong> {{ selectedEquipo.serie }}</li>
                    </ul>
                  </div>
                  <div class="col-md-6">
                    <h6>Ubicación y Estado</h6>
                    <ul class="list-group list-group-flush">
                      <li class="list-group-item"><strong>Piso:</strong> {{ selectedEquipo.piso }}</li>
                      <li class="list-group-item"><strong>Estado:</strong> 
                        <span :class="`badge bg-${getEstadoBadge(selectedEquipo.estado)}`">
                          {{ selectedEquipo.estado }}
                        </span>
                      </li>
                      <li class="list-group-item"><strong>Fecha registro:</strong> {{ selectedEquipo.fecha }}</li>
                    </ul>
                    
                    <h6 class="mt-3">Asignación</h6>
                    <ul class="list-group list-group-flush">
                      <li class="list-group-item"><strong>Usuario:</strong> {{ selectedEquipo.usuario }}</li>
                      <li class="list-group-item"><strong>User:</strong> {{ selectedEquipo.user }}</li>
                      <li class="list-group-item"><strong>Dependencia/Área:</strong> {{ selectedEquipo.dependencia }} / {{ selectedEquipo.area }}</li>
                    </ul>
                  </div>
                </div>
                <div class="row mt-3">
                  <div class="col-12">
                    <h6>Observaciones</h6>
                    <div class="card">
                      <div class="card-body">
                        {{ selectedEquipo.observacion || 'Sin observaciones' }}
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cerrar</button>
              </div>
            </div>
          </div>
        </div>

        <!-- Loading -->
        <div v-if="loading" class="text-center my-5">
          <div class="spinner-border text-primary" role="status">
            <span class="visually-hidden">Cargando...</span>
          </div>
          <p>Cargando inventario...</p>
        </div>

        <!-- Error -->
        <div v-if="error" class="alert alert-danger mt-3">
          <i class="bi bi-exclamation-triangle-fill"></i> Error al cargar los equipos: {{ error }}
          <button @click="fetchEquipos" class="btn btn-sm btn-outline-danger ms-2">Reintentar</button>
        </div>
      </div>
    </div>
  </main>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { api, getAuthToken } from '@/components/services/auth_axios';
import { Modal } from 'bootstrap';

// Estado del componente
const equipos = ref([]);
const filteredEquipos = ref([]);
const loading = ref(false);
const error = ref(null);
const selectedEquipo = ref(null);
const currentPage = ref(1);
const itemsPerPage = ref(10);
const totalPages = ref(1);
const sortField = ref('codigo');
const sortDirection = ref('asc');

// Filtros
const filters = ref({
  codigo: '',
  descripcion: '',
  piso: '',
  estado: ''
});

// Obtener equipos desde la API
const fetchEquipos = async () => {
  try {
    loading.value = true;
    error.value = null;
    
    const token = getAuthToken();
    const response = await api.get('informatica/all/', {
      headers: { Authorization: `Bearer ${token}` }
    });
    
    equipos.value = response.data;
    applyFilters(); // Aplicar filtros iniciales
  } catch (err) {
    error.value = err.response?.data?.message || err.message;
    console.error('Error al obtener equipos:', err);
  } finally {
    loading.value = false;
  }
};

// Aplicar filtros
const applyFilters = () => {
  let result = [...equipos.value];
  
  // Aplicar filtros
  if (filters.value.codigo) {
    result = result.filter(e => 
      e.codigo?.toLowerCase().includes(filters.value.codigo.toLowerCase())
    );
  }
  
  if (filters.value.descripcion) {
    result = result.filter(e => 
      e.descripcion?.toLowerCase().includes(filters.value.descripcion.toLowerCase())
    );
  }
  
  if (filters.value.piso) {
    result = result.filter(e => e.piso === filters.value.piso);
  }
  
  if (filters.value.estado) {
    result = result.filter(e => e.estado === filters.value.estado);
  }
  
  // Ordenar
  result.sort((a, b) => {
    const fieldA = a[sortField.value]?.toString().toLowerCase() || '';
    const fieldB = b[sortField.value]?.toString().toLowerCase() || '';
    
    if (fieldA < fieldB) return sortDirection.value === 'asc' ? -1 : 1;
    if (fieldA > fieldB) return sortDirection.value === 'asc' ? 1 : -1;
    return 0;
  });
  
  filteredEquipos.value = result;
  updatePagination();
};

// Ordenar por campo
const sortBy = (field) => {
  if (sortField.value === field) {
    sortDirection.value = sortDirection.value === 'asc' ? 'desc' : 'asc';
  } else {
    sortField.value = field;
    sortDirection.value = 'asc';
  }
  applyFilters();
};

// Paginación
const updatePagination = () => {
  totalPages.value = Math.ceil(filteredEquipos.value.length / itemsPerPage.value);
  currentPage.value = 1;
};

const goToPage = (page) => {
  currentPage.value = page;
};

const nextPage = () => {
  if (currentPage.value < totalPages.value) {
    currentPage.value++;
  }
};

const prevPage = () => {
  if (currentPage.value > 1) {
    currentPage.value--;
  }
};

// Obtener equipos paginados
const paginatedEquipos = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage.value;
  const end = start + itemsPerPage.value;
  return filteredEquipos.value.slice(start, end);
});

// Ver detalles del equipo
const viewDetails = (equipo) => {
  selectedEquipo.value = equipo;
  const modal = new Modal(document.getElementById('equipoDetailsModal'));
  modal.show();
};

// Clase CSS según estado del equipo
const getEstadoBadge = (estado) => {
  switch (estado) {
    case 'Operativo': return 'success';
    case 'Inoperativo': return 'danger';
    case 'En reparación': return 'warning';
    default: return 'secondary';
  }
};

// Cargar datos al montar el componente
onMounted(() => {
  fetchEquipos();
});
</script>

<style scoped>
.table-responsive {
  max-height: 600px;
  overflow-y: auto;
}

.table th {
  position: sticky;
  top: 0;
  background-color: #0870d8;
  z-index: 10;
}

.badge {
  font-size: 0.85em;
}

.modal-body {
  max-height: 70vh;
  overflow-y: auto;
}

.list-group-item {
  padding: 0.5rem 1rem;
}

.spinner-border {
  width: 3rem;
  height: 3rem;
}
</style>