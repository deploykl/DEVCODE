import UsuarioView from '../views/poi/admin/UsuarioView.vue';
import ProfileView from '../views/poi/admin/ProfileView.vue'; // Ejemplo de vista para admin
import GrupoView from '../views/poi/admin/GrupoView.vue'; // Ejemplo de vista para admin
import ActividadesView from '../views/poi/admin/ActividadesView.vue'; // Ejemplo de vista para admin
import MedidaActividadView from '../views/poi/admin/MedidaActividadView.vue'; // Ejemplo de vista para admin
import TareasView from '../views/poi/admin/TareasView.vue'; // Ejemplo de vista para admin
import MedidaTareaView from '../views/poi/admin/MedidaTareaView.vue'; // Ejemplo de vista para admin
import CamposView from '../views/poi/admin/CamposView.vue'; // Ejemplo de vista para admin

const adminPOI = [
  {
    path: '/admin/usuarios',
    name: 'admin-usuarios',
    component: UsuarioView,
    meta: {
      title: 'USUARIOS',
      requiresAuth: true,
      isAdmin: true,
    },
  },
  {
    path: '/admin/profile',
    name: 'admin-profile',
    component: ProfileView,
    meta: {
      title: 'PERFIL',
      requiresAuth: true,
    },
  },
  {
    path: '/admin/grupo',
    name: 'admin-grupo',
    component: GrupoView,
    meta: {
      title: 'GRUPOS',
      requiresAuth: true,
      isAdmin: true,
    },
  },
  {
    path: '/admin/actividades',
    name: 'admin-actividades',
    component: ActividadesView,
    meta: {
      title: 'ACTIVIDADES',
      requiresAuth: true,
      isAdmin: true,
    },
  },
  {
    path: '/admin/medida-actividad',
    name: 'admin-medida-actividad',
    component: MedidaActividadView,
    meta: {
      title: 'MEDIDA DE ACTIVIDAD',
      requiresAuth: true,
      isAdmin: true,
    },
  },
  {
    path: '/admin/tareas',
    name: 'admin-tareas',
    component: TareasView,
    meta: {
      title: 'TAREAS',
      requiresAuth: true,
      isAdmin: true,
    },
  },
  {
    path: '/admin/medida-tarea',
    name: 'admin-medida-tarea',
    component: MedidaTareaView,
    meta: {
      title: 'MEDIDA DE TAREA',
      requiresAuth: true,
      isAdmin: true,
    },
  },
    {
    path: '/admin/campos',
    name: 'admin-campos',
    component: CamposView,
    meta: {
      title: 'BLOQUEAR CAMPOS',
      requiresAuth: true,
      isAdmin: true,
    },
  },
];

export default adminPOI;