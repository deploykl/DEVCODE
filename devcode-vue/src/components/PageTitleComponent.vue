<template>
    <main id="main" class="container">
        <div class="row">
            <!-- 
            <div class="col-md-6">
                <div class="pagetitle">
                    <h1>{{ currentTitle }}</h1>
                    <nav>
                        <ol class="breadcrumb">
                            <li v-for="(breadcrumb, index) in breadcrumbs" :key="index" class="breadcrumb-item">
                                {{ breadcrumb.text }}
                            </li>
                        </ol>
                    </nav>
                </div>
            </div>
            -->
            <div>
                <h2 class="d-flex align-items-center">
                    <i class="fa-light fa-wave-pulse me-2"></i>
                    {{ currentTitle }}
                </h2>
            </div>
            <div class="col-md-12 d-flex align-items-start">
                <button-float-component-vue v-if="showButton" />
            </div>
        </div>
    </main>
</template>

<script setup>
import { computed } from 'vue';
import { useRoute } from 'vue-router';
import ButtonFloatComponentVue from './widgets/ButtonFloatComponent.vue';

const route = useRoute();

const currentTitle = computed(() => {
    return route.meta.title || 'Default Title';
});

// Determina si se debe mostrar el botón flotante
const showButton = computed(() => route.path !== '/control/utiles');

</script>

<style scoped>
</style>