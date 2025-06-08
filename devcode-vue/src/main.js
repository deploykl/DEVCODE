import { createApp } from 'vue'
import App from './App.vue'
import TableComponent from './components/TableComponent.vue'
import './registerServiceWorker'
import router from './router'
import store from './store'
import 'bootstrap'
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap-icons/font/bootstrap-icons.css';  // Asegúrate de esta línea
import '@/assets/lib/fontawesome-v6.5.2/css/all.css'
import '@/assets/lib/fontawesome-v6.5.2/css/sharp-light.css'
import '@/assets/lib/fontawesome-v6.5.2/css/sharp-regular.css'
import '@/assets/lib/fontawesome-v6.5.2/css/sharp-solid.css'
import '@/assets/lib/fontawesome-v6.5.2/css/sharp-thin.css'

// Importa CSS

//PERSONALIZADO ASIDE
import '@/assets/css/main.css'
import '@/assets/css/aside.css'
import 'sweetalert2';
import 'sweetalert2/dist/sweetalert2.min.css';
import '@/assets/js/validation.js'
import '@/assets/js/alerts.js'
import '@/assets/js/aside.js'

const app = createApp(App);

// Registra el componente globalmente
app.component('TableComponent', TableComponent);
// Proveer el servicio para que esté disponible globalmente
// Usa el store y el router
app.use(store);
app.use(router);

// Monta la aplicación
app.mount('#app');
