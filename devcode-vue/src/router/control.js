import UtilesView from '@/views/control/modulos/UtilesView.vue';
import ModulosView from '@/views/control/modulos/ModulosView.vue';
import InformaticaView from '@/views/control/modulos/InformaticaView.vue';
import PatrimonioView from '@/views/control/modulos/PatrimonioView.vue';
import MaterialesView from '@/views/control/modulos/MaterialesView.vue';
import DashBoardView from '@/views/control/modulos/DashBoardView.vue';
import UsuarioView from '@/views/control/modulos/UsuarioView.vue';
import GastoView from '@/views/control/modulos/GastoView.vue';
import LoginView from '../views/control/login/LoginView.vue';

const adminCONTROL = [
    {
        path: '/control/login',
        name: 'control-login',
        component: LoginView,
        meta: {
          title: 'Login',
        },
      },
      {
        path: '/modulos/materiales',
        name: 'materiales',
        component: MaterialesView,
        meta: {
          title: 'Gestión de Almacenamiento de materiales',
          requiresAuth: true,
          group: 'MATERIALES', // El grupo que tiene acceso a esta ruta
        },
      },
      {
        path: '/modulos',
        name: 'modulos',
        component: ModulosView,
        meta: {
          title: 'MODULOS ADMINISTRATIVOS',
          requiresAuth: true,
          group: 'MODULOS', // El grupo que tiene acceso a esta ruta
        },
      },
      {
        path: '/modulos/dashboard',
        name: 'Modulo-Dashboard',
        component: DashBoardView,
        meta: {
          title: 'MODULOS DASHBOARD',
          requiresAuth: true,
          group: 'MODULOS', // El grupo que tiene acceso a esta ruta
        },
      },
      {
        path: '/modulos/usuarios',
        name: 'Modulo-Usuarios',
        component: UsuarioView,
        meta: {
          title: 'GESTIÓN DE COLABORADORES',
          requiresAuth: true,
          group: 'MODULOS', // El grupo que tiene acceso a esta ruta
        },
      },
      {
        path: '/modulos/gasto',
        name: 'Modulo-gasto',
        component: GastoView,
        meta: {
          title: 'Gasto Diario',
          requiresAuth: true,
          group: 'MODULOS', // El grupo que tiene acceso a esta ruta
        },
      },
      {
        path: '/modulos/informatica',
        name: 'Modulo-informatica',
        component: InformaticaView,
        meta: {
          title: 'Informática',
          requiresAuth: true,
          group: 'MODULOS', 
        },
      },
      {
        path: '/modulos/patrimonio',
        name: 'Modulo-patrimonio',
        component: PatrimonioView,
        meta: {
          title: 'Patrimonio',
          requiresAuth: true,
          group: 'MODULOS', 
        },
      },
]
export default adminCONTROL;