// Funciones para el avance físico

export const getBadgeClassFisico = (porcentaje) => {
    if (porcentaje <= 85) {
        return 'badge bg-danger';
      } else if (porcentaje > 85 && porcentaje <= 90) {
        return 'badge bg-warning';
      } else {
        return 'badge bg-success'; // Incluye todos los casos por encima de 90%, incluyendo > 100
      }
    };
export const getTextClassFisico = (porcentaje) => {
    if (porcentaje <= 85) {
        return 'text-danger';
      } else if (porcentaje > 85 && porcentaje <= 90) {
        return 'text-warning';
      } else {
        return 'text-success'; // Incluye todos los casos por encima de 90%, incluyendo > 100
      }
    };

export const getMensajeAvanceFisico = (porcentaje) => {
    if (porcentaje <= 85) {
        return 'Deficiente';
      } else if (porcentaje > 85 && porcentaje <= 90) {
        return 'Regular';
      } else {
        return 'Bueno'; // Incluye todos los casos por encima de 90%, incluyendo > 100
      }
    };

// Funciones para el avance presupuestal

export const getBadgeClassPresupuestal = (porcentaje) => {
    if (porcentaje < 60) {
      return 'badge bg-danger';
    } else if (porcentaje >= 60 && porcentaje < 80) {
      return 'badge bg-warning';
    } else if (porcentaje >= 80 && porcentaje <= 100) {
      return 'badge bg-success';
    } else {
      return 'text-dark';
    }
};

export const getTextClassPresupuestal = (porcentaje) => {
    if (porcentaje < 60) {
      return 'text-danger';
    } else if (porcentaje >= 60 && porcentaje < 80) {
      return 'text-warning';
    } else if (porcentaje >= 80 && porcentaje <= 100) {
      return 'text-success';
    } else {
      return 'text-dark';
    }
};

export const getMensajeAvancePresupuestal = (porcentaje) => {
    if (porcentaje < 60) {
      return 'Deficiente';
    } else if (porcentaje >= 60 && porcentaje < 80) {
      return 'Regular';
    } else if (porcentaje >= 80 && porcentaje <= 100) {
      return 'Bueno';
    } else {
      return '';
    }
};
