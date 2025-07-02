<template>
    <!-- ======= Sidebar ======= -->
<aside v-if="(isSuperuser && isStaff) && !isControlPage" id="sidebar" class="sidebar d-flex flex-column">
        <ul class="sidebar-nav" id="sidebar-nav">
            <!-- Menú común para todas las rutas -->

            <template v-if="isSuperuser">
                <!-- Menú completo para superusuarios -->
                <li class="nav-heading">Administración</li>
                <!-- ... todo el menú de administración ... -->
                  <li v-if="isStaff || (isSuperuser && !isStaff)" class="nav-item">
                    <router-link :to="{ name: 'Modulo-gasto' }" class="nav-link collapsed">
                        <i class="fa-regular fa-paperclip"></i><span>Módulos de admin</span>
                    </router-link>
                </li>
            </template>

            <li class="nav-heading">Pages</li>
            <!-- MENÚ ESPECÍFICO PARA /modulos -->
            <template v-if="isModulosRoute">
                <li v-if="isStaff || userGroup === 'MODULOS'" class="nav-heading">
                    Menu del Grupo MODULOS
                </li>
                <hr>
                <li class="nav-item">
                    <router-link :to="{ name: 'Modulo-Dashboard' }" class="nav-link collapsed">
                        <i class="fa-solid fa-cubes"></i><span>Dashboard</span>
                    </router-link>
                </li>
                <!-- Aquí puedes agregar los items específicos para MODULOS -->
                <li class="nav-item">
                    <router-link :to="{ name: 'actividades' }" class="nav-link collapsed">
                        <i class="fa-solid fa-cubes"></i><span>Planeamiento Operativo</span>
                    </router-link>
                </li>

                <li class="nav-item">
                    <router-link :to="{ name: 'Modulo-gasto' }" class="nav-link collapsed">
                        <i class="fa-solid fa-gear"></i><span>Presupuesto Institucional</span>
                    </router-link>
                </li>
                <li class="nav-item">
                    <router-link :to="{ name: 'Modulo-Usuarios' }" class="nav-link collapsed">
                        <i class="fa-solid fa-gear"></i><span>Gestión de Colaboradores</span>
                    </router-link>
                </li>
                <li class="nav-item">
                    <a class="nav-link" data-bs-toggle="collapse" href="#sub-menu-actividades" role="button"
                        aria-expanded="false" aria-controls="sub-menu-actividades">
                        <i class="fa-regular fa-gear"></i>
                        <span>Control Patrimonial</span>
                        <i class="bi bi-chevron-down ms-auto"></i>
                    </a>
                    <ul id="sub-menu-actividades" class="nav-content collapse">
                        <li>
                            <router-link :to="{ name: 'Modulo-patrimonio' }" class="nav-link collapsed">
                                <i class="fa-regular fa-circle"></i><span>Equipos patrimoniales</span>
                            </router-link>
                        </li>
                        <li>
                            <router-link :to="{ name: 'Modulo-informatica' }" class="nav-link collapsed">
                                <i class="fa-regular fa-circle"></i><span>Equipos informáticos</span>
                            </router-link>
                        </li>
                    </ul>
                </li>
                <li class="nav-item">
                    <router-link :to="{ name: 'materiales' }" class="nav-link collapsed">
                        <i class="fa-solid fa-gear"></i><span>Gestión de Almacenamiento de materiales</span>
                    </router-link>
                </li>



            </template>

            <!-- MENÚ NORMAL (se muestra cuando NO está en /modulos) -->
            <template v-else>
                <!-- Mostrar si es staff -->
                <li v-if="isStaff" class="nav-item">
                    <router-link :to="{ name: 'dashboard' }" class="nav-link">
                        <i class="fa-solid fa-chart-area"></i>
                        <span>Dashboard</span>
                    </router-link>
                </li>

                <li class="nav-heading">Menu no Staff</li>
                <hr v-if="isStaff || (isSuperuser && !isStaff)">

                <!-- Resto de tu menú actual -->
                <li v-if="isStaff || (isSuperuser && !isStaff)" class="nav-item">
                    <a class="nav-link collapsed" href="#">
                        <i class="bi bi-pen"></i><span>Superuser y Staff condición 3</span>
                    </a>
                </li>

                <!-- Submenú Actividades -->
                <li v-if="isStaff || (isSuperuser && !isStaff)" class="nav-item">
                    <a class="nav-link" data-bs-toggle="collapse" href="#sub-menu-actividades" role="button"
                        aria-expanded="false" aria-controls="sub-menu-actividades">
                        <i class="fa-regular fa-chart-line"></i>
                        <span>Actividades</span>
                        <i class="bi bi-chevron-down ms-auto"></i>
                    </a>
                    <ul id="sub-menu-actividades" class="nav-content collapse">
                        <li>
                            <router-link :to="{ name: 'admin-actividades' }" class="nav-link collapsed">
                                <i class="fa-regular fa-circle"></i><span>Lista de actividades</span>
                            </router-link>
                        </li>
                        <li>
                            <router-link :to="{ name: 'admin-medida-actividad' }" class="nav-link">
                                <i class="fa-regular fa-circle"></i>
                                <span>Medida de actividad</span>
                            </router-link>
                        </li>
                    </ul>
                </li>

                <!-- Submenú Tareas -->
                <li v-if="isStaff || (isSuperuser && !isStaff)" class="nav-item">
                    <a class="nav-link" data-bs-toggle="collapse" href="#sub-menu-tareas" role="button"
                        aria-expanded="false" aria-controls="sub-menu-tareas">
                        <i class="fa-sharp fa-regular fa-pencil"></i>
                        <span>Tareas</span>
                        <i class="bi bi-chevron-down ms-auto"></i>
                    </a>
                    <ul id="sub-menu-tareas" class="nav-content collapse">
                        <li>
                            <router-link :to="{ name: 'admin-tareas' }" class="nav-link collapsed">
                                <i class="fa-regular fa-circle"></i><span>Lista de tareas</span>
                            </router-link>
                        </li>
                        <li>
                            <router-link :to="{ name: 'admin-medida-tarea' }" class="nav-link">
                                <i class="fa-regular fa-circle"></i>
                                <span>Medida de tarea</span>
                            </router-link>
                        </li>
                    </ul>
                </li>
                <li v-if="isStaff || (isSuperuser && !isStaff)" class="nav-item">
                    <router-link :to="{ name: 'admin-usuarios' }" class="nav-link collapsed">
                        <i class="fa-solid fa-user-group"></i><span>Usuarios</span>
                    </router-link>
                </li>
                <li v-if="isStaff || (isSuperuser && !isStaff)" class="nav-item">
                    <router-link :to="{ name: 'admin-grupo' }" class="nav-link collapsed">
                        <i class="fa-sharp fa-solid fa-people-group"></i><span>Grupos</span>
                    </router-link>
                </li>
                <li v-if="isStaff || (isSuperuser && !isStaff)" class="nav-item">
                    <router-link :to="{ name: 'admin-campos' }" class="nav-link collapsed">
                        <i class="fa-regular fa-paperclip"></i><span>Habilitar Campos</span>
                    </router-link>
                </li>
                <!-- Menú UTILES -->
                <template v-if="isStaff || userGroup === 'MATERIALES'">
                    <li class="nav-heading">Menu del Grupo UTILES</li>
                    <hr>
                    <li class="nav-item">
                        <router-link :to="{ name: 'Modulo-Dashboard' }" class="nav-link collapsed">
                            <i class="fa-solid fa-pencil"></i><span>Regresar</span>
                        </router-link>
                    </li>
                </template>
            </template>
        </ul>
    </aside>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router';

const isSuperuser = ref(false)
const isStaff = ref(false)
const userGroup = ref('')
const isControlPage = ref(false)
const route = useRoute()

// Detecta si está en la ruta /modulos
const isModulosRoute = computed(() => {
    return route.path.startsWith('/modulos')
})

onMounted(() => {
    const superuser = localStorage.getItem('is_superuser')
    const staff = localStorage.getItem('is_staff')
    const group = localStorage.getItem('group') || 'No definido'

    isSuperuser.value = superuser === 'true'
    isStaff.value = staff === 'true'
    userGroup.value = group
})
</script>