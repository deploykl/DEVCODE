<template>
    <main id="main" class="main">
      <div class="card">
        <div class="card-body">
          <div class="d-flex justify-content-between align-items-center mb-3">
            <h5 class="card-title mb-0">Inventario de Patrimonio</h5>
            <button @click="fetchPatrimonio" class="btn btn-sm btn-outline-primary">
              <i class="bi bi-arrow-clockwise"></i> Actualizar
            </button>
          </div>
  
          <!-- Filtros -->
          <div class="row mb-3">
            <div class="col-md-3">
              <input v-model="filters.codigo" @input="applyFilters" type="text" class="form-control form-control-sm" placeholder="Filtrar por código">
            </div>
            <div class="col-md-3">
              <input v-model="filters.denominacion" @input="applyFilters" type="text" class="form-control form-control-sm" placeholder="Filtrar por denominación">
            </div>
           
          </div>
  
          <!-- Tabla de patrimonio -->
          <div class="table-responsive">
            <table class="table table-striped table-hover table-bordered">
              <thead class="table-dark">
                <tr>
                  <th @click="sortBy('codigo_2024')" style="cursor: pointer;">
                    Código 2024 <i class="bi bi-arrow-down-up"></i>
                  </th>
                  <th>Denominación</th>
                  <th>Marca/Modelo</th>
                  <th>Serie</th>
                  <th>Usuario</th>
                  <th>Acciones</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="item in filteredPatrimonio" :key="item.id">
                  <td>{{ item.codigo_2024 }}</td>
                  <td>{{ item.denominacion }}</td>
                  <td>{{ item.marca }} {{ item.modelo ? `- ${item.modelo}` : '' }}</td>
                  <td>{{ item.serie }}</td>
                  
                  <td>{{ item.usuario }}</td>
                  <td>
                    <button @click="viewDetails(item)" class="btn btn-sm btn-outline-info me-1" title="Ver detalles">
                      <i class="bi bi-eye"></i>
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
  
          <!-- Modal de detalles -->
          <div class="modal fade" id="patrimonioDetailsModal" tabindex="-1" aria-hidden="true">
            <div class="modal-dialog modal-lg">
              <div class="modal-content">
                <div class="modal-header">
                  <h5 class="modal-title">Detalles del Patrimonio</h5>
                  <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body" v-if="selectedPatrimonio">
                  <div class="row">
                    <div class="col-md-6">
                      <h6>Información del Patrimonio</h6>
                      <ul class="list-group list-group-flush">
                        <li class="list-group-item"><strong>Código 2024:</strong> {{ selectedPatrimonio.codigo_2024 }}</li>
                        <li class="list-group-item"><strong>Denominación:</strong> {{ selectedPatrimonio.denominacion }}</li>
                        <li class="list-group-item"><strong>Marca/Modelo:</strong> {{ selectedPatrimonio.marca }} {{ selectedPatrimonio.modelo }}</li>
                        <li class="list-group-item"><strong>Serie:</strong> {{ selectedPatrimonio.serie }}</li>
                      </ul>
                    </div>
                    <div class="col-md-6">
                      <h6>Estado y Observaciones</h6>
                      <ul class="list-group list-group-flush">
                        <li class="list-group-item"><strong>Estado:</strong>
                          <span :class="`badge bg-${getEstadoBadge(selectedPatrimonio.estado)}`">
                            {{ selectedPatrimonio.estado }}
                          </span>
                        </li>
                        <li class="list-group-item"><strong>Observaciones:</strong> {{ selectedPatrimonio.observaciones || 'Sin observaciones' }}</li>
                      </ul>
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
            <i class="bi bi-exclamation-triangle-fill"></i> Error al cargar el patrimonio: {{ error }}
            <button @click="fetchPatrimonio" class="btn btn-sm btn-outline-danger ms-2">Reintentar</button>
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
  const patrimonio = ref([]);
  const filteredPatrimonio = ref([]);
  const loading = ref(false);
  const error = ref(null);
  const selectedPatrimonio = ref(null);
  
  // Filtros
  const filters = ref({
    codigo: '',
    denominacion: '',
    estado: ''
  });
  
  // Obtener patrimonio desde la API
  const fetchPatrimonio = async () => {
    try {
      loading.value = true;
      error.value = null;
      
      const token = getAuthToken();
      const response = await api.get('patrimonio/all/', {
        headers: { Authorization: `Bearer ${token}` }
      });
      
      patrimonio.value = response.data;
      applyFilters(); // Aplicar filtros iniciales
    } catch (err) {
      error.value = err.response?.data?.message || err.message;
      console.error('Error al obtener patrimonio:', err);
    } finally {
      loading.value = false;
    }
  };
  
  // Aplicar filtros
  const applyFilters = () => {
    let result = [...patrimonio.value];
    
    if (filters.value.codigo) {
      result = result.filter(e => 
        e.codigo_2024?.toLowerCase().includes(filters.value.codigo.toLowerCase())
      );
    }
    
    if (filters.value.denominacion) {
      result = result.filter(e => 
        e.denominacion?.toLowerCase().includes(filters.value.denominacion.toLowerCase())
      );
    }
    
    if (filters.value.estado) {
      result = result.filter(e => e.estado === filters.value.estado);
    }
    
    filteredPatrimonio.value = result;
  };
  
  // Ver detalles del patrimonio
  const viewDetails = (item) => {
    selectedPatrimonio.value = item;
    const modal = new Modal(document.getElementById('patrimonioDetailsModal'));
    modal.show();
  };
  
  // Clase CSS según estado del patrimonio
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
    fetchPatrimonio();
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
  