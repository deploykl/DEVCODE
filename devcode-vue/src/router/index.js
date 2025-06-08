import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '../views/HomeView.vue';
import ActividadesView from '../views/poi/ActividadesView.vue';
import DashboardView from '../views/poi/DashboardView.vue';
import TareasView from '../views/poi/TareasView.vue';
import TareaDetalleView from '../views/poi/TareaDetalleView.vue';
import ActividadDetalleView from '../views/poi/ActividadDetalleView.vue';
import LoginView from '../views/poi/login/LoginView.vue';
import RegisterView from '../views/poi/login/RegisterView.vue';
import UploadFilesView from '../views/poi/UploadFilesView.vue';
import adminPOI from './poi';
import adminCONTROL from './control';
import NotFoundView from '../views/poi/NotFoundView.vue'; // Componente para 404
import adminSGD from './sgd';

const routes = [
  {
    path: '/',
    name: 'HOME',
    component: HomeView,
    meta: {
      title: 'POI',
    },
  },
  {
    path: '/dashboard',
    name: 'dashboard',
    component: DashboardView,
    meta: {
      title: 'Avance de la Ejecución de Metas Físicas y Financieras',
      requiresAuth: true,
    },
  },
  {
    path: '/actividades',
    name: 'actividades',
    component: ActividadesView,
    meta: {
      title: 'ACTIVIDADES',
      requiresAuth: true,
    },
  },
  {
    path: '/actividad-reportes/:id',
    name: 'actividad-reportes',
    component: ActividadDetalleView,
    meta: {
      title: 'REPORTES DE ACTIVIDAD',
      requiresAuth: true,
    },
  },
  {
    path: '/tareas/:id',
    name: 'actividad-tareas',
    component: TareasView,
    meta: {
      title: 'TAREAS DE LA ACTIVIDAD OPERATIVA',
      requiresAuth: true,
    },
  },
  {
    path: '/tareas-detalle/:id',
    name: 'tarea-detalle',
    component: TareaDetalleView,
    meta: {
      title: 'REGISTRO DE EJECUCIÓN FÍSICA',
      requiresAuth: true,
    },
  },
  {
    path: '/upload/:mes/:reporteId',
    name: 'upload',
    component: UploadFilesView,
    meta: {
      title: 'SUSTENTO DE EJECUCIÓN FÍSICA',
      requiresAuth: true,
    },
  },
  {
    path: '/login',
    name: 'login',
    component: LoginView,
    meta: {
      title: 'Login',
    },
  },
  {
    path: '/register',
    name: 'register',
    component: RegisterView,
    meta: {
      title: 'REGISTRO',
    },
  },
  {
    path: '/:catchAll(.*)',
    name: 'not-found',
    component: NotFoundView,
    meta: {
      title: 'Página no encontrada',
    },
  },
  //integrado de poi.js
  ...adminPOI,
  ...adminCONTROL,
  ...adminSGD,
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  const isAuthenticated = !!localStorage.getItem('auth_token');
  const isAdmin = localStorage.getItem('is_superuser') === 'true' || localStorage.getItem('is_staff') === 'true';

  // Verificar si la ruta requiere autenticación
  if (to.meta.requiresAuth && !isAuthenticated) {
    next({ name: 'login' }); // Redirigir a la página de login si no está autenticado
  } 
  // Verificar si la ruta requiere permisos de administrador
  else if (to.meta.isAdmin && !isAdmin) {
    next({ name: 'HOME' }); // Redirigir a la página principal si no es administrador
  } 
  else {
    next(); // Continuar a la ruta solicitada si todo está bien
  }
});



export default router;
