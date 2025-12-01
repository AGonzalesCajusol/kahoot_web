/**
 * MEJORAS DE USABILIDAD - HEURÍSTICAS DE JAKOB NIELSEN
 * Este archivo implementa funcionalidades para mejorar la usabilidad
 * según las 10 heurísticas de Nielsen
 */

// ============================================
// HEURÍSTICA 1: VISIBILIDAD DEL ESTADO DEL SISTEMA
// ============================================

/**
 * Muestra un indicador de carga en la parte superior
 */
function mostrarIndicadorCarga() {
    const barraCarga = document.createElement('div');
    barraCarga.className = 'loading-indicator';
    barraCarga.id = 'loading-indicator';
    document.body.appendChild(barraCarga);
}

/**
 * Oculta el indicador de carga
 */
function ocultarIndicadorCarga() {
    const barraCarga = document.getElementById('loading-indicator');
    if (barraCarga) {
        barraCarga.remove();
    }
}

/**
 * Muestra feedback de acción al usuario
 * @param {string} mensaje - Mensaje a mostrar
 * @param {string} tipo - Tipo: 'success', 'error', 'info', 'warning'
 * @param {number} duracion - Duración en milisegundos (default: 3000)
 */
function mostrarFeedback(mensaje, tipo = 'info', duracion = 3000) {
    // Remover retroalimentación anterior si existe
    const retroalimentacionAnterior = document.querySelector('.action-feedback');
    if (retroalimentacionAnterior) {
        retroalimentacionAnterior.remove();
    }

    const retroalimentacion = document.createElement('div');
    retroalimentacion.className = `action-feedback ${tipo}`;
    retroalimentacion.innerHTML = `
        <div class="d-flex align-items-center gap-2">
            <i class="bi ${obtenerIconoTipo(tipo)}"></i>
            <span>${mensaje}</span>
            <button type="button" class="btn-close btn-close-white ms-auto" onclick="this.parentElement.parentElement.remove()"></button>
        </div>
    `;

    document.body.appendChild(retroalimentacion);

    // Eliminar automáticamente después de la duración
    setTimeout(() => {
        if (retroalimentacion.parentElement) {
            retroalimentacion.style.animation = 'slideInRight 0.3s ease-out reverse';
            setTimeout(() => retroalimentacion.remove(), 300);
        }
    }, duracion);
}

/**
 * Obtiene el icono según el tipo de retroalimentación
 */
function obtenerIconoTipo(tipo) {
    const iconos = {
        'success': 'bi-check-circle-fill',
        'error': 'bi-x-circle-fill',
        'info': 'bi-info-circle-fill',
        'warning': 'bi-exclamation-triangle-fill'
    };
    return iconos[tipo] || iconos['info'];
}

/**
 * Actualiza el estado de un formulario (guardado/no guardado)
 */
function actualizarEstadoFormulario(guardado = false) {
    const estadoIndicador = document.getElementById('form-status-indicator');
    if (estadoIndicador) {
        estadoIndicador.className = `form-status-indicator ${guardado ? 'saved' : 'unsaved'}`;
        estadoIndicador.title = guardado ? 'Cambios guardados' : 'Cambios sin guardar';
    }
}

// ============================================
// HEURÍSTICA 2: CORRESPONDENCIA SISTEMA-MUNDO REAL
// ============================================

/**
 * Formatea fechas en formato legible
 */
function formatearFecha(fecha) {
    if (!fecha) return '';
    const fechaObj = new Date(fecha);
    const opciones = { 
        year: 'numeric', 
        month: 'long', 
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    };
    return fechaObj.toLocaleDateString('es-ES', opciones);
}

/**
 * Formatea números grandes de manera legible
 */
function formatearNumero(numero) {
    if (numero >= 1000000) {
        return (numero / 1000000).toFixed(1) + 'M';
    } else if (numero >= 1000) {
        return (numero / 1000).toFixed(1) + 'K';
    }
    return numero.toString();
}

// ============================================
// HEURÍSTICA 3: CONTROL Y LIBERTAD DEL USUARIO
// ============================================

/**
 * Muestra un diálogo de confirmación antes de acciones destructivas
 * @param {string} mensaje - Mensaje de confirmación
 * @param {Function} funcionCallback - Función a ejecutar si se confirma
 */
function confirmarAccion(mensaje, funcionCallback) {
    if (typeof Swal !== 'undefined') {
        Swal.fire({
            title: '¿Estás seguro?',
            text: mensaje,
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#dc3545',
            cancelButtonColor: '#6c757d',
            confirmButtonText: 'Sí, continuar',
            cancelButtonText: 'Cancelar',
            reverseButtons: true
        }).then((resultado) => {
            if (resultado.isConfirmed && funcionCallback) {
                funcionCallback();
            }
        });
    } else {
        if (confirm(mensaje)) {
            if (funcionCallback) funcionCallback();
        }
    }
}

/**
 * Implementa funcionalidad de deshacer
 */
const historialDeshacer = [];
let indiceHistorial = -1;

function guardarEstadoParaDeshacer(estado) {
    historialDeshacer.push(JSON.parse(JSON.stringify(estado)));
    indiceHistorial = historialDeshacer.length - 1;
    // Limitar historial a 50 estados
    if (historialDeshacer.length > 50) {
        historialDeshacer.shift();
        indiceHistorial--;
    }
}

function deshacer() {
    if (indiceHistorial > 0) {
        indiceHistorial--;
        return historialDeshacer[indiceHistorial];
    }
    return null;
}

function rehacer() {
    if (indiceHistorial < historialDeshacer.length - 1) {
        indiceHistorial++;
        return historialDeshacer[indiceHistorial];
    }
    return null;
}

// ============================================
// HEURÍSTICA 4: CONSISTENCIA Y ESTÁNDARES
// ============================================

/**
 * Estandariza los colores de los botones según su función
 */
function aplicarEstilosConsistentes() {
    // Asegurar que todos los botones de acción primaria tengan el mismo estilo
    document.querySelectorAll('.btn-primary').forEach(boton => {
        if (!boton.classList.contains('no-standardize')) {
            boton.classList.add('btn-primary');
        }
    });
}

// ============================================
// HEURÍSTICA 5: PREVENCIÓN DE ERRORES
// ============================================

/**
 * Valida un campo en tiempo real
 * @param {HTMLElement} campo - Campo a validar
 * @param {Function} funcionValidador - Función de validación
 */
function validarCampoTiempoReal(campo, funcionValidador) {
    campo.addEventListener('blur', function() {
        const valor = this.value;
        const esValido = funcionValidador(valor);
        
        if (esValido) {
            this.classList.remove('is-invalid');
            this.classList.add('is-valid');
        } else {
            this.classList.remove('is-valid');
            this.classList.add('is-invalid');
        }
    });
    
    campo.addEventListener('input', function() {
        this.classList.remove('is-invalid', 'is-valid');
    });
}

/**
 * Previene envío de formulario si hay errores
 */
function prevenirEnvioConErrores(formulario) {
    formulario.addEventListener('submit', function(evento) {
        const camposInvalidos = formulario.querySelectorAll('.is-invalid');
        if (camposInvalidos.length > 0) {
            evento.preventDefault();
            mostrarFeedback('Por favor, corrige los errores antes de enviar', 'error');
            camposInvalidos[0].focus();
            return false;
        }
    });
}

// ============================================
// HEURÍSTICA 6: RECONOCIMIENTO ANTES QUE RECUERDO
// ============================================

/**
 * Inicializa tooltips mejorados
 */
function inicializarTooltips() {
    document.querySelectorAll('[data-tooltip]').forEach(elemento => {
        elemento.classList.add('tooltip-enhanced');
    });
}

/**
 * Muestra ayuda contextual
 */
function mostrarAyudaContextual(elementoId, contenido) {
    const elemento = document.getElementById(elementoId);
    if (elemento) {
        const ayuda = document.createElement('div');
        ayuda.className = 'contextual-suggestion';
        ayuda.textContent = contenido;
        elemento.parentElement.insertBefore(ayuda, elemento.nextSibling);
    }
}

// ============================================
// HEURÍSTICA 7: FLEXIBILIDAD Y EFICIENCIA
// ============================================

/**
 * Registra atajos de teclado
 * @param {string} tecla - Tecla o combinación (ej: 'Ctrl+S', 'Escape')
 * @param {Function} funcionCallback - Función a ejecutar
 */
function registrarAtajoTeclado(tecla, funcionCallback) {
    document.addEventListener('keydown', function(evento) {
        const teclaPresionada = evento.ctrlKey ? `Ctrl+${evento.key}` : evento.key;
        if (teclaPresionada === tecla) {
            evento.preventDefault();
            funcionCallback();
        }
    });
}

/**
 * Inicializa atajos comunes
 */
function inicializarAtajosComunes() {
    // Ctrl+S para guardar
    registrarAtajoTeclado('Ctrl+s', function() {
        const botonGuardar = document.querySelector('[id*="guardar"], [id*="save"]');
        if (botonGuardar && !botonGuardar.disabled) {
            botonGuardar.click();
            mostrarFeedback('Guardado (Ctrl+S)', 'success', 2000);
        }
    });
    
    // Escape para cancelar/cerrar
    registrarAtajoTeclado('Escape', function() {
        const modal = document.querySelector('.modal.show');
        if (modal) {
            const botonCerrar = modal.querySelector('[data-bs-dismiss="modal"]');
            if (botonCerrar) botonCerrar.click();
        }
    });
}

// ============================================
// HEURÍSTICA 8: DISEÑO ESTÉTICO Y MINIMALISTA
// ============================================

/**
 * Oculta elementos innecesarios cuando no se necesitan
 */
function ocultarElementosInnecesarios() {
    document.querySelectorAll('.hide-when-not-needed').forEach(elemento => {
        if (elemento.textContent.trim() === '' || elemento.children.length === 0) {
            elemento.style.display = 'none';
        }
    });
}

// ============================================
// HEURÍSTICA 9: RECONOCER Y RECUPERARSE DE ERRORES
// ============================================

/**
 * Muestra un mensaje de error claro y constructivo
 * @param {string} titulo - Título del error
 * @param {string} descripcion - Descripción del error
 * @param {string} solucion - Solución sugerida
 */
function mostrarErrorClaro(titulo, descripcion, solucion = '') {
    const divError = document.createElement('div');
    divError.className = 'error-message';
    divError.innerHTML = `
        <div>
            <div class="error-title">${titulo}</div>
            <div class="error-description">${descripcion}</div>
            ${solucion ? `<div class="error-solution">${solucion}</div>` : ''}
        </div>
    `;
    
    // Insertar al inicio del contenido principal
    const contenidoPrincipal = document.querySelector('main');
    if (contenidoPrincipal) {
        contenidoPrincipal.insertBefore(divError, contenidoPrincipal.firstChild);
        
        // Eliminar automáticamente después de 10 segundos
        setTimeout(() => {
            divError.style.opacity = '0';
            setTimeout(() => divError.remove(), 300);
        }, 10000);
    }
}

/**
 * Maneja errores de forma centralizada
 */
function manejarError(error, contexto = '') {
    console.error(`Error en ${contexto}:`, error);
    
    let mensaje = 'Ha ocurrido un error. Por favor, intenta nuevamente.';
    let solucion = 'Si el problema persiste, contacta al soporte técnico.';
    
    if (error.message) {
        mensaje = error.message;
    }
    
    if (error.response && error.response.data && error.response.data.mensaje) {
        mensaje = error.response.data.mensaje;
    }
    
    mostrarErrorClaro('Error', mensaje, solucion);
}

// ============================================
// HEURÍSTICA 10: AYUDA Y DOCUMENTACIÓN
// ============================================

/**
 * Inicializa FAQ mejorado
 */
function inicializarFAQ() {
    document.querySelectorAll('.faq-question').forEach(pregunta => {
        pregunta.addEventListener('click', function() {
            const respuesta = this.nextElementSibling;
            const estaActiva = this.classList.contains('active');
            
            // Cerrar todas las demás
            document.querySelectorAll('.faq-question').forEach(preguntaItem => {
                if (preguntaItem !== this) {
                    preguntaItem.classList.remove('active');
                    preguntaItem.nextElementSibling.classList.remove('show');
                }
            });
            
            // Alternar estado actual
            if (estaActiva) {
                this.classList.remove('active');
                respuesta.classList.remove('show');
            } else {
                this.classList.add('active');
                respuesta.classList.add('show');
            }
        });
    });
}

/**
 * Crea botón de ayuda flotante
 */
function crearBotonAyuda() {
    const botonAyuda = document.createElement('button');
    botonAyuda.className = 'help-floating-btn';
    botonAyuda.innerHTML = '<i class="bi bi-question-circle-fill" style="font-size: 1.5rem;"></i>';
    botonAyuda.title = 'Ayuda';
    botonAyuda.setAttribute('aria-label', 'Abrir ayuda');
    
    botonAyuda.addEventListener('click', function() {
        // Abrir página de ayuda o modal
        window.location.href = '/preguntas_frecuentes';
    });
    
    document.body.appendChild(botonAyuda);
}

// ============================================
// INICIALIZACIÓN
// ============================================

/**
 * Inicializa todas las mejoras de usabilidad
 */
function inicializarHeuristicasUsabilidad() {
    // Heurística 1: Estado del sistema
    // Los indicadores de carga se muestran cuando sea necesario
    
    // Heurística 2: Correspondencia sistema-mundo real
    // Se aplica mediante CSS y estructura HTML
    
    // Heurística 3: Control y libertad
    // Las confirmaciones se usan cuando sea necesario
    
    // Heurística 4: Consistencia
    aplicarEstilosConsistentes();
    
    // Heurística 5: Prevención de errores
    // Se aplica en formularios específicos
    
    // Heurística 6: Reconocimiento
    inicializarTooltips();
    
    // Heurística 7: Flexibilidad
    inicializarAtajosComunes();
    
    // Heurística 8: Diseño minimalista
    ocultarElementosInnecesarios();
    
    // Heurística 9: Recuperación de errores
    // Se maneja mediante manejarError()
    
    // Heurística 10: Ayuda
    inicializarFAQ();
    crearBotonAyuda();
}

// Inicializar cuando el DOM esté listo
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', inicializarHeuristicasUsabilidad);
} else {
    inicializarHeuristicasUsabilidad();
}

// Exportar funciones para uso global
window.mostrarFeedback = mostrarFeedback;
window.mostrarIndicadorCarga = mostrarIndicadorCarga;
window.ocultarIndicadorCarga = ocultarIndicadorCarga;
window.confirmarAccion = confirmarAccion;
window.mostrarErrorClaro = mostrarErrorClaro;
window.manejarError = manejarError;
window.actualizarEstadoFormulario = actualizarEstadoFormulario;

