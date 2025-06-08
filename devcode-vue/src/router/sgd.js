import PendientesView from '@/views/sgd/PendientesView.vue';

const adminSGD = [
  {
    path: '/sgd/pendientes',
    name: 'sgd-pendientes',
    component: PendientesView,
    meta: {
      title: 'SGD - Pendientes',
      requiresAuth: false,  // Asegúrate de que esto esté definido como false
    },
  },
];

export default adminSGD;