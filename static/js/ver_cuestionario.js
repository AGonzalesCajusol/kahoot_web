const contenido = document.querySelector(".cont_formulario");

const cuerpo_json = {
    detalle: {
        nombre_formulario: "",
        tipo_formulario: "",
        descripcion_formulario: "",
        estado: "",
    },
    preguntas: [],
};

// GUARDAR DETALLE DEL FORMULARIO
const guardar_detalle = (ss) => {
    const nombre_cuestionario = document.getElementById("nombre_cuestionario");
    const tipo_formulario = document.getElementById("tipo_cuestionario");
    const descripcion_formulario = document.getElementById("descripcion");
    const estado = document.getElementById("estado");

    cuerpo_json.detalle.nombre_formulario = nombre_cuestionario.value;
    cuerpo_json.detalle.tipo_formulario = tipo_formulario.value;
    cuerpo_json.detalle.descripcion_formulario = descripcion_formulario.value;
    cuerpo_json.detalle.estado = estado.value;

    contenido.innerHTML = '';

    if (!ss) {
        agg_pr();
    }

    Swal.fire({
        icon: 'success',
        title: 'Detalle Guardado',
        text: 'El detalle del formulario ha sido guardado correctamente.'
    });
    console.log("Detalle JSON:", cuerpo_json);
};

// CARGAR DETALLE DEL FORMULARIO
const detalle = () => {
    contenido.innerHTML = `
        <h3 class="fw-bold mb-3">Paso 1: Detalle del formulario</h3>
        <p class="text-secondary separador mb-4">Define la información básica de tu nuevo formulario</p>
        <div class="d-flex flex-wrap align-items-start gap-4">
            <div class="d-flex flex-column me-4" style="min-width: 300px;">
                <label for="nombre_cuestionario" class="fw-bold mb-2">
                    <i class="bi bi-pencil-square"></i> Nombre del formulario
                </label>
                <input value="${cuerpo_json.detalle.nombre_formulario}" id="nombre_cuestionario" class="form-control mb-3" type="text" placeholder="Ingrese el nombre del cuestionario">
                
                <label for="tipo_cuestionario" class="fw-bold mb-2">
                    <i class="bi bi-info-circle"></i> Tipo de formulario
                </label>
                <select class="form-select mb-3" id="tipo_cuestionario">
                    <option value="" disabled ${cuerpo_json.detalle.tipo_formulario === "" ? "selected" : ""}>Seleccione una opción</option>
                    <option value="I" ${cuerpo_json.detalle.tipo_formulario === "I" ? "selected" : ""}>Individual</option>
                    <option value="G" ${cuerpo_json.detalle.tipo_formulario === "G" ? "selected" : ""}>Grupal</option>
                </select>
            </div>
            <div class="d-flex flex-column flex-grow-1">
                <label for="descripcion" class="fw-bold mb-2">
                    <i class="bi bi-card-text"></i> Descripción del formulario
                </label>
                <textarea id="descripcion" class="form-control" rows="7">${cuerpo_json.detalle.descripcion_formulario}</textarea>

                <label for="estado" class="fw-bold mb-2">
                    <i class="bi bi-check-circle"></i> Estado
                </label>
                <select id="estado" class="form-select mb-3">
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
            ` : `
                <button type="button" class="btn btn-primary w-100" onclick="guardar_detalle('si')">
                    <i class="bi bi-save"></i> Guardar detalle
                </button>
            `}
        </div>
    `;
};

// AGREGAR NUEVA PREGUNTA
const agg_pr = () => {
    contenido.innerHTML = `
        <div class="d-flex align-items-center mb-3">
            <i class="bi bi-question-circle-fill fs-2 text-primary me-2"></i>
            <h3 class="fw-bold mb-0">Paso 2: Agregar preguntas</h3>
        </div>
        <p class="text-secondary separador mb-4"><i class="bi bi-info-circle me-1"></i>Añade las preguntas que conformarán tu formulario</p>
        <div class="mb-3">
            <div class="d-flex align-items-center justify-content-center">
                <div class="subir btn btn-outline-secondary d-flex flex-column align-items-center" onclick="document.getElementById('archivo_pregunta').click()" style="cursor:pointer;">
                    <i class="bi bi-upload fs-3 mb-1"></i>
                    <span class="fs-6">Puedes subir videos o imágenes</span>
                </div>
                <input type="file" id="archivo_pregunta" class="d-none" accept=".mp3, .jpg, .jpeg, .png">
            </div>
        </div>
        <div class="mb-3">
            <label for="nombre_pregunta" class="fw-bold"><i class="bi bi-pencil-square me-1"></i>Pregunta:</label>
            <input type="text" class="form-control mt-2" id="nombre_pregunta" placeholder="¿Cuál es tu pregunta?">
        </div>
        <div class="row mb-3">
            <div class="col-md-3">
                <div class="mt-2" role="radiogroup" aria-labelledby="tipo_pregunta_label">
                    <span id="tipo_pregunta_label" class="fw-bold"><i class="bi bi-list-check me-1"></i>Tipo pregunta:</span>
                    <div class="form-check mt-2">
                        <input class="form-check-input" type="radio" name="tipo_pregunta" id="verdadero_falso" value="VF" onclick="VF()">
                        <label class="form-check-label" for="verdadero_falso">
                            <i class="bi bi-check2-square me-1"></i>(Verdadero / Falso)
                        </label>
                    </div>
                    <div class="form-check mt-1">
                        <input class="form-check-input" type="radio" name="tipo_pregunta" id="alternativas" value="ALT" onclick="ALT()">
                        <label class="form-check-label" for="alternativas">
                            <i class="bi bi-ui-checks-grid me-1"></i>(Alternativas)
                        </label>
                    </div>
                </div>
            </div>
            <div class="col-md-4">
                <label for="puntos" class="fw-bold mt-2"><i class="bi bi-star-fill text-warning me-1"></i>Puntos:</label>
                <input type="number" class="form-control mt-2" id="puntos" placeholder="Valor de la pregunta" min="0" required>
            </div>
            <div class="col-md-4">
                <label for="tiempo" class="fw-bold mt-2"><i class="bi bi-clock-fill text-primary me-1"></i>Tiempo:</label>
                <input type="number" class="form-control mt-2" id="tiempo" placeholder="Tiempo (segundos)" min="2" required>
            </div>
        </div>
        <div class="mb-3">
            <label class="form-check-label fw-bold" for="alternativas">
                <i class="bi bi-list-ol me-1"></i>Alternativas: 
                <button type="button" onclick="agregar_alternativas()" class="btn btn-outline-success btn-sm d-none" id="btn_add">
                    <i class="bi bi-plus-circle"></i>
                </button>
            </label>
            <div class="alterantivas_form mt-2"></div>
        </div>
        <div>
            <button type="button" class="btn btn-primary w-100" onclick="guardar_pregunta()"> Guardar pregunta</button>
        </div>
    `;
};

// MODIFICAR PREGUNTA
const cargar_pregunta_modificar = (indice) => {
    const pr = cuerpo_json.preguntas[indice];
    let alt = '';

    if (pr.tipo_pregunta === "VF") {
        alt = `
            <button type="button" class="btn ${pr.respuesta == 'Verdadero' ? 'btn-success' : 'btn-outline-success'} btn-sm w-50" onclick="select(this)"> Verdadero </button>
            <button type="button" class="btn ${pr.respuesta == 'Falso' ? 'btn-success' : 'btn-outline-success'} btn-sm w-50" onclick="select(this)"> Falso </button>
        `;
    } else {
        pr.alternativas.forEach(a => {
            alt += `
                <div class="w-50 d-flex alter">
                    <input type="text" class="form-control me-2 ${a === pr.respuesta ? 'border-success' : ''}" value="${a}">
                    <button type="button" class="btn btn-sm ${a === pr.respuesta ? 'btn-success' : 'btn-primary'} me-1 cl" onclick="sl(this)"><i class="bi bi-check2"></i></button>
                    <button type="button" class="btn btn-sm btn-danger" onclick="eliminar_alternativa(this)"><i class="bi bi-trash3-fill"></i></button>
                </div>
            `;
        });
    }

    contenido.innerHTML = `
        <div class="d-flex align-items-center mb-3">
            <i class="bi bi-question-circle-fill fs-2 text-primary me-2"></i>
            <h3 class="fw-bold mb-0">Paso 2: Modificar pregunta</h3>
        </div>
        <p class="text-secondary separador mb-4"><i class="bi bi-info-circle me-1"></i>Edita la pregunta existente</p>
        <div class="mb-3">
            <div class="d-flex align-items-center justify-content-center">
                <div class="subir btn btn-outline-secondary d-flex flex-column align-items-center" onclick="document.getElementById('archivo_pregunta').click()" style="cursor:pointer;">
                    <i class="bi bi-upload fs-3 mb-1"></i>
                    <span class="fs-6">Puedes subir videos o imágenes</span>
                </div>
                <input type="file" id="archivo_pregunta" class="d-none" accept=".mp3, .jpg, .jpeg, .png">
            </div>
        </div>
        <div class="mb-3">
            <label for="nombre_pregunta" class="fw-bold"><i class="bi bi-pencil-square me-1"></i>Pregunta:</label>
            <input type="text" class="form-control mt-2" id="nombre_pregunta" value="${pr.nombre_pregunta}">
        </div>
        <div class="row mb-3">
            <div class="col-md-3">
                <div class="mt-2" role="radiogroup" aria-labelledby="tipo_pregunta_label">
                    <span id="tipo_pregunta_label" class="fw-bold"><i class="bi bi-list-check me-1"></i>Tipo pregunta:</span>
                    <div class="form-check mt-2">
                        <input class="form-check-input" type="radio" name="tipo_pregunta" id="verdadero_falso" value="VF" onclick="VF()" ${pr.tipo_pregunta === 'VF' ? 'checked' : ''}>
                        <label class="form-check-label" for="verdadero_falso">(Verdadero / Falso)</label>
                    </div>
                    <div class="form-check mt-1">
                        <input class="form-check-input" type="radio" name="tipo_pregunta" id="alternativas" value="ALT" onclick="ALT()" ${pr.tipo_pregunta === 'ALT' ? 'checked' : ''}>
                        <label class="form-check-label" for="alternativas">(Alternativas)</label>
                    </div>
                </div>
            </div>
            <div class="col-md-4">
                <label class="fw-bold mt-2">Puntos:</label>
                <input type="number" class="form-control mt-2" id="puntos" value="${pr.puntos}" min="0" required>
            </div>
            <div class="col-md-4">
                <label class="fw-bold mt-2">Tiempo (segundos):</label>
                <input type="number" class="form-control mt-2" id="tiempo" value="${pr.tiempo}" min="2" required>
            </div>
        </div>
        <div class="mb-3">
            <label class="form-check-label fw-bold">Alternativas:
                <button type="button" onclick="agregar_alternativas()" class="btn btn-outline-success btn-sm ${pr.tipo_pregunta==='ALT'?'':'d-none'}" id="btn_add">
                    <i class="bi bi-plus-circle"></i>
                </button>
            </label>
            <div class="alterantivas_form mt-2">${alt}</div>
        </div>
        <div>
            <button type="button" class="btn btn-warning w-100" onclick="guardar_pregunta(${indice})">Modificar pregunta</button>
        </div>
    `;
};

// FUNCIONES AUXILIARES
const ALT = () => {
    document.getElementById("btn_add").classList.remove("d-none");
    document.querySelector(".alterantivas_form").innerHTML = "";
};

const agregar_alternativas = () => {
    const div_alt = document.querySelector(".alterantivas_form");
    div_alt.insertAdjacentHTML("beforeend", `
        <div class="w-50 d-flex alter">
            <input type="text" class="form-control me-2">
            <button type="button" class="btn btn-sm btn-primary me-1 cl" onclick="sl(this)"><i class="bi bi-check2"></i></button>
            <button type="button" class="btn btn-sm btn-danger" onclick="eliminar_alternativa(this)"><i class="bi bi-trash3-fill"></i></button>
        </div>
    `);
};

const eliminar_alternativa = (btn) => {
    btn.closest(".alter").remove();
};

const VF = () => {
    document.querySelector(".alterantivas_form").innerHTML = `
        <button type="button" class="btn btn-outline-success btn-sm w-50" onclick="select(this)">Verdadero</button>
        <button type="button" class="btn btn-outline-success btn-sm w-50" onclick="select(this)">Falso</button>
    `;
};

const select = (btn) => {
    const hermanos = btn.parentNode.children;
    Array.from(hermanos).forEach(h => h.classList.remove("btn-success"));
    btn.classList.add("btn-success");
};

const sl = (btn) => {
    const hermanos = btn.parentNode.parentNode.querySelectorAll(".cl");
    hermanos.forEach(h => h.classList.remove("btn-success"));
    btn.classList.add("btn-success");
};

// GUARDAR PREGUNTA NUEVA O MODIFICADA
const guardar_pregunta = (indice) => {
    const nombre_pregunta = document.getElementById("nombre_pregunta").value;
    const puntos = parseInt(document.getElementById("puntos").value);
    const tiempo = parseInt(document.getElementById("tiempo").value);
    const tipo_pregunta = document.querySelector('input[name="tipo_pregunta"]:checked').value;

    let pregunta = {
        nombre_pregunta,
        puntos,
        tiempo,
        tipo_pregunta,
        alternativas: [],
        respuesta: ""
    };

    if (tipo_pregunta === "VF") {
        const btn_res = document.querySelector(".alterantivas_form .btn-success");
        if (!btn_res) {
            Swal.fire({icon:'error', title:'Error', text:'Debe seleccionar la respuesta'}); return;
        }
        pregunta.respuesta = btn_res.textContent.trim();
    } else {
        const inputs = document.querySelectorAll(".alterantivas_form input");
        inputs.forEach(input => pregunta.alternativas.push(input.value));
        const btn_res = document.querySelector(".alterantivas_form .btn-success");
        if (!btn_res) {
            Swal.fire({icon:'error', title:'Error', text:'Debe seleccionar la respuesta'}); return;
        }
        pregunta.respuesta = btn_res.previousElementSibling ? btn_res.previousElementSibling.value : "";
    }

    if (indice !== undefined) {
        cuerpo_json.preguntas[indice] = pregunta;
        Swal.fire({icon:'success', title:'Pregunta modificada'});
    } else {
        cuerpo_json.preguntas.push(pregunta);
        Swal.fire({icon:'success', title:'Pregunta agregada'});
    }

    console.log("Preguntas JSON:", cuerpo_json.preguntas);
    agg_pr();
};
