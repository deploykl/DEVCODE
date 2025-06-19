<template>
  <main id="main" class="main">
    <p class="h5 text-primary">Actividad:</p>
    <p class="h6 text-secondary">{{ reportes[0]?.actividad_name }}</p>

    <div class="table-responsive">
      <table class="modern-table">
        <thead>
          <tr>
            <th class="month-col">Año</th>
            <th class="month-col">Mes</th>
            <th v-if="isStaff || (isSuperuser && !isStaff)" class="status-col">Campos</th>
            <th class="numeric-col">Prog. Gen. 5.21</th>
            <th class="numeric-col">Prog. Gen. 5.23</th>
            <th class="numeric-col">Prog. Gen. 5.26</th>
            <th class="numeric-col">Prog. PRESUPUESTAL</th>
            <th class="numeric-col">Act. Gen. 5.21</th>
            <th class="numeric-col">Act. Gen. 5.23</th>
            <th class="numeric-col">Act. Gen. 5.26</th>
            <th class="numeric-col">Act. PRESUPUESTAL</th>
            <th class="numeric-col">Ejec. Gen. 5.21</th>
            <th class="numeric-col">Ejec. Gen. 5.23</th>
            <th class="numeric-col">Ejec. Gen. 5.26</th>
            <th class="numeric-col">Ejec. PRESUPUESTAL</th>
            <th class="percent-col">% avance</th>
          </tr>
        </thead>
        <tbody>
          <template v-for="reporte in reportes" :key="reporte.id">
            <tr :class="{
              'current-month': reporte.mes.toUpperCase() === mesActual,
              'previous-month': reporte.mes.toUpperCase() === mesAnterior
            }">
              <td>{{ reporte.year }}</td>
              <td class="month-name">
                <span :class="['badge', reporte.mes.toUpperCase() === mesActual ? 'bg-success' : 'bg-secondary']">
                  {{ reporte.mes }}
                </span>
              </td>

              <td v-if="isStaff || (isSuperuser && !isStaff)" class="toggle-cell">
                <label class="toggle-switch">
                  <input type="checkbox" v-model="reporte.campos_bloqueados" @change="actualizarEstado(reporte)" />
                  <span class="toggle-slider" :class="{ 'active': reporte.campos_bloqueados }"></span>
                  <span class="toggle-label">{{ reporte.campos_bloqueados ? 'Activado' : 'Bloqueado' }}</span>
                </label>
              </td>

              <!-- Campos de Progreso General -->
              <td class="numeric-input">
                <input v-model.number="reporte.prog_5_21" type="text" :disabled="!reporte.campos_bloqueados"
                  @keydown="validarInput">
              </td>
              <td class="numeric-input">
                <input v-model.number="reporte.prog_5_23" type="text" :disabled="!reporte.campos_bloqueados"
                  @keydown="validarInput">
              </td>
              <td class="numeric-input">
                <input v-model.number="reporte.prog_5_26" type="text" :disabled="!reporte.campos_bloqueados"
                  @keydown="validarInput">
              </td>

              <!-- Campo de Prog. PRESUPUESTAL, solo lectura -->
              <td class="numeric-input">
                <input :value="calcularProgPpto(reporte)" type="text" class="readonly-cell" readonly>
              </td>

              <!-- Campos de Actividad General -->
              <td class="numeric-input">
                <input v-model.number="reporte.act_5_21" type="text" :disabled="!reporte.campos_bloqueados"
                  @keydown="validarInput">
              </td>
              <td class="numeric-input">
                <input v-model.number="reporte.act_5_23" type="text" :disabled="!reporte.campos_bloqueados"
                  @keydown="validarInput">
              </td>
              <td class="numeric-input">
                <input v-model.number="reporte.act_5_26" type="text" :disabled="!reporte.campos_bloqueados"
                  @keydown="validarInput">
              </td>
              <td class="numeric-input">
                <input :value="calcularActPpto(reporte)" type="text" class="readonly-cell" readonly>
              </td>

              <!-- Campos de Ejecución General -->
              <td class="numeric-input">
                <input v-model.number="reporte.ejec_5_21" type="text" :disabled="!reporte.campos_bloqueados"
                  @keydown="validarInput">
              </td>
              <td class="numeric-input">
                <input v-model.number="reporte.ejec_5_23" type="text" :disabled="!reporte.campos_bloqueados"
                  @keydown="validarInput">
              </td>
              <td class="numeric-input">
                <input v-model.number="reporte.ejec_5_26" type="text" :disabled="!reporte.campos_bloqueados"
                  @keydown="validarInput">
              </td>
              <td class="numeric-input">
                <input :value="calcularEjecPpto(reporte)" type="text" class="readonly-cell" readonly>
              </td>

              <td class="percent-cell" :class="getTextClassPresupuestal(PorcentajeAvance(reporte))">
                <span :class="getBadgeClassPresupuestal(PorcentajeAvance(reporte))">
                  {{ PorcentajeAvance(reporte) }}%
                </span>
                <span class="ms-2">{{ getMensajeAvancePresupuestal(PorcentajeAvance(reporte)) }}</span>
              </td>
            </tr>

            <!-- Mensaje recordatorio para el mes anterior -->
          <tr v-if="reporte.mes.toUpperCase() === mesAnterior && !reporte.campos_bloqueados"
    class="month-reminder previous-month">
  <td :colspan="isStaff || (isSuperuser && !isStaff) ? 16 : 15" class="reminder-message">
    <i class="fas fa-exclamation-triangle"></i>
    Faltan <strong>{{ diasRestantesMes }}</strong> días de {{ mesActual }} para que se bloquee el reporte
    de {{ reporte.mes.toUpperCase() }}.
  </td>
</tr>
          </template>

          <!-- Fila de totales -->
          <tr class="summary-row">
            <td :colspan="isStaff || (isSuperuser && !isStaff) ? 3 : 2" class="summary-label">Total</td>
            <td class="summary-value">{{ totalProgGen521 }}</td>
            <td class="summary-value">{{ totalProgGen523 }}</td>
            <td class="summary-value">{{ totalProgGen526 }}</td>
            <td class="summary-value">{{ totalProgPpto }}</td>
            <td class="summary-value">{{ totalActGen521 }}</td>
            <td class="summary-value">{{ totalActGen523 }}</td>
            <td class="summary-value">{{ totalActGen526 }}</td>
            <td class="summary-value">{{ totalReproPpto }}</td>
            <td class="summary-value">{{ totalEjecGen521 }}</td>
            <td class="summary-value">{{ totalEjecGen523 }}</td>
            <td class="summary-value">{{ totalEjecGen526 }}</td>
            <td class="summary-value">{{ totalEjecPpto }}</td>
            <td class="summary-percent">{{ totalPorcentajeAvance }}%</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="floating-action-buttons">
      <div class="action-buttons">
        <button @click="guardarTodosRegistros" class="btn-save icon-button" :disabled="loading">
          <i class="fas" :class="loading ? 'fa-spinner fa-spin' : 'fa-save'"></i>
          <span class="button-text">{{ loading ? 'Guardando...' : 'Guardar' }}</span>
        </button>
      </div>
    </div>
  </main>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { api, getAuthToken } from '@/components/services/auth_axios';
import { useRoute } from 'vue-router';
import { SwalSuccess, SwalWarning, SwalDelete, SwalUpdate } from '@/components/widgets/SwalComponent';
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
const isSuperuser = ref(false);
const isStaff = ref(false);

// Obtener mes actual y anterior
const mesActual = computed(() => {
  const fecha = new Date();
  return fecha.toLocaleString('es-ES', { month: 'long' }).toUpperCase();
});

const mesAnterior = computed(() => {
  const fecha = new Date();
  fecha.setMonth(fecha.getMonth() - 1);
  return fecha.toLocaleString('es-ES', { month: 'long' }).toUpperCase();
});

const diasRestantesMes = computed(() => {
  const fechaActual = new Date();
  const ultimoDiaMes = new Date(fechaActual.getFullYear(), fechaActual.getMonth() + 1, 0);
  return Math.ceil((ultimoDiaMes - fechaActual) / (1000 * 60 * 60 * 24));
});

onMounted(() => {
  const superuser = localStorage.getItem('is_superuser');
  const staff = localStorage.getItem('is_staff');

  isSuperuser.value = superuser === 'true';
  isStaff.value = staff === 'true';
});

const actualizarEstado = async (reporte) => {
  // Prevenir desactivar el mes anterior (forzar que permanezca activado/bloqueado según tu lógica)
  if (reporte.mes.toUpperCase() === mesAnterior.value && !reporte.campos_bloqueados) {
    reporte.campos_bloqueados = true; // Forzar a que permanezca activado
    await SwalWarning({
      title: 'Mes anterior protegido',
      text: 'El mes anterior debe permanecer activado'
    });
    return;
  }

  const accessToken = localStorage.getItem('auth_token');
  if (!accessToken) {
    console.error('No se encontró el token de autenticación.');
    return;
  }

  try {
    await api.patch(`poi/reporte-actividad/${reporte.id}/`, 
      { campos_bloqueados: reporte.campos_bloqueados }, 
      {
        headers: {
          Authorization: `Bearer ${accessToken}`,
          'Content-Type': 'application/json'
        }
      }
    );
  } catch (error) {
    console.error('Error al actualizar el estado:', error.response ? error.response.data : error.message);
    reporte.campos_bloqueados = !reporte.campos_bloqueados; // Revertir el cambio visual
  }
};

const LISTAR = async () => {
  try {
    const response = await api.get(`poi/reporte-actividad/?actividad=${route.params.id}`, 
      { headers: { Authorization: `Bearer ${getAuthToken()}` } }
    );
    
    reportes.value = response.data.map(reporte => {
      // Forzar bloqueo para mes anterior
      if (reporte.mes.toUpperCase() === mesAnterior.value) {
        return { ...reporte, campos_bloqueados: false };
      }
      return reporte;
    });
    
  } catch (error) {
    console.error('Error:', error);
  }
};

onMounted(() => {
  LISTAR();
});

const validarInput = (event) => {
  const char = event.key;
  if (!/^\d$/.test(char) && char !== '.' && !["Backspace", "Tab", "ArrowLeft", "ArrowRight"].includes(char)) {
    event.preventDefault();
  }
};

const guardarTodosRegistros = async () => {
  loading.value = true;
  const errores = [];
  const token = getAuthToken();

  try {
    await Promise.all(reportes.value.map(async (reporte) => {
      // Preparar datos para enviar
      const datosActualizar = {
        campos_bloqueados: reporte.campos_bloqueados,
        prog_5_21: reporte.prog_5_21 || 0,
        prog_5_23: reporte.prog_5_23 || 0,
        prog_5_26: reporte.prog_5_26 || 0,
        act_5_21: reporte.act_5_21 || 0,
        act_5_23: reporte.act_5_23 || 0,
        act_5_26: reporte.act_5_26 || 0,
        ejec_5_21: reporte.ejec_5_21 || 0,
        ejec_5_23: reporte.ejec_5_23 || 0,
        ejec_5_26: reporte.ejec_5_26 || 0,
        prog_ppto: calcularProgPpto(reporte),
        repro_ppto: calcularActPpto(reporte),
        ejec_ppto: calcularEjecPpto(reporte)
      };

      try {
        const response = await api.put(
          `poi/reporte-actividad/${reporte.id}/`, 
          datosActualizar,
          { headers: { Authorization: `Bearer ${token}` } }
        );

        const index = reportes.value.findIndex(item => item.id === reporte.id);
        if (index !== -1) {
          reportes.value[index] = response.data;
        }
      } catch (error) {
        errores.push({
          reporteId: reporte.id, 
          error: error.response ? error.response.data : error.message
        });
        console.error('Error en reporte', reporte.id, error.response?.data);
      }
    }));

  } catch (error) {
    console.error('Error inesperado:', error);
  } finally {
    loading.value = false;
    if (errores.length === 0) {
      await SwalUpdate();
    } else {
      await SwalWarning({
        title: 'Error al guardar',
        text: `Hubo errores al guardar ${errores.length} registros. Consulta la consola para más detalles.`
      });
    }
  }
};

const PorcentajeAvance = (reporte) => {
  if (reporte.repro_ppto > 0) {
    return (reporte.ejec_ppto / reporte.repro_ppto * 100).toFixed(2);
  }
  return '0.00';
};

const calcularProgPpto = (reporte) => {
  const prog5_21 = parseFloat(reporte.prog_5_21) || 0;
  const prog5_23 = parseFloat(reporte.prog_5_23) || 0;
  const prog5_26 = parseFloat(reporte.prog_5_26) || 0;
  return (prog5_21 + prog5_23 + prog5_26).toFixed(2);
};

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

// Computed properties para los totales
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

const totalPorcentajeAvance = computed(() => {
  const totalAvance = reportes.value.reduce((total, r) => total + (parseFloat(PorcentajeAvance(r)) || 0), 0);
  return (totalAvance / reportes.value.length).toFixed(2);
});
</script>

<style scoped>
.main {
  padding: 2rem;
  font-family: 'Segoe UI', Roboto, 'Helvetica Neue', sans-serif;
  color: #333;
}

.modern-table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  margin: 1.5rem 0;
}

.modern-table th {
  background-color: #f8f9fa;
  color: #495057;
  font-weight: 600;
  padding: 12px 15px;
  text-align: left;
  border-bottom: 2px solid #dee2e6;
}

.modern-table td {
  padding: 12px 15px;
  border-bottom: 1px solid #eaeaea;
  vertical-align: middle;
}

.month-col {
  width: 100px;
}

.status-col {
  width: 120px;
}

.numeric-col {
  width: 100px;
}

.percent-col {
  width: 120px;
}

.numeric-input input {
  width: 100%;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
  text-align: right;
}

.numeric-input input:disabled {
  background-color: #f5f5f5;
  color: #999;
  cursor: not-allowed;
}

.readonly-cell {
  background-color: #f5f5f5;
  color: #666;
  border: 1px solid #ddd;
  padding: 8px;
  border-radius: 4px;
  text-align: right;
}

.toggle-switch {
  position: relative;
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
}

.toggle-switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

.toggle-slider {
  position: relative;
  width: 40px;
  height: 20px;
  background-color: #ccc;
  border-radius: 20px;
  transition: .3s;
}

.toggle-slider::before {
  content: '';
  position: absolute;
  width: 16px;
  height: 16px;
  border-radius: 50%;
  left: 2px;
  top: 2px;
  background-color: white;
  transition: .3s;
}

.toggle-slider.active {
  background-color: #4CAF50;
}

.toggle-slider.active::before {
  transform: translateX(20px);
}

.toggle-label {
  font-size: 0.85rem;
  color: #555;
}

.previous-month {
  background-color: rgba(103, 58, 183, 0.05);
  position: relative;
}

.previous-month::after {
  content: '';
  position: absolute;
  left: 0;
  bottom: 0;
  width: 100%;
  height: 3px;
  background: linear-gradient(90deg, #673ab7, #b02727);
}

.month-reminder {
  background-color: #fff3f3;
}

.reminder-message {
  padding: 8px;
  font-size: 0.9rem;
  color: #d32f2f;
  text-align: center;
}

.reminder-message i {
  margin-right: 6px;
}

.summary-row {
  background-color: #f8f9fa;
  font-weight: 600;
}

.summary-label {
  text-align: right;
  padding-right: 20px !important;
}

.summary-value {
  text-align: right;
}

.summary-percent {
  font-weight: 600;
  color: #2c3e50;
}

.floating-action-buttons {
  position: fixed;
  right: 20px;
  bottom: 20px;
  z-index: 1000;
}

.action-buttons {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.btn-save {
  background-color: #673ab7;
  color: white;
  border: none;
  border-radius: 50%;
  width: 50px;
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
  transition: all 0.3s;
}

.btn-save:hover {
  background-color: #5e35b1;
  transform: translateY(-2px);
}

.btn-save:disabled {
  background-color: #b39ddb;
  cursor: not-allowed;
}

.icon-button {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
}

.button-text {
  position: absolute;
  white-space: nowrap;
  left: 100%;
  margin-left: 10px;
  background: white;
  padding: 5px 10px;
  border-radius: 4px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  opacity: 0;
  transition: opacity 0.3s;
}

.btn-save:hover .button-text {
  opacity: 1;
}

.percent-cell {
  display: flex;
  align-items: center;
}

.badge {
  padding: 5px 10px;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 500;
}

.bg-success {
  background-color: #4CAF50;
}

.bg-danger {
  background-color: #f44336;
}

.bg-warning {
  background-color: #ff9800;
}

.bg-secondary {
  background-color: #6c757d;
}

.text-success {
  color: #4CAF50;
}

.text-danger {
  color: #f44336;
}

.text-warning {
  color: #ff9800;
}

.text-secondary {
  color: #6c757d;
}

@media (max-width: 1200px) {
  .modern-table {
    display: block;
    overflow-x: auto;
  }
}
</style>