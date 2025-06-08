<template>
    <!-- ======= Sidebar ======= -->
    <aside v-if="!isControlPage" id="sidebar" class="sidebar d-flex flex-column">
        <ul class="sidebar-nav" id="sidebar-nav">
            <li class="nav-item">
                <router-link :to="{ name: 'dashboard' }" class="nav-link collapsed">
                    <i class="fa-solid fa-user"></i><span>Dashboard</span>
                </router-link>
            
            </li><!-- End Dashboard Nav -->
            <li class="nav-heading">Pages</li>
            <hr>
            <li class="nav-item">
                <router-link :to="{ name: 'admin-profile' }" class="nav-link collapsed">
                    <i class="fa-solid fa-user"></i><span>Perfíl</span>
                </router-link>
            </li><!-- End Profile Page Nav -->

            <!-- Mostrar si es staff -->
            <li v-if="isStaff" class="nav-item">
                <a class="nav-link collapsed" href="#">
                    <i class="fa-solid fa-user-crown"></i><span>Superuser y Staff : Admin MASIVO</span>
                </a>
            </li>

            <li class="nav-heading">Menu no Staff</li>
            <hr v-if="isStaff || (isSuperuser && !isStaff)">
            <!-- Mostrar si es staff o si es superuser -->
            <li v-if="isStaff || (isSuperuser && !isStaff)" class="nav-item">
                <a class="nav-link collapsed" href="#">
                    <i class="bi bi-pen"></i><span>Superuser y Staff condición 3</span>
                </a>
            </li>
            <li v-if="isStaff || (isSuperuser && !isStaff)" class="nav-item">
                <!-- Enlace principal que controla el colapso del submenú específico -->
                <a class="nav-link" data-bs-toggle="collapse" href="#sub-menu-actividades" role="button"
                    aria-expanded="false" aria-controls="sub-menu-actividades">
                    <i class="fa-regular fa-chart-line"></i>
                    <span>Actividades</span>
                    <i class="bi bi-chevron-down ms-auto"></i>
                </a>
                <!-- Submenú específico que se despliega/colapsa -->
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

            <li v-if="isStaff || (isSuperuser && !isStaff)" class="nav-item">
                <!-- Enlace principal que controla el colapso del submenú específico -->
                <a class="nav-link" data-bs-toggle="collapse" href="#sub-menu-tareas" role="button"
                    aria-expanded="false" aria-controls="sub-menu-tareas">
                    <i class="fa-sharp fa-regular fa-pencil"></i>
                    <span>Tareas</span>
                    <i class="bi bi-chevron-down ms-auto"></i>
                </a>
                <!-- Submenú específico que se despliega/colapsa -->
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
                <router-link :to="{ name: 'admin-tareas' }" class="nav-link collapsed">
                    <i class="fa-regular fa-paperclip"></i><span>otro</span>
                </router-link>
            </li>

            <!--    MODULO LLAMADO POR GRUPO   -->
            <!-- Mostrar menú basado en el grupo del usuario -->
            <!--    MODULO LLAMADO POR GRUPO   -->
            <li v-if="isStaff || userGroup === 'UTILES'" class="nav-heading">
                Menu del Grupo UTILES
            </li>
            <hr>

            <li v-if="isStaff || userGroup === 'UTILES'" class="nav-item">
                <router-link :to="{ name: 'utiles' }" class="nav-link collapsed">
                    <i class="fa-solid fa-pencil"></i><span>Stock</span>
                </router-link>
            </li>
        </ul>
        <!-- Botón de Logout (al final) -->


    </aside><!-- End Sidebar -->
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router';

const isSuperuser = ref(false)
const isStaff = ref(false)
const userGroup = ref('')
const router = useRouter();
const isControlPage = ref(false); // Variable para controlar la visibilidad del menú

onMounted(() => {
    const superuser = localStorage.getItem('is_superuser');
    const staff = localStorage.getItem('is_staff');
    const group = localStorage.getItem('group') || 'No definido'; // Usa 'No definido' como valor por defecto

    isSuperuser.value = superuser === 'true';
    isStaff.value = staff === 'true';
    userGroup.value = group; // Asigna el valor a `userGroup`

    console.log('Grupo del usuario:', userGroup.value);
    console.log('Superuser:', isSuperuser.value);
    console.log('Staff:', isStaff.value);
});


</script>