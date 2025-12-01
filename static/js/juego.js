const socket = io();
const id = window.idCuestionario || null;

let pollingInterval = null;

function actualizarListaParticipantes(participantes) {
    const container = document.getElementById('participantsContainer');
    const contador = document.getElementById('contadorParticipantes');
    
    if (!container || !contador) return;
    
    if (!Array.isArray(participantes)) {
        participantes = [];
    }
    
    contador.textContent = participantes.length;
    container.innerHTML = '';
    
    if (participantes.length === 0) {
        container.innerHTML = `
            <div class="text-muted py-4">
                <i class="bi bi-hourglass-split fs-3 d-block mb-2"></i>
                <span>Esperando participantes...</span>
            </div>
        `;
        return;
    }
    
    // Ordenar participantes por puntaje (mayor a menor)
    const participantesOrdenados = [...participantes].sort((a, b) => {
        const puntajeA = parseFloat(a.puntaje || 0);
        const puntajeB = parseFloat(b.puntaje || 0);
        return puntajeB - puntajeA;
    });
    
    participantesOrdenados.forEach((participante, index) => {
        const alias = participante.alias || participante.nombre || 'Sin nombre';
        const puntaje = parseFloat(participante.puntaje || 0).toFixed(2);
        const posicion = index + 1;
        
        const participantDiv = document.createElement('div');
        participantDiv.className = 'participant-item';
        participantDiv.style.animationDelay = `${index * 0.1}s`;
        
        // Agregar clase especial para el top 3
        if (posicion === 1) {
            participantDiv.classList.add('top-1');
        } else if (posicion === 2) {
            participantDiv.classList.add('top-2');
        } else if (posicion === 3) {
            participantDiv.classList.add('top-3');
        }
        
        participantDiv.innerHTML = `
            <div class="participant-name">
                <span class="participant-position">${posicion}°</span>
                <i class="bi bi-person-circle"></i>
                <span>${alias}</span>
            </div>
            <div class="participant-score">
                <i class="bi bi-star-fill"></i>
                <span>${puntaje}</span>
            </div>
        `;
        container.appendChild(participantDiv);
    });
}

socket.on('actualizar_participantes', (data) => {
    console.log('[DEBUG] Docente recibió actualizar_participantes:', data);
    let participantes = [];
    
    if (data && data.participantes) {
        participantes = data.participantes;
    } else if (data && Array.isArray(data)) {
        participantes = data;
    }
    
    console.log('[DEBUG] Participantes procesados:', participantes);
    console.log('[DEBUG] Total participantes:', participantes.length);
    if (participantes.length > 0) {
        console.log('[DEBUG] Primer participante:', participantes[0]);
    }
    
    actualizarListaParticipantes(participantes);
});

let startBtn;
let timerDisplay;
let minutesInput;
let secondsInput;
let interval;

let siguientePreguntaBtn;
let finalizarBtn;
let contadorPregunta;
let preguntaActual = null;
let totalPreguntas = 0;

let pregunta = null;
let tiempo = null;
let puntaje = null;

document.addEventListener('DOMContentLoaded', () => {
    if (!id) return;
    
    startBtn = document.getElementById('startBtn');
    timerDisplay = document.getElementById('timer');
    minutesInput = document.getElementById('minutes');
    secondsInput = document.getElementById('seconds');
    
    if (startBtn) {
        startBtn.addEventListener('click', () => {
            clearInterval(interval);
            let totalSeconds = parseInt(minutesInput.value || 0) * 60 + parseInt(secondsInput.value || 0);

            if (totalSeconds <= 0) {
                alert("Por favor selecciona un tiempo válido");
                return;
            }

            startBtn.disabled = true;
            startBtn.innerText = "Contando...";

            socket.emit('iniciar_juego', {'tiempo':totalSeconds});
        });
    }
    
    siguientePreguntaBtn = document.getElementById('siguientePreguntaBtn');
    finalizarBtn = document.getElementById('finalizarBtn');
    contadorPregunta = document.getElementById('contadorPregunta');
    
    if (siguientePreguntaBtn) {
        siguientePreguntaBtn.addEventListener('click', () => {
            siguientePreguntaBtn.disabled = true;
            siguientePreguntaBtn.textContent = 'Cargando...';
            socket.emit('siguiente_pregunta');
            
            setTimeout(() => {
                siguientePreguntaBtn.disabled = false;
            }, 1000);
        });
    }
    
    if (finalizarBtn) {
        finalizarBtn.addEventListener('click', async () => {
            const result = await Swal.fire({
                title: '¿Finalizar cuestionario?',
                html: '<p class="mb-3">¿Estás seguro de que deseas finalizar el cuestionario?</p><p class="text-muted small">Los participantes no podrán responder más preguntas.</p>',
                icon: 'warning',
                showCancelButton: true,
                confirmButtonText: '<i class="bi bi-check-circle me-2"></i>Aceptar',
                cancelButtonText: '<i class="bi bi-x-circle me-2"></i>Cancelar',
                confirmButtonColor: '#dc3545',
                cancelButtonColor: '#6c757d',
                reverseButtons: true,
                customClass: {
                    popup: 'swal2-popup-custom',
                    confirmButton: 'btn btn-danger',
                    cancelButton: 'btn btn-secondary'
                },
                buttonsStyling: false
            });
            
            if (result.isConfirmed) {
                finalizarBtn.disabled = true;
                finalizarBtn.innerHTML = '<i class="bi bi-hourglass-split me-2"></i>Finalizando...';
                socket.emit('finalizar_cuestionario');
            }
        });
    }
    
    socket.emit('unirme_sala', { sala: id });
    console.log('[DEBUG] Docente se unió a la sala:', id);
    
    setTimeout(() => {
        socket.emit('solicitar_participantes', { sala: id });
        console.log('[DEBUG] Solicitando participantes inicial');
    }, 300);
    
    setTimeout(() => {
        socket.emit('solicitar_participantes', { sala: id });
        console.log('[DEBUG] Solicitando participantes después de 1s');
    }, 1000);
    
    // Polling más frecuente para actualizaciones en tiempo real
    pollingInterval = setInterval(() => {
        if (socket.connected) {
            socket.emit('solicitar_participantes', { sala: id });
            console.log('[DEBUG] Polling: solicitando participantes');
        }
    }, 2000);  // Reducido a 2 segundos para actualizaciones más rápidas
});

socket.on('connect', () => {
    if (id) {
        setTimeout(() => {
            socket.emit('solicitar_participantes', { sala: id });
        }, 300);
    }
});

socket.on('disconnect', () => {
    if (pollingInterval) {
        clearInterval(pollingInterval);
    }
});

window.addEventListener('beforeunload', () => {
    if (pollingInterval) {
        clearInterval(pollingInterval);
    }
});

socket.on('actualizar_tiempoAD', (data) => {
    const tiempo = data.tiempo;
    if(tiempo <= 0){
        document.querySelector('.preguntas').classList.remove('d-none');
        document.querySelector('.tempo').classList.add('d-none');
    }
    document.getElementById('timer').textContent = tiempo;
});

socket.on('datos_cuestionario', (data) => {
    console.log('[DEBUG] Docente recibió datos_cuestionario:', data);
    preguntaActual = data;
    estadisticasMostradas = false; // Resetear cuando se muestra una nueva pregunta
    
    const preguntasCard = document.querySelector('.preguntas');
    if (preguntasCard) {
        preguntasCard.innerHTML = `
            <div class="icon-decoration top-left">💡</div>
            <div class="icon-decoration bottom-right">✨</div>
            <div class="question-badge">
                <i class="bi bi-question-circle-fill me-2"></i>Pregunta Activa
                <span id="contadorPregunta" class="badge bg-primary ms-2">${data.numero_pregunta || '?'}/${data.total_preguntas || '?'}</span>
            </div>
            <label for="" class="fw-semibold text-primary">
                <i class="bi bi-chat-quote-fill me-2"></i>Pregunta:
            </label>
            <h2 class="cuest fw-bold">${data.pregunta || ''}</h2>
            <div class="info-grid">
                <div class="info-item">
                    <label for="" class="fw-semibold text-primary">
                        <i class="bi bi-star-fill me-2"></i>Puntos
                    </label>
                    <p class="punt fw-semibold">${data.puntaje || 0}</p>
                </div>
                <div class="info-item">
                    <label for="" class="fw-semibold text-primary">
                        <i class="bi bi-clock-fill me-2"></i>Tiempo
                    </label>
                    <span class="temp fw-semibold">${data.tiempo_respuesta || 0}</span><span class="fw-semibold">s</span>
                </div>
            </div>
            
            <div class="control-buttons mt-4 d-flex gap-2 justify-content-center flex-wrap">
                <button id="siguientePreguntaBtn" class="btn btn-success btn-lg ${(data.numero_pregunta && data.total_preguntas && data.numero_pregunta < data.total_preguntas) ? '' : 'd-none'}" disabled style="opacity: 0.5;">
                    <i class="bi bi-arrow-right-circle-fill me-2"></i>Siguiente Pregunta
                </button>
                <button id="finalizarBtn" class="btn btn-danger btn-lg">
                    <i class="bi bi-stop-circle-fill me-2"></i>Finalizar Cuestionario
                </button>
            </div>
        `;
        
        pregunta = document.querySelector('.cuest');
        tiempo = document.querySelector('.temp');
        puntaje = document.querySelector('.punt');
        contadorPregunta = document.getElementById('contadorPregunta');
        siguientePreguntaBtn = document.getElementById('siguientePreguntaBtn');
        finalizarBtn = document.getElementById('finalizarBtn');
        
        if (siguientePreguntaBtn) {
            siguientePreguntaBtn.addEventListener('click', () => {
                console.log('[DEBUG] Click en siguiente pregunta, estadisticasMostradas:', estadisticasMostradas);
                if (!estadisticasMostradas) {
                    alert('Por favor, espera a que termine el tiempo y revisa las estadísticas antes de continuar.');
                    return;
                }
                siguientePreguntaBtn.disabled = true;
                siguientePreguntaBtn.textContent = 'Cargando...';
                console.log('[DEBUG] Emitiendo siguiente_pregunta');
                socket.emit('siguiente_pregunta');
                
                setTimeout(() => {
                    siguientePreguntaBtn.disabled = false;
                }, 1000);
            });
        }
        
        if (finalizarBtn) {
            finalizarBtn.addEventListener('click', async () => {
                const result = await Swal.fire({
                    title: '¿Finalizar cuestionario?',
                    html: '<p class="mb-3">¿Estás seguro de que deseas finalizar el cuestionario?</p><p class="text-muted small">Los participantes no podrán responder más preguntas.</p>',
                    icon: 'warning',
                    showCancelButton: true,
                    confirmButtonText: '<i class="bi bi-check-circle me-2"></i>Aceptar',
                    cancelButtonText: '<i class="bi bi-x-circle me-2"></i>Cancelar',
                    confirmButtonColor: '#dc3545',
                    cancelButtonColor: '#6c757d',
                    reverseButtons: true,
                    customClass: {
                        popup: 'swal2-popup-custom',
                        confirmButton: 'btn btn-danger',
                        cancelButton: 'btn btn-secondary'
                    },
                    buttonsStyling: false
                });
                
                if (result.isConfirmed) {
                    finalizarBtn.disabled = true;
                    finalizarBtn.innerHTML = '<i class="bi bi-hourglass-split me-2"></i>Finalizando...';
                    socket.emit('finalizar_cuestionario');
                }
            });
        }
    }
    
    document.querySelector('.preguntas').classList.remove('d-none');
    document.querySelector('.tempo').classList.add('d-none');
});

socket.on('juego_iniciado', (data) => {
    totalPreguntas = data.total_preguntas || 0;
    
    document.querySelector('.tempo').classList.add('d-none');
    
    const preguntasCard = document.querySelector('.preguntas');
    if (preguntasCard) {
        preguntasCard.classList.remove('d-none');
        preguntasCard.innerHTML = `
            <div class="text-center p-4">
                <h4 class="mb-3">✅ Juego Iniciado</h4>
                <p class="text-muted mb-4">${data.mensaje || 'Iniciando primera pregunta automáticamente...'}</p>
                <div class="spinner-border text-primary mb-3" role="status">
                    <span class="visually-hidden">Cargando...</span>
                </div>
                <div class="control-buttons mt-4 d-flex gap-2 justify-content-center">
                    <button id="finalizarBtn" class="btn btn-danger btn-lg">
                        <i class="bi bi-stop-circle-fill me-2"></i>Finalizar Cuestionario
                    </button>
                </div>
            </div>
        `;
        
        finalizarBtn = document.getElementById('finalizarBtn');
        
                if (finalizarBtn) {
                    finalizarBtn.addEventListener('click', async () => {
                        const result = await Swal.fire({
                            title: '¿Finalizar cuestionario?',
                            html: '<p class="mb-3">¿Estás seguro de que deseas finalizar el cuestionario?</p><p class="text-muted small">Los participantes no podrán responder más preguntas.</p>',
                            icon: 'warning',
                            showCancelButton: true,
                            confirmButtonText: '<i class="bi bi-check-circle me-2"></i>Aceptar',
                            cancelButtonText: '<i class="bi bi-x-circle me-2"></i>Cancelar',
                            confirmButtonColor: '#dc3545',
                            cancelButtonColor: '#6c757d',
                            reverseButtons: true,
                            customClass: {
                                popup: 'swal2-popup-custom',
                                confirmButton: 'btn btn-danger',
                                cancelButton: 'btn btn-secondary'
                            },
                            buttonsStyling: false
                        });
                        
                        if (result.isConfirmed) {
                            finalizarBtn.disabled = true;
                            finalizarBtn.innerHTML = '<i class="bi bi-hourglass-split me-2"></i>Finalizando...';
                            socket.emit('finalizar_cuestionario');
                        }
                    });
                }
            }
        });

socket.on('pregunta_mostrada', (data) => {
    if (siguientePreguntaBtn) {
        if (data.numero_pregunta < data.total_preguntas) {
            siguientePreguntaBtn.textContent = `▶️ Siguiente Pregunta (${data.numero_pregunta + 1}/${data.total_preguntas})`;
            siguientePreguntaBtn.classList.remove('d-none');
            // Mantener deshabilitado hasta que se muestren las estadísticas
            siguientePreguntaBtn.disabled = true;
            siguientePreguntaBtn.style.opacity = '0.5';
        } else {
            siguientePreguntaBtn.textContent = 'No hay más preguntas';
            siguientePreguntaBtn.classList.add('d-none');
        }
    }
    
    if (contadorPregunta) {
        contadorPregunta.textContent = `${data.numero_pregunta}/${data.total_preguntas}`;
    }
});

socket.on('sin_mas_preguntas', (data) => {
    // Mostrar mensaje informativo con SweetAlert2
    Swal.fire({
        title: '¡Última pregunta completada!',
        html: '<p class="mb-3">No hay más preguntas disponibles.</p><p class="text-muted small">El cuestionario se finalizará automáticamente y serás redirigido a los resultados.</p>',
        icon: 'info',
        confirmButtonText: '<i class="bi bi-check-circle me-2"></i>Entendido',
        confirmButtonColor: '#007bff',
        customClass: {
            popup: 'swal2-popup-custom',
            confirmButton: 'btn btn-primary'
        },
        buttonsStyling: false,
        allowOutsideClick: false,
        allowEscapeKey: false
    });
    
    if (siguientePreguntaBtn) {
        siguientePreguntaBtn.classList.add('d-none');
    }
    
    // Ocultar también el botón de finalizar ya que se finalizará automáticamente
    if (finalizarBtn) {
        finalizarBtn.disabled = true;
        finalizarBtn.innerHTML = '<i class="bi bi-hourglass-split me-2"></i>Finalizando automáticamente...';
    }
});

socket.on('actualiza_tiempocuestionario', (data) => {
    if (tiempo) {
        tiempo.textContent = data.tiempo;
    }
});

let estadisticasMostradas = false;

socket.on('tiempo_agotado', (data) => {
    estadisticasMostradas = false;
    
    // Deshabilitar el botón de siguiente pregunta hasta que se vean las estadísticas
    if (siguientePreguntaBtn) {
        siguientePreguntaBtn.disabled = true;
        siguientePreguntaBtn.style.opacity = '0.5';
    }
    
    const preguntasCard = document.querySelector('.preguntas');
    if (!preguntasCard) return;
    
    const estadisticas = data.estadisticas;
    if (!estadisticas || !estadisticas.estado) {
        // Si no hay estadísticas, mostrar mensaje simple
        const contenidoAnterior = preguntasCard.innerHTML;
        preguntasCard.innerHTML = `
            <div class="text-center p-4">
                <h4 class="text-danger mb-3">⏱️ Tiempo Agotado</h4>
                <p class="text-muted mb-4">El tiempo para esta pregunta ha finalizado.</p>
                <button id="continuarBtn" class="btn btn-success btn-lg">
                    <i class="bi bi-arrow-right-circle-fill me-2"></i>Continuar
                </button>
            </div>
        `;
        
        const continuarBtn = document.getElementById('continuarBtn');
        if (continuarBtn) {
            continuarBtn.addEventListener('click', () => {
                estadisticasMostradas = true;
                preguntasCard.innerHTML = contenidoAnterior;
                // Re-bindear los event listeners
                siguientePreguntaBtn = document.getElementById('siguientePreguntaBtn');
                finalizarBtn = document.getElementById('finalizarBtn');
                
                // Asegurar que el botón siguiente pregunta esté visible y habilitado
                if (siguientePreguntaBtn) {
                    siguientePreguntaBtn.disabled = false;
                    siguientePreguntaBtn.style.opacity = '1';
                    siguientePreguntaBtn.classList.remove('d-none');
                    siguientePreguntaBtn.addEventListener('click', () => {
                        if (!estadisticasMostradas) {
                            alert('Por favor, espera a que termine el tiempo y revisa las estadísticas antes de continuar.');
                            return;
                        }
                        siguientePreguntaBtn.disabled = true;
                        siguientePreguntaBtn.textContent = 'Cargando...';
                        console.log('[DEBUG] Emitiendo siguiente_pregunta');
                        socket.emit('siguiente_pregunta');
                        setTimeout(() => {
                            siguientePreguntaBtn.disabled = false;
                        }, 1000);
                    });
                }
                if (finalizarBtn) {
                    finalizarBtn.addEventListener('click', async () => {
                        const result = await Swal.fire({
                            title: '¿Finalizar cuestionario?',
                            html: '<p class="mb-3">¿Estás seguro de que deseas finalizar el cuestionario?</p><p class="text-muted small">Los participantes no podrán responder más preguntas.</p>',
                            icon: 'warning',
                            showCancelButton: true,
                            confirmButtonText: '<i class="bi bi-check-circle me-2"></i>Aceptar',
                            cancelButtonText: '<i class="bi bi-x-circle me-2"></i>Cancelar',
                            confirmButtonColor: '#dc3545',
                            cancelButtonColor: '#6c757d',
                            reverseButtons: true,
                            customClass: {
                                popup: 'swal2-popup-custom',
                                confirmButton: 'btn btn-danger',
                                cancelButton: 'btn btn-secondary'
                            },
                            buttonsStyling: false
                        });
                        
                        if (result.isConfirmed) {
                            finalizarBtn.disabled = true;
                            finalizarBtn.innerHTML = '<i class="bi bi-hourglass-split me-2"></i>Finalizando...';
                            socket.emit('finalizar_cuestionario');
                        }
                    });
                }
            });
        }
        return;
    }
    
    // Construir HTML de estadísticas tipo Kahoot
    let htmlEstadisticas = `
        <div class="estadisticas-container">
            <div class="text-center mb-4">
                <h3 class="text-danger mb-2">⏱️ Tiempo Agotado</h3>
                <p class="text-muted">Estadísticas de respuestas</p>
            </div>
            
            <div class="mb-3">
                <div class="d-flex justify-content-between align-items-center mb-2">
                    <span class="fw-semibold">Total de participantes:</span>
                    <span class="badge bg-primary">${estadisticas.total_participantes}</span>
                </div>
                <div class="d-flex justify-content-between align-items-center mb-2">
                    <span class="fw-semibold">Respondieron:</span>
                    <span class="badge bg-success">${estadisticas.total_respuestas}</span>
                </div>
                ${estadisticas.sin_respuesta > 0 ? `
                <div class="d-flex justify-content-between align-items-center mb-3">
                    <span class="fw-semibold">Sin respuesta:</span>
                    <span class="badge bg-secondary">${estadisticas.sin_respuesta} (${estadisticas.porcentaje_sin_respuesta}%)</span>
                </div>
                ` : ''}
            </div>
            
            <div class="estadisticas-alternativas">
    `;
    
    estadisticas.alternativas.forEach((alt, index) => {
        const colorClass = alt.es_correcta ? 'success' : 'secondary';
        const icono = alt.es_correcta ? '✓' : '';
        const barraWidth = Math.max(alt.porcentaje, 5); // Mínimo 5% para visibilidad
        
        htmlEstadisticas += `
            <div class="alternativa-estadistica mb-3 ${alt.es_correcta ? 'correcta' : ''}">
                <div class="d-flex justify-content-between align-items-center mb-2">
                    <span class="fw-semibold">
                        ${icono} ${alt.respuesta}
                    </span>
                    <span class="badge bg-${colorClass}">
                        ${alt.cantidad} (${alt.porcentaje}%)
                    </span>
                </div>
                <div class="progress" style="height: 30px;">
                    <div class="progress-bar bg-${colorClass}" 
                         role="progressbar" 
                         style="width: ${barraWidth}%" 
                         aria-valuenow="${alt.porcentaje}" 
                         aria-valuemin="0" 
                         aria-valuemax="100">
                        ${alt.porcentaje > 5 ? `${alt.porcentaje}%` : ''}
                    </div>
                </div>
            </div>
        `;
    });
    
    htmlEstadisticas += `
            </div>
            
            <div class="text-center mt-4">
                <button id="continuarBtn" class="btn btn-success btn-lg">
                    <i class="bi bi-arrow-right-circle-fill me-2"></i>Continuar a Siguiente Pregunta
                </button>
            </div>
        </div>
    `;
    
    // Guardar contenido anterior
    const contenidoAnterior = preguntasCard.innerHTML;
    
    // Mostrar estadísticas
    preguntasCard.innerHTML = htmlEstadisticas;
    
    // Agregar estilos para las estadísticas
    if (!document.getElementById('estadisticas-styles')) {
        const style = document.createElement('style');
        style.id = 'estadisticas-styles';
        style.textContent = `
            .estadisticas-container {
                padding: 20px;
            }
            .alternativa-estadistica {
                padding: 10px;
                border-radius: 8px;
                background-color: #f8f9fa;
            }
            .alternativa-estadistica.correcta {
                background-color: #d4edda;
                border: 2px solid #28a745;
            }
            .progress {
                border-radius: 15px;
                overflow: hidden;
            }
            .progress-bar {
                display: flex;
                align-items: center;
                justify-content: center;
                font-weight: bold;
                color: white;
                text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
            }
        `;
        document.head.appendChild(style);
    }
    
    // Verificar si es la última pregunta y finalizar automáticamente
    const esUltimaPregunta = preguntaActual && 
                             preguntaActual.numero_pregunta && 
                             preguntaActual.total_preguntas && 
                             preguntaActual.numero_pregunta >= preguntaActual.total_preguntas;
    
    if (esUltimaPregunta) {
        // Es la última pregunta, finalizar automáticamente después de 5 segundos
        setTimeout(() => {
            Swal.fire({
                title: '¡Última pregunta completada!',
                html: '<p class="mb-3">Has completado todas las preguntas del cuestionario.</p><p class="text-muted small">Finalizando y redirigiendo a resultados...</p>',
                icon: 'success',
                confirmButtonText: '<i class="bi bi-check-circle me-2"></i>Entendido',
                confirmButtonColor: '#28a745',
                customClass: {
                    popup: 'swal2-popup-custom',
                    confirmButton: 'btn btn-success'
                },
                buttonsStyling: false,
                allowOutsideClick: false,
                allowEscapeKey: false,
                timer: 2000,
                timerProgressBar: true
            }).then(() => {
                // Finalizar el cuestionario automáticamente
                socket.emit('finalizar_cuestionario');
            });
        }, 5000); // Esperar 5 segundos para que el docente vea las estadísticas
    }
    
    // Event listener para el botón continuar
    const continuarBtn = document.getElementById('continuarBtn');
    if (continuarBtn) {
        // Si es la última pregunta, cambiar el texto del botón
        if (esUltimaPregunta) {
            continuarBtn.textContent = 'Finalizando cuestionario...';
            continuarBtn.disabled = true;
            continuarBtn.classList.remove('btn-success');
            continuarBtn.classList.add('btn-secondary');
        }
        
        continuarBtn.addEventListener('click', () => {
            // Si es la última pregunta, no hacer nada (ya se finalizará automáticamente)
            if (esUltimaPregunta) {
                return;
            }
            
            estadisticasMostradas = true;
            preguntasCard.innerHTML = contenidoAnterior;
            // Re-bindear los event listeners
            siguientePreguntaBtn = document.getElementById('siguientePreguntaBtn');
            finalizarBtn = document.getElementById('finalizarBtn');
            
            // Asegurar que el botón siguiente pregunta esté visible y habilitado
            if (siguientePreguntaBtn) {
                siguientePreguntaBtn.disabled = false;
                siguientePreguntaBtn.style.opacity = '1';
                siguientePreguntaBtn.classList.remove('d-none');
                siguientePreguntaBtn.addEventListener('click', () => {
                    if (!estadisticasMostradas) {
                        alert('Por favor, espera a que termine el tiempo y revisa las estadísticas antes de continuar.');
                        return;
                    }
                    siguientePreguntaBtn.disabled = true;
                    siguientePreguntaBtn.textContent = 'Cargando...';
                    console.log('[DEBUG] Emitiendo siguiente_pregunta');
                    socket.emit('siguiente_pregunta');
                    setTimeout(() => {
                        siguientePreguntaBtn.disabled = false;
                    }, 1000);
                });
            }
            if (finalizarBtn) {
                finalizarBtn.addEventListener('click', async () => {
                    const result = await Swal.fire({
                        title: '¿Finalizar cuestionario?',
                        html: '<p class="mb-3">¿Estás seguro de que deseas finalizar el cuestionario?</p><p class="text-muted small">Los participantes no podrán responder más preguntas.</p>',
                        icon: 'warning',
                        showCancelButton: true,
                        confirmButtonText: '<i class="bi bi-check-circle me-2"></i>Aceptar',
                        cancelButtonText: '<i class="bi bi-x-circle me-2"></i>Cancelar',
                        confirmButtonColor: '#dc3545',
                        cancelButtonColor: '#6c757d',
                        reverseButtons: true,
                        customClass: {
                            popup: 'swal2-popup-custom',
                            confirmButton: 'btn btn-danger',
                            cancelButton: 'btn btn-secondary'
                        },
                        buttonsStyling: false
                    });
                    
                    if (result.isConfirmed) {
                        finalizarBtn.disabled = true;
                        finalizarBtn.innerHTML = '<i class="bi bi-hourglass-split me-2"></i>Finalizando...';
                        socket.emit('finalizar_cuestionario');
                    }
                });
            }
        });
    }
});

socket.on('pantalla_finalizada', (data) => {
    const preguntasDiv = document.querySelector('.preguntas');
    if (preguntasDiv) {
        preguntasDiv.textContent = `✅ Cuestionario finalizado. Redirigiendo a resultados...`;
    }
    
    setTimeout(() => {
        window.location.href = `/resultados_inter/${id}`;
    }, 1500);
});
