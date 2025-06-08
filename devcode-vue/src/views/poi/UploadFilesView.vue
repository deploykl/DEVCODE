<template>
  <main id="main" class="main">
    <div class="container-fluid">
      <div class="row">
        <div class="col-12">
          <div class="page-header d-flex justify-content-between align-items-center mb-4">
            <h1 class="page-title">Archivos del Mes: <span class="text-primary">{{ mes }}</span></h1>
            <button v-if="archivosSubidos.length > 0" @click="downloadAllAsZip" class="btn btn-outline-primary"
              :disabled="loadingZip">
              <i class="fas fa-file-archive me-2"></i>
              {{ loadingZip ? 'Preparando ZIP...' : 'Descargar Todo (ZIP)' }}
            </button>
          </div>

          <!-- Panel de Subida -->
          <div class="card shadow-sm mb-4">
            <div class="card-header bg-white">
              <h5 class="mb-0">Subir Archivos</h5>
            </div>
            <div class="card-body">
              <form @submit.prevent="ADD">
                <div class="drop-area" @dragover.prevent="dragOver" @dragleave.prevent="dragLeave"
                  @drop.prevent="handleDrop" @click="fileInput.click()" :class="{ 'drag-active': isDragging }">
                  <input type="file" ref="fileInput" class="d-none" @change="handleFileUpload" multiple />
                  <div class="drop-content text-center">
                    <i class="fas fa-cloud-upload-alt fa-3x text-primary mb-3"></i>
                    <h5>Arrastra tus archivos aquí</h5>
                    <p class="text-muted">o haz clic para seleccionar archivos</p>
                    <div class="file-types mt-2">
                      <span class="badge bg-light text-dark me-2">JPG/PNG</span>
                      <span class="badge bg-light text-dark me-2">PDF</span>
                      <span class="badge bg-light text-dark me-2">DOC/XLS/PPT</span>
                      <span class="badge bg-light text-dark">TXT</span>
                    </div>
                    <p class="small text-muted mt-2">Tamaño máximo por archivo: 200MB</p>
                  </div>
                </div>

                <div v-if="uploadProgress > 0 && uploadProgress < 100" class="mt-3">
                  <div class="d-flex justify-content-between mb-1">
                    <span>Progreso de subida:</span>
                    <span>{{ uploadProgress }}%</span>
                  </div>
                  <div class="progress" style="height: 8px;">
                    <div class="progress-bar progress-bar-striped progress-bar-animated bg-success" role="progressbar"
                      :style="`width: ${uploadProgress}%`" :aria-valuenow="uploadProgress" aria-valuemin="0"
                      aria-valuemax="100"></div>
                  </div>
                </div>

                <button type="submit" class="btn btn-primary mt-3 w-100" :disabled="loading || archivos.length === 0">
                  <i class="fas fa-upload me-2"></i>
                  {{ loading ? 'Subiendo...' : `Subir ${archivos.length} Archivo(s)` }}
                </button>
              </form>
            </div>
          </div>

          <!-- Archivos Seleccionados -->
          <div class="card shadow-sm mb-4" v-if="archivos.length > 0">
            <div class="card-header bg-white d-flex justify-content-between align-items-center">
              <h5 class="mb-0">Archivos Seleccionados</h5>
              <span class="badge bg-primary">{{ archivos.length }}</span>
            </div>
            <div class="card-body p-0">
              <ul class="list-group list-group-flush">
                <li v-for="(file, index) in archivos" :key="index"
                  class="list-group-item d-flex justify-content-between align-items-center">
                  <div class="d-flex align-items-center">
                    <div class="file-icon me-3" :class="fileIconClass(file)">
                      <i :class="fileIcon(file)"></i>
                    </div>
                    <div>
                      <div class="fw-bold text-truncate" style="max-width: 300px;">{{ file.name }}</div>
                      <small class="text-muted">{{ formatFileSize(file.size) }}</small>
                    </div>
                  </div>
                  <button @click.stop="removeFile(index)" class="btn btn-sm btn-outline-danger">
                    <i class="fas fa-times"></i>
                  </button>
                </li>
              </ul>
            </div>
          </div>

          <!-- Archivos Subidos -->
          <div class="card shadow-sm">
            <div class="card-header bg-white d-flex justify-content-between align-items-center">
              <h5 class="mb-0">Archivos Subidos</h5>
              <span class="badge bg-primary">{{ totalArchivos }}</span>
            </div>
            <div class="card-body p-0">
              <div v-if="archivosSubidos.length > 0">
                <div class="table-responsive">
                  <table class="table table-hover align-middle">
                    <thead class="table-light">
                      <tr>
                        <th width="50">#</th>
                        <th>Nombre</th>
                        <th width="120">Tamaño</th>
                        <th width="180">Fecha</th>
                        <th width="100" class="text-center">Vista Previa</th>
                        <th width="100" class="text-center">Acciones</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr v-for="(file, index) in archivosSubidos" :key="file.id">
                        <td>{{ index + 1 }}</td>
                        <td>
                          <div class="d-flex align-items-center">
                            <div class="file-icon me-2" :class="fileIconClass(file.archivo)">
                              <i :class="fileIconFromUrl(file.archivo)"></i>
                            </div>
                            <span class="text-truncate" style="max-width: 250px;">{{ getFileName(file.archivo) }}</span>
                          </div>
                        </td>
                        <td>{{ file.size ? formatFileSize(file.size) : 'N/A' }}</td>
                        <td>{{ formatDate(file.fecha_subida) }}</td>
                        <td class="text-center">
                          <button @click="verArchivo(file.archivo)" class="btn btn-sm btn-icon"
                            :class="previewButtonClass(file.archivo)" :title="previewButtonTitle(file.archivo)">
                            <i :class="previewButtonIcon(file.archivo)"></i>
                          </button>
                        </td>
                        <td class="text-center">
                          <div class="btn-group btn-group-sm" role="group">
                            <button @click="downloadFile(file.archivo)" class="btn btn-outline-primary"
                              title="Descargar">
                              <i class="fas fa-download"></i>
                            </button>
                            <button @click="confirmDelete(file.id)" class="btn btn-outline-danger" title="Eliminar">
                              <i class="fas fa-trash"></i>
                            </button>
                          </div>
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
              <div v-else class="text-center py-4">
                <i class="fas fa-folder-open fa-3x text-muted mb-3"></i>
                <p class="text-muted">No hay archivos subidos para este mes</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal para vista previa -->
    <div class="modal fade" id="previewModal" tabindex="-1" aria-hidden="true">
      <div class="modal-dialog modal-xl modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">
              <i :class="previewButtonIcon(currentPreviewFile)" class="me-2"></i>
              {{ currentFileName }}
            </h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body text-center p-0">
            <div v-if="isImage(currentPreviewFile)" class="image-preview-container">
              <img :src="currentPreviewFile" :alt="currentFileName" class="img-fluid" />
            </div>
            <div v-else-if="isPdf(currentPreviewFile)" class="pdf-preview-container">
              <iframe :src="`https://docs.google.com/gview?url=${currentPreviewFile}&embedded=true`" frameborder="0"
                class="w-100" style="height: 70vh;"></iframe>
            </div>
            <div v-else class="d-flex align-items-center justify-content-center" style="height: 300px;">
              <div class="text-center">
                <i :class="previewButtonIcon(currentPreviewFile)" class="fa-5x mb-3"></i>
                <p>Vista previa no disponible para este tipo de archivo</p>
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
              <i class="fas fa-times me-2"></i>Cerrar
            </button>
            <a :href="currentPreviewFile" download class="btn btn-primary">
              <i class="fas fa-download me-2"></i>Descargar
            </a>
          </div>
        </div>
      </div>
    </div>
  </main>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { api, getAuthToken } from '@/components/services/auth_axios';
import { SwalSuccess, SwalWarning, SwalError, SwalDelete } from '@/components/widgets/SwalComponent';
import JSZip from 'jszip';
import { saveAs } from 'file-saver';
import { Modal } from 'bootstrap';

const fileInput = ref(null);
const loading = ref(false);
const loadingZip = ref(false);
const archivos = ref([]);
const archivosSubidos = ref([]);
const totalArchivos = ref(0);
const route = useRoute();
const mes = route.params.mes;
const reporteId = route.params.reporteId;
const currentPreviewFile = ref(null);
const currentFileName = ref('');
const uploadProgress = ref(0);
const isDeleting = ref(false);
const isDragging = ref(false);

// Configuración de archivos permitidos
const ALLOWED_TYPES = [
  'image/jpeg',
  'image/png',
  'image/gif',
  'application/pdf',
  'application/vnd.ms-excel',
  'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
  'application/msword',
  'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
  'application/vnd.ms-powerpoint',
  'application/vnd.openxmlformats-officedocument.presentationml.presentation',
  'text/plain'
];
const MAX_FILE_SIZE = 200 * 1024 * 1024; // 200MB

// Funciones de utilidad
const formatFileSize = (bytes) => {
  if (bytes === 0) return '0 Bytes';
  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2) + ' ' + sizes[i]);
};

const formatDate = (dateString) => {
  const options = { year: 'numeric', month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' };
  return new Date(dateString).toLocaleDateString('es-ES', options);
};

const getFileName = (filename) => {
  return filename ? filename.split('/').pop().split('\\').pop() : 'Archivo sin nombre';
};

// Funciones para determinar tipos de archivo
const isImage = (filename) => {
  return filename && /\.(jpg|jpeg|png|gif|webp|bmp)$/i.test(filename);
};

const isPdf = (filename) => {
  return filename && /\.pdf$/i.test(filename);
};

const isExcel = (filename) => {
  return filename && /\.(xls|xlsx|csv)$/i.test(filename);
};

const isWord = (filename) => {
  return filename && /\.(doc|docx|rtf)$/i.test(filename);
};

const isPowerPoint = (filename) => {
  return filename && /\.(ppt|pptx)$/i.test(filename);
};

const isText = (filename) => {
  return filename && /\.(txt|log|md)$/i.test(filename);
};

// Funciones para iconos y estilos
const fileIcon = (file) => {
  const type = file.type;
  if (type.includes('image')) return 'fas fa-image';
  if (type.includes('pdf')) return 'fas fa-file-pdf';
  if (type.includes('excel') || type.includes('spreadsheet')) return 'fas fa-file-excel';
  if (type.includes('word') || type.includes('document')) return 'fas fa-file-word';
  if (type.includes('powerpoint') || type.includes('presentation')) return 'fas fa-file-powerpoint';
  if (type.includes('text')) return 'fas fa-file-alt';
  return 'fas fa-file';
};

const fileIconFromUrl = (filename) => {
  if (isImage(filename)) return 'fas fa-image';
  if (isPdf(filename)) return 'fas fa-file-pdf';
  if (isExcel(filename)) return 'fas fa-file-excel';
  if (isWord(filename)) return 'fas fa-file-word';
  if (isPowerPoint(filename)) return 'fas fa-file-powerpoint';
  if (isText(filename)) return 'fas fa-file-alt';
  return 'fas fa-file';
};

const fileIconClass = (fileOrUrl) => {
  const isUrl = typeof fileOrUrl === 'string';
  const filename = isUrl ? fileOrUrl : fileOrUrl.name;

  if (isImage(filename)) return 'bg-primary-light text-primary';
  if (isPdf(filename)) return 'bg-danger-light text-danger';
  if (isExcel(filename)) return 'bg-success-light text-success';
  if (isWord(filename)) return 'bg-info-light text-info';
  if (isPowerPoint(filename)) return 'bg-warning-light text-warning';
  return 'bg-secondary-light text-secondary';
};

const previewButtonIcon = (filename) => {
  if (isImage(filename)) return 'fas fa-eye';
  if (isPdf(filename)) return 'fas fa-file-pdf';
  if (isExcel(filename)) return 'fas fa-file-excel';
  if (isWord(filename)) return 'fas fa-file-word';
  if (isPowerPoint(filename)) return 'fas fa-file-powerpoint';
  return 'fas fa-file-download';
};

const previewButtonClass = (filename) => {
  if (isImage(filename)) return 'btn-primary';
  if (isPdf(filename)) return 'btn-danger';
  if (isExcel(filename)) return 'btn-success';
  if (isWord(filename)) return 'btn-info';
  if (isPowerPoint(filename)) return 'btn-warning';
  return 'btn-secondary';
};

const previewButtonTitle = (filename) => {
  if (isImage(filename)) return 'Ver imagen';
  if (isPdf(filename)) return 'Ver PDF';
  if (isExcel(filename)) return 'Abrir en Excel';
  if (isWord(filename)) return 'Abrir en Word';
  if (isPowerPoint(filename)) return 'Abrir en PowerPoint';
  return 'Descargar archivo';
};

// Manejo de archivos
const handleFileUpload = (event) => {
  const files = Array.from(event.target.files);
  if (files.length) {
    processFiles(files);
  }
  event.target.value = '';
};

const processFiles = (files) => {
  const validFiles = files.filter(file => {
    const isValidType = ALLOWED_TYPES.includes(file.type);
    const isValidSize = file.size <= MAX_FILE_SIZE;

    if (!isValidType) {
      SwalWarning(`El archivo ${file.name} no tiene un formato permitido.`, '', false);
      return false;
    }

    if (!isValidSize) {
      SwalWarning(`El archivo ${file.name} (${formatFileSize(file.size)}) excede el tamaño máximo de 200MB.`, '', false);
      return false;
    }

    if (file.size > 50 * 1024 * 1024) {
      SwalWarning(`Archivo grande: ${file.name} (${formatFileSize(file.size)}). La subida puede tardar varios minutos.`);
    }

    return true;
  });

  archivos.value = [...archivos.value, ...validFiles];
};

const dragOver = () => {
  isDragging.value = true;
};

const dragLeave = () => {
  isDragging.value = false;
};

const handleDrop = (event) => {
  isDragging.value = false;
  const files = Array.from(event.dataTransfer.files);
  if (files.length) {
    processFiles(files);
  }
};

const removeFile = (index) => {
  archivos.value.splice(index, 1);
};

// Operaciones con archivos
const verArchivo = (fileUrl) => {
  currentPreviewFile.value = fileUrl;
  currentFileName.value = getFileName(fileUrl);

  if (isImage(fileUrl)) {
    const modal = new Modal(document.getElementById('previewModal'));
    modal.show();
  } else if (isPdf(fileUrl)) {
    window.open(fileUrl, '_blank');
  } else if (isExcel(fileUrl) || isWord(fileUrl) || isPowerPoint(fileUrl)) {
    abrirArchivoOffice(fileUrl);
  } else {
    window.open(fileUrl, '_blank');
  }
};


function abrirArchivoOffice(url) {
  const baseUrl = window.location.href.split('#')[0];
  const fullUrl = url.startsWith('http') ? url : `${baseUrl}${url}`;
  const extension = url.split('.').pop().toLowerCase();

  try {
    switch (extension) {
      case 'doc':
      case 'docx':
        window.location.href = `ms-word:ofe|u|${fullUrl}`;
        break;
      case 'xls':
      case 'xlsx':
        window.location.href = `ms-excel:ofe|u|${fullUrl}`;
        break;
      case 'ppt':
      case 'pptx':
        window.location.href = `ms-powerpoint:ofe|u|${fullUrl}`;
        break;
      default:
        window.open(fullUrl, '_blank');
    }
  } catch (error) {
    console.error('Error al abrir el archivo:', error);
    window.open(fullUrl, '_blank');
  }
}


const downloadFile = (fileUrl) => {
  const link = document.createElement('a');
  link.href = fileUrl;
  link.download = getFileName(fileUrl);
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
};

const downloadAllAsZip = async () => {
  if (loadingZip.value) return;

  loadingZip.value = true;

  try {
    const zip = new JSZip();
    const token = getAuthToken();

    // Crear una carpeta en el ZIP con el nombre del mes
    const folder = zip.folder(`Archivos_${mes}`);

    // Descargar cada archivo y agregarlo al ZIP
    for (const file of archivosSubidos.value) {
      try {
        const response = await fetch(file.archivo, {
          headers: { Authorization: `Bearer ${token}` }
        });

        if (response.ok) {
          const blob = await response.blob();
          folder.file(getFileName(file.archivo), blob);
        }
      } catch (error) {
        console.error(`Error al descargar ${file.archivo}:`, error);
      }
    }

    // Generar el archivo ZIP
    const content = await zip.generateAsync({ type: 'blob' });
    saveAs(content, `Archivos_${mes}.zip`);

    await SwalSuccess('Archivo ZIP generado con éxito', 'Todos los archivos han sido comprimidos y están listos para descargar.');
  } catch (error) {
    console.error('Error al generar el ZIP:', error);
    await SwalError('Error al generar el archivo ZIP', 'Por favor intente nuevamente.');
  } finally {
    loadingZip.value = false;
  }
};

// Operaciones CRUD
const LISTAR = async () => {
  try {
    const token = getAuthToken();
    const response = await api.get(`poi/archivo/`, {
      params: { mes, tarea: reporteId },
      headers: { Authorization: `Bearer ${token}` }
    });

    archivosSubidos.value = response.data.map(file => ({
      ...file,
      archivo: file.archivo || ''
    }));
    totalArchivos.value = archivosSubidos.value.length;
  } catch (error) {
    console.error('Error al obtener los archivos:', error);
    SwalError('Error al cargar los archivos subidos.');
  }
};

const ADD = async () => {
  if (archivos.value.length === 0) {
    SwalWarning();
    return;
  }

  const largeFiles = archivos.value.filter(f => f.size > 100 * 1024 * 1024);
  if (largeFiles.length > 0) {
    const confirm = await SwalWarning(
      'Advertencia',
      `Está intentando subir ${largeFiles.length} archivo(s) grande(s) (>100MB). 
      Esto puede tardar varios minutos. ¿Desea continuar?`,
      true
    );
    if (!confirm.isConfirmed) return;
  }

  loading.value = true;
  uploadProgress.value = 0;
  const token = getAuthToken();
  const successfulUploads = [];
  const failedUploads = [];

  try {
    for (const [index, file] of archivos.value.entries()) {
      const formData = new FormData();
      formData.append('archivo', file);
      formData.append('reporte_tarea', reporteId);

      try {
        await api.post(`poi/archivo/`, formData, {
          headers: {
            Authorization: `Bearer ${token}`,
            'Content-Type': 'multipart/form-data'
          },
          timeout: 600000,
          onUploadProgress: (progressEvent) => {
            if (progressEvent.total) {
              const percent = Math.round((progressEvent.loaded * 100) / progressEvent.total);
              uploadProgress.value = Math.round(((index * 100) + percent) / archivos.value.length);
            }
          }
        });
        successfulUploads.push(file.name);
      } catch (error) {
        console.error(`Error al subir ${file.name}:`, error);
        failedUploads.push({
          name: file.name,
          error: error.response?.data?.message || 'Error desconocido'
        });
        await new Promise(resolve => setTimeout(resolve, 1000));
      }
    }

    if (failedUploads.length > 0) {
      const errorList = failedUploads.map(f => `${f.name}: ${f.error}`).join('<br>');
      await SwalWarning(
        `Subida parcialmente completada`,
        `Se subieron ${successfulUploads.length} de ${archivos.value.length} archivos.<br><br>
        Errores:<br>${errorList}`,
        true
      );
    } else {
      await SwalSuccess(`Todos los archivos (${successfulUploads.length}) se subieron correctamente.`);
    }

    await LISTAR();
    archivos.value = [];
  } catch (error) {
    console.error('Error general:', error);
    await SwalError();
  } finally {
    loading.value = false;
    uploadProgress.value = 0;
  }
};

const confirmDelete = async (id) => {
  if (isDeleting.value) return;

  const result = await SwalWarning();

  if (result.isConfirmed) {
    await DELETE(id);
  }
};

const DELETE = async (id) => {
  isDeleting.value = true;
  try {
    const token = getAuthToken();
    await api.delete(`poi/archivo/${id}/`, {
      headers: { Authorization: `Bearer ${token}` },
    });

    archivosSubidos.value = archivosSubidos.value.filter(archivo => archivo.id !== id);
    totalArchivos.value = archivosSubidos.value.length;
    await SwalDelete();
  } catch (error) {
    console.error('Error al eliminar el archivo:', error);
    await SwalError('Error al eliminar el archivo. Por favor intente nuevamente.');
  } finally {
    isDeleting.value = false;
  }
};

onMounted(() => {
  LISTAR();
});
</script>

<style scoped>
.main {
  padding: 2rem;
  background-color: #f8f9fa;
}

.page-header {
  padding: 1rem 0;
  border-bottom: 1px solid #eaeaea;
}

.page-title {
  font-weight: 600;
  color: #2c3e50;
}

.card {
  border: none;
  border-radius: 10px;
  overflow: hidden;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.card:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
}

.card-header {
  padding: 1rem 1.5rem;
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
}

.drop-area {
  border: 2px dashed #dee2e6;
  border-radius: 8px;
  padding: 2.5rem;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
  background-color: #f8fafc;
}

.drop-area.drag-active {
  border-color: #4361ee;
  background-color: rgba(67, 97, 238, 0.05);
}

.drop-content {
  pointer-events: none;
}

.file-icon {
  width: 40px;
  height: 40px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.bg-primary-light {
  background-color: rgba(67, 97, 238, 0.1);
}

.bg-danger-light {
  background-color: rgba(220, 53, 69, 0.1);
}

.bg-success-light {
  background-color: rgba(25, 135, 84, 0.1);
}

.bg-info-light {
  background-color: rgba(13, 202, 240, 0.1);
}

.bg-warning-light {
  background-color: rgba(255, 193, 7, 0.1);
}

.bg-secondary-light {
  background-color: rgba(108, 117, 125, 0.1);
}

.list-group-item {
  padding: 1rem 1.5rem;
  border-color: rgba(0, 0, 0, 0.03);
}

.table {
  margin-bottom: 0;
}

.table th {
  font-weight: 600;
  color: #495057;
  text-transform: uppercase;
  font-size: 0.75rem;
  letter-spacing: 0.5px;
}

.table td {
  vertical-align: middle;
}

.btn-icon {
  width: 32px;
  height: 32px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0;
}

.image-preview-container {
  max-height: 70vh;
  overflow: auto;
  display: flex;
  align-items: center;
  justify-content: center;
}

.pdf-preview-container {
  width: 100%;
  height: 70vh;
}

.file-types {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
}

@media (max-width: 768px) {
  .main {
    padding: 1rem;
  }

  .card-header,
  .card-body {
    padding: 0.75rem;
  }

  .drop-area {
    padding: 1.5rem;
  }

  .table-responsive {
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
  }
}
</style>