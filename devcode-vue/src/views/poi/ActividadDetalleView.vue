<template>
  <main id="main" class="main">
    <p class="h5 text-primary">Actividad:</p>
    <p class="h6 text-secondary">{{ reportes[0]?.actividad_name }}</p>
    <!-- Suponiendo que 'reportes' es un array y estás mostrando el primer reporte -->

    <table class="table table-bordered">
      <thead>
        <tr>
          <th>Año</th>
          <th>Mes</th>
          <th>Prog. Gen. 5.21</th>
          <th>Prog. Gen. 5.23</th>
          <th>Prog. Gen. 5.26</th>
          <th>Prog. PRESUPUESTAL</th>
          <th>Act. Gen. 5.21</th>
          <th>Act. Gen. 5.23</th>
          <th>Act. Gen. 5.26</th>
          <th>Act. PRESUPUESTAL</th>
          <th>Ejec. Gen. 5.21</th>
          <th>Ejec. Gen. 5.23</th>
          <th>Ejec. Gen. 5.26</th>
          <th>Ejec. PRESUPUESTAL</th>
          <th>% avance</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="reporte in reportes" :key="reporte.id"
          :class="{ 'bg-light': reporte.mes.toUpperCase() === currentMonthName }">
          <td>{{ reporte.year }}</td>
          <td>
            <span :class="['badge', reporte.mes.toUpperCase() === currentMonthName ? 'bg-success' : 'bg-secondary']">
              {{ reporte.mes }}
            </span>
          </td>
          <!-- Campos de Progreso General -->
          <td>
            <input v-model.number="reporte.prog_5_21" type="text"  class="form-control"
              @keydown="validarInput">
          </td>
          <td>
            <input v-model.number="reporte.prog_5_23" type="text" step="0.01" class="form-control"
              @keydown="validarInput">
          </td>
          <td>
            <input v-model.number="reporte.prog_5_26" type="text" step="0.01" class="form-control"
              @keydown="validarInput">
          </td>
          <!-- Campo de Prog. PRESUPUESTAL, solo lectura -->
          <td>
            <input :value="calcularProgPpto(reporte)" type="text" class="form-control readonly-cell" readonly>
          </td>
          <!-- Campos de Actividad General -->
          <td>
            <input v-model.number="reporte.act_5_21" type="text" step="0.01" class="form-control"
              @keydown="validarInput">
          </td>
          <td>
            <input v-model.number="reporte.act_5_23" type="text" step="0.01" class="form-control"
              @keydown="validarInput">
          </td>
          <td>
            <input v-model.number="reporte.act_5_26" type="text" step="0.01" class="form-control"
              @keydown="validarInput">
          </td>
          <td>
            <input :value="calcularActPpto(reporte)" type="text" class="form-control readonly-cell" readonly>
          </td>
          <!-- Campos de Ejecución General -->
          <td>
            <input v-model.number="reporte.ejec_5_21" type="text" step="0.01" class="form-control"
              @keydown="validarInput">
          </td>
          <td>
            <input v-model.number="reporte.ejec_5_23" type="text" step="0.01" class="form-control"
              @keydown="validarInput">
          </td>
          <td>
            <input v-model.number="reporte.ejec_5_26" type="text" step="0.01" class="form-control"
              @keydown="validarInput">
          </td>
          <td>
            <input :value="calcularEjecPpto(reporte)" type="text" class="form-control readonly-cell" readonly>
          </td>
          <td :class="getTextClassPresupuestal(PorcentajeAvance(reporte))">
            <span :class="getBadgeClassPresupuestal(PorcentajeAvance(reporte))">{{ PorcentajeAvance(reporte) }}%</span>
            <span class="ms-2">{{ getMensajeAvancePresupuestal(PorcentajeAvance(reporte)) }}</span>
          </td>
        </tr>
        <!-- Fila de totales -->
        <tr>
          <td colspan="2" class="text-center"><strong>Total</strong></td>
          <td>
            <CurrencyFormatter :value="totalProgGen521" />
          </td>
          <td>
            <CurrencyFormatter :value="totalProgGen523" />
          </td>
          <td>
            <CurrencyFormatter :value="totalProgGen526" />
          </td>
          <td>
            <CurrencyFormatter :value="totalProgPpto" />
          </td>
          <td>
            <CurrencyFormatter :value="totalActGen521" />
          </td>
          <td>
            <CurrencyFormatter :value="totalActGen523" />
          </td>
          <td>
            <CurrencyFormatter :value="totalActGen526" />
          </td>
          <td>
            <CurrencyFormatter :value="totalReproPpto" />
          </td>
          <td>
            <CurrencyFormatter :value="totalEjecGen521" />
          </td>
          <td>
            <CurrencyFormatter :value="totalEjecGen523" />
          </td>
          <td>
            <CurrencyFormatter :value="totalEjecGen526" />
          </td>
          <td>
            <CurrencyFormatter :value="totalEjecPpto" />
          </td>
          <td>{{ totalPorcentajeAvance }}%</td>
        </tr>
      </tbody>
    </table>
    <button @click="guardarTodosRegistros" class="btn btn-primary mt-3" :disabled="loading">
      <span v-if="loading">Guardando...</span>
      <span v-else>Guardar Todos los Registros</span>
    </button>
  </main>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { api, getAuthToken } from '@/components/services/auth_axios';
import { useRoute } from 'vue-router';
import { SwalSuccess, SwalWarning, SwalDelete, SwalUpdate } from '@/components/widgets/SwalComponent'; // Asegúrate de que la ruta sea correcta
import CurrencyFormatter from '@/components/widgets/FormatoMoneda.vue';
import {
  getBadgeClassPresupuestal,
  getTextClassPresupuestal,
  getMensajeAvancePresupuestal
} from '@/components/widgets/avancePresupuestal';

const actividades = ref([]);
const reportes = ref([]);
const loading = ref(false);
const route = useRoute();
const currentMonthName = ref(new Date().toLocaleString('es-ES', { month: 'long' }).toUpperCase());


const mesActual = computed(() => {
  const fecha = new Date();
  return fecha.toLocaleString('es-ES', { month: 'long' }).toUpperCase();
});

const diasRestantesMes = computed(() => {
  const fechaActual = new Date();
  const ultimoDiaMes = new Date(fechaActual.getFullYear(), fechaActual.getMonth() + 1, 0);
  return Math.ceil((ultimoDiaMes - fechaActual) / (1000 * 60 * 60 * 24));
});


const LISTAR = async () => {
  try {
    const token = getAuthToken();

    const actividadId = route.params.id;

    const [responseReporteActividad, responseActividades] = await Promise.all([
      api.get(`poi/reporte-actividad/?actividad=${actividadId}`, { headers: { Authorization: `Bearer ${token}` } }),
      api.get('poi/actividad/', { headers: { Authorization: `Bearer ${token}` } }),
      ]);

    reportes.value = responseReporteActividad.data; // Corrección aquí
    actividades.value = responseActividades.data; // Mantenido

  } catch (error) {
    console.error('Error al obtener los reportes:', error.response ? error.response.data : error.message); // Corrección aquí
  }
};

onMounted(() => {
  LISTAR();
});

const validarInput = (event) => {
  const char = event.key;

  // Permitir solo números, el punto decimal y las teclas de control
  if (!/^\d$/.test(char) && char !== '.' && !["Backspace", "Tab", "ArrowLeft", "ArrowRight"].includes(char)) {
    event.preventDefault(); // Prevenir la entrada del carácter no deseado
  }
};

const guardarTodosRegistros = async () => {
  loading.value = true;
  const errores = [];
  const token = getAuthToken();

  try {
    // Ejecutar cada registro en paralelo
    await Promise.all(reportes.value.map(async (reporte) => {
      // Calcular y asignar los valores necesarios
      reporte.prog_ppto = calcularProgPpto(reporte);
      reporte.repro_ppto = calcularActPpto(reporte);
      reporte.ejec_ppto = calcularEjecPpto(reporte);

      try {
        const response = await api.put(`poi/reporte-actividad/${reporte.id}/`, reporte, {
          headers: { Authorization: `Bearer ${token}` }
        });

        // Actualizar el reporte en la lista
        const index = reportes.value.findIndex(item => item.id === reporte.id);
        if (index !== -1) {
          reportes.value[index] = response.data;
        } else {
          reportes.value.push(response.data);
        }

      } catch (error) {
        const errorMsg = error.response ? error.response.data : error.message;
        errores.push({ reporteId: reporte.id, error: errorMsg });
        console.error(`Error al guardar el reporte ${reporte.id}:`, errorMsg);
      }
    }));

  } catch (error) {
    console.error('Error inesperado al guardar todos los registros:', error);
  } finally {
    loading.value = false;
  }

  // Mostrar mensajes de éxito o errores
  if (errores.length === 0) {
    await SwalUpdate();
  } else {
    alert(`Se encontraron errores al guardar algunos registros: ${errores.map(e => `ID ${e.reporteId}: ${e.error}`).join(', ')}`);
    console.error('Errores al guardar los registros:', errores);
  }
};


const PorcentajeAvance = (reporte) => {
  if (reporte.repro_ppto > 0) {
    return (reporte.ejec_ppto / reporte.repro_ppto * 100).toFixed(2);
  }
  return '0.00';
};

// Método para calcular Prog. PRESUPUESTAL
const calcularProgPpto = (reporte) => {
  const prog5_21 = parseFloat(reporte.prog_5_21) || 0;
  const prog5_23 = parseFloat(reporte.prog_5_23) || 0;
  const prog5_26 = parseFloat(reporte.prog_5_26) || 0;
  return (prog5_21 + prog5_23 + prog5_26).toFixed(2);
};

// Método para calcular Prog. PRESUPUESTAL
const calcularActPpto = (reporte) => {
  const act5_21 = parseFloat(reporte.act_5_21) || 0;
  const act5_23 = parseFloat(reporte.act_5_23) || 0;
  const act5_26 = parseFloat(reporte.act_5_26) || 0;
  return (act5_21 + act5_23 + act5_26).toFixed(2);
};

const calcularEjecPpto = (reporte) => {
  const ejec5_21 = parseFloat(reporte.ejec_5_21) || 0;
  const ejec_23 = parseFloat(reporte.ejec_5_23) || 0;
  const ejec5_26 = parseFloat(reporte.ejec_5_26) || 0;
  return (ejec5_21 + ejec_23 + ejec5_26).toFixed(2);
};
// Sumar todas las columnas correspondientes
const totalProgGen521 = computed(() => reportes.value.reduce((total, r) => total + (parseFloat(r.prog_5_21) || 0), 0).toFixed(2));
const totalProgGen523 = computed(() => reportes.value.reduce((total, r) => total + (parseFloat(r.prog_5_23) || 0), 0).toFixed(2));
const totalProgGen526 = computed(() => reportes.value.reduce((total, r) => total + (parseFloat(r.prog_5_26) || 0), 0).toFixed(2));
const totalActGen521 = computed(() => reportes.value.reduce((total, r) => total + (parseFloat(r.act_5_21) || 0), 0).toFixed(2));
const totalActGen523 = computed(() => reportes.value.reduce((total, r) => total + (parseFloat(r.act_5_23) || 0), 0).toFixed(2));
const totalActGen526 = computed(() => reportes.value.reduce((total, r) => total + (parseFloat(r.act_5_26) || 0), 0).toFixed(2));
const totalEjecGen521 = computed(() => reportes.value.reduce((total, r) => total + (parseFloat(r.ejec_5_21) || 0), 0).toFixed(2));
const totalEjecGen523 = computed(() => reportes.value.reduce((total, r) => total + (parseFloat(r.ejec_5_23) || 0), 0).toFixed(2));
const totalEjecGen526 = computed(() => reportes.value.reduce((total, r) => total + (parseFloat(r.ejec_5_26) || 0), 0).toFixed(2));
const totalProgPpto = computed(() => reportes.value.reduce((total, r) => total + (parseFloat(r.prog_ppto) || 0), 0).toFixed(2));
const totalReproPpto = computed(() => reportes.value.reduce((total, r) => total + (parseFloat(r.repro_ppto) || 0), 0).toFixed(2));
const totalEjecPpto = computed(() => reportes.value.reduce((total, r) => total + (parseFloat(r.ejec_ppto) || 0), 0).toFixed(2));

// Sumar los porcentajes de avance
const totalPorcentajeAvance = computed(() => {
  const totalAvance = reportes.value.reduce((total, r) => total + (parseFloat(PorcentajeAvance(r)) || 0), 0);
  return (totalAvance / reportes.value.length).toFixed(2); // Promedio de los porcentajes de avance
});


</script>

<style scoped>
.table input.form-control {
  width: 100px;
}

.badge {
  font-size: 0.8rem;
  padding: 0.5em 1em;
}

.bg-light {
  background-color: #f8f9fa !important;
}

.readonly-cell {
  background-color: #f5e7e7;
  /* Color gris claro */
}
</style>
