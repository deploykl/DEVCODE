<template>
  <main id="main" class="main">
    <div class="card">
      <div class="card-body mt-2">
        <button type="button" class="btn btn-success float-start mt-1" @click="openModal">
          <i class="fa-solid fa-circle-plus"></i> Agregar
        </button>
        <TableComponent :headers="[
          { key: 'codigo', label: 'Código', filterable: false },
          { key: 'name', label: 'Nombre', filterable: false },
        ]" :items="MedidaActividad" :columnStyles="{
          'name': 'col-8',
          'codigo': 'col-1',
        }" @edit="UPDATE_ID" @delete="DELETE" @delete-multiple="ELIMINARMULTIPLE" />
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
                <input type="text" class="form-control" id="name" v-model="form.name" rows="4" required></input>
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

const MedidaActividad = ref([]);
const isEditing = ref(false);

const defaultFormValues = {
  codigo: '',
  name: '',
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

    // Ejecutar la solicitud de medida-actividad
    const responseMedidaActividad = await api.get('poi/medida-actividad/', { headers: { Authorization: `Bearer ${token}` } });

    // Asignar los datos de la respuesta
    MedidaActividad.value = responseMedidaActividad.data; // Ajusta según la estructura real de la respuesta

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
    const response = await api.post('poi/medida-actividad/', form.value, { headers: { Authorization: `Bearer ${token}` } });

    MedidaActividad.value.push(response.data);

    const modal = bootstrap.Modal.getInstance(document.getElementById('addActivityModal'));
    modal.hide();
    resetForm();

    await SwalSuccess();

  } catch (error) {
    console.error('Error al agregar la actividad:', error.response ? error.response.data : error.message);
  }
};

const UPDATE_ID = (item) => {
  isEditing.value = true;
  Object.assign(form.value, item); // Copiar directamente los valores al form
  new bootstrap.Modal('#addActivityModal').show(); // Inicializar y mostrar el modal de manera más compacta
};

const UPDATE = async () => {
  try {
    const { id, ...rest } = form.value; // Desestructuración para más claridad
    const token = getAuthToken();
    const response = await api.put(`poi/medida-actividad/${id}/`, {
      ...rest,
      MedidaActividad,
    }, {
      headers: { Authorization: `Bearer ${token}` },
    });

    const index = MedidaActividad.value.findIndex(item => item.id === form.value.id);
    MedidaActividad.value[index] = response.data;

    bootstrap.Modal.getInstance(document.getElementById('addActivityModal')).hide();
    resetForm();

    await SwalUpdate();

  } catch (error) {
    console.error('Error al actualizar la actividad:', error.response ? error.response.data : error.message);
  }
};

const DELETE = async (id) => {
  try {
    const result = await SwalWarning();

    if (result.isConfirmed) {
      const token = getAuthToken();

      await api.delete(`poi/medida-actividad/${id}/`, {
        headers: { Authorization: `Bearer ${token}` },
      });

      MedidaActividad.value = MedidaActividad.value.filter(MedidaActividad => MedidaActividad.id !== id);

      await SwalDelete();

    }
  } catch (error) {
    console.error('Error al eliminar la actividad:', error.response ? error.response.data : error.message);
  }
};

const ELIMINARMULTIPLE = async (selectedIds) => {
  try {
    const result = await SwalWarning();

    if (result.isConfirmed) {
      const token = getAuthToken();

      await api.post('poi/medida-actividad/bulk-delete/', { ids: selectedIds }, {
        headers: { Authorization: `Bearer ${token}` },
      });

      MedidaActividad.value = MedidaActividad.value.filter(MedidaActividad => !selectedIds.includes(MedidaActividad.id));

      // SWEETALERT IMPORTADO SWALCOMPONENT
      await SwalDelete();
    }
  } catch (error) {
    console.error('Error al eliminar múltiples MedidaActividad:', error.response ? error.response.data : error.message);
  }
};

</script>

<style scoped></style>