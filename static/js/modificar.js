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

    // Normalizar preguntas: si backend envía alternativas como string JSON, parsear
    cuerpo_json.preguntas = (respuestas || []).map(r => {
        const cop = { ...r };
        if (cop.alternativas && typeof cop.alternativas === 'string') {
            try { cop.alternativas = JSON.parse(cop.alternativas); }
            catch (e) { cop.alternativas = []; }
        }
        // nombres distintos posible: normalizar a nombre_pregunta / pregunta
        cop.nombre_pregunta = cop.nombre_pregunta || cop.pregunta || "";
        cop.puntaje = cop.puntaje || cop.puntos || 0;
        cop.tiempo = cop.tiempo || cop.tiempo_respuesta || 0;
        cop.respuesta = cop.respuesta || cop.respuesta_correcta || "";
        cop.id_pregunta = cop.id_pregunta || cop.id || null;
        return cop;
    });

    llenar_detalle();
};

const llenar_detalle = () => {
    nombre_formulario.value = cuerpo_json.detalle.nombre_formulario;
    descripcion_formulario.value = cuerpo_json.detalle.descripcion_formulario;
    ttipo_formulario.value = cuerpo_json.detalle.tipo_formulario;
    estado_formulario.value = cuerpo_json.detalle.estado;
    dibujar_preguntas();
};

// ---------- MODIFICAR DETALLE ----------
const fn_modificardetalle = async () => {
    cuerpo_json.detalle.nombre_formulario = nombre_formulario.value;
    cuerpo_json.detalle.tipo_formulario = ttipo_formulario.value;
    cuerpo_json.detalle.descripcion_formulario = descripcion_formulario.value;
    cuerpo_json.detalle.estado = estado_formulario.value;

    try {
        const respuesta = await fetch('/fn_modificar', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(cuerpo_json.detalle)
        });
        const rpt = await respuesta.json();

        if (rpt.estado === true) {
            Swal.fire('Éxito', rpt.mensaje || 'Formulario modificado correctamente', 'success');
            // opcional: actualizar id si backend devuelve algo
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
    const alternativas = pr ? (Array.isArray(pr.alternativas) ? pr.alternativas : (pr.alternativas ? pr.alternativas : [])) : [];

    // construir HTML del formulario de pregunta
    contenido.innerHTML = `
        <div class="d-flex align-items-center mb-3">
            <i class="bi bi-question-circle-fill fs-2 text-primary me-2"></i>
            <h3 class="fw-bold mb-0">${pr ? 'Editar pregunta' : 'Agregar pregunta'}</h3>
        </div>

        <div class="mb-3">
            <div class="d-flex align-items-center justify-content-center">
                <div class="subir btn btn-outline-secondary d-flex flex-column align-items-center" onclick="document.getElementById('archivo_pregunta').click()" style="cursor:pointer;">
                    <i class="bi bi-upload fs-3 mb-1"></i>
                    <span class="fs-6">Puedes subir un archivo (opcional)</span>
                </div>
                <input type="file" id="archivo_pregunta" name="archivo_pregunta" class="d-none" accept=".mp3, .jpg, .jpeg, .png">
            </div>
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
            <button class="btn ${pr ? 'btn-warning' : 'btn-primary'}" onclick="guardar_pregunta(${index !== null ? index : -1})">${pr ? 'Guardar cambios' : 'Agregar pregunta'}</button>
            <button class="btn btn-secondary" onclick="detalle()">Cancelar</button>
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
        elems.forEach(el => {
            const val = el.querySelector('input')?.value?.trim() || '';
            if (val) alternativas.push(val);
            if (el.querySelector('input')?.classList.contains('border-success')) {
                respuesta_correcta = val;
            }
        });
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
        id_formulario: cuerpo_json.detalle.id_formulario,
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
                detalle(); // volver al detalle o a la lista
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
                detalle(); // regresar a pantalla principal o lo que prefieras
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
    btn.closest('.alter')?.remove();
};

const marcar_correcta = (btn) => {
    // marcador visual: poner btn-success y input con border-success
    const items = document.querySelectorAll('.alterantivas_form .alter');
    items.forEach(el => {
        const b = el.querySelector('button.cl');
        const inp = el.querySelector('input');
        if (b) { b.classList.remove('btn-success'); b.classList.add('btn-primary'); }
        if (inp) inp.classList.remove('border-success');
    });
    btn.classList.remove('btn-primary');
    btn.classList.add('btn-success');
    btn.closest('.alter').querySelector('input')?.classList.add('border-success');
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
