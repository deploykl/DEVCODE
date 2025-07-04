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
                    { key: 'condition_name', label: 'CONDICIÓN LABORAL', filterable: true },
                    { key: 'cargo_name', label: 'CARGO', filterable: true },
                    { key: 'celular', label: 'CELULAR', filterable: false},
                    { key: 'salario', label: 'SALARIO', filterable: true },
                    { key: 'grupoOcupacional_name', label: 'GRUPO_Ocu', filterable: true },
                    { key: 'generica_name', label: 'Generica', filterable: true },
                ]" :items="usuario" @edit="UPDATE_ID" @delete="DELETE" @delete-multiple="ELIMINARMULTIPLE" />
            </div>
        </div>

        <!-- Modal para Agregar/Editar Usuario -->
        <div class="modal fade" id="addActivityModal" tabindex="-1" aria-labelledby="addActivityModalLabel" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered modal-lg">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="addActivityModalLabel">{{ isEditing ? 'Editar Usuario' : 'Agregar Usuario' }}</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close" @click="resetForm"></button>
                    </div>
                    <div class="modal-body">
                        <form @submit.prevent="isEditing ? UPDATE() : ADD()">
                            <div class="row">
                                <!-- Columna 1 -->
                                <div class="col-md-6">
                                    <div class="mb-3">
                                        <label for="username" class="form-label">Nombre de usuario</label>
                                        <input type="text" class="form-control" id="username" v-model="form.username" required />
                                    </div>
                                    <div class="mb-3">
                                        <label for="first_name" class="form-label">Nombres</label>
                                        <input type="text" class="form-control" id="first_name" v-model="form.first_name" required />
                                    </div>
                                    <div class="mb-3">
                                        <label for="last_name" class="form-label">Apellidos</label>
                                        <input type="text" class="form-control" id="last_name" v-model="form.last_name" required />
                                    </div>
                                    <div class="mb-3">
                                        <label for="email" class="form-label">Correo</label>
                                        <input type="email" class="form-control" id="email" v-model="form.email" required />
                                    </div>
                                    <div class="mb-3">
                                        <label for="dependencia" class="form-label">Dependencia</label>
                                        <select class="form-select" id="dependencia" v-model="form.dependencia" required>
                                            <option disabled value="">-- Elija una opción --</option>
                                            <option v-for="dep in dependencia" :key="dep.id" :value="dep.id">{{ dep.name }}</option>
                                        </select>
                                    </div>
                                    <div class="mb-3">
                                        <label for="area" class="form-label">Área</label>
                                        <select class="form-select" id="area" v-model="form.area" required>
                                            <option disabled value="">-- Elija una opción --</option>
                                            <option v-for="ar in area" :key="ar.id" :value="ar.id">{{ ar.name }}</option>
                                        </select>
                                    </div>
                                </div>
                                
                                <!-- Columna 2 -->
                                <div class="col-md-6">
                                    <div class="mb-3">
                                        <label for="condition" class="form-label">Condición</label>
                                        <select class="form-select" id="condition" v-model="form.condition" required>
                                            <option disabled value="">-- Elija una opción --</option>
                                            <option v-for="con in condition" :key="con.id" :value="con.id">{{ con.name }}</option>
                                        </select>
                                    </div>
                                    <div class="mb-3">
                                        <label for="cargo" class="form-label">Cargo</label>
                                        <select class="form-select" id="cargo" v-model="form.cargo">
                                            <option disabled value="">-- Elija una opción --</option>
                                            <option v-for="car in cargo" :key="car.id" :value="car.id">{{ car.name }}</option>
                                        </select>
                                    </div>
                                    <div class="mb-3">
                                        <label for="grupo" class="form-label">Grupo</label>
                                        <select class="form-select" id="grupo" v-model="form.grupo">
                                            <option disabled value="">-- Elija una opción --</option>
                                            <option v-for="gru in grupo" :key="gru.id" :value="gru.id">{{ gru.name }}</option>
                                        </select>
                                    </div>
                                    <div class="mb-3">
                                        <label for="celular" class="form-label">Celular (Opcional)</label>
                                        <input type="number" class="form-control" id="celular" v-model="form.celular" />
                                    </div>
                                    <div class="mb-3">
                                        <label for="fecha_inicio" class="form-label">Fecha Inicio (Opcional)</label>
                                        <input type="date" class="form-control" id="fecha_inicio" v-model="form.fecha_inicio" />
                                    </div>
                                    <div class="mb-3">
                                        <label for="fecha_cesado" class="form-label">Fecha Cesado (Opcional)</label>
                                        <input type="date" class="form-control" id="fecha_cesado" v-model="form.fecha_cesado" />
                                    </div>
                                </div>
                            </div>
                            
                            <!-- Segunda fila de columnas -->
                            <div class="row mt-2">
                                <div class="col-md-6">
                                    <div class="mb-3">
                                        <label for="salario" class="form-label">Salario (Opcional)</label>
                                        <input type="number" step="0.01" class="form-control" id="salario" v-model="form.salario" />
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <div class="mb-3">
                                        <label for="grupoOcupacional" class="form-label">Grupo Ocupacional</label>
                                        <select class="form-select" id="grupoOcupacional" v-model="form.grupoOcupacional">
                                            <option disabled value="">-- Elija una opción --</option>
                                            <option v-for="goc in grupoOcupacional" :key="goc.id" :value="goc.id">{{ goc.descripcion }}</option>
                                        </select>
                                    </div>
                                    <div class="mb-3">
                                        <label for="generica" class="form-label">Genérica</label>
                                        <select class="form-select" id="generica" v-model="form.generica">
                                            <option disabled value="">-- Elija una opción --</option>
                                            <option v-for="gen in generica" :key="gen.id" :value="gen.id">{{ gen.descripcion }}</option>
                                        </select>
                                    </div>
                                </div>
                            </div>
                            
                            <div class="d-flex justify-content-end mt-3">
                                <button type="submit" class="btn btn-primary me-2">{{ isEditing ? 'Actualizar' : 'Agregar' }}</button>
                                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal" @click="resetForm">Cancelar</button>
                            </div>
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
const cargo = ref([])
const grupoOcupacional = ref([]);
const generica = ref([]);

const isEditing = ref(false);

const defaultFormValues = {
    id: null, // Asegúrate de incluir el ID
    username: '',
    first_name: '',
    last_name: '',
    condition: '',
    dependencia: '',
    cargo: null,  // Cambiado a null para que sea claramente opcional
    area: '',
    grupoOcupacional: null,  // Nuevo campo
    generica: null,         // Nuevo campo
    celular: null,  // Cambiado a null
    fecha_inicio: null,  // Cambiado a null
    fecha_cesado: null,  // Cambiado a null
    salario: null  // Cambiado a null
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

// Actualiza LISTAR para cargar los nuevos datos
const LISTAR = async () => {
    try {
        const token = getAuthToken();

        const [
            responseUsuario, 
            responseCondition, 
            responseDependencias, 
            responseCargo, 
            responseGrupo,
            responseGrupoOcupacional,
            responseGenerica
        ] = await Promise.all([
            api.get('user/usuario/', { headers: { Authorization: `Bearer ${token}` } }),
            api.get('personal/condition/', { headers: { Authorization: `Bearer ${token}` } }),
            api.get('personal/dependencia/', { headers: { Authorization: `Bearer ${token}` } }),
            api.get('personal/cargo/', { headers: { Authorization: `Bearer ${token}` } }),
            api.get('user/group/', { headers: { Authorization: `Bearer ${token}` } }),
            api.get('personal/grupo_ocupacional/', { headers: { Authorization: `Bearer ${token}` } }),
            api.get('personal/generica/', { headers: { Authorization: `Bearer ${token}` } })
        ]);

        usuario.value = responseUsuario.data;
        condition.value = responseCondition.data;
        dependencia.value = responseDependencias.data;
        cargo.value = responseCargo.data;
        grupo.value = responseGrupo.data;
        grupoOcupacional.value = responseGrupoOcupacional.data;
        generica.value = responseGenerica.data;

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
        const token = getAuthToken();

        // Preparar los datos para actualizar
        const updateData = {
            username: form.value.username,
            first_name: form.value.first_name,
            last_name: form.value.last_name,
            email: form.value.email,
            condition: form.value.condition,
            dependencia: form.value.dependencia,
            ...(form.value.cargo && { cargo: form.value.cargo }),
            ...(form.value.grupoOcupacional && { grupoOcupacional: form.value.grupoOcupacional }),
            ...(form.value.generica && { generica: form.value.generica }),
            area: form.value.area,
            grupo: form.value.grupo,
            // Campos opcionales
            celular: form.value.celular !== null ? form.value.celular : null,
            fecha_inicio: form.value.fecha_inicio !== null ? form.value.fecha_inicio : null,
            fecha_cesado: form.value.fecha_cesado !== null ? form.value.fecha_cesado : null,
            salario: form.value.salario !== null ? form.value.salario : null
        };

        const response = await api.put(`user/usuario/${form.value.id}/`, updateData, {
            headers: { Authorization: `Bearer ${token}` },
        });

        const index = usuario.value.findIndex(item => item.id === form.value.id);
        if (index !== -1) {
            usuario.value[index] = response.data;
        }

        bootstrap.Modal.getInstance(document.getElementById('addActivityModal')).hide();
        resetForm();
        await SwalUpdate();
    } catch (error) {
        console.error('Error al actualizar:', error.response ? error.response.data : error.message);
        alert('Error al actualizar: ' + (error.response?.data?.message || error.message));
    }
};
const ADD = async () => {
    try {
        const token = getAuthToken();

        // Preparar los datos del formulario para enviar
        const userData = {
            username: form.value.username,
            first_name: form.value.first_name,
            last_name: form.value.last_name,
            email: form.value.email,
            condition: form.value.condition,
            dependencia: form.value.dependencia,
            ...(form.value.cargo && { cargo: form.value.cargo }),
            ...(form.value.grupoOcupacional && { grupoOcupacional: form.value.grupoOcupacional }),
            ...(form.value.generica && { generica: form.value.generica }),
            area: form.value.area,
            grupo: form.value.grupo,
            // Campos opcionales - solo se incluyen si tienen valor
            ...(form.value.celular !== null && { celular: form.value.celular }),
            ...(form.value.fecha_inicio !== null && { fecha_inicio: form.value.fecha_inicio }),
            ...(form.value.fecha_cesado !== null && { fecha_cesado: form.value.fecha_cesado }),
            salario: form.value.salario !== null ? form.value.salario : null
        };

        const response = await api.post('user/usuario/', userData, {
            headers: { Authorization: `Bearer ${token}` }
        });

        usuario.value.push(response.data);
        bootstrap.Modal.getInstance(document.getElementById('addActivityModal')).hide();
        resetForm();
        await SwalSuccess('Usuario creado exitosamente');
    } catch (error) {
        console.error('Error al crear usuario:', error.response ? error.response.data : error.message);

        let errorMessage = 'Error al crear el usuario';
        if (error.response && error.response.data) {
            if (typeof error.response.data === 'object') {
                errorMessage = Object.values(error.response.data).join('\n');
            } else {
                errorMessage = error.response.data;
            }
        }

        alert(errorMessage);
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
