// Inicializar contenido cuando el DOM esté listo
let contenido = null;

// Función para obtener o inicializar contenido
const getContenido = () => {
    if (!contenido) {
        contenido = document.querySelector(".cont_formulario");
    }
    return contenido;
};

const cuerpo_json = {
    detalle: {
        nombre_formulario: "",
        tipo_formulario: "",
        descripcion_formulario: "",
        estado: "",
    },
    preguntas: [],
};

// Heurística 5: Prevención de errores - Validación en tiempo real
const validarCampo = (campo, valor, tipo = 'texto') => {
    const divError = document.getElementById(`${campo}_error`);
    
    // Limpiar error previo
    if (divError) divError.remove();
    
    // Validaciones según tipo
    let esValido = true;
    let mensaje = '';
    
    if (tipo === 'texto') {
        if (!valor || valor.trim().length === 0) {
            esValido = false;
            mensaje = 'Este campo es obligatorio';
        } else if (valor.trim().length < 3) {
            esValido = false;
            mensaje = 'Debe tener al menos 3 caracteres';
        } else if (valor.length > 200) {
            esValido = false;
            mensaje = 'Máximo 200 caracteres permitidos';
        }
    } else if (tipo === 'textarea') {
        if (valor && valor.length > 1000) {
            esValido = false;
            mensaje = 'Máximo 1000 caracteres permitidos';
        }
    }
    
    // Mostrar error si es necesario
    if (!esValido && mensaje) {
        const entrada = document.getElementById(campo);
        if (entrada) {
            entrada.classList.add('is-invalid');
            const elementoError = document.createElement('div');
            elementoError.id = `${campo}_error`;
            elementoError.className = 'invalid-feedback';
            elementoError.textContent = mensaje;
            entrada.parentElement.appendChild(elementoError);
        }
    } else if (esValido) {
        const entrada = document.getElementById(campo);
        if (entrada) {
            entrada.classList.remove('is-invalid');
            entrada.classList.add('is-valid');
        }
    }
    
    return esValido;
};

// Actualizar estado del formulario cuando se guarda (Heurística 1)
const actualizarEstadoFormularioGuardado = () => {
    if (typeof window.actualizarEstadoFormulario === 'function') {
        window.actualizarEstadoFormulario(true);
        const textoEstado = document.getElementById('form-status-text');
        if (textoEstado) textoEstado.textContent = 'Guardado';
    }
};

const guardar_detalle = async (ss) => {
    const nombre_cuestionario = document.getElementById("nombre_cuestionario");
    const tipo_formulario = document.getElementById("tipo_cuestionario");
    const descripcion_formulario = document.getElementById("descripcion");
    const estado = document.getElementById("estado");

    // Validar que los elementos existan
    if (!nombre_cuestionario || !tipo_formulario || !estado) {
        Swal.fire({
            icon: 'error',
            title: 'Error',
            text: 'No se pudieron encontrar los campos del formulario. Por favor, recarga la página.',
            confirmButtonText: 'Entendido'
        });
        return;
    }

    // Heurística 9: Recuperación de errores - Validación completa antes de guardar
    const nombreValido = validarCampo("nombre_cuestionario", nombre_cuestionario?.value || '', 'texto');
    const descripcionValida = validarCampo("descripcion", descripcion_formulario?.value || '', 'textarea');
    
    if (!nombreValido) {
        Swal.fire({
            icon: 'error',
            title: 'Campo incompleto',
            text: 'Por favor, completa correctamente el nombre del cuestionario (mínimo 3 caracteres)',
            confirmButtonText: 'Entendido'
        });
        return;
    }
    
    if (!tipo_formulario?.value) {
        Swal.fire({
            icon: 'error',
            title: 'Campo incompleto',
            text: 'Por favor, selecciona el tipo de cuestionario',
            confirmButtonText: 'Entendido'
        });
        return;
    }

    // Determinar si es modificación o guardado nuevo
    const esModificacion = ss === true || ss === 'si' || ss === 'modificar' || cuerpo_json.detalle.nombre_formulario !== '';
    const textoAccion = esModificacion ? 'modificar' : 'guardar';
    
    const resultado = await Swal.fire({
        title: `¿Estás seguro de ${textoAccion} este detalle?`,
        text: `El cuestionario "${nombre_cuestionario.value.trim()}" será ${esModificacion ? 'modificado' : 'guardado'}.`,
        icon: 'question',
        showCancelButton: true,
        confirmButtonText: `Sí, ${textoAccion}`,
        cancelButtonText: 'Cancelar',
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33'
    });
    
    if (resultado.isConfirmed) {
        // Subir imagen si existe
        const imagenInput = document.getElementById('imagen_cuestionario');
        let imagenUrl = null;
        
        if (imagenInput && imagenInput.files && imagenInput.files[0]) {
            try {
                Swal.fire({
                    title: 'Subiendo imagen...',
                    text: 'Por favor espera',
                    allowOutsideClick: false,
                    didOpen: () => {
                        Swal.showLoading();
                    }
                });
                
                const formData = new FormData();
                formData.append('imagen', imagenInput.files[0]);
                
                const imagenResponse = await fetch('/subir_imagen_cuestionario', {
                    method: 'POST',
                    body: formData
                });
                
                const imagenData = await imagenResponse.json();
                
                if (imagenData.estado) {
                    imagenUrl = imagenData.ruta;
                    Swal.close();
                } else {
                    await Swal.fire({
                        icon: 'warning',
                        title: 'Advertencia',
                        text: imagenData.mensaje || 'No se pudo subir la imagen, pero puedes continuar sin ella.',
                        confirmButtonText: 'Continuar'
                    });
                }
            } catch (error) {
                console.error('Error al subir imagen:', error);
                await Swal.fire({
                    icon: 'warning',
                    title: 'Advertencia',
                    text: 'No se pudo subir la imagen, pero puedes continuar sin ella.',
                    confirmButtonText: 'Continuar'
                });
            }
        }
        
        // Proceder con el guardado
        cuerpo_json.detalle.nombre_formulario = nombre_cuestionario.value.trim();
        cuerpo_json.detalle.tipo_formulario = tipo_formulario.value;
        cuerpo_json.detalle.descripcion_formulario = descripcion_formulario?.value?.trim() || '';
        cuerpo_json.detalle.estado = estado.value === 'P' ? 'Público' : 'Privado';
        cuerpo_json.detalle.imagen_url = imagenUrl;
        
        const cont = getContenido();
        if (!cont) {
            console.error("No se encontró el elemento .cont_formulario");
            Swal.fire({
                icon: 'error',
                title: 'Error',
                text: 'No se pudo encontrar el formulario. Por favor, recarga la página.',
                confirmButtonText: 'Entendido'
            });
            return;
        }
        cont.innerHTML = '';
        if (!esModificacion) {
        cont.innerHTML = `
            <div class="d-flex align-items-center mb-3">
                <i class="bi bi-question-circle-fill fs-2 text-primary me-2"></i>
                <h3 class="fw-bold mb-0">Paso 2: Agregar preguntas</h3>
            </div>
            <p class="text-secondary separador mb-4"><i class="bi bi-info-circle me-1"></i>Añade las preguntas que conformarán tu formulario</p>
            <div class="mb-3">
                        <label for="nombre_pregunta" class="fw-bold">
                            <i class="bi bi-pencil-square me-1"></i>Pregunta:
                            <span class="text-danger">*</span>
                            <i class="bi bi-info-circle text-primary ms-1" data-bs-toggle="tooltip" data-bs-placement="top" title="Mínimo 5 caracteres, máximo 500"></i>
                        </label>
                        <input type="text" class="form-control mt-2" id="nombre_pregunta" placeholder="¿Cuál es tu pregunta?" 
                               maxlength="500" required onblur="if(window.validarCampo) validarCampo('nombre_pregunta', this.value, 'texto')" 
                               oninput="const contador = document.getElementById('contador_pregunta'); if(contador) contador.textContent = this.value.length">
                        <small class="text-muted">Caracteres: <span id="contador_pregunta">0</span>/500</small>
            </div>
            <div class="row mb-3">
                <div class="col-md-3">
                    <div class="mt-2" role="radiogroup" aria-labelledby="tipo_pregunta_label">
                        <span id="tipo_pregunta_label" class="fw-bold"><i class="bi bi-list-check me-1"></i>Tipo pregunta:</span>
                        <div class="form-check mt-2">
                            <input class="form-check-input" type="radio" name="tipo_pregunta" id="verdadero_falso" value="VF" onclick="if(window.VF) VF()">
                        <label class="form-check-label" for="verdadero_falso">
                            <i class="bi bi-check2-square me-1"></i>(Verdadero / Falso)
                        </label>
                    </div>
                    <div class="form-check mt-1">
                        <input class="form-check-input" type="radio" name="tipo_pregunta" id="alternativas" value="ALT" onclick="if(window.ALT) ALT()">
                            <label class="form-check-label" for="alternativas">
                                <i class="bi bi-ui-checks-grid me-1"></i>(Alternativas)
                            </label>
                        </div>
                    </div>
                </div>
                <div class="col-md-4">
                <label for="puntos" class="fw-bold mt-2">
                    <i class="bi bi-star-fill text-warning me-1"></i>Puntos:
                    <span class="text-danger">*</span>
                    <i class="bi bi-info-circle text-primary ms-1" data-bs-toggle="tooltip" title="Valor entre 1 y 1000"></i>
                </label>
                <input type="number" class="form-control mt-2" name="puntos" id="puntos" placeholder="Valor de la pregunta" min="1" max="1000" required>
                </div>
                <div class="col-md-4">
                <label for="tiempo" class="fw-bold mt-2">
                    <i class="bi bi-clock-fill text-primary me-1"></i>Tiempo (segundos):
                    <span class="text-danger">*</span>
                    <i class="bi bi-info-circle text-primary ms-1" data-bs-toggle="tooltip" title="Mínimo 2 segundos, máximo 300"></i>
                </label>
                <input type="number" class="form-control mt-2" name="tiempo" id="tiempo" placeholder="Tiempo (segundos)" min="2" max="300" required>
                </div>
            </div>
            <div class="mb-3">
                <label class="form-check-label fw-bold" for="alternativas"><i class="bi bi-list-ol me-1"></i>Alternativas: <button type="button" onclick="if(window.agregar_alternativas) agregar_alternativas()" class="btn btn-outline-success btn-sm d-none" id="btn_add"><i class="bi bi-plus-circle"></i></button></label>
                <div class="alterantivas_form mt-2 ">
        
                </div>
            </div>
            <div >
                <button type="button" class="btn btn-primary w-100" onclick="if(window.guardar_pregunta) guardar_pregunta()"> Guardar pregunta</button>
            </div>
        `;
            // Reinicializar tooltips después de agregar contenido dinámico
            setTimeout(() => {
                const listaTooltips = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
                listaTooltips.map(function (elementoTooltip) {
                    return new bootstrap.Tooltip(elementoTooltip);
                });
            }, 100);
            } else {
                // Si es modificación, mostrar mensaje de éxito y recargar detalle
                Swal.fire({
                    icon: 'success',
                    title: 'Detalle Modificado',
                    text: 'El detalle del formulario ha sido modificado correctamente.',
                    timer: 2000,
                    showConfirmButton: false
                }).then(() => {
                    detalle();
                });
            }
            
            // Actualizar el estado visual del detalle guardado
            const detalleCard = document.getElementById('detalle_card');
            if (detalleCard) {
                detalleCard.classList.add('border-success');
                detalleCard.querySelector('p.fw-bold').innerHTML = `
                    <i class="bi bi-check-circle-fill text-success me-2"></i>Detalle de formulario
                `;
            }
            
            console.log("Detalle JSON:", cuerpo_json);
        } else {
            // Usuario canceló la acción
            console.log('El usuario canceló la acción de guardar/modificar el detalle.');
        }
};

const detalle = () => {
    const cont = getContenido();
    if (!cont) {
        console.error("No se encontró el elemento .cont_formulario");
        return;
    }
    // Generar HTML para la imagen si existe
    const imagenHtml = cuerpo_json.detalle.imagen_url ? `
        <div class="mb-4">
            <label class="fw-bold mb-2">
                <i class="bi bi-image"></i>
                Imagen del cuestionario
            </label>
            <div class="text-center">
                <img src="/${cuerpo_json.detalle.imagen_url}" alt="Imagen del cuestionario" 
                     class="img-thumbnail" 
                     style="max-width: 100%; max-height: 300px; object-fit: contain; border-radius: 8px;">
            </div>
        </div>
    ` : '';
    
    cont.innerHTML = `
            <h3 class="fw-bold mb-3">Paso 1: Detalle del formulario</h3>
            <p class="text-secondary separador mb-4">Define la información básica de tu nuevo formulario</p>
            ${imagenHtml}
            <div class="d-flex flex-wrap align-items-start gap-4">
                <div class="d-flex flex-column me-4" style="min-width: 300px;">
                    <label for="nombre_cuestionario" class="fw-bold mb-2">
                        <i class="bi bi-pencil-square"></i>
                        Nombre del formulario
                    </label>
                    <input value ="${cuerpo_json.detalle.nombre_formulario}" id="nombre_cuestionario" class="form-control mb-3" name="nombre_cuestionario" type="text" placeholder="Ingrese el nombre del cuestionario" >
                
                    <label for="tipo_cuestionario" class="fw-bold mb-2">
                        <i class="bi bi-info-circle"></i>
                        Tipo de formulario
                    </label>
                    <select class="form-select mb-3" name="tipo_cuestionario" id="tipo_cuestionario">
                        <option value="" disabled ${cuerpo_json.detalle.tipo_formulario === "" ? "selected" : ""}>Seleccione una opción</option>
                        <option value="I" ${cuerpo_json.detalle.tipo_formulario === "I" ? "selected" : ""}>Individual</option>
                        <option value="G" ${cuerpo_json.detalle.tipo_formulario === "G" ? "selected" : ""}>Grupal</option>
                    </select>
                                    
                </div>

                <div class="d-flex flex-column flex-grow-1">
                    <label for="descripcion" class="fw-bold mb-2">
                        <i class="bi bi-card-text"></i>
                        Descripción del formulario
                    </label>
                    <textarea  id="descripcion" class="form-control" name="descripcion" rows="7" placeholder="Ingrese la descripción del cuestionario" >${cuerpo_json.detalle.descripcion_formulario}</textarea>

                    <label for="estado" class="fw-bold mb-2">
                        <i class="bi bi-check-circle"></i> Estado
                    </label>
                    <select id="estado" class="form-select mb-3" name="estado">
                        <option value="P" ${cuerpo_json.detalle.estado === "P" ? "selected" : ""}>Público</option>
                        <option value="R" ${cuerpo_json.detalle.estado === "R" ? "selected" : ""}>Privado</option>
                    </select>   
                </div>

                
            </div>
            <div class="mb-1 mt-4">
                ${cuerpo_json.detalle.nombre_formulario ? `
                        <button type="button" class="btn btn-warning w-100" onclick="guardar_detalle()">
                            <i class="bi bi-save"></i> Modificar detalle
                        </button>
                    `
            : ` <button type="button" class="btn btn-primary w-100" onclick="guardar_detalle('si')">
                            <i class="bi bi-save"></i> Guardar detalle
                        </button>`
        }
            </div>
    `;
};

const pregunta = (indice) => {
    const pr = cuerpo_json.preguntas[indice];
    var alt = '';
    if (pr.tipo_pregunta == "VF") {
        alt = `
            <button type="button" class="btn ${pr.respuesta == 'Verdadero' ? 'btn-success' : 'btn-outline-success'} btn-sm w-50 " onclick="select(this)"> Verdadero </button>
            <button type="button" class="btn ${pr.respuesta == 'Falso' ? 'btn-success' : 'btn-outline-success'} btn-sm w-50 " onclick="select(this)"> Falso </button>
        `;
    } else {
        const alternativas = pr.alternativas;
        alternativas.forEach(a => {
            alt += `
                <div class="w-50 d-flex alter ">
                    <input type="text" class="form-control me-2 ${a == pr.respuesta ? 'border-success' : ''}" value="${a}">
                    <button type="button" class="btn btn-sm  ${a == pr.respuesta ? 'btn-success' : 'btn-primary'} me-1 cl" onclick ="sl(this)"><i class="bi bi-check2"></i></button>
                    <button type="button" class="btn btn-sm btn-danger" onclick= "eliminar_alternativa(this)"><i class="bi bi-trash3-fill"></i></button>
                </div>   
            `;
        });
    }
    const cont = getContenido();
    if (!cont) {
        console.error("No se encontró el elemento .cont_formulario");
        return;
    }
    cont.innerHTML = `
         <div class="d-flex align-items-center mb-3">
            <i class="bi bi-question-circle-fill fs-2 text-primary me-2"></i>
            <h3 class="fw-bold mb-0">Paso 2: Agregar preguntas</h3>
        </div>
        <p class="text-secondary separador mb-4"><i class="bi bi-info-circle me-1"></i>Añade las preguntas que conformarán tu formulario</p>
        <div class="mb-3">
            <label for="nombre_pregunta" class="fw-bold"><i class="bi bi-pencil-square me-1"></i>Pregunta:</label>
            <input type="text"  value="${pr.nombre_pregunta}" class="form-control mt-2" id="nombre_pregunta" placeholder="¿Cuál es tu pregunta?">
        </div>
        <div class="row mb-3">
            <div class="col-md-3">
                <div class="mt-2" role="radiogroup" aria-labelledby="tipo_pregunta_label">
                    <span id="tipo_pregunta_label" class="fw-bold"><i class="bi bi-list-check me-1"></i>Tipo pregunta:</span>
                    <div class="form-check mt-2">
                        <input class="form-check-input" type="radio" name="tipo_pregunta" id="verdadero_falso" value="VF" onclick="VF()" ${pr.tipo_pregunta == 'VF' ? 'checked' : ''}>
                        <label class="form-check-label" for="verdadero_falso">
                            <i class="bi bi-check2-square me-1"></i>(Verdadero / Falso)
                        </label>
                    </div>
                    <div class="form-check mt-1">
                        <input class="form-check-input" type="radio" name="tipo_pregunta" id="alternativas" value="ALT" onclick="ALT()" ${pr.tipo_pregunta == 'ALT' ? 'checked' : ''}>
                        <label class="form-check-label" for="alternativas">
                            <i class="bi bi-ui-checks-grid me-1"></i>(Alternativas)
                        </label>
                    </div>
                </div>
            </div>
            <div class="col-md-4">
                <label for="puntos" class="fw-bold mt-2"><i class="bi bi-star-fill text-warning me-1"></i>Puntos:</label>
                <input type="number" value="${pr.puntos}" class="form-control mt-2" name="puntos" id="puntos" placeholder="Valor de la pregunta" min="0" required>
            </div>
            <div class="col-md-4">
                <label for="tiempo" class="fw-bold mt-2"><i class="bi bi-clock-fill text-primary me-1"></i>Tiempo:</label>
                <input type="number" value="${pr.tiempo}" class="form-control mt-2" name="tiempo" id="tiempo" placeholder="Tiempo (segundos)" min="2" required>
            </div>
        </div>
        <div class="mb-3">
            <label class="form-check-label fw-bold" for="alternativas"><i class="bi bi-list-ol me-1"></i>Alternativas: <button type="button" onclick="agregar_alternativas()" class="btn btn-outline-success btn-sm d-none" id="btn_add"><i class="bi bi-plus-circle"></i></button></label>
            <div class="alterantivas_form mt-2 ">
                ${alt}
            </div>
        </div>
        <div >
            <button type="button" class="btn btn-warning w-100" onclick="guardar_pregunta(${indice})"> Modificar pregunta</button>
        </div>
    `;
};

const ALT = () => {
    document.getElementById("btn_add").classList.remove("d-none");
    const div_alt = document.querySelector(".alterantivas_form");
    div_alt.innerHTML = `

    `;
};

const agregar_alternativas = () => {
    const div_alt = document.querySelector(".alterantivas_form");
    div_alt.insertAdjacentHTML(
        "beforeend",
        `
        <div class="w-50 d-flex alter ">
            <input type="text" class="form-control me-2 " >
            <button type="button" class="btn btn-sm btn-primary me-1 cl" onclick ="sl(this)"><i class="bi bi-check2"></i></button>
            <button type="button" class="btn btn-sm btn-danger" onclick= "eliminar_alternativa(this)"><i class="bi bi-trash3-fill"></i></button>
        </div> 
        `
    );
};

const eliminar_alternativa = (elemento) => {
    // Heurística 3: Control y libertad - Confirmación antes de eliminar
    Swal.fire({
        title: '¿Eliminar esta alternativa?',
        text: 'Esta acción no se puede deshacer.',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: 'Sí, eliminar',
        cancelButtonText: 'Cancelar',
        confirmButtonColor: '#dc3545',
        cancelButtonColor: '#6c757d'
    }).then((resultado) => {
        if (resultado.isConfirmed) {
    elemento.parentElement.remove();
            Swal.fire({
                icon: 'success',
                title: 'Alternativa eliminada',
                timer: 1500,
                showConfirmButton: false
            });
        }
    });
};

const VF = () => {
    document.getElementById("btn_add").classList.add("d-none");
    const div_alt = document.querySelector(".alterantivas_form");
    div_alt.innerHTML = `
        <button type="button" class="btn btn-outline-success btn-sm w-50 " onclick="select(this)"> Verdadero </button>
        <button type="button" class="btn btn-outline-success btn-sm w-50 " onclick="select(this)"> Falso </button>
    `;
};
const sl = (elemento) => {
    const elementos = document.querySelectorAll(".alterantivas_form .alter");
    elementos.forEach((el) => {
        const e = el.querySelector("input");
        const bt = el.querySelector("button.cl");
        bt.classList.remove("btn-success");
        bt.classList.add("btn-primary");
        e.classList.remove("border-success");
    });
    elemento.classList.remove("btn-primary");
    elemento.classList.add("btn-success");
    elemento.parentElement.querySelector("input").classList.add("border-success");
};

const select = (elemento) => {
    const elementos = document.querySelectorAll(".alterantivas_form .btn");
    elementos.forEach((el) => {
        el.classList.remove("btn-success");
        el.classList.add("btn-outline-success");
    });

    if (!elemento.classList.contains("btn-success")) {
        elemento.classList.remove("btn-outline-success");
        elemento.classList.add("btn-success");
    }
};

const agg_pr = () => {
    // Verificar que el detalle esté guardado antes de agregar preguntas
    if (!cuerpo_json.detalle.nombre_formulario || cuerpo_json.detalle.nombre_formulario.trim() === '') {
        Swal.fire({
            icon: 'warning',
            title: 'Detalle no guardado',
            text: 'Por favor, guarda primero el detalle del formulario antes de agregar preguntas.',
            confirmButtonText: 'Entendido'
        });
        // Volver a mostrar el formulario de detalle
        detalle();
        return;
    }
    
    const cont = getContenido();
    if (!cont) {
        console.error("No se encontró el elemento .cont_formulario");
        Swal.fire({
            icon: 'error',
            title: 'Error',
            text: 'No se pudo encontrar el formulario. Por favor, recarga la página.',
            confirmButtonText: 'Entendido'
        });
        return;
    }
    
    cont.innerHTML = `
        <div class="d-flex align-items-center mb-3">
            <i class="bi bi-question-circle-fill fs-2 text-primary me-2"></i>
            <h3 class="fw-bold mb-0">Paso 2: Agregar preguntas</h3>
        </div>
        <p class="text-secondary separador mb-4"><i class="bi bi-info-circle me-1"></i>Añade las preguntas que conformarán tu formulario</p>
        <div class="mb-3">
            <label for="nombre_pregunta" class="fw-bold">
                <i class="bi bi-pencil-square me-1"></i>Pregunta:
                <span class="text-danger">*</span>
                <i class="bi bi-info-circle text-primary ms-1" data-bs-toggle="tooltip" data-bs-placement="top" title="Mínimo 5 caracteres, máximo 500"></i>
            </label>
            <input type="text" class="form-control mt-2" id="nombre_pregunta" placeholder="¿Cuál es tu pregunta?" 
                   maxlength="500" required onblur="if(window.validarCampo) validarCampo('nombre_pregunta', this.value, 'texto')" 
                   oninput="const contador = document.getElementById('contador_pregunta'); if(contador) contador.textContent = this.value.length">
            <small class="text-muted">Caracteres: <span id="contador_pregunta">0</span>/500</small>
        </div>
        <div class="row mb-3">
            <div class="col-md-3">
                <div class="mt-2" role="radiogroup" aria-labelledby="tipo_pregunta_label">
                    <span id="tipo_pregunta_label" class="fw-bold"><i class="bi bi-list-check me-1"></i>Tipo pregunta:</span>
                    <div class="form-check mt-2">
                        <input class="form-check-input" type="radio" name="tipo_pregunta" id="verdadero_falso" value="VF" onclick="if(window.VF) VF()">
                        <label class="form-check-label" for="verdadero_falso">
                            <i class="bi bi-check2-square me-1"></i>(Verdadero / Falso)
                        </label>
                    </div>
                    <div class="form-check mt-1">
                        <input class="form-check-input" type="radio" name="tipo_pregunta" id="alternativas" value="ALT" onclick="if(window.ALT) ALT()">
                        <label class="form-check-label" for="alternativas">
                            <i class="bi bi-ui-checks-grid me-1"></i>(Alternativas)
                        </label>
                    </div>
                </div>
            </div>
            <div class="col-md-4">
                <label for="puntos" class="fw-bold mt-2">
                    <i class="bi bi-star-fill text-warning me-1"></i>Puntos:
                    <span class="text-danger">*</span>
                    <i class="bi bi-info-circle text-primary ms-1" data-bs-toggle="tooltip" title="Valor entre 1 y 1000"></i>
                </label>
                <input type="number" class="form-control mt-2" name="puntos" id="puntos" placeholder="Valor de la pregunta" min="1" max="1000" required>
            </div>
            <div class="col-md-4">
                <label for="tiempo" class="fw-bold mt-2">
                    <i class="bi bi-clock-fill text-primary me-1"></i>Tiempo (segundos):
                    <span class="text-danger">*</span>
                    <i class="bi bi-info-circle text-primary ms-1" data-bs-toggle="tooltip" title="Mínimo 2 segundos, máximo 300"></i>
                </label>
                <input type="number" class="form-control mt-2" name="tiempo" id="tiempo" placeholder="Tiempo (segundos)" min="2" max="300" required>
            </div>
        </div>
        <div class="mb-3">
            <label class="form-check-label fw-bold" for="alternativas"><i class="bi bi-list-ol me-1"></i>Alternativas: <button type="button" onclick="if(window.agregar_alternativas) agregar_alternativas()" class="btn btn-outline-success btn-sm d-none" id="btn_add"><i class="bi bi-plus-circle"></i></button></label>
            <div class="alterantivas_form mt-2 ">
    
            </div>
        </div>
        <div >
            <button type="button" class="btn btn-primary w-100" onclick="if(window.guardar_pregunta) guardar_pregunta()"> Guardar pregunta</button>
        </div>
    `;
    
    // Reinicializar tooltips después de agregar contenido dinámico
    setTimeout(() => {
        const listaTooltips = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        listaTooltips.map(function (elementoTooltip) {
            return new bootstrap.Tooltip(elementoTooltip);
        });
    }, 100);
};
const guardar_pregunta = (ss) => {
    // Obtener los valores de los campos
    const nombre_pregunta = document.getElementById("nombre_pregunta")?.value?.trim() || '';
    const tipo_pregunta = document.querySelector('input[name="tipo_pregunta"]:checked')?.value;
    const puntos = parseInt(document.getElementById("puntos")?.value || 0);
    const tiempo = parseInt(document.getElementById("tiempo")?.value || 0);

    // Heurística 9: Recuperación de errores - Validación completa con mensajes claros
    let errores = [];

    // Validar pregunta
    if (!nombre_pregunta) {
        errores.push('La pregunta no puede estar vacía');
    } else if (nombre_pregunta.length < 5) {
        errores.push('La pregunta debe tener al menos 5 caracteres');
    } else if (nombre_pregunta.length > 500) {
        errores.push('La pregunta no puede exceder 500 caracteres');
    }

    // Validar tipo de pregunta
    if (!tipo_pregunta) {
        errores.push('Debes seleccionar un tipo de pregunta (Verdadero/Falso o Alternativas)');
    }

    // Validar puntos
    if (!puntos || puntos <= 0) {
        errores.push('Los puntos deben ser mayor que 0 (recomendado: 1-100)');
    } else if (puntos > 1000) {
        errores.push('Los puntos no pueden exceder 1000');
    }

    // Validar tiempo
    if (!tiempo || tiempo < 2) {
        errores.push('El tiempo debe ser al menos 2 segundos');
    } else if (tiempo > 300) {
        errores.push('El tiempo no puede exceder 300 segundos (5 minutos)');
    }

    // Validar alternativas según el tipo
    if (tipo_pregunta === "VF") {
        const respuestaSeleccionada = document.querySelector(".alterantivas_form .btn.btn-success");
        if (!respuestaSeleccionada) {
            errores.push('Debes seleccionar la respuesta correcta (Verdadero o Falso)');
        }
    } else if (tipo_pregunta === "ALT") {
        const alternativas = document.querySelectorAll(".alterantivas_form .alter input");
        const alternativasValidas = Array.from(alternativas).filter(input => input.value.trim().length > 0);
        
        if (alternativasValidas.length < 2) {
            errores.push('Debes agregar al menos 2 alternativas');
        } else if (alternativasValidas.length > 6) {
            errores.push('No puedes tener más de 6 alternativas');
        }
        
        // Validar que todas las alternativas tengan contenido
        alternativasValidas.forEach((input, index) => {
            if (input.value.trim().length < 1) {
                errores.push(`La alternativa ${index + 1} no puede estar vacía`);
            }
            if (input.value.trim().length > 200) {
                errores.push(`La alternativa ${index + 1} no puede exceder 200 caracteres`);
    }
        });
        
        // Validar que haya una respuesta correcta seleccionada
        const respuestaCorrecta = document.querySelector(".alterantivas_form .alter input.border-success");
        if (!respuestaCorrecta) {
            errores.push('Debes seleccionar la respuesta correcta (clic en el botón ✓ junto a la alternativa correcta)');
        }
        
        // Validar que no haya alternativas duplicadas
        const valoresAlternativas = alternativasValidas.map(input => input.value.trim().toLowerCase());
        const valoresUnicos = new Set(valoresAlternativas);
        if (valoresAlternativas.length !== valoresUnicos.size) {
            errores.push('No puedes tener alternativas duplicadas');
        }
    }

    // Mostrar errores si existen
    if (errores.length > 0) {
        Swal.fire({
            icon: 'error',
            title: 'Error de validación',
            html: '<ul style="text-align: left;">' + errores.map(e => `<li>${e}</li>`).join('') + '</ul>',
            confirmButtonText: 'Entendido'
        });
        return;
    }

    // Mostrar confirmación antes de guardar la pregunta
    Swal.fire({
        text: '¿Quieres guardar esta pregunta?',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: 'Sí, guardar',
        cancelButtonText: 'Cancelar'
    }).then((resultado) => {
        if (resultado.isConfirmed) {
            // Si el usuario confirma, guardar la pregunta

            const al = [];
            let rpt = "";

            if (tipo_pregunta === "VF") {
                al.push("Verdadero");
                al.push("Falso");
                const ed = document.querySelector(".alterantivas_form .btn.btn-success");
                rpt = ed ? ed.textContent : ""; // Obtener la respuesta seleccionada
            } else {
                const conjunto = document.querySelectorAll(".alterantivas_form .alter");
                conjunto.forEach((el) => {
                    const element = el.querySelector("input");
                    if (element.classList.contains("border-success")) {
                        rpt = element.value;
                    }
                    al.push(element.value);
                });
            }

            // Si se está modificando una pregunta existente (ss >= 0), actualizarla
            if (ss >= 0 && ss !== null && ss !== undefined) {
                const res = cuerpo_json.preguntas[ss];
                if (res) {
                    res.nombre_pregunta = nombre_pregunta;
                    res.tipo_pregunta = tipo_pregunta;
                    res.puntos = puntos;
                    res.tiempo = tiempo;
                    res.alternativas = al.map(a => a.trim());
                    res.respuesta = rpt.trim();
                }
            } else {
                // Si se está agregando una nueva pregunta, crearla
                const pr = {
                    nombre_pregunta: nombre_pregunta.trim(),
                    tipo_pregunta: tipo_pregunta,
                    puntos: puntos,
                    tiempo: tiempo,
                    alternativas: al.map(a => a.trim()),
                    respuesta: rpt.trim(),
                };
                cuerpo_json.preguntas.push(pr);
            }
            
            // Heurística 1: Visibilidad del estado - Actualizar contador de preguntas
            actualizarContadorPreguntas();

            // Limpiar y renderizar el contenido
            const cont = getContenido();
            if (!cont) {
                console.error("No se encontró el elemento .cont_formulario");
                return;
            }
            cont.innerHTML = "";
            const cards_continue = document.querySelector(".cards_continue");
            cards_continue.innerHTML = "";

            // Actualizar las preguntas en el DOM
            dibujar_preguntas();
            Swal.fire({
                icon: 'success',
                title: 'Pregunta Guardada',
                text: 'La pregunta ha sido guardada correctamente.',
                timer: 2000,
                showConfirmButton: false
            }).then(() => {
                // Volver a la vista de detalle después de guardar
                if (window.detalle) {
                    detalle();
                }
            });
        } else {
            // Si el usuario cancela, no hacer nada
            console.log('El usuario canceló la acción de guardar.');
        }
    });
};



const eliminar_pr = (el, indice) => {
    // Heurística 3: Control y libertad - Confirmación antes de eliminar
    Swal.fire({
        text: '¿Quieres eliminar esta pregunta?',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: 'Sí, eliminar',
        cancelButtonText: 'Cancelar',
        confirmButtonColor: '#dc3545'
    }).then((resultado) => {
        if (resultado.isConfirmed) {
            // Si el usuario confirma, eliminar la pregunta
            const cc = el.parentElement.parentElement.parentElement;
            cc.remove();  // Eliminar el elemento del DOM
            cuerpo_json.preguntas.splice(indice, 1);  // Eliminar la pregunta del array

            // Actualizar los índices de las preguntas en la vista
            const enumeracion = document.querySelectorAll('.texto_pregunta');
            enumeracion.forEach((enu, index) => {
                enu.textContent = `Pregunta ${index + 1}:`;  // Actualizar la numeración de las preguntas
            });
            
            // Heurística 1: Visibilidad del estado - Actualizar contador
            actualizarContadorPreguntas();

            // Mostrar mensaje de éxito
            Swal.fire({
                icon: 'success',
                title: 'Pregunta eliminada',
                text: 'La pregunta ha sido eliminada correctamente.',
                timer: 2000,
                showConfirmButton: false
            });
        }
    });
};

const confirmarEnvio = () => {
    // Validar que el detalle esté guardado
    if (!cuerpo_json.detalle.nombre_formulario || cuerpo_json.detalle.nombre_formulario.trim() === '') {
        Swal.fire({
            icon: 'warning',
            title: 'Detalle no guardado',
            text: 'Por favor, guarda primero el detalle del formulario antes de crear el cuestionario.',
            confirmButtonText: 'Entendido'
        });
        detalle();
        return;
    }
    
    // Validar que haya al menos una pregunta
    if (!cuerpo_json.preguntas || cuerpo_json.preguntas.length === 0) {
        Swal.fire({
            icon: 'warning',
            title: 'Sin preguntas',
            text: 'Debes agregar al menos una pregunta antes de crear el cuestionario.',
            confirmButtonText: 'Entendido'
        });
        return;
    }
    
    Swal.fire({
        title: '¿Estás seguro de que deseas crear este formulario?',
        text: `Se creará el cuestionario "${cuerpo_json.detalle.nombre_formulario}" con ${cuerpo_json.preguntas.length} pregunta(s).`,
        icon: 'question',
        showCancelButton: true,
        confirmButtonText: 'Sí, crear',
        cancelButtonText: 'Cancelar',
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33'
    }).then((resultado) => {
        if (resultado.isConfirmed) {
            // Si el usuario confirma, se envían los datos
            enviar_datos();
        } else {
            console.log('El usuario canceló la acción de crear el formulario.');
        }
    });
};


// Heurística 1: Visibilidad del estado - Función para actualizar contador
const actualizarContadorPreguntas = () => {
    const contadorElement = document.getElementById('contador_preguntas');
    if (contadorElement) {
        const cantidad = cuerpo_json.preguntas.length;
        contadorElement.textContent = `${cantidad} pregunta${cantidad !== 1 ? 's' : ''}`;
        contadorElement.className = `badge ${cantidad === 0 ? 'bg-danger' : cantidad < 3 ? 'bg-warning' : 'bg-success'}`;
    }
};

// Heurística 3: Control y libertad - Inicializar contador al cargar
// Heurística 6: Reconocimiento - Inicializar tooltips
document.addEventListener('DOMContentLoaded', () => {
    // Crear contador si no existe
    const navegacion = document.querySelector('.navegacion_formulario');
    if (navegacion && !document.getElementById('contador_preguntas')) {
        const contadorHtml = `
            <div class="card shadow-sm p-2 mb-2 mt-2">
                <small class="text-muted d-block mb-1">Progreso</small>
                <span id="contador_preguntas" class="badge bg-secondary">0 preguntas</span>
            </div>
        `;
        const separador = document.querySelector('.separador');
        if (separador) {
            separador.insertAdjacentHTML('afterend', contadorHtml);
        }
    }
    actualizarContadorPreguntas();
    
    // Inicializar tooltips de Bootstrap
    const listaTooltips = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    listaTooltips.map(function (elementoTooltip) {
        return new bootstrap.Tooltip(elementoTooltip);
    });
    
    // Heurística 5: Prevención de errores - Validación en tiempo real para nombre del cuestionario
    const nombreInput = document.getElementById('nombre_cuestionario');
    if (nombreInput) {
        nombreInput.addEventListener('blur', function() {
            validarCampo('nombre_cuestionario', this.value, 'texto');
        });
        nombreInput.addEventListener('input', function() {
            this.classList.remove('is-invalid', 'is-valid');
            const divError = document.getElementById('nombre_cuestionario_error');
            if (divError) divError.remove();
        });
    }
    
    // Validación en tiempo real para descripción
    const descripcionInput = document.getElementById('descripcion');
    if (descripcionInput) {
        descripcionInput.addEventListener('blur', function() {
            validarCampo('descripcion', this.value, 'textarea');
        });
        descripcionInput.addEventListener('input', function() {
            this.classList.remove('is-invalid', 'is-valid');
            const divError = document.getElementById('descripcion_error');
            if (divError) divError.remove();
        });
    }
});

// Función para enviar los datos del formulario
const enviar_datos = async () => {
    // Heurística 9: Recuperación de errores - Validación completa antes de enviar
    const errores = [];
    
    // Validar detalle
    if (!cuerpo_json.detalle.nombre_formulario || cuerpo_json.detalle.nombre_formulario.trim().length === 0) {
        errores.push('El nombre del cuestionario es obligatorio');
    }
    
    if (!cuerpo_json.detalle.tipo_formulario) {
        errores.push('Debes seleccionar el tipo de cuestionario');
    }
    
    // Validar que haya al menos una pregunta
    if (!cuerpo_json.preguntas || cuerpo_json.preguntas.length === 0) {
        errores.push('Debes agregar al menos una pregunta antes de crear el cuestionario');
    } else if (cuerpo_json.preguntas.length < 1) {
        errores.push('El cuestionario debe tener al menos 1 pregunta');
    }
    
    // Validar cada pregunta
    cuerpo_json.preguntas.forEach((pregunta, index) => {
        if (!pregunta.respuesta || pregunta.respuesta.trim().length === 0) {
            errores.push(`La pregunta ${index + 1} no tiene respuesta correcta seleccionada`);
        }
        if (pregunta.tipo_pregunta === 'ALT' && (!pregunta.alternativas || pregunta.alternativas.length < 2)) {
            errores.push(`La pregunta ${index + 1} debe tener al menos 2 alternativas`);
        }
    });
    
    if (errores.length > 0) {
        Swal.fire({
            icon: 'error',
            title: 'No se puede crear el cuestionario',
            html: '<ul style="text-align: left;">' + errores.map(e => `<li>${e}</li>`).join('') + '</ul>',
            confirmButtonText: 'Entendido'
        });
        return;
    }
    
    // Heurística 1: Visibilidad del estado - Mostrar indicador de carga
    Swal.fire({
        title: 'Creando cuestionario...',
        text: 'Por favor espera',
        allowOutsideClick: false,
        didOpen: () => {
            Swal.showLoading();
        }
    });
    
    const ruta = "/registrar_pregunta";
    console.log(cuerpo_json);

    try {
    const response = await fetch(ruta, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(cuerpo_json)
    });

    const resp = await response.json();

    if (resp.estado) {
        Swal.fire({
            icon: 'success',
                title: '¡Formulario creado exitosamente!',
                text: resp.mensaje || 'El formulario ha sido creado y guardado correctamente.',
                confirmButtonText: 'Aceptar'
            }).then(() => {
                location.reload();
            });
    } else {
        Swal.fire({
            icon: 'error',
                title: 'Error al crear el formulario',
                html: resp.mensaje || 'No se pudo crear el formulario. Por favor intenta nuevamente.',
                confirmButtonText: 'Entendido'
            });
        }
    } catch (error) {
        Swal.fire({
            icon: 'error',
            title: 'Error de conexión',
            text: 'No se pudo conectar con el servidor. Verifica tu conexión a internet.',
            confirmButtonText: 'Entendido'
        });
    }
};

// Función para dibujar todas las preguntas en el DOM
const dibujar_preguntas = () => {
    const cards_continue = document.querySelector(".cards_continue");
    if (!cards_continue) return;
    
    cards_continue.innerHTML = "";
    
    cuerpo_json.preguntas.forEach((pregunta, index) => {
        cards_continue.innerHTML += `
            <div class="detalle_inicial card shadow-lg p-3 enfocar mt-2" id="detalle_card_${index}" onclick="pregunta(${index})">
                <div class="row">
                    <div class="col-9">
                        <p class="text-secondary texto_pregunta">Pregunta ${index + 1}: </p>
                        <p class="name_cuestion">
                            ${pregunta.nombre_pregunta}
                        </p>
                    </div>
                    <div class="col-2">
                        <button onclick="eliminar_pr(this, ${index})" class="btn btn-danger rounded-circle" style="width: 2.5rem; height: 2.5rem;">
                            <i class="bi bi-trash3 fs-9"></i>
                        </button>
                    </div>
                </div>
            </div>
        `;
    });
    
    // Actualizar contador
    actualizarContadorPreguntas();
};

// Función para importar preguntas desde Excel
const importarDesdeExcel = async () => {
    // Crear input file dinámicamente
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = '.xlsx,.xls';
    input.style.display = 'none';
    
    input.onchange = async (e) => {
        const file = e.target.files[0];
        if (!file) return;
        
        // Validar extensión
        const extension = file.name.split('.').pop().toLowerCase();
        if (!['xlsx', 'xls'].includes(extension)) {
            Swal.fire({
                icon: 'error',
                title: 'Error',
                text: 'Solo se permiten archivos Excel (.xlsx, .xls)'
            });
            return;
        }
        
        // Mostrar loading
        Swal.fire({
            title: 'Importando preguntas...',
            text: 'Por favor espera mientras procesamos el archivo',
            allowOutsideClick: false,
            didOpen: () => {
                Swal.showLoading();
            }
        });
        
        try {
            const formData = new FormData();
            formData.append('excel_archivo', file);
            
            const response = await fetch('/importar_preguntas_excel', {
                method: 'POST',
                body: formData
            });
            
            const data = await response.json();
            
            if (data.estado) {
                // Agregar las preguntas importadas al cuerpo_json
                if (data.preguntas && Array.isArray(data.preguntas)) {
                    data.preguntas.forEach(pregunta => {
                        cuerpo_json.preguntas.push(pregunta);
                    });
                    
                    // Actualizar la vista
                    dibujar_preguntas();
                    
                    Swal.fire({
                        icon: 'success',
                        title: '¡Éxito!',
                        html: `
                            <p>Se importaron <strong>${data.total_preguntas}</strong> pregunta(s) correctamente.</p>
                            ${data.errores && data.errores.length > 0 ? 
                                `<p class="text-warning">Advertencia: Se encontraron ${data.total_errores} error(es).</p>` : 
                                ''}
                        `,
                        confirmButtonText: 'Aceptar'
                    });
                } else {
                    Swal.fire({
                        icon: 'error',
                        title: 'Error',
                        text: 'No se recibieron preguntas del servidor'
                    });
                }
            } else {
                // Mostrar errores si los hay
                let mensajeError = data.mensaje || 'Error al importar el archivo';
                if (data.errores && data.errores.length > 0) {
                    mensajeError += '<br><br><strong>Errores encontrados:</strong><ul style="text-align: left; max-height: 200px; overflow-y: auto;">';
                    data.errores.slice(0, 10).forEach(error => {
                        mensajeError += `<li>${error}</li>`;
                    });
                    if (data.errores.length > 10) {
                        mensajeError += `<li>... y ${data.errores.length - 10} error(es) más</li>`;
                    }
                    mensajeError += '</ul>';
                }
                
                Swal.fire({
                    icon: 'error',
                    title: 'Error al importar',
                    html: mensajeError,
                    width: '600px'
                });
            }
        } catch (error) {
            console.error('Error al importar Excel:', error);
            Swal.fire({
                icon: 'error',
                title: 'Error',
                text: 'Error al procesar el archivo. Por favor, verifica que el formato sea correcto.'
            });
        } finally {
            // Limpiar input
            document.body.removeChild(input);
        }
    };
    
    document.body.appendChild(input);
    input.click();
};

// Agregar event listener al botón de importar Excel
document.addEventListener('DOMContentLoaded', () => {
    const btnImportarExcel = document.getElementById('btn_importar_excel');
    if (btnImportarExcel) {
        btnImportarExcel.addEventListener('click', importarDesdeExcel);
    }
});

// Asegurar que las funciones estén disponibles globalmente para los onclick handlers
window.guardar_detalle = guardar_detalle;
window.agg_pr = agg_pr;
window.detalle = detalle;
window.pregunta = pregunta;
window.guardar_pregunta = guardar_pregunta;
window.importarDesdeExcel = importarDesdeExcel;
window.eliminar_pr = eliminar_pr;
window.confirmarEnvio = confirmarEnvio;
window.VF = VF;
window.ALT = ALT;
window.agregar_alternativas = agregar_alternativas;
window.eliminar_alternativa = eliminar_alternativa;
window.sl = sl;
window.select = select;
window.validarCampo = validarCampo;
window.dibujar_preguntas = dibujar_preguntas;