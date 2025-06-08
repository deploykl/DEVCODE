<template>
  <main id="main" class="main">
    <div v-if="dependenciaCounts && tareaCounts">
      <div class="card py-3 my-1 shadow">
        <h3 class="text-center mb-3 text-primary">Seguimiento del Plan Operativo Institucional {{ year }}</h3>

        <table class="table table-bordered table-hover text-center">
          <thead class="table-light">
            <tr>
              <th rowspan="2">Centro de Costo</th>
              <th rowspan="2">Actividades</th>
              <th rowspan="2">Tareas</th>
              <th colspan="4" v-if="isStaff || (isSuperuser && !isStaff)" class="text-center">Física</th>
              <th colspan="3" v-else class="text-center">Física</th>
              <th colspan="4" v-if="isStaff || (isSuperuser && !isStaff)" class="text-center">Presupuestal</th>
              <th colspan="3" v-else class="text-center">Presupuestal</th>
            </tr>
            <tr>
              <th v-if="isStaff || (isSuperuser && !isStaff)">Prog.</th>
              <th>Act.</th>
              <th>Ejec.</th>
              <th>% Ejec.</th>
              <th v-if="isStaff || (isSuperuser && !isStaff)">PIA</th>
              <th>PIM</th>
              <th>Ejec.</th>
              <th>% Ejec.</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(actividadCount, dependencia) in dependenciaCounts" :key="dependencia">
              <td>{{ dependencia }}</td>
              <td>{{ actividadCount }}</td>
              <td>{{ tareaCounts[dependencia] || 0 }}</td>
              <td v-if="isStaff || (isSuperuser && !isStaff)">{{ SUM_TAREA_REPORT[dependencia]?.total_prog_fisica || 0
                }}</td>
              <td>{{ SUM_TAREA_REPORT[dependencia]?.total_repro_fisica || 0 }}</td>
              <td>{{ SUM_TAREA_REPORT[dependencia]?.total_ejec_fisica || 0 }}</td>

              <td>
                <span :class="getBadgeClassFisico(PorEjecFisica(dependencia))">
                  {{ PorEjecFisica(dependencia) }}%
                </span>
                <div :class="getTextClassFisico(PorEjecFisica(dependencia))">
                  {{ getMensajeAvanceFisico(PorEjecFisica(dependencia)) }}
                </div>
              </td>
              <td v-if="isStaff || (isSuperuser && !isStaff)">
                {{ SUM_ACTIVIDAD_REPORT[dependencia]?.total_prog_ppto ? new Intl.NumberFormat('es-PE', {
                  style:
                    'currency', currency: 'PEN'
                }).format(SUM_ACTIVIDAD_REPORT[dependencia]?.total_prog_ppto) : 'S/ 0.00' }}
              </td>
              <td>
                {{ SUM_ACTIVIDAD_REPORT[dependencia]?.total_repro_ppto ? new Intl.NumberFormat('es-PE', {
                  style:
                    'currency', currency: 'PEN'
                }).format(SUM_ACTIVIDAD_REPORT[dependencia]?.total_repro_ppto) : 'S/ 0.00'
                }}
              </td>
              <td>
                {{ SUM_ACTIVIDAD_REPORT[dependencia]?.total_ejec_ppto ? new Intl.NumberFormat('es-PE', {
                  style:
                    'currency', currency: 'PEN'
                }).format(SUM_ACTIVIDAD_REPORT[dependencia]?.total_ejec_ppto) : 'S/ 0.00' }}
              </td>
              <td>
                <span :class="getBadgeClassPresupuestal(PorEjecPresupuesto(dependencia))">
                  {{ PorEjecPresupuesto(dependencia) }}%
                </span>
                <div :class="getTextClassPresupuestal(PorEjecPresupuesto(dependencia))">
                  {{ getMensajeAvancePresupuestal(PorEjecPresupuesto(dependencia)) }}
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <export-buttons-vue />
    <!-- Contenedor de Filtros -->
    <div class="d-flex justify-content-between align-items-center mb-3">

      <div class="d-flex align-items-start">
        <!-- Filtro de Dependencia -->
        <div v-if="isStaff || (isSuperuser && !isStaff)" class="flex-grow-1 me-3" style="max-width: 200px;">
          <label for="dependenciaFilter" class="form-label">Filtrar por Dependencia:</label>
          <select v-model="selectedDependencia" id="dependenciaFilter" class="form-select">
            <option value="">Todas las dependencias</option>
            <option v-for="(count, dependencia) in dependenciaCounts" :key="dependencia" :value="dependencia">
              {{ dependencia }}
            </option>
          </select>
        </div>

        <!-- Filtro de Grupo -->
        <div class="flex-grow-1" style="max-width: 200px;" v-if="isStaff || (isSuperuser && !isStaff)">
          <label for="grupoFilter" class="form-label">Filtrar por Grupo:</label>
          <select v-model="selectedGrupo" id="grupoFilter" class="form-select">
            <option value="">Todos los grupos</option>
            <option v-for="grupo in uniqueGrupos" :key="grupo" :value="grupo">{{ grupo }}</option>
          </select>
        </div>
      </div>


      <!-- Campo de búsqueda -->
      <div class="input-group" style="max-width: 300px;">
        <input v-model="searchQuery" type="text" class="form-control" placeholder="Buscar en la tabla..." />
        <span class="input-group-text">
          <i class="fas fa-search"></i>
        </span>
      </div>
    </div>


    <div class="card py-4 my-4 shadow">
      <!-- Tabla con detalles -->
      <table ref="table" class="table">

        <thead>
          <tr>
            <td colspan="5" v-if="isStaff || (isSuperuser && !isStaff)" class="text-center"><strong></strong></td>
            <td colspan="3" v-else class="text-center"><strong></strong></td>
            <td colspan="4" v-if="isStaff || (isSuperuser && !isStaff)" class="text-center"><strong>Física</strong></td>
            <td colspan="3" v-else class="text-center"><strong>Física</strong></td>
            <td colspan="4" v-if="isStaff || (isSuperuser && !isStaff)" class="text-center">
              <strong>Presupuestal</strong>
            </td>
            <td colspan="3" v-else class="text-center"><strong>Presupuestal</strong></td>
            <td colspan="2" v-if="isStaff || (isSuperuser && !isStaff)" class="text-center"><strong>Editar
                Registros</strong>
            </td>
            <td colspan="2" v-else class="text-center"><strong>Editar Registro</strong></td>

          </tr>
          <tr>
            <th scope="col">N°</th>
            <th>Dependencia</th>
            <th v-if="isStaff || (isSuperuser && !isStaff)">Estado</th>
            <th v-if="isStaff || (isSuperuser && !isStaff)">Grupo</th>
            <th>Actividad Operativa</th>
            <th v-if="isStaff || (isSuperuser && !isStaff)">Prog.</th>
            <th>Act.</th>
            <th>Ejec.</th>
            <th>% Ejec.</th>
            <th v-if="isStaff || (isSuperuser && !isStaff)">Prog.</th>
            <th>Act.</th>
            <th>Ejec.</th>
            <th>% Ejec.</th>
            <th>Física</th>
            <th>Presupuestal</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(actividad, index) in filteredActividades" :key="actividad.id">
            <td>{{ index + 1 }}</td>
            <td>{{ actividad.dependencia_name }}</td>

            <td v-if="isStaff || (isSuperuser && !isStaff)">
              <span :class="{
                'badge': true,
                'bg-success': actividad.estado,
                'bg-danger': !actividad.estado
              }">
                {{ actividad.estado ? 'Activo' : 'Inactivo' }}
              </span>
            </td>
            <td v-if="isStaff || (isSuperuser && !isStaff)">{{ actividad.grupo_name }}</td>
            <td>{{ actividad.name }}</td>
            <td v-if="isStaff || (isSuperuser && !isStaff)">{{ actividad.suma_prog_fisica || 0 }}</td>
            <td>{{ actividad.suma_repro_fisica || 0 }}</td>
            <td>{{ actividad.suma_ejec_fisica || 0 }}</td>
            <td>
              <span :class="getBadgeClassFisico(actividad.PorEjecAvance)">
                {{ actividad.PorEjecAvance }}%
              </span>
              <div :class="getTextClassFisico(actividad.PorEjecAvance)">
                {{ getMensajeAvanceFisico(actividad.PorEjecAvance) }}
              </div>
            </td>
            <td v-if="isStaff || (isSuperuser && !isStaff)">
              {{ actividad.PROG_PPTO_ANUAL ? new Intl.NumberFormat('es-PE', {
                style: 'currency', currency: 'PEN'
              }).format(actividad.PROG_PPTO_ANUAL) : 'S/ 0.00' }}
            </td>
            <td>{{ actividad.REPRO_PPTO_ANUAL ? new Intl.NumberFormat('es-PE', {
              style: 'currency', currency: 'PEN'
            }).format(actividad.REPRO_PPTO_ANUAL) : 'S/ 0.00' }}</td>
            <td>{{ actividad.EJEC_PPTO_ANUAL ? new Intl.NumberFormat('es-PE', {
              style: 'currency', currency: 'PEN'
            }).format(actividad.EJEC_PPTO_ANUAL) : 'S/ 0.00' }}</td>
            <td>
              <span :class="getBadgeClassPresupuestal(actividad.POR_PPTO_AVANCE)">
                {{ actividad.POR_PPTO_AVANCE }}%
              </span>
              <div :class="getTextClassPresupuestal(actividad.POR_PPTO_AVANCE)">
                {{ getMensajeAvancePresupuestal(actividad.POR_PPTO_AVANCE) }}
              </div>
            </td>
            <td>
              <button @click.stop="goToTareas(actividad.id)" class="btn btn-danger"><i
                  class="fa-solid fa-pen-to-square"></i></button>
            </td>
            <td>
              <button @click="goToActividadDetalle(actividad.id)" class="btn btn-warning"><i
                  class="fa-solid fa-pen-to-square"></i></button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </main>
</template>


<script setup>
import ExportButtonsVue from '../../components/buttons/ExportButtons.vue';
import { api, getAuthToken } from '@/components/services/auth_axios';
import {
  getBadgeClassFisico,
  getTextClassFisico,
  getMensajeAvanceFisico,
  getBadgeClassPresupuestal,
  getTextClassPresupuestal,
  getMensajeAvancePresupuestal
} from '@/components/widgets/avancePresupuestal';

import { ref, computed, onMounted, watch } from 'vue';
import { useRouter } from 'vue-router';

// Definición de variables
const actividades = ref([]);
const dependenciaCounts = ref({});
const SUM_TAREA_REPORT = ref({});
const SUM_ACTIVIDAD_REPORT = ref({});
const tareaCounts = ref({});
const searchQuery = ref('');
const isSuperuser = ref(false);
const isStaff = ref(false);
const year = ref(new Date().getFullYear());
const router = useRouter();

// Recuperar valores del localStorage o establecer valores por defecto
const selectedDependencia = ref(localStorage.getItem('selectedDependencia') || '');
const selectedGrupo = ref(localStorage.getItem('selectedGrupo') || '');

// Función para guardar en localStorage
const saveToLocalStorage = (key, value) => {
  localStorage.setItem(key, value);
};

// Función para ir a la vista de tareas
const goToTareas = (actividadId) => {
  router.push({ name: 'actividad-tareas', params: { id: actividadId } });
};

// Función para ir al detalle de la actividad
const goToActividadDetalle = (actividadId) => {
  router.push({ name: 'actividad-reportes', params: { id: actividadId } });
};

// Obtener datos al montar el componente
const LISTAR = async () => {
  try {
    const token = getAuthToken();
    
    // Verificar que el token exista
    if (!token) {
      console.error('No se encontró el token de autenticación.');
      return;
    }

    // Ejecutar las solicitudes en paralelo
    const [responseActividades] = await Promise.all([
      api.get('poi/actividad/', { headers: { Authorization: `Bearer ${token}` } }),
    ]);

    // Asignar los datos de las respuestas a las variables reactivas
    actividades.value = responseActividades.data.activities;
    dependenciaCounts.value = responseActividades.data.dependencia_counts;
    SUM_TAREA_REPORT.value = responseActividades.data.SUM_TAREA_REPORT;
    SUM_ACTIVIDAD_REPORT.value = responseActividades.data.SUM_ACTIVIDAD_REPORT;
    tareaCounts.value = responseActividades.data.tarea_counts;

    // Verificar los datos recibidos en consola
    console.log('Datos de actividades:', responseActividades.data);

  } catch (error) {
    console.error('Error al obtener los datos:', error.response ? error.response.data : error.message);
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

onMounted(() => {
  LISTAR();
});

// Watchers para guardar cambios en los filtros
watch(selectedDependencia, (newVal) => {
  saveToLocalStorage('selectedDependencia', newVal);
});

watch(selectedGrupo, (newVal) => {
  saveToLocalStorage('selectedGrupo', newVal);
});

// Filtrar las actividades según búsqueda, dependencia seleccionada y grupo seleccionado
const filteredActividades = computed(() => {
  const query = searchQuery.value.toLowerCase();
  return actividades.value.filter(actividad => {
    const dependenciaName = actividad.dependencia_name || '';
    const grupoName = actividad.grupo_name || '';

    const matchQuery =
      actividad.codigo.toLowerCase().includes(query) ||
      actividad.name.toLowerCase().includes(query) ||
      dependenciaName.toLowerCase().includes(query);

    const matchDependencia =
      !selectedDependencia.value || dependenciaName === selectedDependencia.value;

    const matchGrupo =
      !selectedGrupo.value || grupoName === selectedGrupo.value;

    return matchQuery && matchDependencia && matchGrupo;
  });
});

const uniqueGrupos = computed(() => {
  const grupos = actividades.value.map(actividad => actividad.grupo_name || '');
  return [...new Set(grupos)]; // Elimina duplicados
});

// Calcular los totales en base a las actividades filtradas
const totalSumaProgFisica = computed(() => {
  return filteredActividades.value.reduce((total, actividad) => total + (actividad.suma_prog_fisica || 0), 0);
});

const totalSumaReproFisica = computed(() => {
  return filteredActividades.value.reduce((total, actividad) => total + (actividad.suma_repro_fisica || 0), 0);
});

const totalSumaEjecFisica = computed(() => {
  return filteredActividades.value.reduce((total, actividad) => total + (actividad.suma_ejec_fisica || 0), 0);
});

const totalProgPptoAnual = computed(() => {
  return filteredActividades.value.reduce((total, actividad) => total + (actividad.PROG_PPTO_ANUAL || 0), 0);
});

const totalReproPptoAnual = computed(() => {
  return filteredActividades.value.reduce((total, actividad) => total + (actividad.REPRO_PPTO_ANUAL || 0), 0);
});

const totalEjecPptoAnual = computed(() => {
  return filteredActividades.value.reduce((total, actividad) => total + (actividad.EJEC_PPTO_ANUAL || 0), 0);
});

// Porcentaje de ejecución física y presupuestal basado en actividades filtradas
const totalPorEjecAvance = computed(() => {
  const totalRepro = totalSumaReproFisica.value;
  const totalEjec = totalSumaEjecFisica.value;
  if (totalRepro === 0) return 0;
  return Number(((totalEjec / totalRepro) * 100).toFixed(2));
});

const totalPorPPTO_AVANCE = computed(() => {
  const totalRepro = totalReproPptoAnual.value;
  const totalEjec = totalEjecPptoAnual.value;
  if (totalRepro === 0) return 0;
  return Number(((totalEjec / totalRepro) * 100).toFixed(2));
});

const PorEjecFisica = (dependencia) => {
  const totalEjec = SUM_TAREA_REPORT.value[dependencia]?.total_ejec_fisica || 0;
  const totalRepro = SUM_TAREA_REPORT.value[dependencia]?.total_repro_fisica || 1; // Evita la división por cero
  return ((totalEjec / totalRepro) * 100).toFixed(2);
};

const PorEjecPresupuesto = (dependencia) => {
  const totalEjec = SUM_ACTIVIDAD_REPORT.value[dependencia]?.total_ejec_ppto || 0;
  const totalRepro = SUM_ACTIVIDAD_REPORT.value[dependencia]?.total_repro_ppto || 1; // Evita la división por cero
  return ((totalEjec / totalRepro) * 100).toFixed(2);
};
</script>