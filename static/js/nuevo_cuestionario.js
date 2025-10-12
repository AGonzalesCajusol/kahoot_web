const contenido = document.querySelector(".cont_formulario");

const cuerpo_json = {
    detallle: {
        nombre_cuestionario: "",
        tipo_formulario: "",
        descripcion_formulario: "",
        estado: "",
        pin: "",
        fecha_programacion: ""
    },
    preguntas: [],
};

const guardar_detalle = () => {
    const nombre_cuestionario = document.getElementById("nombre_cuestionario");
    const tipo_formulario = document.getElementById("tipo_cuestionario");
    const descripcion_formulario = document.getElementById("descripcion");
    const estado = document.getElementById("estado");
    const pin_f  = document.getElementById('pin');
    const f_pro = document.getElementById('fecha_programacion');

    cuerpo_json.detallle.nombre_cuestionario = nombre_cuestionario.value;
    cuerpo_json.detallle.tipo_formulario = tipo_formulario.value;
    cuerpo_json.detallle.descripcion_formulario = descripcion_formulario.value;
    cuerpo_json.detallle.estado = estado.value;
    cuerpo_json.detallle.pin = pin_f.value;
    cuerpo_json.detallle.fecha_programacion = f_pro.value;


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
                <input type="file" id="archivo_pregunta" name="archivo_pregunta" class="d-none" accept=".mp3, .jpg, .jpeg, .png">
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
                <input type="number" class="form-control mt-2" name="puntos" id="puntos" placeholder="Valor de la pregunta" min="0" required>
            </div>
            <div class="col-md-4">
                <label for="tiempo" class="fw-bold mt-2"><i class="bi bi-clock-fill text-primary me-1"></i>Tiempo:</label>
                <input type="number" class="form-control mt-2" name="tiempo" id="tiempo" placeholder="Tiempo (segundos)" min="2" required>
            </div>
        </div>
        <div class="mb-3">
            <label class="form-check-label fw-bold" for="alternativas"><i class="bi bi-list-ol me-1"></i>Alternativas: <button type="button" onclick="agregar_alternativas()" class="btn btn-outline-success btn-sm d-none" id="btn_add"><i class="bi bi-plus-circle"></i></button></label>
            <div class="alterantivas_form mt-2 ">
    
            </div>
        </div>
        <div >
            <button type="button" class="btn btn-primary w-100" onclick="guardar_pregunta()"> Guardar pregunta</button>
        </div>
    `;
};

const detalle = () => {
    contenido.innerHTML = `
            <h3 class="fw-bold mb-3">Paso 1: Detalle del formulario</h3>
            <p class="text-secondary separador mb-4">Define la información básica de tu nuevo formulario</p>
            <div class="d-flex flex-wrap align-items-start gap-4">
                <div class="d-flex flex-column me-4" style="min-width: 300px;">
                    <label for="nombre_cuestionario" class="fw-bold mb-2">
                        <i class="bi bi-pencil-square"></i>
                        Nombre del formulario
                    </label>
                    <input value ="${cuerpo_json.detallle.nombre_cuestionario}" id="nombre_cuestionario" class="form-control mb-3" name="nombre_cuestionario" type="text" placeholder="Ingrese el nombre del cuestionario" >
                
                    <label for="tipo_cuestionario" class="fw-bold mb-2">
                        <i class="bi bi-info-circle"></i>
                        Tipo de formulario
                    </label>
                    <select class="form-select mb-3" name="tipo_cuestionario" id="tipo_cuestionario">
                        <option value="" disabled ${cuerpo_json.detallle.tipo_formulario === ""? "selected" : "" }>Seleccione una opción</option>
                        <option value="I" ${cuerpo_json.detallle.tipo_formulario === "I" ? "selected" : "" }>Individual</option>
                        <option value="G" ${cuerpo_json.detallle.tipo_formulario === "G"? "selected" : "" }>Grupal</option>
                    </select>

                    <label for="pin" class="fw-bold mb-2">
                        <i class="bi bi-key"></i> PIN
                    </label>
                    <input id="pin" value="${cuerpo_json.detallle.pin}" class="form-control mb-3" name="pin" type="text" placeholder="PIN automático" readonly />

                    <label for="fecha_programacion" class="fw-bold mb-2">
                        <i class="bi bi-calendar"></i> Fecha de Programación
                    </label>
                    <input id="fecha_programacion" value="${cuerpo_json.detallle.fecha_programacion}"   class="form-control mb-3" name="fecha_programacion" type="datetime-local" />
                     
                </div>

                <div class="d-flex flex-column flex-grow-1">
                    <label for="descripcion" class="fw-bold mb-2">
                        <i class="bi bi-card-text"></i>
                        Descripción del formulario
                    </label>
                    <textarea  id="descripcion" class="form-control" name="descripcion" rows="7" placeholder="Ingrese la descripción del cuestionario" >${cuerpo_json.detallle.descripcion_formulario}</textarea>

                    <label for="estado" class="fw-bold mb-2">
                        <i class="bi bi-check-circle"></i> Estado
                    </label>
                    <select id="estado" class="form-select mb-3" name="estado">
                        <option value="P" ${cuerpo_json.detallle.estado === "P" ? "selected" : "" }>Público</option>
                        <option value="R" ${cuerpo_json.detallle.estado === "R" ? "selected" : "" }>Privado</option>
                    </select>   
                </div>

                
            </div>
            <div class="mb-1 mt-4">
                <button type="button" class="btn btn-primary w-100" onclick="guardar_detalle()">
                    <i class="bi bi-save"></i> Guardar detalle
                </button>
            </div>
    `;
};

const pregunta = (elemento) => {
    contenido.innerHTML = `

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
    elemento.parentElement.remove();
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
                <input type="file" id="archivo_pregunta" name="archivo_pregunta" class="d-none" accept=".mp3, .jpg, .jpeg, .png">
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
                <input type="number" class="form-control mt-2" name="puntos" id="puntos" placeholder="Valor de la pregunta" min="0" required>
            </div>
            <div class="col-md-4">
                <label for="tiempo" class="fw-bold mt-2"><i class="bi bi-clock-fill text-primary me-1"></i>Tiempo:</label>
                <input type="number" class="form-control mt-2" name="tiempo" id="tiempo" placeholder="Tiempo (segundos)" min="2" required>
            </div>
        </div>
        <div class="mb-3">
            <label class="form-check-label fw-bold" for="alternativas"><i class="bi bi-list-ol me-1"></i>Alternativas: <button type="button" onclick="agregar_alternativas()" class="btn btn-outline-success btn-sm d-none" id="btn_add"><i class="bi bi-plus-circle"></i></button></label>
            <div class="alterantivas_form mt-2 ">
    
            </div>
        </div>
        <div >
            <button type="button" class="btn btn-primary w-100" onclick="guardar_pregunta()"> Guardar pregunta</button>
        </div>
    `;
};
const guardar_pregunta = () => {
    const nombre_pregunta = document.getElementById("nombre_pregunta").value;
    const arc = document.getElementById('archivo_pregunta').files[0] ?  document.getElementById('archivo_pregunta').files[0] : '';
    const tipo_pregunta = document.querySelector(
        'input[name="tipo_pregunta"]:checked'
    ).value;
    const puntos = document.getElementById("puntos").value;
    const tiempo = document.getElementById("tiempo").value;
    const al = [];
    var rpt = "";
    if (tipo_pregunta == "VF") {
        al.push("Verdadero");
        al.push("Falso");
        const ed = document.querySelector(".alterantivas_form .btn.btn-success");
        rpt = ed.textContent;
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
    const pr = {
        nombre_pregunta: nombre_pregunta,
        tipo_pregunta: tipo_pregunta,
        archivo : arc,
        puntos: puntos,
        tiempo: tiempo,
        alternativas: al,
        respuesta: rpt.trim(),
    };

    cuerpo_json.preguntas.push(pr);

    //renderizamos contenido
    contenido.innerHTML = "";
    const cards_continue = document.querySelector(".cards_continue");
    cards_continue.innerHTML = "";
    cuerpo_json.preguntas.forEach((pregunta) => {
        cards_continue.innerHTML += `
            <div class="detalle_inicial card shadow-lg p-3 enfocar mt-2" id="detalle_card" onclick="pregunta(this)">
                <div class="row">
                    <div class="col-9">
                    <p class="text-secondary texto_pregunta">Pregunta ${cuerpo_json.preguntas.indexOf(pregunta) + 1 }: </p> 
                    <p class="name_cuestion">
                        ${pregunta.nombre_pregunta}
                    </p>
                    </div>
                    <div class="col-2">
                        <button onclick="eliminar_pr(this, ${cuerpo_json.preguntas.indexOf(pregunta)})" class="btn btn-danger rounded-circle " style="width: 2.5rem; height: 2.5rem;"><i class="bi bi-trash3 fs-9"></i></button>
                    </div>
                </div>
            </div>
        `;
    });
};


const pin = () =>{
    var numero =  Math.floor(10000 + Math.random() * 90000);
    document.getElementById('pin').value = numero;
    cuerpo_json.detallle.pin = numero

}
pin();


const eliminar_pr = (el, indice) =>{
    const cc = el.parentElement.parentElement.parentElement;
    cc.remove();
    cuerpo_json.preguntas.splice(indice, 1); 
    const enumeracion = document.querySelectorAll('.texto_pregunta');
    enumeracion.forEach((enu, index) => {  
        enu.textContent = `Pregunta ${index+1}:`
    });

}
