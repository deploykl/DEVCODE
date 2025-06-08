<template>
    <aside v-if="!isControlPage" id="sidebar" class="sidebar d-flex flex-column">
        <ul class="sidebar-nav" id="sidebar-nav">
            <!-- Mostrar solo el menú correspondiente al grupo del usuario -->
            <template v-if="isSuperuser">
                <!-- Menú completo para superusuarios -->
                <li class="nav-heading">Administración</li>
                <!-- ... todo el menú de administración ... -->
            </template>
            <template v-else-if="userGroup === 'MATERIALES' && isModulosRoute">
                <li class="nav-heading">Menu del Grupo MATERIALES</li>
                <hr>
                <li class="nav-item">
                    <router-link :to="{ name: 'materiales' }" class="nav-link collapsed">
                        <i class="fa-solid fa-gear"></i><span>Gestión de Almacenamiento de materiales</span>
                    </router-link>
                </li>
                <!-- Solo mostrar este ítem si necesitas un regreso -->
                <li class="nav-item">
                    <router-link :to="{ name: 'Modulo-Dashboard' }" class="nav-link collapsed">
                        <i class="fa-solid fa-pencil"></i><span>Regresar</span>
                    </router-link>
                </li>
            </template>
            <template v-else-if="userGroup === 'ADMIN' && isModulosRoute">
                <!-- Menú para administradores no superusuarios -->
                <li class="nav-heading">Menu del Grupo ADMIN</li>
                <hr>
                <!-- ... ítems del menú para ADMIN ... -->
            </template>
            <template v-else>
                <li class="nav-item">
                    <div class="alert alert-warning">
                        No tiene permisos para ver este menú
                    </div>
                </li>
            </template>
        </ul>
    </aside>
</template>
<script setup>
</script>


