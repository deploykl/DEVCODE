<template>
  <main id="main" class="main">
    <div class="card shadow-sm">
      <div class="card-body p-0">
        <div class="table-responsive">
          <!-- Subtítulo de medida general -->
          <div class="px-3 pt-3 pb-2 border-bottom">
            <h2 class="text-muted mb-0">
              {{ tareas[0]?.actividad_name || 'Sin medida específica' }}
            </h2>
            <h6 class="text-muted mb-0">
              Unidad de medida de actividad - {{ tareas[0]?.actividad_medida_name || 'Sin medida específica' }}
            </h6>
          </div>
          
          <table class="table table-hover align-middle">
            <thead class="table-light">
              <tr>
                <th scope="col" style="width: 50px;">#</th>
                <th>Tarea</th>
                <th v-if="isStaff || (isSuperuser && !isStaff)">Trazabilidad</th>
                <th>Unidad</th>
                <th v-if="isStaff || (isSuperuser && !isStaff)" class="text-end">Prog. Anual</th>
                <th class="text-end">Act. Anual</th>
                <th class="text-end">Ejec. Anual</th>
                <th class="text-center">% Avance</th>
                <th style="width: 80px;">Acción</th>
              </tr>
            </thead>
            <tbody v-if="tareas.length > 0">
              <tr v-for="(tarea, index) in tareas" :key="tarea.id" class="border-top">
                <td class="text-muted">{{ index + 1 }}</td>
                <td class="fw-semibold">{{ tarea.name }}</td>
                <td v-if="isStaff || (isSuperuser && !isStaff)" class="text-center">
                  <span :class="`badge ${tarea.trazabilidad === 'SI' ? 'bg-success' : 'bg-secondary'}`">
                    {{ tarea.trazabilidad }}
                  </span>
                </td>
                <td class="text-muted">
                  {{ tarea.medida_name || 'Sin unidad' }}
                </td>
                <td v-if="isStaff || (isSuperuser && !isStaff)" class="text-end">{{ tarea.TotalProgFisica }}</td>
                <td class="text-end">{{ tarea.TotalReproFisica }}</td>
                <td class="text-end">{{ tarea.TotalEjecFisica }}</td>
                <td>
                  <div class="d-flex flex-column align-items-center">
                    <div class="progress w-100" style="height: 6px;">
                      <div :class="`progress-bar ${getBadgeClassFisico(tarea.PorEjecAvance).replace('badge', 'bg')}`"
                        role="progressbar" :style="`width: ${Math.min(100, tarea.PorEjecAvance)}%`"
                        :aria-valuenow="tarea.PorEjecAvance" aria-valuemin="0" aria-valuemax="100"></div>
                    </div>
                    <span :class="`small mt-1 fw-semibold ${getTextClassFisico(tarea.PorEjecAvance)}`">
                      {{ tarea.PorEjecAvance }}%
                    </span>
                    <span class="text-muted x-small">{{ getMensajeAvanceFisico(tarea.PorEjecAvance) }}</span>
                  </div>
                </td>
                <td class="text-center">
                  <button @click="goToTareaDetalle(tarea.id)" class="btn btn-sm btn-outline-primary rounded-circle"
                    title="Editar ejecución">
                    <i class="fa-solid fa-pen"></i>
                  </button>
                </td>
              </tr>
              <!-- Fila de totales -->
              <tr class="border-top table-active">
                <td colspan="4" v-if="isStaff || (isSuperuser && !isStaff)" class="text-end fw-bold">
                  Total General
                </td>
                <td colspan="3" v-else class="text-end fw-bold">Total General</td>
                <td v-if="isStaff || (isSuperuser && !isStaff)" class="text-end fw-bold">{{ totalProgFisica }}</td>
                <td class="text-end fw-bold">{{ totalReproFisica }}</td>
                <td class="text-end fw-bold">{{ totalEjecFisica }}</td>
                <td>
                  <div class="d-flex flex-column align-items-center">
                    <div class="progress w-100" style="height: 8px;">
                      <div :class="`progress-bar ${getBadgeClassFisico(totalPorEjecAvance).replace('badge', 'bg')}`"
                        role="progressbar" :style="`width: ${Math.min(100, totalPorEjecAvance)}%`"></div>
                    </div>
                    <span :class="`small mt-1 fw-bold ${getTextClassFisico(totalPorEjecAvance)}`">
                      {{ totalPorEjecAvance }}%
                    </span>
                  </div>
                </td>
                <td></td>
              </tr>
            </tbody>
            <tbody v-else>
              <tr>
                <td colspan="9" class="text-center py-4">
                  <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">Cargando...</span>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </main>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { api, getAuthToken } from '@/components/services/auth_axios';
import {
  getBadgeClassFisico,
  getTextClassFisico,
  getMensajeAvanceFisico,
} from '@/components/widgets/avancePresupuestal';

const tareas = ref([]);
const isLoading = ref(true);
const route = useRoute();
const router = useRouter();
const isSuperuser = ref(false);
const isStaff = ref(false);

const goToTareaDetalle = (tareaId) => {
  router.push({ name: 'tarea-detalle', params: { id: tareaId } });
};

const LISTAR_TAREAS = async () => {
  try {
    isLoading.value = true;
    const token = getAuthToken();
    const actividadId = route.params.id;

    const response = await api.get(`poi/tarea/?actividad=${actividadId}`, {
      headers: { Authorization: `Bearer ${token}` }
    });

    // Normalizar datos y asegurar campos requeridos
    tareas.value = response.data.map(tarea => ({
      ...tarea,
      actividad_medida_name: tarea.actividad_medida_name || tarea.actividad?.medida?.name || 'Sin medida',
      medida_name: tarea.medida_name || tarea.medida?.name || 'Sin unidad'
    }));

    // Configurar permisos de usuario
    isSuperuser.value = localStorage.getItem('is_superuser') === 'true';
    isStaff.value = localStorage.getItem('is_staff') === 'true';

    console.log('Datos normalizados:', tareas.value);
  } catch (error) {
    console.error('Error al obtener las tareas:', error);
  } finally {
    isLoading.value = false;
  }
};

// Calcula los totales solo para las filas con Trazabilidad "SI"
const totalProgFisica = computed(() =>
  tareas.value.filter(tarea => tarea.trazabilidad === 'SI')
    .reduce((total, tarea) => total + (parseFloat(tarea.TotalProgFisica) || 0), 0).toFixed(2)
);

const totalReproFisica = computed(() =>
  tareas.value.filter(tarea => tarea.trazabilidad === 'SI')
    .reduce((total, tarea) => total + (parseFloat(tarea.TotalReproFisica) || 0), 0).toFixed(2)
);

const totalEjecFisica = computed(() =>
  tareas.value.filter(tarea => tarea.trazabilidad === 'SI')
    .reduce((total, tarea) => total + (parseFloat(tarea.TotalEjecFisica) || 0), 0).toFixed(2)
);

const totalPorEjecAvance = computed(() => {
  const totalRepro = parseFloat(totalReproFisica.value);
  const totalEjec = parseFloat(totalEjecFisica.value);
  return totalRepro > 0 ? (totalEjec / totalRepro * 100).toFixed(2) : '0.00';
});

onMounted(() => {
  LISTAR_TAREAS();
});
</script>

<style scoped>
.main {
  background-color: #f8f9fa;
  padding: 20px;
}

.card {
  border: none;
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
}

.table-responsive {
  overflow-x: auto;
}

.table {
  margin-bottom: 0;
  font-size: 0.875rem;
}

.table thead th {
  border-bottom: 2px solid #e9ecef;
  text-transform: uppercase;
  font-size: 0.75rem;
  letter-spacing: 0.5px;
  padding: 12px 15px;
  background-color: #f8f9fa;
}

.table tbody td {
  padding: 12px 15px;
  vertical-align: middle;
}

.progress {
  background-color: #e9ecef;
  border-radius: 10px;
}

.btn-outline-primary {
  border-width: 1.5px;
  padding: 5px 8px;
  transition: all 0.3s;
}

.btn-outline-primary:hover {
  background-color: #0d6efd;
  color: white;
}

.table-active {
  background-color: rgba(0, 0, 0, 0.03);
}

.x-small {
  font-size: 0.7rem;
}

/* Estilos para el subtítulo de medida */
.border-bottom {
  border-bottom: 1px solid #dee2e6 !important;
}

.px-3 {
  padding-left: 1rem !important;
  padding-right: 1rem !important;
}

.pt-3 {
  padding-top: 1rem !important;
}

.pb-2 {
  padding-bottom: 0.5rem !important;
}

.text-muted {
  color: #6c757d !important;
}

.mb-0 {
  margin-bottom: 0 !important;
}
</style>