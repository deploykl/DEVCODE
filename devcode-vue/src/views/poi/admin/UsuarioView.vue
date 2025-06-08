<template>

    <main id="main" class="main">

        <div class="card">
            <div class="card-body mt-2">
                <button type="button" class="btn btn-success float-start mt-1" @click="openModal">
                    <i class="fa-solid fa-circle-plus"></i> Agregar
                </button>
                <TableComponent :headers="[
                    { key: 'username', label: 'USUARIO', filterable: false },
                    { key: 'first_name', label: 'NOMBRES', filterable: false },
                    { key: 'last_name', label: 'APELLIDOS', filterable: false },
                    { key: 'email', label: 'CORREO', filterable: false },
                    { key: 'dependencia_name', label: 'DEPENDENCIA', filterable: true },
                    { key: 'area_name', label: 'ÁREA', filterable: true },
                    { key: 'condition_name', label: 'CONDICIÓN', filterable: true },
                    { key: 'grupo_name', label: 'GRUPO', filterable: true },
                ]" :items="usuario" @edit="UPDATE_ID" @delete="DELETE" @delete-multiple="ELIMINARMULTIPLE" />
            </div>
        </div>

        <!-- Modal para Agregar/Editar Usuario -->
        <div class="modal fade" id="addActivityModal" tabindex="-1" aria-labelledby="addActivityModalLabel"
            aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="addActivityModalLabel">{{ isEditing ? 'Editar Usuario' : 'Agregar Usuario' }}</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"
                            @click="resetForm"></button>
                    </div>
                    <div class="modal-body">
                        <form @submit.prevent="isEditing ? UPDATE() : ADD()">
                            <div class="mb-3">
                                <label for="username" class="form-label">Nombre de usuario</label>
                                <input type="text" class="form-control" id="username" v-model="form.username"
                                    required />
                            </div>
                            <div class="mb-3">
                                <label for="first_name" class="form-label">Nombres</label>
                                <input type="text" class="form-control" id="first_name" v-model="form.first_name"
                                    required />
                            </div>
                            <div class="mb-3">
                                <label for="last_name" class="form-label">Apellidos</label>
                                <input type="text" class="form-control" id="last_name" v-model="form.last_name"
                                    required />
                            </div>
                            <div class="mb-3">
                                <label for="email" class="form-label">Correo</label>
                                <input type="email" class="form-control" id="email" v-model="form.email" required />
                            </div>
                            <div class="mb-3">
                                <label for="dependencia" class="form-label">Dependencia</label>
                                <select class="form-select" id="dependencia" v-model="form.dependencia" required>
                                    <option disabled value="">-- Elija una opción --</option>
                                    <option v-for="dep in dependencia" :key="dep.id" :value="dep.id">{{ dep.name }}
                                    </option>
                                </select>
                            </div>
                            <div class="mb-3">
                                <label for="area" class="form-label">Área</label>
                                <select class="form-select" id="area" v-model="form.area" required>
                                    <option disabled value="">-- Elija una opción --</option>
                                    <option v-for="ar in area" :key="ar.id" :value="ar.id">{{ ar.name }}</option>
                                </select>
                            </div>
                            <div class="mb-3">
                                <label for="condition" class="form-label">Condición</label>
                                <select class="form-select" id="condition" v-model="form.condition" required>
                                    <option disabled value="">-- Elija una opción --</option>
                                    <option v-for="con in condition" :key="con.id" :value="con.id">{{ con.name }}
                                    </option>
                                </select>
                            </div>
                            <div class="mb-3">
                                <label for="grupo" class="form-label">Grupo</label>
                                <select class="form-select" id="grupo" v-model="form.grupo">
                                    <option disabled value="">-- Elija una opción --</option>
                                    <option v-for="gru in grupo" :key="gru.id" :value="gru.id">{{ gru.name }}</option>
                                </select>

                            </div>
                            <button type="submit" class="btn btn-primary">{{ isEditing ? 'Actualizar' : 'Agregar'
                                }}</button>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </main>
</template>

<script setup>
import { onMounted, ref, watch } from 'vue';
import { api, getAuthToken } from '@/components/services/auth_axios';
import * as bootstrap from 'bootstrap';
import TableComponent from '@/components/TableComponent.vue';
import { SwalSuccess, SwalWarning, SwalDelete, SwalUpdate } from '../../../components/widgets/SwalComponent';

const usuario = ref([]);
const condition = ref([]);
const area = ref([]);
const grupo = ref([]);
const dependencia = ref([]);

const isEditing = ref(false);

const defaultFormValues = {
    id: null, // Asegúrate de incluir el ID
    username: '',
    first_name: '',
    last_name: '',
    condition: '',
    dependencia: '',
    area: '',
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
        const [responseUsuario, responseCondition, responseDependencias, responseGrupo] = await Promise.all([
            api.get('user/usuario/', { headers: { Authorization: `Bearer ${token}` } }),
            api.get('personal/condition/', { headers: { Authorization: `Bearer ${token}` } }),
            api.get('personal/dependencia/', { headers: { Authorization: `Bearer ${token}` } }),
            api.get('user/group/', { headers: { Authorization: `Bearer ${token}` } }),
        ]);

        // Asignar los datos de las respuestas
        usuario.value = responseUsuario.data;
        condition.value = responseCondition.data;
        dependencia.value = responseDependencias.data;
        grupo.value = responseGrupo.data;

    } catch (error) {
        console.error('Error al obtener los datos:', error.response ? error.response.data : error.message);
    }
};


// Carga las áreas cuando cambia la dependencia
watch(() => form.value.dependencia, async (newDependencia) => {
    if (newDependencia) {
        try {
            const Token = getAuthToken();
            const responseArea = await api.get(`personal/area/filtrar_por_dependencia/?dependencia=${newDependencia}`, {
                headers: { Authorization: `Bearer ${Token}` }
            });
            area.value = responseArea.data; // Actualiza la lista de áreas
        } catch (error) {
            console.error('Error al obtener las áreas:', error.response ? error.response.data : error.message);
        }
    } else {
        area.value = []; // Vacía las áreas si no hay dependencia seleccionada
    }
});

onMounted(() => {
    LISTAR();
});

const UPDATE_ID = (usuario) => {
    isEditing.value = true;
    Object.assign(form.value, usuario);
    new bootstrap.Modal('#addActivityModal').show();
};

const UPDATE = async () => {
    try {
        const { id, grupo, ...rest } = form.value; // Desestructuración para extraer id y grupo

        const token = getAuthToken();
        const response = await api.put(`user/usuario/${id}/`, {
            ...rest,
            grupo,
        }, {
            headers: { Authorization: `Bearer ${token}` },
        });
        // Actualizar el usuario en la tabla
        const index = usuario.value.findIndex(item => item.id === form.value.id);
        usuario.value[index] = response.data;

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

            await api.delete(`user/usuario/${id}/`, {
                headers: { Authorization: `Bearer ${token}` }
            });

            usuario.value = usuario.value.filter(user => user.id !== id);
            await SwalDelete();
        }
    } catch (error) {
        console.error('Error al eliminar el usuario:', error.response ? error.response.data : error.message);
    }
};

</script>

<style scoped></style>
