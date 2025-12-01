// ===============================
// modificar.js - módulo completo
// ===============================

// REFERENCIAS DOM
const contenido = document.querySelector(".cont_formulario");
const nombre_formulario = document.getElementById('nombre_cuestionario');
const ttipo_formulario = document.getElementById('tipo_cuestionario');
const estado_formulario = document.getElementById('estado');
const descripcion_formulario = document.getElementById('descripcion');
const cards_continue = document.querySelector(".cards_continue");

// OBJETO LOCAL
const cuerpo_json = {
    detalle: {
        id_formulario: "",
        nombre_formulario: "",
        tipo_formulario: "",
        descripcion_formulario: "",
        estado: "",
    },
    preguntas: [],
};

// ---------- CARGA INICIAL ----------
document.addEventListener('DOMContentLoaded', () => {
    console.log("Datos recibidos del backend:", typeof datos !== 'undefined' ? datos : null);
    // Protección si 'datos' no viene
    if (typeof datos === 'undefined' || datos == null) {
        Swal.fire('Error', 'No se cargaron los datos desde el servidor.', 'error');
        return;
    }
    llenar_formato();
});

// ---------- LLENADO ----------
const llenar_formato = () => {
    const detalle = datos.detalle || {};
    const respuestas = datos.respuestas || [];

    cuerpo_json.detalle.id_formulario = detalle.id_cuestionario || "";
    cuerpo_json.detalle.nombre_formulario = detalle.nombre || "";
    cuerpo_json.detalle.tipo_formulario = detalle.tipo_cuestionario || "";
    cuerpo_json.detalle.descripcion_formulario = detalle.descripcion || "";
    cuerpo_json.detalle.estado = detalle.estado || "";
    cuerpo_json.detalle.imagen_url = detalle.imagen_url || null;

    // Normalizar preguntas: si backend envía alternativas como string JSON, parsear
    cuerpo_json.preguntas = (respuestas || []).map(r => {
        const cop = { ...r };
        if (cop.alternativas && typeof cop.alternativas === 'string') {
            try { cop.alternativas = JSON.parse(cop.alternativas); }
            catch (e) { cop.alternativas = []; }
        }
        // Si alternativas es un array de objetos, mantener los objetos completos para preservar estado_alternativa
        if (Array.isArray(cop.alternativas) && cop.alternativas.length > 0 && typeof cop.alternativas[0] === 'object') {
            // Mantener los objetos completos para poder marcar la respuesta correcta
            // No convertir a strings aquí, se hará en render_form_pregunta si es necesario
            // Encontrar la respuesta correcta
            const altCorrectaObj = cop.alternativas.find(alt => alt.estado_alternativa == 1);
            if (altCorrectaObj && !cop.respuesta) {
                cop.respuesta = altCorrectaObj.respuesta || altCorrectaObj.texto || '';
            }
        } else if (Array.isArray(cop.alternativas) && cop.alternativas.length > 0) {
            // Si ya son strings, buscar la respuesta correcta en el array original
            // Necesitamos buscar en el array original antes de convertirlo
            const alternativasOriginales = r.alternativas;
            if (Array.isArray(alternativasOriginales) && alternativasOriginales.length > 0 && typeof alternativasOriginales[0] === 'object') {
                const altCorrectaObj = alternativasOriginales.find(alt => alt.estado_alternativa == 1);
                if (altCorrectaObj && !cop.respuesta) {
                    cop.respuesta = altCorrectaObj.respuesta || altCorrectaObj.texto || '';
                }
            }
        }
        // nombres distintos posible: normalizar a nombre_pregunta / pregunta
        cop.nombre_pregunta = cop.nombre_pregunta || cop.pregunta || "";
        cop.puntaje = cop.puntaje || cop.puntos || 0;
        cop.tiempo = cop.tiempo || cop.tiempo_respuesta || 0;
        cop.respuesta = cop.respuesta || cop.respuesta_correcta || "";
        cop.id_pregunta = cop.id_pregunta || cop.id || null;
        cop.tipo_pregunta = cop.tipo_pregunta || 'ALT'; // Default a ALT si no viene
        return cop;
    });

    llenar_detalle();
};

const llenar_detalle = () => {
    nombre_formulario.value = cuerpo_json.detalle.nombre_formulario;
    descripcion_formulario.value = cuerpo_json.detalle.descripcion_formulario;
    ttipo_formulario.value = cuerpo_json.detalle.tipo_formulario;
    estado_formulario.value = cuerpo_json.detalle.estado;
    
    // Mostrar imagen existente si hay una
    if (cuerpo_json.detalle.imagen_url) {
        const previewDiv = document.getElementById('preview_imagen_cuestionario');
        const imgPreview = document.getElementById('img_preview_cuestionario');
        if (previewDiv && imgPreview) {
            imgPreview.src = '/' + cuerpo_json.detalle.imagen_url;
            previewDiv.classList.remove('d-none');
        }
    }
    
    dibujar_preguntas();
};

// ---------- MODIFICAR DETALLE ----------
const fn_modificardetalle = async () => {
    // Subir imagen si existe una nueva
    const imagenInput = document.getElementById('imagen_cuestionario');
    let imagenUrl = cuerpo_json.detalle.imagen_url || null; // Mantener la imagen actual si no hay nueva
    
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
    
    cuerpo_json.detalle.nombre_formulario = nombre_formulario.value;
    cuerpo_json.detalle.tipo_formulario = ttipo_formulario.value;
    cuerpo_json.detalle.descripcion_formulario = descripcion_formulario.value;
    cuerpo_json.detalle.estado = estado_formulario.value;
    cuerpo_json.detalle.imagen_url = imagenUrl; // Incluir imagen_url en los datos
    
    console.log('[DEBUG] Datos a enviar al backend:', cuerpo_json.detalle);
    console.log('[DEBUG] imagen_url que se enviará:', imagenUrl);

    try {
        const respuesta = await fetch('/fn_modificar', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(cuerpo_json.detalle)
        });
        const rpt = await respuesta.json();

        if (rpt.estado === true) {
            // Recargar los datos del cuestionario desde el backend para sincronizar imagen_url
            const idFormulario = cuerpo_json.detalle.id_formulario;
            try {
                const datosResponse = await fetch(`/api_obtener_cuestionario_modificar/${idFormulario}`);
                if (datosResponse.ok) {
                    const datosActualizados = await datosResponse.json();
                    console.log('[DEBUG] Datos actualizados después de guardar:', datosActualizados);
                    if (datosActualizados && datosActualizados.detalle) {
                        // Actualizar cuerpo_json con los datos actualizados del backend
                        cuerpo_json.detalle.imagen_url = datosActualizados.detalle.imagen_url || null;
                        console.log('[DEBUG] cuerpo_json.detalle.imagen_url actualizado a:', cuerpo_json.detalle.imagen_url);
                    }
                }
            } catch (e) {
                console.error('[DEBUG] Error al recargar datos después de guardar:', e);
            }
            
            Swal.fire({
                icon: 'success',
                title: 'Éxito',
                text: rpt.mensaje || 'Formulario modificado correctamente',
                timer: 1500,
                showConfirmButton: false
            }).then(() => {
                // Recargar el detalle para mostrar la nueva imagen si se subió una
                if (typeof detalle === 'function') {
                    detalle();
                }
            });
        } else {
            Swal.fire('Error', rpt.mensaje || 'No se pudo modificar', 'error');
        }
    } catch (err) {
        console.error('Error al modificar detalle:', err);
        Swal.fire('Error', 'Fallo de conexión al modificar detalle', 'error');
    }
};

const modificar_detalle = () => {
    Swal.fire({
        text: '¿Estás seguro de que deseas modificar este formulario?',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: 'Sí, modificar',
        cancelButtonText: 'Cancelar'
    }).then(res => {
        if (res.isConfirmed) fn_modificardetalle();
    });
};

// ---------- DIBUJAR LISTA DE PREGUNTAS ----------
const dibujar_preguntas = () => {
    const contenedor = cards_continue;
    contenedor.innerHTML = '';

    if (!Array.isArray(cuerpo_json.preguntas) || cuerpo_json.preguntas.length === 0) {
        contenedor.innerHTML = '<p class="text-muted text-center mt-3">No hay preguntas registradas.</p>';
        return;
    }

    cuerpo_json.preguntas.forEach((pregunta, index) => {
        contenedor.innerHTML += `
            <div class="detalle_inicial card shadow-lg p-3 enfocar mt-2" id="detalle_card_${index}">
                <div class="row align-items-center">
                    <div class="col-9" style="cursor:pointer" onclick="mostrar_pregunta(${index})">
                        <p class="text-secondary texto_pregunta">Pregunta ${index + 1}:</p>
                        <p class="name_cuestion fw-bold">${escapeHtml(pregunta.nombre_pregunta)}</p>
                    </div>
                    <div class="col-3 text-end">
                        <button onclick="eliminar_pr(event, ${pregunta.id_pregunta}, ${index})" class="btn btn-danger rounded-circle" style="width: 2.5rem; height: 2.5rem;">
                            <i class="bi bi-trash3"></i>
                        </button>
                    </div>
                </div>
            </div>
        `;
    });
};

// ---------- MOSTRAR FORMULARIO PARA AÑADIR / EDITAR PREGUNTA ----------
const agg_pr = () => {
    // ss undefined => nueva pregunta
    render_form_pregunta(null);
};

const mostrar_pregunta = (index) => {
    const pr = cuerpo_json.preguntas[index];
    if (!pr) return Swal.fire('Error', 'Pregunta no encontrada', 'error');
    render_form_pregunta(pr, index);
};

const render_form_pregunta = (pr = null, index = null) => {
    // pr == null => nuevo
    const nombre = pr ? pr.nombre_pregunta : '';
    const tipo = pr ? pr.tipo_pregunta : '';
    const puntos = pr ? (pr.puntaje || pr.puntos || 0) : 0;
    const tiempo = pr ? (pr.tiempo || pr.tiempo_respuesta || 0) : 10;
    const archivoVal = pr ? (pr.archivo || '') : '';
    // Normalizar alternativas: mantener objetos completos para preservar estado_alternativa
    let alternativas = [];
    if (pr && pr.alternativas) {
        if (Array.isArray(pr.alternativas)) {
            // Mantener objetos completos si vienen como objetos, para preservar estado_alternativa
            alternativas = pr.alternativas.map(alt => {
                if (typeof alt === 'object' && alt !== null) {
                    // Mantener el objeto completo con estado_alternativa
                    return {
                        respuesta: alt.respuesta || alt.texto || '',
                        estado_alternativa: alt.estado_alternativa || 0,
                        id_alternativa: alt.id_alternativa || null
                    };
                }
                // Si es string, crear objeto básico
                return {
                    respuesta: alt,
                    estado_alternativa: 0
                };
            }).filter(alt => alt && alt.respuesta); // Filtrar vacíos
        } else if (typeof pr.alternativas === 'string') {
            try {
                const parsed = JSON.parse(pr.alternativas);
                alternativas = Array.isArray(parsed) ? parsed.map(alt => {
                    if (typeof alt === 'object') {
                        return {
                            respuesta: alt.respuesta || alt.texto || '',
                            estado_alternativa: alt.estado_alternativa || 0,
                            id_alternativa: alt.id_alternativa || null
                        };
                    }
                    return {
                        respuesta: alt,
                        estado_alternativa: 0
                    };
                }).filter(alt => alt && alt.respuesta) : [];
            } catch (e) {
                alternativas = [];
            }
        }
    }

    // construir HTML del formulario de pregunta
    contenido.innerHTML = `
        <div class="d-flex align-items-center mb-3">
            <i class="bi bi-question-circle-fill fs-2 text-primary me-2"></i>
            <h3 class="fw-bold mb-0">${pr ? 'Editar pregunta' : 'Agregar pregunta'}</h3>
        </div>

        <div class="mb-3">
            <label class="fw-bold">Pregunta</label>
            <input id="nombre_pregunta" class="form-control mt-2" value="${escapeAttr(nombre)}" placeholder="¿Cuál es la pregunta?">
        </div>

        <div class="row mb-3">
            <div class="col-md-3">
                <span class="fw-bold">Tipo:</span>
                <div class="form-check mt-2">
                    <input class="form-check-input" type="radio" name="tipo_pregunta" id="vf_radio" value="VF" ${tipo === 'VF' ? 'checked' : ''} onclick="mostrar_VF()">
                    <label class="form-check-label" for="vf_radio">(Verdadero / Falso)</label>
                </div>
                <div class="form-check mt-1">
                    <input class="form-check-input" type="radio" name="tipo_pregunta" id="alt_radio" value="ALT" ${tipo === 'ALT' ? 'checked' : ''} onclick="mostrar_ALT()">
                    <label class="form-check-label" for="alt_radio">(Alternativas)</label>
                </div>
            </div>

            <div class="col-md-4">
                <label class="fw-bold">Puntos</label>
                <input id="puntos" class="form-control mt-2" type="number" min="0" value="${puntos}">
            </div>

            <div class="col-md-4">
                <label class="fw-bold">Tiempo (s)</label>
                <input id="tiempo" class="form-control mt-2" type="number" min="2" value="${tiempo}">
            </div>
        </div>

        <div class="mb-3">
            <label class="fw-bold">Alternativas <button id="btn_add" type="button" class="btn btn-outline-success btn-sm ${tipo === 'ALT' ? '' : 'd-none'}" onclick="agregar_alternativas()"><i class="bi bi-plus-circle"></i></button></label>
            <div class="alterantivas_form mt-2">
                ${ (tipo === 'ALT' && alternativas.length) ? alternativas.map(a => render_alternativa_html(a)).join('') : (tipo === 'VF' ? `
                    <div class="d-flex gap-2">
                        <button type="button" class="btn btn-outline-success btn-sm w-50" onclick="seleccionar_VF(this)" ${pr && pr.respuesta === 'Verdadero' ? 'data-selected="true"' : ''}>Verdadero</button>
                        <button type="button" class="btn btn-outline-success btn-sm w-50" onclick="seleccionar_VF(this)" ${pr && pr.respuesta === 'Falso' ? 'data-selected="true"' : ''}>Falso</button>
                    </div>
                ` : '')}
            </div>
        </div>

        <div class="d-grid gap-2">
            <button type="button" class="btn ${pr ? 'btn-warning' : 'btn-primary'}" onclick="if(window.guardar_pregunta) guardar_pregunta(${index !== null ? index : -1}); else console.error('guardar_pregunta no disponible');">${pr ? 'Guardar cambios' : 'Agregar pregunta'}</button>
            <button type="button" class="btn btn-secondary" onclick="if(window.detalle) detalle(); else console.error('detalle no disponible');">Cancelar</button>
        </div>
    `;
};

// helper para alternativa
const render_alternativa_html = (a) => {
    // a puede ser string o objeto {respuesta, id_alternativa, estado_alternativa}
    if (typeof a === 'string') {
        return `
            <div class="w-50 d-flex alter mb-2">
                <input type="text" class="form-control me-2" value="${escapeAttr(a)}">
                <button type="button" class="btn btn-sm btn-primary me-1 cl" onclick="marcar_correcta(this)"><i class="bi bi-check2"></i></button>
                <button type="button" class="btn btn-sm btn-danger" onclick="eliminar_alternativa(this)"><i class="bi bi-trash3-fill"></i></button>
            </div>
        `;
    } else {
        const text = a.respuesta || a.texto || '';
        const marcado = a.estado_alternativa == 1 ? 'btn-success' : 'btn-primary';
        const border = a.estado_alternativa == 1 ? 'border-success' : '';
        return `
            <div class="w-50 d-flex alter mb-2">
                <input type="text" class="form-control me-2 ${border}" value="${escapeAttr(text)}">
                <button type="button" class="btn btn-sm ${marcado} me-1 cl" onclick="marcar_correcta(this)"><i class="bi bi-check2"></i></button>
                <button type="button" class="btn btn-sm btn-danger" onclick="eliminar_alternativa(this)"><i class="bi bi-trash3-fill"></i></button>
            </div>
        `;
    }
};

// ---------- AGREGAR / GUARDAR PREGUNTA ----------
const guardar_pregunta = async (index) => {
    // index === -1 -> nueva pregunta; index >=0 editar existente
    const nombre = document.getElementById('nombre_pregunta')?.value?.trim() || '';
    const tipo = document.querySelector('input[name="tipo_pregunta"]:checked')?.value;
    const puntos = Number(document.getElementById('puntos')?.value || 0);
    const tiempo = Number(document.getElementById('tiempo')?.value || 0);

    if (!nombre) return Swal.fire('Error', 'La pregunta no puede estar vacía', 'error');
    if (!tipo) return Swal.fire('Error', 'Selecciona el tipo de pregunta', 'error');
    if (puntos <= 0) return Swal.fire('Error', 'Puntos debe ser mayor a 0', 'error');
    if (tiempo < 2) return Swal.fire('Error', 'Tiempo mínimo 2s', 'error');

    // construir alternativas
    let alternativas = [];
    let respuesta_correcta = '';

    if (tipo === 'VF') {
        // buscar botón VF con clase success
        const vfBtns = document.querySelectorAll('.alterantivas_form .btn');
        vfBtns.forEach(b => {
            if (b.classList.contains('btn-success') && b.textContent.trim()) {
                respuesta_correcta = b.textContent.trim();
            }
        });
        alternativas = ['Verdadero', 'Falso'];
    } else {
        const elems = document.querySelectorAll('.alterantivas_form .alter');
        let encontradaCorrecta = false;
        
        elems.forEach(el => {
            const input = el.querySelector('input');
            const btn = el.querySelector('button.cl');
            const val = input?.value?.trim() || '';
            
            if (val) {
                alternativas.push(val);
                // Verificar si esta alternativa está marcada como correcta
                // Verificar tanto el input (border-success) como el botón (btn-success)
                const esCorrecta = input?.classList.contains('border-success') || btn?.classList.contains('btn-success');
                if (esCorrecta && !encontradaCorrecta) {
                    respuesta_correcta = val;
                    encontradaCorrecta = true;
                    console.log('Respuesta correcta encontrada:', val);
                }
            }
        });
        
        // Debug: mostrar qué alternativas se encontraron
        console.log('Alternativas capturadas:', alternativas);
        console.log('Respuesta correcta capturada:', respuesta_correcta);
    }
    
    // Validar que se haya encontrado una respuesta correcta
    if (!respuesta_correcta && tipo === 'ALT') {
        return Swal.fire('Error', 'Debes marcar una alternativa como respuesta correcta. Haz clic en el botón ✓ verde de la alternativa correcta.', 'error');
    }

    if (tipo === 'ALT' && alternativas.length < 2) {
        return Swal.fire('Error', 'Agrega al menos 2 alternativas', 'error');
    }

    // confirmar
    const confirm = await Swal.fire({
        text: index >= 0 ? '¿Guardar cambios de la pregunta?' : '¿Agregar esta pregunta?',
        icon: 'question',
        showCancelButton: true,
        confirmButtonText: 'Sí',
        cancelButtonText: 'Cancelar'
    });
    if (!confirm.isConfirmed) return;

    // construir payload
    const payload = {
        id_formulario: cuerpo_json.detalle.id_formulario || cuerpo_json.detalle.id_cuestionario,
        nombre_pregunta: nombre,
        tipo_pregunta: tipo,
        alternativas: alternativas, // array de strings
        respuesta: respuesta_correcta,
        puntos: puntos,
        tiempo: tiempo
    };

    try {
        if (index >= 0 && cuerpo_json.preguntas[index] && cuerpo_json.preguntas[index].id_pregunta) {
            // editar -> PUT a endpoint de modificar pregunta
            const id = cuerpo_json.preguntas[index].id_pregunta;
            const resp = await fetch(`/fn_modificar_pregunta/${id}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            const data = await resp.json();
            if (data.estado) {
                // actualizar localmente (puedes usar la respuesta del servidor si devuelve el objeto actualizado)
                cuerpo_json.preguntas[index] = {
                    ...cuerpo_json.preguntas[index],
                    nombre_pregunta: nombre,
                    tipo_pregunta: tipo,
                    alternativas: alternativas,
                    respuesta: respuesta_correcta,
                    puntaje: puntos,
                    tiempo: tiempo
                };
                dibujar_preguntas();
                Swal.fire('Guardado', data.mensaje || 'Pregunta actualizada', 'success');
                // Volver al detalle después de guardar
                setTimeout(() => {
                    if (window.detalle) detalle();
                }, 1000);
            } else {
                Swal.fire('Error', data.mensaje || 'No se pudo actualizar la pregunta', 'error');
            }
        } else {
            // crear nueva -> POST a endpoint registrar pregunta
            const resp = await fetch('/registrar_pregunta', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            const data = await resp.json();
            if (data.estado) {
                // si server devuelve id, úsalo; sino agregamos sin id
                const nueva = {
                    id_pregunta: data.id_pregunta || null,
                    nombre_pregunta: nombre,
                    tipo_pregunta: tipo,
                    alternativas: alternativas,
                    respuesta: respuesta_correcta,
                    puntaje: puntos,
                    tiempo: tiempo
                };
                cuerpo_json.preguntas.push(nueva);
                dibujar_preguntas();
                Swal.fire('Creado', data.mensaje || 'Pregunta creada', 'success');
                // Volver al detalle después de guardar
                setTimeout(() => {
                    if (window.detalle) detalle();
                }, 1000);
            } else {
                Swal.fire('Error', data.mensaje || 'No se pudo crear la pregunta', 'error');
            }
        }
    } catch (err) {
        console.error('Error guardar pregunta:', err);
        Swal.fire('Error', 'Fallo de conexión con el servidor', 'error');
    }
};

// ---------- ELIMINAR PREGUNTA (actualizado para usar event) ----------
const eliminar_pr = async (event, id_pregunta, index) => {
    event.stopPropagation();
    if (!id_pregunta) {
        // si no tiene id en backend sólo borramos local
        cuerpo_json.preguntas.splice(index, 1);
        dibujar_preguntas();
        return;
    }

    const res = await Swal.fire({
        text: '¿Eliminar esta pregunta?',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: 'Sí, eliminar',
        cancelButtonText: 'Cancelar'
    });
    if (!res.isConfirmed) return;

    try {
        const respuesta = await fetch(`/fn_eliminar_pregunta/${id_pregunta}`, { method: 'DELETE' });
        const rpt = await respuesta.json();
        if (rpt.estado) {
            // quitar local
            const idx = cuerpo_json.preguntas.findIndex(p => p.id_pregunta == id_pregunta);
            if (idx >= 0) cuerpo_json.preguntas.splice(idx, 1);
            dibujar_preguntas();
            Swal.fire('Eliminado', rpt.mensaje || 'Pregunta eliminada', 'success');
        } else {
            Swal.fire('Error', rpt.mensaje || 'No se pudo eliminar', 'error');
        }
    } catch (err) {
        console.error('Error eliminar pregunta:', err);
        Swal.fire('Error', 'Fallo de conexión', 'error');
    }
};

// ---------- FUNCIONES DE UI (alternativas, VF, etc.) ----------
const agregar_alternativas = () => {
    const div_alt = document.querySelector(".alterantivas_form");
    if (!div_alt) return;
    div_alt.insertAdjacentHTML(
        "beforeend",
        `<div class="w-50 d-flex alter mb-2">
            <input type="text" class="form-control me-2" value="">
            <button type="button" class="btn btn-sm btn-primary me-1 cl" onclick="marcar_correcta(this)"><i class="bi bi-check2"></i></button>
            <button type="button" class="btn btn-sm btn-danger" onclick="eliminar_alternativa(this)"><i class="bi bi-trash3-fill"></i></button>
        </div>`
    );
};

const eliminar_alternativa = (btn) => {
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
    }).then((result) => {
        if (result.isConfirmed) {
            btn.closest('.alter')?.remove();
            Swal.fire({
                icon: 'success',
                title: 'Alternativa eliminada',
                timer: 1500,
                showConfirmButton: false
            });
        }
    });
};

const marcar_correcta = (btn) => {
    // marcador visual: poner btn-success y input con border-success
    const items = document.querySelectorAll('.alterantivas_form .alter');
    items.forEach(el => {
        const b = el.querySelector('button.cl');
        const inp = el.querySelector('input');
        if (b) { 
            b.classList.remove('btn-success'); 
            b.classList.add('btn-primary'); 
        }
        if (inp) {
            inp.classList.remove('border-success');
        }
    });
    
    // Marcar la alternativa seleccionada
    const alterDiv = btn.closest('.alter');
    if (alterDiv) {
        btn.classList.remove('btn-primary');
        btn.classList.add('btn-success');
        const input = alterDiv.querySelector('input');
        if (input) {
            input.classList.add('border-success');
            console.log('Alternativa marcada como correcta:', input.value);
        }
    }
};

const mostrar_VF = () => {
    const div_alt = document.querySelector(".alterantivas_form");
    if (!div_alt) return;
    div_alt.innerHTML = `
        <div class="d-flex gap-2">
            <button type="button" class="btn btn-outline-success btn-sm w-50" onclick="seleccionar_VF(this)">Verdadero</button>
            <button type="button" class="btn btn-outline-success btn-sm w-50" onclick="seleccionar_VF(this)">Falso</button>
        </div>
    `;
};

const seleccionar_VF = (btn) => {
    // quitar selected previo
    const btns = document.querySelectorAll('.alterantivas_form .btn');
    btns.forEach(b => { b.classList.remove('btn-success'); b.classList.add('btn-outline-success'); });
    btn.classList.remove('btn-outline-success'); btn.classList.add('btn-success');
};

const mostrar_ALT = () => {
    const div_alt = document.querySelector(".alterantivas_form");
    if (!div_alt) return;
    div_alt.innerHTML = ''; // listo para agregar alternativas
    document.getElementById('btn_add')?.classList.remove('d-none');
};

// ---------- FUNCIÓN PARA ELIMINAR IMAGEN ACTUAL (definida globalmente) ----------
window.eliminarImagenActual = async function() {
    const idFormulario = cuerpo_json.detalle.id_formulario;
    if (!idFormulario) {
        Swal.fire('Error', 'No se encontró el ID del cuestionario', 'error');
        return;
    }
    
    const result = await Swal.fire({
        title: '¿Eliminar imagen?',
        text: 'Esta acción eliminará la imagen del cuestionario. ¿Estás seguro?',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: 'Sí, eliminar',
        cancelButtonText: 'Cancelar',
        confirmButtonColor: '#d33',
        cancelButtonColor: '#6c757d'
    });
    
    if (result.isConfirmed) {
        try {
            Swal.fire({
                title: 'Eliminando imagen...',
                text: 'Por favor espera',
                allowOutsideClick: false,
                didOpen: () => {
                    Swal.showLoading();
                }
            });
            
            const response = await fetch(`/eliminar_imagen_cuestionario/${idFormulario}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            
            const data = await response.json();
            
            if (data.estado) {
                // Actualizar cuerpo_json localmente
                cuerpo_json.detalle.imagen_url = null;
                
                // Recargar los datos del cuestionario desde el backend para sincronizar
                try {
                    const datosResponse = await fetch(`/api_obtener_cuestionario_modificar/${idFormulario}`);
                    if (datosResponse.ok) {
                        const datosActualizados = await datosResponse.json();
                        console.log('[DEBUG] Datos actualizados del backend:', datosActualizados);
                        if (datosActualizados && datosActualizados.detalle) {
                            // Actualizar cuerpo_json con los datos actualizados del backend
                            const nuevaImagenUrl = datosActualizados.detalle.imagen_url;
                            console.log('[DEBUG] Nueva imagen_url del backend:', nuevaImagenUrl);
                            cuerpo_json.detalle.imagen_url = nuevaImagenUrl || null;
                            console.log('[DEBUG] cuerpo_json.detalle.imagen_url actualizado a:', cuerpo_json.detalle.imagen_url);
                        }
                    } else {
                        console.error('[DEBUG] Error al obtener datos actualizados:', datosResponse.status, datosResponse.statusText);
                    }
                } catch (e) {
                    console.error('[DEBUG] Error al recargar datos:', e);
                    // Si falla, mantener el valor null que ya establecimos
                }
                
                Swal.fire({
                    icon: 'success',
                    title: 'Imagen eliminada',
                    text: 'La imagen ha sido eliminada correctamente.',
                    timer: 1500,
                    showConfirmButton: false
                }).then(() => {
                    // Recargar el detalle para actualizar la vista
                    if (typeof detalle === 'function') {
                        detalle();
                    }
                });
            } else {
                Swal.fire('Error', data.mensaje || 'No se pudo eliminar la imagen', 'error');
            }
        } catch (error) {
            console.error('Error al eliminar imagen:', error);
            Swal.fire('Error', 'Error de conexión al eliminar la imagen', 'error');
        }
    }
};

// ---------- UTILIDADES ----------
function escapeHtml(text) {
    if (!text) return '';
    return text
        .toString()
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}
function escapeAttr(text) {
    return escapeHtml(text).replace(/"/g, '&quot;');
}

// ---------- FUNCIÓN PARA MOSTRAR DETALLE ----------
const detalle = () => {
    if (!contenido) return;
    contenido.innerHTML = `
        <h3 class="fw-bold mb-3">Paso 1: Detalle del formulario</h3>
        <p class="text-secondary separador mb-4">Define la información básica de tu formulario</p>
        
        <!-- Campo para subir/cambiar imagen del cuestionario -->
        <div class="mb-4">
            <label class="fw-bold mb-2">
                <i class="bi bi-image"></i>
                Imagen del cuestionario
                <i class="bi bi-info-circle text-primary ms-1" data-bs-toggle="tooltip" data-bs-placement="top" title="Opcional: Sube o cambia la imagen de tu cuestionario"></i>
            </label>
            <div class="mb-3">
                ${cuerpo_json.detalle.imagen_url ? `
                    <div class="mb-2" id="imagen_actual_container">
                        <p class="text-muted small mb-2">Imagen actual:</p>
                        <img src="/${cuerpo_json.detalle.imagen_url}" alt="Imagen actual" 
                             class="img-thumbnail" 
                             style="max-width: 200px; max-height: 150px; object-fit: contain; border-radius: 8px;">
                        <button type="button" id="btn_eliminar_imagen_actual" class="btn btn-sm btn-danger mt-2">
                            <i class="bi bi-trash"></i> Eliminar imagen
                        </button>
                    </div>
                ` : ''}
                <div class="d-flex align-items-center justify-content-center border rounded p-3" style="background-color: #f8f9fa; cursor: pointer;" onclick="document.getElementById('imagen_cuestionario').click()">
                    <div class="text-center">
                        <i class="bi bi-upload fs-3 mb-1 text-muted"></i>
                        <p class="text-muted mb-0 small">${cuerpo_json.detalle.imagen_url ? 'Cambiar imagen' : 'Subir una imagen (opcional)'}</p>
                        <p class="text-muted mb-0" style="font-size: 0.75rem;">JPG, PNG, GIF</p>
                    </div>
                </div>
                <input type="file" id="imagen_cuestionario" name="imagen_cuestionario" class="d-none" accept=".jpg,.jpeg,.png,.gif" onchange="previewImagenCuestionarioModificar(this)">
                <div id="preview_imagen_cuestionario" class="mt-2 d-none">
                    <p class="text-muted small mb-2">Nueva imagen seleccionada:</p>
                    <img id="img_preview_cuestionario" src="" alt="Vista previa" class="img-thumbnail" style="max-width: 200px; max-height: 150px;">
                    <button type="button" class="btn btn-sm btn-danger mt-2" onclick="eliminarImagenCuestionarioModificar()">
                        <i class="bi bi-trash"></i> Cancelar cambio
                    </button>
                </div>
            </div>
        </div>
        
        <div class="d-flex flex-wrap align-items-start gap-4">
            <div class="d-flex flex-column me-4" style="min-width: 300px;">
                <label for="nombre_cuestionario" class="fw-bold mb-2">
                    <i class="bi bi-pencil-square"></i>
                    Nombre del formulario
                    <span class="text-danger">*</span>
                </label>
                <input id="nombre_cuestionario" class="form-control mb-3" name="nombre_cuestionario" type="text"
                    placeholder="Ingrese el nombre del cuestionario" maxlength="200" required>
                
                <label for="tipo_cuestionario" class="fw-bold mb-2">
                    <i class="bi bi-info-circle"></i>
                    Tipo de formulario
                    <span class="text-danger">*</span>
                </label>
                <select class="form-select mb-3" name="tipo_cuestionario" id="tipo_cuestionario" required>
                    <option value="I" ${cuerpo_json.detalle.tipo_formulario === 'I' ? 'selected' : ''}>Individual - Cada estudiante juega solo</option>
                    <option value="G" ${cuerpo_json.detalle.tipo_formulario === 'G' ? 'selected' : ''}>Grupal - Los estudiantes forman equipos</option>
                </select>
                
                <label for="estado" class="fw-bold mb-2">
                    <i class="bi bi-check-circle"></i> Estado
                </label>
                <select id="estado" class="form-select mb-3" name="estado">
                    <option value="P" ${cuerpo_json.detalle.estado === 'P' ? 'selected' : ''}>Público</option>
                    <option value="R" ${cuerpo_json.detalle.estado === 'R' ? 'selected' : ''}>Privado</option>
                </select>
            </div>
            
            <div class="d-flex flex-column flex-grow-1">
                <label for="descripcion" class="fw-bold mb-2">
                    <i class="bi bi-card-text"></i>
                    Descripción del formulario
                </label>
                <textarea id="descripcion" class="form-control" name="descripcion" rows="7"
                    placeholder="Ingrese la descripción del cuestionario (opcional)" maxlength="1000">${escapeHtml(cuerpo_json.detalle.descripcion_formulario || '')}</textarea>
                <small class="text-muted">Caracteres: <span id="contador_descripcion">${(cuerpo_json.detalle.descripcion_formulario || '').length}</span>/1000</small>
            </div>
        </div>
        <div class="mb-1 mt-4">
            <button type="button" class="btn btn-warning w-100" onclick="if(window.modificar_detalle) modificar_detalle(); else console.error('modificar_detalle no disponible');">
                <i class="bi bi-save"></i> Modificar detalle
            </button>
        </div>
    `;
    
    // Actualizar referencias después de renderizar
    nombre_formulario = document.getElementById('nombre_cuestionario');
    ttipo_formulario = document.getElementById('tipo_cuestionario');
    estado_formulario = document.getElementById('estado');
    descripcion_formulario = document.getElementById('descripcion');
    
    // Llenar valores
    if (nombre_formulario) nombre_formulario.value = cuerpo_json.detalle.nombre_formulario;
    if (ttipo_formulario) ttipo_formulario.value = cuerpo_json.detalle.tipo_formulario;
    if (estado_formulario) estado_formulario.value = cuerpo_json.detalle.estado;
    if (descripcion_formulario) descripcion_formulario.value = cuerpo_json.detalle.descripcion_formulario;
    
    // Contador de caracteres
    const contador = document.getElementById('contador_descripcion');
    if (descripcion_formulario && contador) {
        descripcion_formulario.addEventListener('input', function() {
            contador.textContent = this.value.length;
        });
    }
    
    // Inicializar funciones de preview de imagen si no existen
    if (typeof window.previewImagenCuestionarioModificar === 'undefined') {
        window.previewImagenCuestionarioModificar = function(input) {
            if (input.files && input.files[0]) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    const imgPreview = document.getElementById('img_preview_cuestionario');
                    const previewDiv = document.getElementById('preview_imagen_cuestionario');
                    if (imgPreview) imgPreview.src = e.target.result;
                    if (previewDiv) previewDiv.classList.remove('d-none');
                };
                reader.readAsDataURL(input.files[0]);
            }
        };
    }
    
    if (typeof window.eliminarImagenCuestionarioModificar === 'undefined') {
        window.eliminarImagenCuestionarioModificar = function() {
            const imagenInput = document.getElementById('imagen_cuestionario');
            const previewDiv = document.getElementById('preview_imagen_cuestionario');
            if (imagenInput) imagenInput.value = '';
            if (previewDiv) previewDiv.classList.add('d-none');
        };
    }
    
    // Asegurar que el botón de eliminar imagen actual tenga el event listener correcto
    const btnEliminarImagen = document.getElementById('btn_eliminar_imagen_actual');
    if (btnEliminarImagen) {
        btnEliminarImagen.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            if (window.eliminarImagenActual) {
                window.eliminarImagenActual();
            } else {
                console.error('eliminarImagenActual no está disponible');
                Swal.fire('Error', 'La función para eliminar imagen no está disponible', 'error');
            }
        });
    }
};

// ---------- GUARDAR Y FINALIZAR (GUARDAR TODO Y RESETEAR) ----------
const guardar_y_finalizar = async () => {
    // Confirmar acción
    const confirm = await Swal.fire({
        title: '¿Guardar todos los cambios?',
        text: 'Se guardarán todos los cambios del cuestionario y se reseteará para reutilizarse desde cero.',
        icon: 'question',
        showCancelButton: true,
        confirmButtonText: 'Sí, guardar y finalizar',
        cancelButtonText: 'Cancelar',
        confirmButtonColor: '#28a745',
        cancelButtonColor: '#6c757d'
    });
    
    if (!confirm.isConfirmed) return;
    
    // Mostrar loading
    Swal.fire({
        title: 'Guardando cambios...',
        text: 'Por favor espera',
        allowOutsideClick: false,
        didOpen: () => {
            Swal.showLoading();
        }
    });
    
    try {
        // 1. Guardar el detalle del cuestionario
        cuerpo_json.detalle.nombre_formulario = nombre_formulario.value;
        cuerpo_json.detalle.tipo_formulario = ttipo_formulario.value;
        cuerpo_json.detalle.descripcion_formulario = descripcion_formulario.value;
        cuerpo_json.detalle.estado = estado_formulario.value;
        
        const respuestaDetalle = await fetch('/fn_modificar', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(cuerpo_json.detalle)
        });
        
        const rptDetalle = await respuestaDetalle.json();
        
        if (rptDetalle.estado !== true) {
            Swal.fire('Error', rptDetalle.mensaje || 'No se pudo guardar el detalle', 'error');
            return;
        }
        
        // 2. Resetear el estado del juego para que pueda reutilizarse
        const id_cuestionario = cuerpo_json.detalle.id_formulario || cuerpo_json.detalle.id_cuestionario;
        if (id_cuestionario) {
            const respuestaReset = await fetch(`/resetear_cuestionario/${id_cuestionario}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' }
            });
            
            const rptReset = await respuestaReset.json();
            
            if (rptReset.estado !== true) {
                console.warn('No se pudo resetear el cuestionario, pero los cambios se guardaron');
            }
        }
        
        // 3. Mostrar éxito y redirigir
        Swal.fire({
            icon: 'success',
            title: '¡Guardado exitosamente!',
            text: 'Todos los cambios se han guardado. El cuestionario está listo para reutilizarse.',
            confirmButtonText: 'Ir a mis cuestionarios',
            timer: 2000,
            timerProgressBar: true
        }).then(() => {
            window.location.href = '/dashboard';
        });
        
    } catch (err) {
        console.error('Error al guardar y finalizar:', err);
        Swal.fire('Error', 'Fallo de conexión al guardar los cambios', 'error');
    }
};

// ---------- EXPONER FUNCIONES GLOBALMENTE ----------
window.modificar_detalle = modificar_detalle;
window.agg_pr = agg_pr;
window.detalle = detalle;
window.mostrar_pregunta = mostrar_pregunta;
window.guardar_pregunta = guardar_pregunta;
window.eliminar_pr = eliminar_pr;
window.agregar_alternativas = agregar_alternativas;
window.eliminar_alternativa = eliminar_alternativa;
window.marcar_correcta = marcar_correcta;
window.mostrar_VF = mostrar_VF;
window.mostrar_ALT = mostrar_ALT;
window.seleccionar_VF = seleccionar_VF;
window.guardar_y_finalizar = guardar_y_finalizar;
