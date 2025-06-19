<template>
  <main id="main" class="container-fluid ">
    <div class="header-section mb-4 border-bottom">
      <p class="activity-name h5 text-secondary">{{ reportes[0]?.actividad_name }}</p>
    </div>

    <div class="table-responsive">
      <table class="table table-bordered table-hover">
        <thead class="table-light">
          <tr>
            <th class="period-col">Periodo</th>
            <th v-if="isStaff || (isSuperuser && !isStaff)" class="status-col">Estado</th>

            <th colspan="4" class="group-header text-center bg-light">Programado</th>
            <th colspan="4" class="group-header text-center bg-light">Reprogramado</th>
            <th colspan="4" class="group-header text-center bg-light">Ejecutado</th>

            <th class="comment-col">Comentario</th>
            <th class="progress-col">Avance</th>
          </tr>

          <tr class="subheaders">
            <th class="period-col"></th>
            <th v-if="isStaff || (isSuperuser && !isStaff)" class="status-col"></th>

            <th class="amount-col">5.21</th>
            <th class="amount-col">5.23</th>
            <th class="amount-col">5.26</th>
            <th class="amount-col">Total</th>

            <th class="amount-col">5.21</th>
            <th class="amount-col">5.23</th>
            <th class="amount-col">5.26</th>
            <th class="amount-col">Total</th>

            <th class="amount-col">5.21</th>
            <th class="amount-col">5.23</th>
            <th class="amount-col">5.26</th>
            <th class="amount-col">Total</th>

            <th class="comment-col"></th>
            <th class="progress-col"></th>
          </tr>
        </thead>

        <tbody>
          <template v-for="reporte in reportes" :key="reporte.id">
            <tr :class="{
              'table-success': reporte.mes.toUpperCase() === mesActual,
              'table-warning': reporte.mes.toUpperCase() === mesAnterior
            }">
              <td class="period-cell">
                <div class="d-flex flex-column align-items-center">
                  <span class="small text-muted">{{ reporte.year }}</span>
                  <span :class="['badge', reporte.mes.toUpperCase() === mesActual ? 'bg-success' : 'bg-secondary']">
                    {{ reporte.mes }}
                  </span>
                </div>
              </td>

              <td v-if="isStaff || (isSuperuser && !isStaff)" class="status-cell">
                <div class="form-check form-switch">
                  <input 
                    class="form-check-input" 
                    type="checkbox" 
                    role="switch" 
                    v-model="reporte.campos_bloqueados" 
                    @change="actualizarEstado(reporte)"
                    :disabled="reporte.mes.toUpperCase() === mesAnterior"
                  >
                  <label class="form-check-label small ms-2">
                    {{ reporte.campos_bloqueados ? 'Activado' : 'Bloqueado' }}
                  </label>
                </div>
              </td>

              <!-- Programado 5.21 -->
              <td class="amount-cell">
                <input 
                  :value="formatInputValue(reporte.prog_5_21)"
                  @input="formatInput($event, 'prog_5_21', reporte)"
                  @blur="formatBlur($event, 'prog_5_21', reporte)"
                  @focus="handleFocus($event)"
                  type="text" 
                  :disabled="!reporte.campos_bloqueados"
                  class="form-control form-control-sm text-end" 
                  :placeholder="getPlaceholder(reporte.prog_5_21)"
                />
              </td>
              
              <!-- Programado 5.23 -->
              <td class="amount-cell">
                <input 
                  :value="formatInputValue(reporte.prog_5_23)"
                  @input="formatInput($event, 'prog_5_23', reporte)"
                  @blur="formatBlur($event, 'prog_5_23', reporte)"
                  @focus="handleFocus($event)"
                  type="text" 
                  :disabled="!reporte.campos_bloqueados"
                  class="form-control form-control-sm text-end" 
                  :placeholder="getPlaceholder(reporte.prog_5_23)"
                />
              </td>
              
              <!-- Programado 5.26 -->
              <td class="amount-cell">
                <input 
                  :value="formatInputValue(reporte.prog_5_26)"
                  @input="formatInput($event, 'prog_5_26', reporte)"
                  @blur="formatBlur($event, 'prog_5_26', reporte)"
                  @focus="handleFocus($event)"
                  type="text" 
                  :disabled="!reporte.campos_bloqueados"
                  class="form-control form-control-sm text-end" 
                  :placeholder="getPlaceholder(reporte.prog_5_26)"
                />
              </td>
              
              <td class="amount-total bg-light fw-bold">
                {{ formatCurrency(calcularProgPpto(reporte)) }}
              </td>

              <!-- Reprogramado 5.21 -->
              <td class="amount-cell">
                <input 
                  :value="formatInputValue(reporte.act_5_21)"
                  @input="formatInput($event, 'act_5_21', reporte)"
                  @blur="formatBlur($event, 'act_5_21', reporte)"
                  @focus="handleFocus($event)"
                  type="text" 
                  :disabled="!reporte.campos_bloqueados"
                  class="form-control form-control-sm text-end" 
                  :placeholder="getPlaceholder(reporte.act_5_21)"
                />
              </td>
              
              <!-- Reprogramado 5.23 -->
              <td class="amount-cell">
                <input 
                  :value="formatInputValue(reporte.act_5_23)"
                  @input="formatInput($event, 'act_5_23', reporte)"
                  @blur="formatBlur($event, 'act_5_23', reporte)"
                  @focus="handleFocus($event)"
                  type="text" 
                  :disabled="!reporte.campos_bloqueados"
                  class="form-control form-control-sm text-end" 
                  :placeholder="getPlaceholder(reporte.act_5_23)"
                />
              </td>
              
              <!-- Reprogramado 5.26 -->
              <td class="amount-cell">
                <input 
                  :value="formatInputValue(reporte.act_5_26)"
                  @input="formatInput($event, 'act_5_26', reporte)"
                  @blur="formatBlur($event, 'act_5_26', reporte)"
                  @focus="handleFocus($event)"
                  type="text" 
                  :disabled="!reporte.campos_bloqueados"
                  class="form-control form-control-sm text-end" 
                  :placeholder="getPlaceholder(reporte.act_5_26)"
                />
              </td>
              
              <td class="amount-total bg-light fw-bold">
                {{ formatCurrency(calcularActPpto(reporte)) }}
              </td>

              <!-- Ejecutado 5.21 -->
              <td class="amount-cell">
                <input 
                  :value="formatInputValue(reporte.ejec_5_21)"
                  @input="formatInput($event, 'ejec_5_21', reporte)"
                  @blur="formatBlur($event, 'ejec_5_21', reporte)"
                  @focus="handleFocus($event)"
                  type="text" 
                  :disabled="!reporte.campos_bloqueados"
                  class="form-control form-control-sm text-end" 
                  :placeholder="getPlaceholder(reporte.ejec_5_21)"
                />
              </td>
              
              <!-- Ejecutado 5.23 -->
              <td class="amount-cell">
                <input 
                  :value="formatInputValue(reporte.ejec_5_23)"
                  @input="formatInput($event, 'ejec_5_23', reporte)"
                  @blur="formatBlur($event, 'ejec_5_23', reporte)"
                  @focus="handleFocus($event)"
                  type="text" 
                  :disabled="!reporte.campos_bloqueados"
                  class="form-control form-control-sm text-end" 
                  :placeholder="getPlaceholder(reporte.ejec_5_23)"
                />
              </td>
              
              <!-- Ejecutado 5.26 -->
              <td class="amount-cell">
                <input 
                  :value="formatInputValue(reporte.ejec_5_26)"
                  @input="formatInput($event, 'ejec_5_26', reporte)"
                  @blur="formatBlur($event, 'ejec_5_26', reporte)"
                  @focus="handleFocus($event)"
                  type="text" 
                  :disabled="!reporte.campos_bloqueados"
                  class="form-control form-control-sm text-end" 
                  :placeholder="getPlaceholder(reporte.ejec_5_26)"
                />
              </td>
              
              <td class="amount-total bg-light fw-bold">
                {{ formatCurrency(calcularEjecPpto(reporte)) }}
              </td>

              <td class="comment-cell">
                <div class="comment-textarea-wrapper">
                  <textarea
                    v-model="reporte.comentario"
                    :disabled="!reporte.campos_bloqueados"
                    class="form-control form-control-sm comment-textarea"
                    placeholder="Escriba su comentario aquí (máx. 500 caracteres)"
                    maxlength="500"
                    rows="3"
                    @input="autoResizeTextarea($event)"
                  ></textarea>
                  <span class="character-counter small text-muted">
                    {{ reporte.comentario ? reporte.comentario.length : 0 }}/500
                  </span>
                </div>
              </td>

              <td class="progress-cell" :class="getTextClassPresupuestal(PorcentajeAvance(reporte))">
                <div class="d-flex flex-column align-items-start">
                  <span :class="getBadgeClassPresupuestal(PorcentajeAvance(reporte))" class="badge mb-1">
                    {{ PorcentajeAvance(reporte) }}%
                  </span>
                  <span class="small text-wrap text-start">
                    {{ getMensajeAvancePresupuestal(PorcentajeAvance(reporte)) }}
                    <span v-if="PorcentajeAvance(reporte) > 100" class="text-dark">(OBSERVADO)</span>
                  </span>
                </div>
              </td>
            </tr>

            <tr v-if="reporte.mes.toUpperCase() === mesAnterior && reporte.campos_bloqueados" class="table-warning">
              <td :colspan="isStaff || (isSuperuser && !isStaff) ? 14 : 13" class="small text-danger">
                <i class="fas fa-exclamation-circle me-2"></i>
                Faltan <strong>{{ diasRestantesMes }}</strong> días de {{ mesActual }} para que se bloquee el reporte
                de {{ reporte.mes.toUpperCase() }}.
              </td>
            </tr>
            <!-- Agrega esto dentro de tu template, preferiblemente al final -->

          </template>

          <tr class="table-primary">
            <td :colspan="isStaff || (isSuperuser && !isStaff) ? 2 : 1" class="fw-bold">TOTALES</td>

            <td class="total-amount fw-bold">{{ formatCurrency(totalProgGen521) }}</td>
            <td class="total-amount fw-bold">{{ formatCurrency(totalProgGen523) }}</td>
            <td class="total-amount fw-bold">{{ formatCurrency(totalProgGen526) }}</td>
            <td class="total-amount fw-bold bg-info">{{ formatCurrency(totalProgPpto) }}</td>

            <td class="total-amount fw-bold">{{ formatCurrency(totalActGen521) }}</td>
            <td class="total-amount fw-bold">{{ formatCurrency(totalActGen523) }}</td>
            <td class="total-amount fw-bold">{{ formatCurrency(totalActGen526) }}</td>
            <td class="total-amount fw-bold bg-info">{{ formatCurrency(totalReproPpto) }}</td>

            <td class="total-amount fw-bold">{{ formatCurrency(totalEjecGen521) }}</td>
            <td class="total-amount fw-bold">{{ formatCurrency(totalEjecGen523) }}</td>
            <td class="total-amount fw-bold">{{ formatCurrency(totalEjecGen526) }}</td>
            <td class="total-amount fw-bold bg-info">{{ formatCurrency(totalEjecPpto) }}</td>

            <td class="total-comment"></td>
            <td class="total-progress fw-bold bg-info">{{ totalPorcentajeAvance }}%</td>
          </tr>
        </tbody>
      </table>
    </div>
<div class="floating-action-buttons">
  <div class="action-buttons">
    <button @click="guardarTodosRegistros" class="btn-save icon-button" :disabled="loading">
      <i class="fas" :class="loading ? 'fa-spinner fa-spin' : 'fa-save'"></i>
      <span class="button-text">{{ loading ? 'Guardando...' : 'Guardar Cambios' }}</span>
    </button>
    <button @click="crearReportesFaltantes" class="btn-update icon-button">
      <i class="fas fa-sync-alt"></i>
      <span class="button-text">Actualizar</span>
    </button>
  </div>
</div>
   
  </main>
</template>

<script setup>
import { ref, onMounted, computed, nextTick } from 'vue';
import { api, getAuthToken } from '@/components/services/auth_axios';
import { useRoute } from 'vue-router';
import { SwalSuccess, SwalWarning, SwalDelete, SwalUpdate } from '@/components/widgets/SwalComponent';
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

// Función para autoajustar altura del textarea
const autoResizeTextarea = (event) => {
  const textarea = event.target;
  textarea.style.height = 'auto';
  textarea.style.height = `${textarea.scrollHeight}px`;
};

// Aplicar autoajuste al montar el componente
onMounted(() => {
  nextTick(() => {
    document.querySelectorAll('.comment-textarea').forEach(textarea => {
      textarea.style.height = 'auto';
      textarea.style.height = `${textarea.scrollHeight}px`;
    });
  });
});

// Función para formatear moneda (para mostrar en totales)
const formatCurrency = (value) => {
  const num = parseFloat(value || 0);
  return new Intl.NumberFormat('es-PE', {
    style: 'currency',
    currency: 'PEN',
    minimumFractionDigits: 2,
    maximumFractionDigits: 2
  }).format(num).replace('PEN', 'S/');
};

// Función simplificada para mostrar valores en inputs
const formatInputValue = (value) => {
  if (value === null || value === undefined || value === '') return '';
  return value; // Mostrar el valor exacto sin formato
};

// Función para manejar el evento input
const formatInput = (event, field, reporte) => {
  // Permitir solo números y un punto decimal
  let value = event.target.value.replace(/[^0-9.]/g, '');
  
  // Manejar múltiples puntos decimales
  const decimalParts = value.split('.');
  if (decimalParts.length > 2) {
    value = decimalParts[0] + '.' + decimalParts.slice(1).join('');
  }
  
  // Guardar el valor sin formato en el modelo
  reporte[field] = value === '' ? null : value;
  
  // Mostrar el valor limpio (sin formato)
  event.target.value = value;
};

// Función para manejar el evento blur (formato final)
const formatBlur = (event, field, reporte) => {
  let value = event.target.value.replace(/[^0-9.]/g, '');
  
  if (value === '') {
    reporte[field] = null;
    event.target.value = '';
    return;
  }
  
  const num = parseFloat(value);
  if (isNaN(num)) {
    reporte[field] = null;
    event.target.value = '';
    return;
  }
  
  // Guardar con 2 decimales
  reporte[field] = num.toFixed(2);
  
  // Aplicar formato visual solo al perder el foco
  event.target.value = num.toLocaleString('es-PE', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
    useGrouping: true
  });
};

// Función para manejar el foco
const handleFocus = (event) => {
  // Al enfocar, mostrar el valor numérico puro sin formato
  const value = event.target.value.replace(/[^0-9.]/g, '');
  event.target.value = value === '' ? '' : value;
  
  // Seleccionar todo el texto para facilitar la edición
  event.target.select();
};

// Función para obtener placeholder
const getPlaceholder = (value) => {
  return value === null || value === undefined || value === '' ? '0.00' : '';
};

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
  LISTAR();
});

const actualizarEstado = async (reporte) => {
  if (reporte.mes.toUpperCase() === mesAnterior.value && !reporte.campos_bloqueados) {
    reporte.campos_bloqueados = true;
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
    reporte.campos_bloqueados = !reporte.campos_bloqueados;
  }
};

const LISTAR = async () => {
  try {
    const response = await api.get(`poi/reporte-actividad/?actividad=${route.params.id}`,
      { headers: { Authorization: `Bearer ${getAuthToken()}` } }
    );

    reportes.value = response.data.map(reporte => {
      if (reporte.mes.toUpperCase() === mesAnterior.value) {
        return { ...reporte, campos_bloqueados: true };
      }
      return reporte;
    });

  } catch (error) {
    console.error('Error:', error);
  }
};

const guardarTodosRegistros = async () => {
  loading.value = true;
  const errores = [];
  const token = getAuthToken();

  try {
    await Promise.all(reportes.value.map(async (reporte) => {
      const datosActualizar = {
        campos_bloqueados: reporte.campos_bloqueados,
        prog_5_21: reporte.prog_5_21 === null ? null : (reporte.prog_5_21 || 0),
        prog_5_23: reporte.prog_5_23 === null ? null : (reporte.prog_5_23 || 0),
        prog_5_26: reporte.prog_5_26 === null ? null : (reporte.prog_5_26 || 0),
        act_5_21: reporte.act_5_21 === null ? null : (reporte.act_5_21 || 0),
        act_5_23: reporte.act_5_23 === null ? null : (reporte.act_5_23 || 0),
        act_5_26: reporte.act_5_26 === null ? null : (reporte.act_5_26 || 0),
        ejec_5_21: reporte.ejec_5_21 === null ? null : (reporte.ejec_5_21 || 0),
        ejec_5_23: reporte.ejec_5_23 === null ? null : (reporte.ejec_5_23 || 0),
        ejec_5_26: reporte.ejec_5_26 === null ? null : (reporte.ejec_5_26 || 0),
        comentario: reporte.comentario || '',
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
#main{
  margin-top: 0;
}
/* Estilos base */
.table {
  font-size: 0.85rem;
  border-collapse: separate;
  border-spacing: 0;
}

.table th, .table td {
  vertical-align: middle;
  padding: 0.5rem;
}

/* Estilos para celdas de montos */
.amount-cell input {
  font-family: 'Courier New', monospace;
  text-align: right;
  direction: ltr;
  unicode-bidi: isolate;
  padding-right: 8px;
  min-width: 80px;
}
.floating-action-buttons {
  position: fixed;
  right: 0;
  top: 50%;
  transform: translateY(-50%);
  z-index: 1000;
  transition: all 0.3s ease;
}

.floating-action-buttons .action-buttons {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  padding: 1rem 0.5rem;
  background: rgba(255, 255, 255, 0.9);
  border-radius: 8px 0 0 8px;
  box-shadow: -2px 0 8px rgba(0, 0, 0, 0.1);
  border: 1px solid #eaeaea;
  border-right: none;
  transition: all 0.3s ease;
}

.icon-button {
  position: relative;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0;
  overflow: hidden;
  transition: all 0.3s ease;
  white-space: nowrap;
  border: none;
  cursor: pointer;
}

.icon-button .button-text {
  position: absolute;
  left: 100%;
  opacity: 0;
  transition: all 0.3s ease;
  pointer-events: none;
  font-size: 0.9rem;
  margin-left: 10px;
}

.icon-button:hover {
  width: auto;
  padding: 0 15px 0 15px;
  border-radius: 20px;
}

.icon-button:hover .button-text {
  opacity: 1;
  left: 40px;
}

.btn-save {
  background-color: #673ab7;
  color: white;
}

.btn-save:hover {
  background-color: #5e35b1;
}

.btn-save:disabled {
  background-color: #b39ddb;
  cursor: not-allowed;
}

.btn-update {
  background-color: #ff9800;
  color: white;
}

.btn-update:hover {
  background-color: #fb8c00;
}

/* Para pantallas pequeñas */
@media (max-width: 768px) {
  .floating-action-buttons {
    position: static;
    transform: none;
    margin-top: 1rem;
  }

  .floating-action-buttons .action-buttons {
    flex-direction: row;
    flex-wrap: wrap;
    justify-content: center;
    padding: 1rem;
    border-radius: 8px;
    border-right: 1px solid #eaeaea;
  }

  .icon-button {
    width: auto;
    padding: 0 15px;
    border-radius: 20px;
  }

  .icon-button .button-text {
    position: static;
    opacity: 1;
    margin-left: 8px;
  }

  .icon-button:hover {
    padding: 0 15px;
  }
}
.amount-cell input:focus {
  background-color: #fff8e1;
  border-color: #ffc107;
  box-shadow: 0 0 0 0.25rem rgba(255, 193, 7, 0.25);
}

.amount-cell input::placeholder {
  text-align: right;
  opacity: 0.5;
}

/* Estilos para el textarea de comentarios */
.comment-textarea-wrapper {
  position: relative;
  min-width: 200px;
}

.comment-textarea {
  resize: none;
  overflow-y: hidden;
  min-height: 38px;
  transition: all 0.3s ease;
  font-size: 0.85rem;
  padding-right: 30px;
}

.comment-textarea:focus {
  border-color: #86b7fe;
  box-shadow: 0 0 0 0.25rem rgba(13, 110, 253, 0.25);
}

.character-counter {
  position: absolute;
  bottom: 2px;
  right: 5px;
  background-color: rgba(255, 255, 255, 0.8);
  padding: 0 3px;
  border-radius: 3px;
  font-size: 0.7rem;
}

/* Estilos para celdas de progreso */
.progress-cell {
  min-width: 180px;
}

.badge {
  font-size: 0.75rem;
  padding: 0.35em 0.65em;
  font-weight: 500;
}

/* Colores de filas */
.table-success td {
  background-color: rgba(25, 135, 84, 0.05);
}

.table-warning td {
  background-color: rgba(255, 193, 7, 0.05);
}

/* Estilo para el switch */
.form-switch .form-check-input {
  width: 2.5em;
  height: 1.3em;
  cursor: pointer;
}

.form-switch .form-check-input:checked {
  background-color: #198754;
  border-color: #198754;
}

/* Estilos para totales */
.total-amount, .amount-total {
  background-color: #f8f9fa;
}

.table-primary td {
  background-color: #e7f1ff;
  font-weight: bold;
}

/* Estilos responsivos */
@media (max-width: 1200px) {
  .table {
    font-size: 0.8rem;
  }
  
  .comment-textarea {
    min-width: 150px;
  }
}

@media (max-width: 992px) {
  .table-responsive {
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
  }
  
  .comment-textarea {
    min-width: 120px;
  }
  
  .progress-cell {
    min-width: 160px;
  }
}

@media (max-width: 768px) {
  .header-section {
    text-align: center;
  }
  
  .comment-textarea {
    min-width: 100px;
  }
  
  .progress-cell {
    min-width: 140px;
  }
}

/* Animaciones y transiciones */
.table-hover tbody tr {
  transition: background-color 0.2s ease;
}

.btn-primary {
  transition: all 0.3s ease;
  padding: 0.5rem 1.5rem;
  font-weight: 500;
}

.btn-primary:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

/* Estilo para inputs numéricos */
input[type="text"].form-control-sm.text-end {
  font-family: monospace;
  letter-spacing: 0.5px;
  transition: all 0.3s ease;
}

/* Mejoras visuales para los headers */
.group-header {
  position: relative;
}

.group-header:after {
  content: "";
  position: absolute;
  bottom: -1px;
  left: 0;
  right: 0;
  height: 2px;
  background-color: #dee2e6;
}

.subheaders th {
  font-weight: normal;
  font-size: 0.8rem;
  color: #6c757d;
}

/* Efecto hover para filas */
.table-hover tbody tr:hover {
  background-color: rgba(0, 0, 0, 0.02);
}

/* Estilo para el botón de guardar */
.btn-primary:disabled {
  opacity: 0.7;
  transform: none;
  box-shadow: none;
}

.fa-spinner {
  margin-right: 8px;
}
</style>