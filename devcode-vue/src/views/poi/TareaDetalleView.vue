<template>
  <main id="main" class="main-container">
    <div v-if="tarea" class="task-details">
      <div class="task-header">
        <span class="activity-name">AO - {{ tarea.actividad_name }}</span>
        <h1 class="task-title">Tarea - {{ tarea.name }}</h1>
        <div class="task-meta">
          <div class="meta-item">
            <span class="meta-label">Criterio de reprogramación:</span>
            <span class="meta-value">{{ tarea.criterio }}</span>
          </div>
          <div class="meta-item">
            <span class="meta-label">Definición operacional:</span>
            <span class="meta-value">{{ tarea.definicion }}</span>
          </div>
        </div>
      </div>

      <div class="table-responsive">
        <table class="modern-table">
          <thead>
            <tr>
              <th class="month-col">Mes</th>
              <th v-if="isStaff || (isSuperuser && !isStaff)" class="status-col">Campos</th>
              <th v-if="isStaff || (isSuperuser && !isStaff)" class="numeric-col">Prog. Física</th>
              <th class="numeric-col">Act. Física</th>
              <th class="numeric-col">Ejec. Física</th>
              <th class="percent-col">% Física</th>
              <th class="status-col">Estado</th>
              <th class="comment-col">Sustento</th>
              <th class="comment-col">Alerta</th>
              <th class="comment-col">Recomendaciones</th>
              <th class="action-col">Registrar Sustento</th>
            </tr>
          </thead>
          <tbody>
            <template v-for="(reporte) in reportes" :key="reporte.id">
              <tr :class="{ 'current-month': reporte.mes.toUpperCase() === mesActual }">
                <td class="month-name">{{ reporte.mes }}</td>

                <td v-if="isStaff || (isSuperuser && !isStaff)" class="toggle-cell">
                  <label class="toggle-switch">
                    <input type="checkbox" v-model="reporte.campos_bloqueados" @change="actualizarEstado(reporte)" />
                    <span class="toggle-slider" :class="{ 'active': reporte.campos_bloqueados }"></span>
                    <span class="toggle-label">{{ reporte.campos_bloqueados ? 'Activado' : 'Desactivado' }}</span>
                  </label>
                </td>

                <td v-if="isStaff || (isSuperuser && !isStaff)" class="numeric-input">
                  <input v-model.number="reporte.prog_fisica" type="text" :disabled="!reporte.campos_bloqueados"
                    @keydown="validarInput" maxlength="3" />
                </td>

                <td class="numeric-input">
                  <input v-model.number="reporte.repro_fisica" type="text"
                    :disabled="!reporte.campos_bloqueados || !isSuperuser" maxlength="3" />
                </td>

                <td class="numeric-input">
                  <input v-model.number="reporte.ejec_fisica" type="text" :disabled="!reporte.campos_bloqueados"
                    @input="validarEjecucionFisica(reporte)" maxlength="3" />
                </td>

                <td class="percent-cell">
                  <span class="percent-badge" :class="getBadgeClass(reporte)">
                    {{ calcularPorcentajeFisica(reporte) }}%
                  </span>
                </td>

                <td class="status-cell" :class="calcularSustento(reporte).class">
                  {{ calcularSustento(reporte).text || 'Sin información' }}
                </td>

                <td class="comment-cell">
                  <div class="textarea-container">
                    <textarea v-model="reporte.comentario" :disabled="!reporte.campos_bloqueados" maxlength="500"
                      placeholder="Ingrese el sustento..." rows="3"></textarea>
                    <span class="char-counter">{{ reporte.comentario ? reporte.comentario.length : 0 }}/500</span>
                  </div>
                </td>

                <td class="comment-cell">
                  <div class="textarea-container">
                    <textarea v-model="reporte.alerta" :disabled="!reporte.campos_bloqueados" maxlength="500"
                      placeholder="Ingrese alertas..." rows="3"></textarea>
                    <span class="char-counter">{{ reporte.alerta ? reporte.alerta.length : 0 }}/500</span>
                  </div>
                </td>

                <td class="comment-cell">
                  <div class="textarea-container">
                    <textarea v-model="reporte.recomendaciones" :disabled="!reporte.campos_bloqueados" maxlength="500"
                      placeholder="Ingrese recomendaciones..." rows="3"></textarea>
                    <span class="char-counter">{{ reporte.recomendaciones ? reporte.recomendaciones.length : 0
                    }}/500</span>
                  </div>
                </td>

                <td class="action-cell">
                  <router-link v-if="reporte.campos_bloqueados"
                    :to="{ name: 'upload', params: { mes: reporte.mes, reporteId: reporte.id } }" class="upload-btn"
                    title="Subir sustento">
                    <i class="fas fa-cloud-upload-alt"></i>
                  </router-link>
                  <button v-else class="upload-btn disabled" disabled>
                    <i class="fas fa-cloud-upload-alt"></i>
                  </button>
                </td>
              </tr>

              <tr v-if="reporte.mes.toUpperCase() === mesActual && reporte.campos_bloqueados" class="month-reminder">
                <td :colspan="isStaff || (isSuperuser && !isStaff) ? 11 : 10" class="reminder-message">
                  <i class="fas fa-clock"></i> Días restantes para el final del mes: <strong>{{ diasRestantesMes
                  }}</strong>
                </td>
              </tr>
            </template>

            <tr class="summary-row">
              <td :colspan="isStaff || (isSuperuser && !isStaff) ? 2 : 1" class="summary-label">Total</td>
              <td v-if="isStaff || (isSuperuser && !isStaff)" class="summary-value">{{ totalProgFisica }}</td>
              <td class="summary-value">{{ totalReproFisica }}</td>
              <td class="summary-value">{{ totalEjecFisica }}</td>
              <td class="summary-percent">{{ totalPorcentajeFisica }}%</td>
              <td colspan="5"></td>
            </tr>
          </tbody>
        </table>
      </div>

      <div class="floating-action-buttons">
        <div class="action-buttons">
          <button @click="guardarTodosRegistros" class="btn-save icon-button" :disabled="loading">
            <i class="fas" :class="loading ? 'fa-spinner fa-spin' : 'fa-save'"></i>
            <span class="button-text">{{ loading ? 'Guardando...' : '' }}</span>
          </button>
          <button @click="crearReportesFaltantes" class="btn-update icon-button">
            <i class="fas fa-sync-alt"></i>
            <span class="button-text"></span>
          </button>
        </div>
      </div>
    </div>

    <div v-else class="loading-state">
      <div class="spinner"></div>
      <p>Cargando detalles de la tarea...</p>
    </div>
  </main>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRoute } from 'vue-router';
import { api, getAuthToken } from '@/components/services/auth_axios';
import { SwalSuccess, SwalWarning, SwalDelete, SwalUpdate } from '@/components/widgets/SwalComponent'; // Asegúrate de que la ruta sea correcta

const isSuperuser = ref(false);
const isStaff = ref(false);

onMounted(() => {
  const superuser = localStorage.getItem('is_superuser');
  const staff = localStorage.getItem('is_staff');

  isSuperuser.value = superuser === 'true';
  isStaff.value = staff === 'true';
});

const reportes = ref([]);
const tarea = ref(null);
const loading = ref(false);
const route = useRoute();

const validarInput = (event) => {
  const char = event.key;

  // Permitir solo números y las teclas de control
  if (!/^\d$/.test(char) && !["Backspace", "Tab", "ArrowLeft", "ArrowRight"].includes(char)) {
    event.preventDefault(); // Prevenir la entrada del carácter no deseado
  }
};

const validarEjecucionFisica = (reporte) => {

  // Validación adicional: asegurarse de que ambos valores sean números positivos
  if (reporte.ejec_fisica < 0 || reporte.repro_fisica < 0) {
    //alert('Los valores deben ser números positivos.');
    // Puedes restablecer los valores a 0 o a un valor predeterminado aquí
  }
};

const mesActual = computed(() => {
  const fecha = new Date();
  return fecha.toLocaleString('es-ES', { month: 'long' }).toUpperCase();
});

const diasRestantesMes = computed(() => {
  const fechaActual = new Date();
  const ultimoDiaMes = new Date(fechaActual.getFullYear(), fechaActual.getMonth() + 1, 0);
  return Math.ceil((ultimoDiaMes - fechaActual) / (1000 * 60 * 60 * 24));
});

onMounted(async () => {
  const accessToken = localStorage.getItem('auth_token');
  if (!accessToken) {
    console.error('No se encontró el token de autenticación.');
    return;
  }

  try {
    const tareaId = route.params.id;
    const response = await api.get(`poi/tarea/${tareaId}/`, {
      headers: {
        Authorization: `Bearer ${accessToken}`
      }
    });
    tarea.value = response.data;
    reportes.value = response.data.mes || [];
    // Crear reportes faltantes automáticamente al cargar la tarea
    //await crearReportesFaltantes();
    reportes.value.forEach(reporte => {
      reporte.campos_bloqueados = reporte.mes.toUpperCase() === mesActual.value ? true : reporte.campos_bloqueados;
    });
  } catch (error) {
    console.error('Error al obtener los detalles de la tarea:', error.response ? error.response.data : error.message);
  }
});

// Función modificada para manejar correctamente el caso cuando repro_fisica es 0
const calcularPorcentajeFisica = (reporte) => {
  if (reporte.repro_fisica === 0) {
    return reporte.ejec_fisica > 0 ? 'N/A' : '0.00'; // MP = Mala Programación
  }
  return (reporte.ejec_fisica / reporte.repro_fisica * 100).toFixed(2);
};

// Función de sustento actualizada
// Función de sustento actualizada
const calcularSustento = (reporte) => {
  let sustento = { 
    text: '', 
    class: '', 
    porcentaje: calcularPorcentajeFisica(reporte),
    esValido: true
  };

  if (reporte.repro_fisica === 0) {
    if (reporte.ejec_fisica > 0) {
      sustento.text = 'Ejecución no programada'; // Cambiado aquí
      sustento.class = 'text-info';
      sustento.esValido = false;
    } else {
      sustento.text = 'No programado';
      sustento.class = 'text-secondary';
    }
  } else if (reporte.ejec_fisica > reporte.repro_fisica) {
    sustento.text = 'Exceso de ejecución 🤔';
    sustento.class = 'text-dark';
  } else if (reporte.repro_fisica > reporte.ejec_fisica) {
    sustento.text = 'Déficit de ejecución';
    sustento.class = 'text-danger';
  } else if (calcularPorcentajeFisica(reporte) === '100.00') {
    sustento.text = 'Bueno';
    sustento.class = 'text-success';
  }

  return sustento;
};

const getBadgeClass = (reporte) => {
  const porcentaje = calcularPorcentajeFisica(reporte);
  
  if (reporte.repro_fisica === 0 && reporte.ejec_fisica > 0) {
    return 'bg-info'; // Para "Mala programación"
  } else if (reporte.repro_fisica > reporte.ejec_fisica) {
    return 'bg-danger';
  } else if (porcentaje === '100.00') {
    return 'bg-success';
  } else if (porcentaje.includes('MP')) {
    return 'bg-danger'; // Clase para "Mala programación"
  } else {
    return 'bg-dark';
  }
};


const actualizarEstado = async (reporte) => {
  const accessToken = localStorage.getItem('auth_token');
  if (!accessToken) {
    console.error('No se encontró el token de autenticación.');
    return;
  }

  try {
    await api.patch(`poi/reporte-tarea/${reporte.id}/`, { campos_bloqueados: reporte.campos_bloqueados }, {
      headers: {
        Authorization: `Bearer ${accessToken}`,
        'Content-Type': 'application/json'
      }
    });
  } catch (error) {
    console.error('Error al actualizar el estado:', error.response ? error.response.data : error.message);
  }
};

const guardarRegistro = async (reporte) => {
  const accessToken = localStorage.getItem('auth_token');
  if (!accessToken) {
    console.error('No se encontró el token de autenticación.');
    return 'No se encontró el token de autenticación.';
  }

  // Calcular el sustento antes de guardar
  const sustento = calcularSustento(reporte);

  // Solo asignar sustento si es válido
  if (sustento && sustento.text) {
    reporte.sustento = sustento.text; // Asigna solo el texto
  } else {
    delete reporte.sustento; // Elimina la propiedad si no es válida
  }

  try {
    await api.put(`poi/reporte-tarea/${reporte.id}/`, reporte, {
      headers: {
        Authorization: `Bearer ${accessToken}`,
        'Content-Type': 'application/json'
      }
    });
  } catch (error) {
    console.error('Error al guardar el registro:', error.response ? error.response.data : error.message);
    return 'Error al guardar el registro.';
  }
};


const guardarTodosRegistros = async () => {
  loading.value = true;

  for (const reporte of reportes.value) {
    await guardarRegistro(reporte);
  }
  SwalUpdate();
  loading.value = false;
};

const totalProgFisica = computed(() => {
  return reportes.value.reduce((acc, reporte) => acc + (reporte.prog_fisica || 0), 0);
});

const totalReproFisica = computed(() => {
  return reportes.value.reduce((acc, reporte) => acc + (reporte.repro_fisica || 0), 0);
});

const totalEjecFisica = computed(() => {
  return reportes.value.reduce((acc, reporte) => acc + (reporte.ejec_fisica || 0), 0);
});

const totalPorcentajeFisica = computed(() => {
  const reproTotal = totalReproFisica.value;
  return reproTotal > 0 ? ((totalEjecFisica.value / reproTotal) * 100).toFixed(2) : 0;
});

const crearReportesFaltantes = async () => {
  const accessToken = localStorage.getItem('auth_token');
  if (!accessToken) {
    console.error('No se encontró el token de autenticación.');
    return;
  }

  try {
    const tareaId = route.params.id;  // Obtener el ID de la tarea desde la URL
    await api.post(`poi/tarea/${tareaId}/crear-reportes-faltantes/`, null, {
      headers: {
        Authorization: `Bearer ${accessToken}`
      }
    });
    alert('Reportes faltantes creados o actualizados correctamente');
  } catch (error) {
    console.error('Error al crear los reportes faltantes:', error.response ? error.response.data : error.message);
    alert('Error al crear los reportes faltantes');
  }
};

</script>


<style scoped>
#main {
  margin-top: 0;
}

/* Estilos generales */
.main-container {
  padding: 2rem;
  font-family: 'Segoe UI', Roboto, 'Helvetica Neue', sans-serif;
  color: #333;
}

.task-details {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  padding: 2rem;
}

.task-header {
  margin-bottom: 2rem;
  padding-bottom: 1.5rem;
  border-bottom: 1px solid #eaeaea;
}

.task-title {
  font-size: 1.8rem;
  color: #2c3e50;
  margin-bottom: 1rem;
  font-weight: 600;
}

.task-meta {
  display: flex;
  flex-direction: column;
  gap: 0.8rem;
}

.meta-item {
  display: flex;
  gap: 0.5rem;
}

.meta-label {
  font-weight: 600;
  color: #555;
}

.meta-value {
  color: #666;
}

/* Tabla moderna */
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

.modern-table tr:last-child td {
  border-bottom: none;
}

.modern-table tr:hover td {
  background-color: #f8f9fa;
}

/* Columnas específicas */
.month-col {
  width: 120px;
}

.status-col {
  width: 100px;
}

.numeric-col {
  width: 80px;
}

.percent-col {
  width: 90px;
}

.comment-col {
  min-width: 150px;
}

.action-col {
  width: 100px;
}

/* Estilo para el mes actual */
.current-month {
  background-color: rgba(103, 58, 183, 0.05);
  position: relative;
}

.current-month::after {
  content: '';
  position: absolute;
  left: 0;
  bottom: 0;
  width: 100%;
  height: 3px;
  background: linear-gradient(90deg, #673ab7, #9c27b0);
}

.month-name {
  font-weight: 500;
  color: #2c3e50;
}

/* Toggle switch */
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

/* Inputs */
.numeric-input input,
.comment-input input {
  width: 100%;
  padding: 8px 10px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 0.9rem;
  transition: border 0.2s;
}

.numeric-input input {
  text-align: center;
  max-width: 60px;
}

.numeric-input input:focus,
.comment-input input:focus {
  border-color: #673ab7;
  outline: none;
  box-shadow: 0 0 0 2px rgba(103, 58, 183, 0.2);
}

.numeric-input input:disabled,
.comment-input input:disabled {
  background-color: #f5f5f5;
  color: #999;
  cursor: not-allowed;
}

/* Badges */
.percent-badge {
  display: inline-block;
  padding: 5px 10px;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 500;
  color: white;
}

.bg-success {
  background-color: #4CAF50;
}

.bg-danger {
  background-color: #f44336;
}

.bg-dark {
  background-color: #333;
}

.bg-secondary {
  background-color: #6c757d;
}

/* Status cell */
.status-cell {
  font-size: 0.9rem;
  font-weight: 500;
}

.text-success {
  color: #4CAF50;
}

.text-danger {
  color: #f44336;
}

.text-secondary {
  color: #6c757d;
}

/* Botón de upload */
.upload-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background-color: #673ab7;
  color: white;
  border: none;
  cursor: pointer;
  transition: all 0.2s;
}

.upload-btn:hover {
  background-color: #5e35b1;
  transform: translateY(-1px);
}

.upload-btn.disabled {
  background-color: #b0bec5;
  cursor: not-allowed;
}

.upload-btn i {
  font-size: 1rem;
}

/* Recordatorio de mes */
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

/* Fila de resumen */
.summary-row {
  background-color: #f8f9fa;
  font-weight: 600;
}

.summary-label {
  text-align: right;
  padding-right: 20px !important;
}

.summary-value {
  text-align: center;
}

.summary-percent {
  font-weight: 600;
  color: #2c3e50;
}

/* Botones de acción */
.action-buttons {
  display: flex;
  gap: 1rem;
  margin-top: 2rem;
  flex-wrap: wrap;
}

.btn-save,
.btn-update {
  padding: 10px 20px;
  border-radius: 6px;
  font-weight: 500;
  border: none;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  transition: all 0.2s;
}

.btn-save {
  background-color: #673ab7;
  color: white;
}

.btn-save:hover {
  background-color: #5e35b1;
  box-shadow: 0 2px 8px rgba(103, 58, 183, 0.3);
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
  box-shadow: 0 2px 8px rgba(255, 152, 0, 0.3);
}

/* Estado de carga */
.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 200px;
  gap: 1rem;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid rgba(103, 58, 183, 0.1);
  border-radius: 50%;
  border-top-color: #673ab7;
  animation: spin 1s ease-in-out infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

/* Responsive */
@media (max-width: 1200px) {
  .modern-table {
    display: block;
    overflow-x: auto;
  }

  .action-buttons {
    flex-direction: column;
  }

  .btn-save,
  .btn-update {
    width: 100%;
    justify-content: center;
  }
}

/* Estilos mejorados para los campos de texto */
.comment-cell {
  min-width: 250px;
  max-width: 300px;
  vertical-align: top;
}

.textarea-container {
  position: relative;
  display: flex;
  flex-direction: column;
}

textarea {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-family: inherit;
  font-size: 0.9rem;
  resize: vertical;
  min-height: 80px;
  transition: all 0.2s;
}

textarea:focus {
  border-color: #673ab7;
  outline: none;
  box-shadow: 0 0 0 2px rgba(103, 58, 183, 0.2);
}

textarea:disabled {
  background-color: #f5f5f5;
  color: #999;
  cursor: not-allowed;
}

.char-counter {
  font-size: 0.75rem;
  color: #666;
  text-align: right;
  margin-top: 4px;
}

/* Ajustes responsive */
@media (max-width: 1200px) {
  .comment-cell {
    min-width: 200px;
  }
}

@media (max-width: 992px) {
  .comment-cell {
    min-width: 180px;
  }

  textarea {
    min-height: 60px;
  }
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
  gap: 2rem;
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
}

.icon-button .button-text {
  position: absolute;
  left: 100%;
  opacity: 0;
  transition: all 0.3s ease;
  pointer-events: none;
}

.icon-button:hover {
  width: auto;
  padding: 0 10px 0 20px;
  border-radius: 20px;
}

.icon-button:hover .button-text {
  opacity: 1;
  left: 40px;
}


/* Efecto hover para el contenedor */
.floating-action-buttons:hover {
  right: 0;
  background: white;
  padding-right: 10px;
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
</style>