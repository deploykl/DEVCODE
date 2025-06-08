<template>
  <main id="main" class="main">
    <div class="card">
      <div class="card-body mt-2">
        <button type="button" class="btn btn-success float-start mt-2" @click="openModal">
          <i class="fa-solid fa-circle-plus"></i> Agregar
        </button>
        <TableComponent :headers="[
          { key: 'codigo', label: 'CÓDIGO', filterable: false },
          { key: 'name', label: 'ACTIVIDAD', filterable: false },
          { key: 'grupo_name', label: 'GRUPO', filterable: true },
          { key: 'estado', label: 'ESTADO', filterable: true },
          { key: 'dependencia_name', label: 'CENTRO DE COSTO', filterable: true },
          { key: 'medida_name', label: 'MEDIDA', filterable: true }
        ]" :items="actividades" @edit="UPDATE_ID" @delete="DELETE" @delete-multiple="ELIMINARMULTIPLE" />
      </div>
    </div>

    <!-- Modal para Agregar/Editar Actividad -->
    <div class="modal fade" id="addActivityModal" tabindex="-1" aria-labelledby="addActivityModalLabel"
      aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="addActivityModalLabel">{{ isEditing ? 'Editar Actividad' : 'Agregar Actividad'
              }}</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"
              @click="resetForm"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="isEditing ? UPDATE() : ADD()">
              <div class="mb-3">
                <label for="codigo" class="form-label">Código</label>
                <input type="text" class="form-control" id="codigo" v-model="form.codigo">
              </div>
              <div class="mb-3">
                <label for="name" class="form-label">Nombre</label>
                <textarea class="form-control" id="name" v-model="form.name" rows="4" required></textarea>
              </div>
              <div class="mb-3">
                <label for="grupo" class="form-label">Grupo</label>
                <select class="form-select" id="grupo" v-model="form.grupo">
                  <option disabled value="">-- Elija una opción --</option>
                  <option v-for="gru in grupos" :key="gru.id" :value="gru.id">{{ gru.name }}</option>
                </select>
              </div>
              <div class="mb-3">
                <label for="estado" class="form-label">Estado</label>
                <select class="form-select" id="estado" v-model="form.estado" required>
                  <option disabled value="">-- Elija una opción --</option>
                  <option :value="true">Activo</option>
                  <option :value="false">Inactivo</option>
                </select>
              </div>
              <div class="mb-3">
                <label for="dependencia" class="form-label">Dependencia</label>
                <select class="form-select" id="dependencia" v-model="form.dependencia" required>
                  <option disabled value="">-- Elija una opción --</option>
                  <option v-for="dep in dependencias" :key="dep.id" :value="dep.id">{{ dep.name }}</option>
                </select>
              </div>
              <div class="mb-3">
                <label for="medida" class="form-label">Medida</label>
                <select class="form-select" id="medida" v-model="form.medida" required>
                  <option disabled value="">-- Elija una opción --</option>
                  <option v-for="med in medidas" :key="med.id" :value="med.id">{{ med.codigo }} - {{ med.name }}
                  </option>
                </select>
              </div>
              <button type="submit" class="btn btn-primary">{{ isEditing ? 'Actualizar' : 'Agregar' }}</button>
            </form>
          </div>
        </div>
      </div>
    </div>
  </main>
</template>

<script setup>
import { onMounted, ref } from 'vue';
import { api, getAuthToken } from '@/components/services/auth_axios';
import { SwalSuccess, SwalWarning, SwalDelete, SwalUpdate } from '@/components/widgets/SwalComponent'; // Asegúrate de que la ruta sea correcta

import TableComponent from '@/components/TableComponent.vue';
import * as bootstrap from 'bootstrap';

// -------------------- State Variables --------------------
const dependencias = ref([]);
const medidas = ref([]); 
const actividades = ref([]);
const grupos = ref([]);

const isEditing = ref(false);

// Valores predeterminados del formulario
const defaultFormValues = {
  codigo: '',
  name: '',
  estado: '',
  dependencia: '',
  medida: '',
  grupo: '',
};

// Inicializa el formulario con los valores predeterminados
const form = ref({ ...defaultFormValues });

// Función para restablecer el formulario usando los valores predeterminados
const resetForm = () => {
  form.value = { ...defaultFormValues };
};

const openModal = () => {
  isEditing.value = false;

  const modalElement = document.getElementById('addActivityModal');
  if (modalElement) {
    const modal = new bootstrap.Modal(modalElement);
    modal.show();
  }
};

const LISTAR = async () => {
  try {
    const token = getAuthToken();
    // Ejecutar todas las solicitudes en paralelo
    const [responseDependencias, responseMedidas, responseActividades, responseGrupo] = await Promise.all([
      api.get('personal/dependencia/', { headers: { Authorization: `Bearer ${token}` } }),
      api.get('poi/medida-actividad/', { headers: { Authorization: `Bearer ${token}` } }),
      api.get('poi/actividad/', { headers: { Authorization: `Bearer ${token}` } }),
      api.get('poi/grupo/', { headers: { Authorization: `Bearer ${token}` } }),
    ]);

    // Asignar los datos de las respuestas
    dependencias.value = responseDependencias.data;
    medidas.value = responseMedidas.data;
    actividades.value = responseActividades.data.activities;
    grupos.value = responseGrupo.data;

    // Verificar que group_name esté presente en cada actividad
    console.log(actividades.value);

  } catch (error) {
    console.error('Error al obtener los datos:', error.response ? error.response.data : error.message);
  }
};

onMounted(() => {
  LISTAR();
});

const ADD = async () => {
  try {
    const token = getAuthToken();

    const response = await api.post('poi/actividad/', form.value, {
      headers: { Authorization: `Bearer ${token}` }
    });    
    // Agregar la nueva actividad a la lista
    actividades.value.push(response.data);

    // Cerrar el modal y resetear el formulario
    const modal = bootstrap.Modal.getInstance(document.getElementById('addActivityModal'));
    modal.hide();
    resetForm();

    await SwalSuccess();

  } catch (error) {
    console.error('Error al agregar:', error.response ? error.response.data : error.message);
  }
};

const UPDATE_ID = (actividad) => {
  isEditing.value = true;
  Object.assign(form.value, actividad); // Copiar directamente los valores al form
  new bootstrap.Modal('#addActivityModal').show(); // Inicializar y mostrar el modal de manera más compacta
};

const UPDATE = async () => {
  try {
    const { id, dependencia, medida, grupo, ...rest } = form.value;

    const token = getAuthToken();
    const response = await api.put(`poi/actividad/${id}/`, {
      ...rest,
      dependencia,
      medida,
      grupo,
    }, {
      headers: { Authorization: `Bearer ${token}` },
    });

    // Actualiza la actividad en la lista
    const index = actividades.value.findIndex(actividad => actividad.id === id);
    actividades.value[index] = response.data;

    // Cierra el modal y reinicia el formulario
    bootstrap.Modal.getInstance(document.getElementById('addActivityModal')).hide();
    resetForm();

    await SwalUpdate();

  } catch (error) {
    console.error('Error al actualizar:', error.response ? error.response.data : error.message);
  }
};

const DELETE = async (id) => {
  try {
    const result = await SwalWarning();

    if (result.isConfirmed) {
      const token = getAuthToken();

      await api.delete(`poi/actividad/${id}/`, {
        headers: { Authorization: `Bearer ${token}` },
      });

      // Filtrar la actividad eliminada
      actividades.value = actividades.value.filter(actividad => actividad.id !== id);

      // Mostrar mensaje de éxito
      await SwalDelete();
    }
  } catch (error) {
    console.error('Error al eliminar:', error.response?.data || error.message);
  }
};

const ELIMINARMULTIPLE = async (selectedIds) => {
  try {
    const result = await SwalWarning();

    if (result.isConfirmed) {
      const token = getAuthToken();

      await api.post('poi/actividad/bulk-delete/', { ids: selectedIds }, {
        headers: { Authorization: `Bearer ${token}` },
      });

      // Filtrar las actividades eliminadas
      actividades.value = actividades.value.filter(actividad => !selectedIds.includes(actividad.id));

      // Mostrar mensaje de éxito
      await SwalDelete();
    }
  } catch (error) {
    console.error('Error al eliminar múltiples elementos:', error.response?.data || error.message);
  }
};
</script>
