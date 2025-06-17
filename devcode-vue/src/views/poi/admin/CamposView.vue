<template>
  <main id="main" class="main">
    <section class="section">
      <div class="row">
        <div class="col-lg-12">
          <div class="card">
            <div class="card-body">
              <h5 class="card-title">Filtros de Bloqueo</h5>
              
              <!-- Filtros -->
              <div class="row mb-3">
                <div class="col-md-3">
                  <label for="yearSelect" class="form-label">Año</label>
                  <select 
                    id="yearSelect" 
                    v-model="selectedYear" 
                    class="form-select" 
                    @change="saveFilters"
                  >
                    <option v-for="year in years" :key="year" :value="year">{{ year }}</option>
                  </select>
                </div>
                
                <div class="col-md-3">
                  <label for="monthSelect" class="form-label">Mes</label>
                  <select 
                    id="monthSelect" 
                    v-model="selectedMonth" 
                    class="form-select" 
                    @change="saveFilters"
                  >
                    <option value="">Seleccione mes</option>
                    <option v-for="month in months" :key="month" :value="month">{{ month }}</option>
                  </select>
                </div>

                <div class="col-md-3">
                  <label for="activitySelect" class="form-label">Actividad</label>
                  <select 
                    id="activitySelect" 
                    v-model="selectedActivity" 
                    class="form-select" 
                    @change="updateTasks"
                  >
                    <option value="">Todas las actividades</option>
                    <option v-for="activity in activities" :key="activity.id" :value="activity.id">
                      {{ activity.nombre || activity.name }}
                    </option>
                  </select>
                </div>

                <div class="col-md-3">
                  <label for="taskSelect" class="form-label">Tarea</label>
                  <select 
                    id="taskSelect" 
                    v-model="selectedTask" 
                    class="form-select" 
                    @change="saveFilters"
                  >
                    <option value="">Todas las tareas</option>
                    <option v-for="task in filteredTasks" :key="task.id" :value="task.id">
                      {{ task.nombre || task.name }}
                    </option>
                  </select>
                </div>

                <div class="col-md-3 mt-3">
                  <label for="searchInput" class="form-label">Buscar</label>
                  <input 
                    id="searchInput" 
                    v-model="searchQuery" 
                    type="text" 
                    class="form-control" 
                    placeholder="Buscar actividad/tarea..."
                    @input="saveFilters"
                  >
                </div>
                
                <div class="col-md-3 d-flex align-items-end">
                  <button 
                    class="btn btn-success" 
                    @click="toggleBlockAll"
                    :disabled="loading"
                  >
                    <i class="bi" :class="allBlocked ? 'bi-lock' : 'bi-unlock'"></i>
                    {{ allBlocked ? 'Bloquear Todos' : 'Activar Todos' }}
                  </button>
                </div>
              </div>

              <!-- Tabla -->
              <div v-if="loading" class="text-center py-5">
                <div class="spinner-border text-primary" role="status">
                  <span class="visually-hidden">Cargando...</span>
                </div>
                <p class="mt-2">Cargando registros...</p>
              </div>

              <div v-else>
                <div class="table-responsive">
                  <table class="table table-hover">
                    <thead>
                      <tr>
                        <th scope="col">#</th>
                        <th scope="col">Actividad</th>
                        <th scope="col">Tarea</th>
                        <th scope="col">Mes/Año</th>
                        <th scope="col">Estado</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr v-for="(report, index) in paginatedReports" :key="report.id" @click="toggleBlock(report)">
                        <th scope="row">{{ (currentPage - 1) * itemsPerPage + index + 1 }}</th>
                        <td>{{ report.actividad_name || 'N/A' }}</td>
                        <td>{{ report.tarea_name || 'N/A' }}</td>
                        <td>{{ report.mes }} / {{ report.year }}</td>
                        <td>
                          <div class="form-check form-switch d-flex justify-content-center">
                            <input 
                              class="form-check-input" 
                              type="checkbox" 
                              role="switch"
                              :checked="report.campos_bloqueados"
                              @click.stop="toggleBlock(report)"
                              :disabled="updatingId === report.id"
                              style="width: 3em; height: 1.5em;"
                            >
                            <span class="ms-2">
                              {{ report.campos_bloqueados ? 'Activado' : 'Bloqueado' }}
                              <span v-if="updatingId === report.id" class="spinner-border spinner-border-sm ms-1"></span>
                            </span>
                          </div>
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>

                <!-- Paginación -->
                <nav v-if="totalPages > 1" class="mt-3">
                  <ul class="pagination justify-content-center">
                    <li class="page-item" :class="{ disabled: currentPage === 1 }">
                      <button class="page-link" @click="prevPage">
                        <i class="bi bi-chevron-left"></i>
                      </button>
                    </li>
                    <li 
                      v-for="page in visiblePages" 
                      :key="page" 
                      class="page-item" 
                      :class="{ active: currentPage === page }"
                    >
                      <button class="page-link" @click="goToPage(page)">{{ page }}</button>
                    </li>
                    <li class="page-item" :class="{ disabled: currentPage === totalPages }">
                      <button class="page-link" @click="nextPage">
                        <i class="bi bi-chevron-right"></i>
                      </button>
                    </li>
                  </ul>
                </nav>

                <div v-if="filteredReports.length === 0" class="alert alert-info mt-3">
                  No se encontraron registros para los filtros seleccionados.
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  </main>
</template>
<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import { api, getAuthToken } from '@/components/services/auth_axios';
import { useToast } from 'vue-toastification';
import { useRouter } from 'vue-router';

const toast = useToast();
const router = useRouter();

// Reactive data
const reports = ref([]);
const activities = ref([]);
const tasks = ref([]);
const loading = ref(false);
const updatingId = ref(null);
const selectedYear = ref(new Date().getFullYear());
const selectedMonth = ref('');
const selectedActivity = ref('');
const selectedTask = ref('');
const searchQuery = ref('');
const years = ref([]);
const months = [
  'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
  'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'
];
const currentPage = ref(1);
const itemsPerPage = ref(10);
const totalItems = ref(0);
const allBlocked = ref(false);

// Computed properties
const filteredTasks = computed(() => {
  if (!selectedActivity.value) return tasks.value;
  return tasks.value.filter(task => task.actividad === selectedActivity.value);
});

const filteredReports = computed(() => {
  let result = reports.value.filter(report => {
    const yearMatch = report.year == selectedYear.value;
    const monthMatch = selectedMonth.value ? report.mes === selectedMonth.value : true;
    return yearMatch && monthMatch;
  });

  if (selectedActivity.value) {
    result = result.filter(report => {
      const actividad = activities.value.find(a => a.id == selectedActivity.value);
      return actividad && report.actividad_name === (actividad.nombre || actividad.name);
    });
  }

  if (selectedTask.value) {
    result = result.filter(report => {
      const tarea = tasks.value.find(t => t.id == selectedTask.value);
      return tarea && report.tarea_name === (tarea.nombre || tarea.name);
    });
  }

  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase();
    result = result.filter(report => {
      const actividadName = report.actividad_name?.toLowerCase() || '';
      const tareaName = report.tarea_name?.toLowerCase() || '';
      return actividadName.includes(query) || tareaName.includes(query);
    });
  }

  // Actualizar estado de allBlocked
  if (result.length > 0) {
    allBlocked.value = result.every(r => r.campos_bloqueados);
  } else {
    allBlocked.value = false;
  }

  return result;
});

const paginatedReports = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage.value;
  const end = start + itemsPerPage.value;
  return filteredReports.value.slice(start, end);
});

const totalPages = computed(() => {
  return Math.ceil(filteredReports.value.length / itemsPerPage.value);
});

const visiblePages = computed(() => {
  const maxVisible = 5;
  const half = Math.floor(maxVisible / 2);
  let start = Math.max(currentPage.value - half, 1);
  let end = Math.min(start + maxVisible - 1, totalPages.value);
  
  if (end - start + 1 < maxVisible) {
    start = Math.max(end - maxVisible + 1, 1);
  }
  
  return Array.from({ length: end - start + 1 }, (_, i) => start + i);
});

// Methods
const generateYears = () => {
  const currentYear = new Date().getFullYear();
  years.value = Array.from({ length: 3 }, (_, i) => currentYear - 1 + i);
};

const loadActivities = async () => {
  try {
    const response = await api.get('/poi/actividad/', {
      headers: {
        'Authorization': `Bearer ${getAuthToken()}`
      }
    });
    activities.value = response.data.activities || response.data || [];
  } catch (error) {
    console.error('Error al cargar actividades:', error);
    toast.error('Error al cargar las actividades');
  }
};

const loadTasks = async () => {
  try {
    const response = await api.get('/poi/tarea/', {
      headers: {
        'Authorization': `Bearer ${getAuthToken()}`
      }
    });
    tasks.value = response.data.tasks || response.data || [];
  } catch (error) {
    console.error('Error al cargar tareas:', error);
    toast.error('Error al cargar las tareas');
  }
};

const loadData = async () => {
  loading.value = true;
  try {
    const response = await api.get('/poi/reporte-tarea/', {
      params: {
        year: selectedYear.value,
        mes: selectedMonth.value,
        page: currentPage.value,
        page_size: itemsPerPage.value
      },
      headers: {
        'Authorization': `Bearer ${getAuthToken()}`
      }
    });
    
    reports.value = response.data.results || response.data;
    totalItems.value = response.data.count || reports.value.length;
    
  } catch (error) {
    console.error('Error al cargar reportes:', error);
    toast.error('Error al cargar los reportes');
  } finally {
    loading.value = false;
  }
};

const toggleBlock = async (report) => {
  updatingId.value = report.id;
  try {
    const nuevoEstado = !report.campos_bloqueados;
    const response = await api.patch(`/poi/reporte-tarea/${report.id}/`, {
      campos_bloqueados: nuevoEstado
    });
    
    const index = reports.value.findIndex(r => r.id === report.id);
    if (index !== -1) {
      reports.value[index] = response.data;
    }
    
    toast.success(`Registro ${nuevoEstado ? 'desbloqueado' : 'bloqueado'} correctamente`);
  } catch (error) {
    console.error('Error al actualizar:', error);
    toast.error('Error al cambiar el estado');
  } finally {
    updatingId.value = null;
  }
};

const toggleBlockAll = async () => {
  if (filteredReports.value.length === 0) {
    toast.warning('No hay registros para actualizar');
    return;
  }
  
  loading.value = true;
  try {
    const nuevoEstado = !allBlocked.value;
    const reportIds = filteredReports.value.map(report => report.id);
    
    await api.post('/poi/reporte-tarea/bulk-update/', {
      ids: reportIds,
      campos_bloqueados: nuevoEstado
    });
    
    // Update local state
    reports.value = reports.value.map(report => {
      if (reportIds.includes(report.id)) {
        return {...report, campos_bloqueados: nuevoEstado};
      }
      return report;
    });
    
    toast.success(`Todos los registros han sido ${nuevoEstado ? 'bloqueados' : 'desbloqueados'}`);
    allBlocked.value = nuevoEstado;
  } catch (error) {
    console.error('Error al actualizar todos:', error);
    toast.error('Error al actualizar los registros');
  } finally {
    loading.value = false;
  }
};

const updateTasks = () => {
  selectedTask.value = '';
  saveFilters();
};

const saveFilters = () => {
  const filters = {
    year: selectedYear.value,
    month: selectedMonth.value,
    activity: selectedActivity.value,
    task: selectedTask.value,
    search: searchQuery.value,
    page: currentPage.value
  };
  localStorage.setItem('blockFilters', JSON.stringify(filters));
  
  const query = {
    year: selectedYear.value,
    month: selectedMonth.value,
    activity: selectedActivity.value,
    task: selectedTask.value,
    search: searchQuery.value
  };
  router.replace({ query });
  
  loadData();
};

const loadFilters = () => {
  const query = router.currentRoute.value.query;
  if (query.year || query.month || query.activity || query.task || query.search) {
    selectedYear.value = query.year || new Date().getFullYear();
    selectedMonth.value = query.month || '';
    selectedActivity.value = query.activity || '';
    selectedTask.value = query.task || '';
    searchQuery.value = query.search || '';
    return;
  }
  
  const savedFilters = localStorage.getItem('blockFilters');
  if (savedFilters) {
    const filters = JSON.parse(savedFilters);
    selectedYear.value = filters.year || new Date().getFullYear();
    selectedMonth.value = filters.month || '';
    selectedActivity.value = filters.activity || '';
    selectedTask.value = filters.task || '';
    searchQuery.value = filters.search || '';
    currentPage.value = filters.page || 1;
  }
};

// Pagination methods
const goToPage = (page) => {
  if (page !== currentPage.value) {
    currentPage.value = page;
    saveFilters();
  }
};

const prevPage = () => {
  if (currentPage.value > 1) {
    currentPage.value--;
    saveFilters();
  }
};

const nextPage = () => {
  if (currentPage.value < totalPages.value) {
    currentPage.value++;
    saveFilters();
  }
};

// Watchers
watch(filteredReports, () => {
  if (currentPage.value > totalPages.value) {
    currentPage.value = 1;
  }
});

// Lifecycle hooks
onMounted(() => {
  generateYears();
  loadActivities();
  loadTasks();
  loadFilters();
  loadData();
});
</script>

<style scoped>
.card {
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.card-body {
  padding: 1.5rem;
}

.table {
  font-size: 0.9rem;
}

.table th {
  font-weight: 600;
  background-color: #f8f9fa;
}

.badge {
  font-size: 0.8rem;
  padding: 0.35em 0.65em;
  font-weight: 500;
}

.btn-sm {
  padding: 0.25rem 0.5rem;
  font-size: 0.8rem;
}

.pagination {
  margin-bottom: 0;
}

.spinner-border {
  width: 1.2rem;
  height: 1.2rem;
  border-width: 0.15em;
}

.alert {
  margin-bottom: 0;
}

@media (max-width: 768px) {
  .col-md-3 {
    margin-bottom: 1rem;
  }
}
</style>