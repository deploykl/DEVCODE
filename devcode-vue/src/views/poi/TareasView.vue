<template>
  <main id="main" class="main">
    <div class="card shadow-sm">
      <div class="card-body p-0">
        <div class="table-responsive">
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
            <tbody>
              <tr v-for="(tarea, index) in tareas" :key="tarea.id" class="border-top">
                <td class="text-muted">{{ index + 1 }}</td>
                <td class="fw-semibold">{{ tarea.name }}</td>
                <td v-if="isStaff || (isSuperuser && !isStaff)" class="text-center">
                  <span :class="`badge ${tarea.trazabilidad === 'SI' ? 'bg-success' : 'bg-secondary'}`">
                    {{ tarea.trazabilidad }}
                  </span>
                </td>
                <td class="text-muted">{{ tarea.medida_name }}</td>
                <td v-if="isStaff || (isSuperuser && !isStaff)" class="text-end">{{ tarea.TotalProgFisica }}</td>
                <td class="text-end">{{ tarea.TotalReproFisica }}</td>
                <td class="text-end">{{ tarea.TotalEjecFisica }}</td>
                <td>
                  <div class="d-flex flex-column align-items-center">
                    <div class="progress w-100" style="height: 6px;">
                      <div 
                        :class="`progress-bar ${getBadgeClassFisico(tarea.PorEjecAvance).replace('badge', 'bg')}`" 
                        role="progressbar" 
                        :style="`width: ${Math.min(100, tarea.PorEjecAvance)}%`"
                        :aria-valuenow="tarea.PorEjecAvance"
                        aria-valuemin="0"
                        aria-valuemax="100"
                      ></div>
                    </div>
                    <span :class="`small mt-1 fw-semibold ${getTextClassFisico(tarea.PorEjecAvance)}`">
                      {{ tarea.PorEjecAvance }}%
                    </span>
                    <span class="text-muted x-small">{{ getMensajeAvanceFisico(tarea.PorEjecAvance) }}</span>
                  </div>
                </td>
                <td class="text-center">
                  <button 
                    @click="goToTareaDetalle(tarea.id)" 
                    class="btn btn-sm btn-outline-primary rounded-circle"
                    title="Editar ejecución"
                  >
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
                      <div 
                        :class="`progress-bar ${getBadgeClassFisico(totalPorEjecAvance).replace('badge', 'bg')}`" 
                        role="progressbar" 
                        :style="`width: ${Math.min(100, totalPorEjecAvance)}%`"
                      ></div>
                    </div>
                    <span :class="`small mt-1 fw-bold ${getTextClassFisico(totalPorEjecAvance)}`">
                      {{ totalPorEjecAvance }}%
                    </span>
                  </div>
                </td>
                <td></td>
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
const route = useRoute();
const router = useRouter();
// Definir las variables reactivas
const isSuperuser = ref(false);
const isStaff = ref(false);

const goToTareaDetalle = (tareaId) => {
  router.push({ name: 'tarea-detalle', params: { id: tareaId } });
};

const LISTAR_TAREAS = async () => {
  try {
    const token = getAuthToken();

    // Obtener el ID de la actividad desde las rutas
    const actividadId = route.params.id;

    // Realizar la solicitud para obtener las tareas
    const response = await api.get(`poi/tarea/?actividad=${actividadId}`, {
      headers: { Authorization: `Bearer ${token}` }
    });

    // Asignar las tareas a la variable reactiva
    tareas.value = response.data;

    console.log('Tareas obtenidas:', tareas.value);
  } catch (error) {
    console.error('Error al obtener las tareas:', error.response ? error.response.data : error.message);
  }

  // Configurar los permisos de usuario desde localStorage
  const superuser = localStorage.getItem('is_superuser');
  const staff = localStorage.getItem('is_staff');

  isSuperuser.value = superuser === 'true';
  isStaff.value = staff === 'true';

  // Mostrar permisos en consola
  console.log('Superuser:', isSuperuser.value);
  console.log('Staff:', isStaff.value);
};

// Llamar a LISTAR_TAREAS al montar el componente
onMounted(() => {
  LISTAR_TAREAS();
});

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
}

.table {
  margin-bottom: 0;
}

.table thead th {
  border-bottom: 2px solid #e9ecef;
  text-transform: uppercase;
  font-size: 0.8rem;
  letter-spacing: 0.5px;
  padding: 12px 15px;
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
</style>
