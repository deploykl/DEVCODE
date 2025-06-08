<template>
    <main id="main" class="main">
      <div class="card">
        <div class="card-body">
         <h5>--</h5>
          <!-- Filtros -->
          <div class="row mb-3">
            <div class="col-md-4">
              <input v-model="filters.descripcion" type="text" class="form-control" placeholder="Filtrar por descripción">
            </div>
            <div class="col-md-3">
              <select v-model="filters.unidad_medida" class="form-select">
                <option value="">Todas las unidades</option>
                <option v-for="unidad in unidadesMedida" :key="unidad" :value="unidad">{{ unidad }}</option>
              </select>
            </div>
            <div class="col-md-2">
              <button class="btn btn-primary" @click="agregarMaterial">
                <i class="bi bi-plus-circle"></i> Nuevo
              </button>
            </div>
          </div>
  
          <!-- Tabla de materiales -->
          <div class="table-responsive">
            <table class="table table-striped table-hover">
              <thead>
                <tr>
                  <th @click="sortBy('descripcion')" class="sortable">Descripción <i class="bi bi-arrow-down-up"></i></th>
                  <th>Cantidad</th>
                  <th>Unidad</th>
                  <th>Marca</th>
                  <th>P. Unitario</th>
                  <th>Acciones</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="material in materialesFiltrados" :key="material.id">
                  <td>{{ material.descripcion }}</td>
                  <td>{{ material.cantidad }}</td>
                  <td>{{ material.unidad_medida }}</td>
                  <td>{{ material.marca || 'Sin marca' }}</td>
                  <td>S/ {{ material.p_u.toFixed(2) }}</td>
                  <td>
                    <button @click="editarMaterial(material)" class="btn btn-sm btn-outline-primary me-1">
                      <i class="bi bi-pencil"></i>
                    </button>
                    <button @click="eliminarMaterial(material.id)" class="btn btn-sm btn-outline-danger">
                      <i class="bi bi-trash"></i>
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
  
          <!-- Paginación -->
          <nav aria-label="Page navigation" class="mt-3">
            <ul class="pagination justify-content-center">
              <li class="page-item" :class="{ disabled: currentPage === 1 }">
                <button class="page-link" @click="currentPage--">Anterior</button>
              </li>
              <li class="page-item" v-for="page in totalPages" :key="page" :class="{ active: currentPage === page }">
                <button class="page-link" @click="currentPage = page">{{ page }}</button>
              </li>
              <li class="page-item" :class="{ disabled: currentPage === totalPages }">
                <button class="page-link" @click="currentPage++">Siguiente</button>
              </li>
            </ul>
          </nav>
        </div>
      </div>
  
      <!-- Modal para agregar/editar material -->
      <div class="modal fade" id="materialModal" tabindex="-1" aria-hidden="true">
        <div class="modal-dialog">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title">{{ materialEditando ? 'Editar Material' : 'Agregar Material' }}</h5>
              <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
            </div>
            <div class="modal-body">
              <form @submit.prevent="guardarMaterial">
                <div class="mb-3">
                  <label class="form-label">Descripción</label>
                  <input v-model="formMaterial.descripcion" type="text" class="form-control" required>
                </div>
                <div class="row">
                  <div class="col-md-6 mb-3">
                    <label class="form-label">Cantidad</label>
                    <input v-model.number="formMaterial.cantidad" type="number" class="form-control" required>
                  </div>
                  <div class="col-md-6 mb-3">
                    <label class="form-label">Unidad de Medida</label>
                    <select v-model="formMaterial.unidad_medida" class="form-select" required>
                      <option value="unidad">Unidad</option>
                      <option value="EMP X 25">Empaque x 25</option>
                      <option value="EMP X 50">Empaque x 50</option>
                    </select>
                  </div>
                </div>
                <div class="row">
                  <div class="col-md-6 mb-3">
                    <label class="form-label">Marca</label>
                    <input v-model="formMaterial.marca" type="text" class="form-control">
                  </div>
                  <div class="col-md-6 mb-3">
                    <label class="form-label">Precio Unitario (S/)</label>
                    <input v-model.number="formMaterial.p_u" type="number" step="0.01" class="form-control" required>
                  </div>
                </div>
                <div class="d-flex justify-content-end">
                  <button type="button" class="btn btn-secondary me-2" data-bs-dismiss="modal">Cancelar</button>
                  <button type="submit" class="btn btn-primary">Guardar</button>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </main>
  </template>
  
  <script setup>
  import { ref, computed, onMounted } from 'vue';
  import { Modal } from 'bootstrap';
  
  // Datos de ejemplo (reemplazar con llamadas a API)
  const materiales = ref([
    { id: 1, descripcion: 'BOLIGRAFO (LAPICERO) DE TINTA SECA PUNTA FINA COLOR AZUL', cantidad: 50, unidad_medida: 'unidad', marca: 'SIN MARCA.', p_u: 1.062 },
    { id: 2, descripcion: 'BOLIGRAFO (LAPICERO) DE TINTA SECA PUNTA FINA COLOR NEGRO', cantidad: 50, unidad_medida: 'unidad', marca: 'SIN MARCA.', p_u: 1.062 },
    { id: 3, descripcion: 'BOLIGRAFO (LAPICERO) DE TINTA SECA PUNTA FINA COLOR ROJO', cantidad: 50, unidad_medida: 'unidad', marca: 'SIN MARCA.', p_u: 0.9086 },
    { id: 4, descripcion: 'BORRADOR BLANCO PARA LAPIZ TAMAÑO GRANDE', cantidad: 50, unidad_medida: 'unidad', marca: 'SIN MARCA.', p_u: 0.5782 },
    { id: 5, descripcion: 'CINTA ADHESIVA TRANSPARENTE 1/2 in X 36 yd', cantidad: 10, unidad_medida: 'unidad', marca: 'SIN MARCA.', p_u: 0.814196 },
    { id: 6, descripcion: 'CINTA DE PLASTICO ADHESIVA PARA EMBALAJE 3 in X 110 yd', cantidad: 5, unidad_medida: 'unidad', marca: 'SIN MARCA.', p_u: 14.16 },
    { id: 7, descripcion: 'CLIP DE METAL 33 MM X 100', cantidad: 5, unidad_medida: 'unidad', marca: 'SIN MARCA.', p_u: 1.0856 },
    { id: 8, descripcion: 'CLIP MARIPOSA DE METAL Nº 2 X 50', cantidad: 5, unidad_medida: 'unidad', marca: 'SIN MARCA.', p_u: 3.044401 },
    { id: 9, descripcion: 'CORRECTOR LIQUIDO TIPO LAPICERO', cantidad: 50, unidad_medida: 'unidad', marca: 'SIN MARCA.', p_u: 1.8998 },
    { id: 10, descripcion: 'CUADERNO ESPIRAL CUADRICULADO TAMAÑO A4 X 100 HOJAS', cantidad: 10, unidad_medida: 'unidad', marca: 'SIN MARCA.', p_u: 6.076996 },
    { id: 11, descripcion: 'FOLDER MANILA TAMAÑO A4', cantidad: 10, unidad_medida: 'EMP X 25', marca: 'SIN MARCA.', p_u: 14.75 },
    { id: 12, descripcion: 'GRAPA 26/6 X 5000', cantidad: 5, unidad_medida: 'unidad', marca: 'SIN MARCA.', p_u: 3.54 },
    { id: 13, descripcion: 'LAPIZ NEGRO Nº 2 CON BORRADOR', cantidad: 25, unidad_medida: 'unidad', marca: 'SIN MARCA.', p_u: 0.413001 },
    { id: 14, descripcion: 'PAPEL BOND 80 G TAMAÑO A4', cantidad: 50, unidad_medida: 'EMP X 25', marca: 'SIN MARCA.', p_u: 10.608202 },
    { id: 15, descripcion: 'PLUMON RESALTADOR PUNTA GRUESA BISELADA COLOR AMARILLO', cantidad: 50, unidad_medida: 'unidad', marca: 'SIN MARCA.', p_u: 2.088601 },
    { id: 16, descripcion: 'SOBRE MANILA TAMAÑO A4', cantidad: 10, unidad_medida: 'EMP X 25', marca: 'SIN MARCA.', p_u: 10.620003 },
    { id: 17, descripcion: 'SOBRE MANILA TAMAÑO OFICIO', cantidad: 10, unidad_medida: 'EMP X 25', marca: 'SIN MARCA.', p_u: 11.8 },
    { id: 18, descripcion: 'SUJETADOR PARA PAPEL (TIPO FASTENER) DE METAL X 50', cantidad: 3, unidad_medida: 'unidad', marca: 'SIN MARCA.', p_u: 6.490002 },
    { id: 19, descripcion: 'FOLDER MANILA TAMAÑO A4', cantidad: 20, unidad_medida: 'EMP X 25', marca: 'SIN MARCA.', p_u: 14.75 },
    { id: 20, descripcion: 'SOBRE MANILA TAMAÑO A4', cantidad: 30, unidad_medida: 'EMP X 25', marca: 'SIN MARCA.', p_u: 10.620008 },
    { id: 21, descripcion: 'SOBRE MANILA TAMAÑO OFICIO', cantidad: 30, unidad_medida: 'EMP X 25', marca: 'SIN MARCA.', p_u: 10.62 }
  ]);
  
  // Estado del componente
  const filters = ref({
    descripcion: '',
    unidad_medida: ''
  });
  
  const currentPage = ref(1);
  const itemsPerPage = 10;
  const sortField = ref('descripcion');
  const sortDirection = ref('asc');
  const materialModal = ref(null);
  const materialEditando = ref(null);
  const formMaterial = ref({
    descripcion: '',
    cantidad: 1,
    unidad_medida: 'unidad',
    marca: '',
    p_u: 0
  });
  
  // Computed
  const unidadesMedida = computed(() => {
    return [...new Set(materiales.value.map(m => m.unidad_medida))];
  });
  
  const materialesFiltrados = computed(() => {
    let result = [...materiales.value];
    
    // Aplicar filtros
    if (filters.value.descripcion) {
      result = result.filter(m => 
        m.descripcion.toLowerCase().includes(filters.value.descripcion.toLowerCase())
      );
    }
    
    if (filters.value.unidad_medida) {
      result = result.filter(m => m.unidad_medida === filters.value.unidad_medida);
    }
    
    // Ordenar
    result.sort((a, b) => {
      const fieldA = a[sortField.value].toString().toLowerCase();
      const fieldB = b[sortField.value].toString().toLowerCase();
      
      if (fieldA < fieldB) return sortDirection.value === 'asc' ? -1 : 1;
      if (fieldA > fieldB) return sortDirection.value === 'asc' ? 1 : -1;
      return 0;
    });
    
    // Paginar
    const start = (currentPage.value - 1) * itemsPerPage;
    const end = start + itemsPerPage;
    return result.slice(start, end);
  });
  
  const totalPages = computed(() => {
    return Math.ceil(materiales.value.length / itemsPerPage);
  });
  
  // Métodos
  const sortBy = (field) => {
    if (sortField.value === field) {
      sortDirection.value = sortDirection.value === 'asc' ? 'desc' : 'asc';
    } else {
      sortField.value = field;
      sortDirection.value = 'asc';
    }
  };
  
  const agregarMaterial = () => {
    materialEditando.value = null;
    formMaterial.value = {
      descripcion: '',
      cantidad: 1,
      unidad_medida: 'unidad',
      marca: '',
      p_u: 0
    };
    const modal = new Modal(document.getElementById('materialModal'));
    modal.show();
  };
  
  const editarMaterial = (material) => {
    materialEditando.value = material.id;
    formMaterial.value = { ...material };
    const modal = new Modal(document.getElementById('materialModal'));
    modal.show();
  };
  
  const guardarMaterial = () => {
    if (materialEditando.value) {
      // Editar
      const index = materiales.value.findIndex(m => m.id === materialEditando.value);
      if (index !== -1) {
        materiales.value[index] = { ...formMaterial.value };
      }
    } else {
      // Agregar
      const nuevoId = Math.max(...materiales.value.map(m => m.id)) + 1;
      materiales.value.push({
        id: nuevoId,
        ...formMaterial.value
      });
    }
    
    const modal = Modal.getInstance(document.getElementById('materialModal'));
    modal.hide();
  };
  
  const eliminarMaterial = (id) => {
    if (confirm('¿Está seguro de eliminar este material?')) {
      materiales.value = materiales.value.filter(m => m.id !== id);
    }
  };
  
  // Inicialización
  onMounted(() => {
    materialModal.value = new Modal(document.getElementById('materialModal'));
  });
  </script>
  
  <style scoped>
  .sortable {
    cursor: pointer;
  }
  .sortable:hover {
    background-color: #f8f9fa;
  }
  .table-responsive {
    max-height: 600px;
    overflow-y: auto;
  }
  </style>