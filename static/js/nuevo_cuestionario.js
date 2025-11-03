const contenido = document.querySelector(".cont_formulario");

const cuerpo_json = {
    detalle: {
        nombre_cuestionario: "",
        tipo_formulario: "",
        descripcion_formulario: "",
        estado: "",
        pin: ""
    },
    preguntas: [],
};

const guardar_detalle = (ss) => {
    const nombre_cuestionario = document.getElementById("nombre_cuestionario");
    const tipo_formulario = document.getElementById("tipo_cuestionario");
    const descripcion_formulario = document.getElementById("descripcion");
    const estado = document.getElementById("estado");
    const pin_f = document.getElementById('pin');

    

    cuerpo_json.detalle.nombre_cuestionario = nombre_cuestionario.value;
    cuerpo_json.detalle.tipo_formulario = tipo_formulario.value;
    cuerpo_json.detalle.descripcion_formulario = descripcion_formulario.value;
    cuerpo_json.detalle.estado = estado.value;
    cuerpo_json.detalle.pin = pin_f.value;    
    contenido.innerHTML = '';
    if (!ss) {
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
    Swal.fire({
        icon: 'success',
        title: 'Detalle Guardado',
        text: 'El detalle del formulario ha sido guardado correctamente.'
    });
    console.log("1", cuerpo_json);
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
                    <input value ="${cuerpo_json.detalle.nombre_cuestionario}" id="nombre_cuestionario" class="form-control mb-3" name="nombre_cuestionario" type="text" placeholder="Ingrese el nombre del cuestionario" >
                
                    <label for="tipo_cuestionario" class="fw-bold mb-2">
                        <i class="bi bi-info-circle"></i>
                        Tipo de formulario
                    </label>
                    <select class="form-select mb-3" name="tipo_cuestionario" id="tipo_cuestionario">
                        <option value="" disabled ${cuerpo_json.detalle.tipo_formulario === "" ? "selected" : ""}>Seleccione una opción</option>
                        <option value="I" ${cuerpo_json.detalle.tipo_formulario === "I" ? "selected" : ""}>Individual</option>
                        <option value="G" ${cuerpo_json.detalle.tipo_formulario === "G" ? "selected" : ""}>Grupal</option>
                    </select>

                    <label for="pin" class="fw-bold mb-2">
                        <i class="bi bi-key"></i> PIN
                    </label>
                    <input id="pin" value="${cuerpo_json.detalle.pin}" class="form-control mb-3" name="pin" type="text" placeholder="PIN automático" readonly />

                                    
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
                ${cuerpo_json.detalle.nombre_cuestionario ? `
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
                <input type="file" value="${pr.archivo}" id="archivo_pregunta" name="archivo_pregunta" class="d-none" accept=".mp3, .jpg, .jpeg, .png">
            </div>
        </div>
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
const guardar_pregunta = (ss) => {
    // Obtener los valores de los campos
    const nombre_pregunta = document.getElementById("nombre_pregunta").value;
    const arc = document.getElementById('archivo_pregunta').files[0] ? document.getElementById('archivo_pregunta').files[0] : '';
    const tipo_pregunta = document.querySelector('input[name="tipo_pregunta"]:checked')?.value;
    const puntos = document.getElementById("puntos").value;
    const tiempo = document.getElementById("tiempo").value;

    // Verificar si el campo de pregunta está vacío
    if (!nombre_pregunta.trim()) {
        Swal.fire({
            icon: 'error',
            title: '¡Error!',
            text: 'El campo de la pregunta no puede estar vacío.'
        });
        return;
    }

    // Verificar si el tipo de pregunta no está seleccionado
    if (!tipo_pregunta) {
        Swal.fire({
            icon: 'error',
            title: '¡Error!',
            text: 'Por favor, selecciona el tipo de pregunta.'
        });
        return;
    }

    // Verificar que el valor de los puntos sea mayor que 0
    if (!puntos || puntos <= 0) {
        Swal.fire({
            icon: 'error',
            title: '¡Error!',
            text: 'El valor de los puntos debe ser mayor que 0.'
        });
        return;
    }

    // Verificar que el tiempo sea al menos 2 segundos
    if (!tiempo || tiempo < 2) {
        Swal.fire({
            icon: 'error',
            title: '¡Error!',
            text: 'El tiempo debe ser al menos de 2 segundos.'
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
    }).then((result) => {
        if (result.isConfirmed) {
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
            if (ss >= 0) {
                const res = cuerpo_json.preguntas[ss];
                res.nombre_pregunta = nombre_pregunta;
                res.tipo_pregunta = tipo_pregunta;
                res.archivo = arc;
                res.puntos = puntos;
                res.tiempo = tiempo;
                res.alternativas = al;
                res.respuesta = rpt.trim();
            } else {
                // Si se está agregando una nueva pregunta, crearla
                const pr = {
                    nombre_pregunta: nombre_pregunta,
                    tipo_pregunta: tipo_pregunta,
                    archivo: arc,
                    puntos: puntos,
                    tiempo: tiempo,
                    alternativas: al,
                    respuesta: rpt.trim(),
                };
                cuerpo_json.preguntas.push(pr);
            }

            // Limpiar y renderizar el contenido
            contenido.innerHTML = "";
            const cards_continue = document.querySelector(".cards_continue");
            cards_continue.innerHTML = "";

            // Actualizar las preguntas en el DOM
            cuerpo_json.preguntas.forEach((pregunta, index) => {
                cards_continue.innerHTML += `
                    <div class="detalle_inicial card shadow-lg p-3 enfocar mt-2" id="detalle_card" onclick="pregunta(${index})">
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
            Swal.fire({
                icon: 'success',
                title: 'Pregunta Guardada',
                text: 'La pregunta ha sido guardada correctamente.'
            });
        } else {
            // Si el usuario cancela, no hacer nada
            console.log('El usuario canceló la acción de guardar.');
        }
    });
};



const pin = () => {
    var numero = Math.floor(10000 + Math.random() * 90000);
    document.getElementById('pin').value = numero;
    cuerpo_json.detalle.pin = numero

}
pin();


const eliminar_pr = (el, indice) => {
    // Mostrar un cuadro de confirmación con SweetAlert2
    Swal.fire({
        text: '¿Quieres eliminar esta pregunta?',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: 'Sí, eliminar',
        cancelButtonText: 'Cancelar'
    }).then((result) => {
        if (result.isConfirmed) {
            // Si el usuario confirma, eliminar la pregunta
            const cc = el.parentElement.parentElement.parentElement;
            cc.remove();  // Eliminar el elemento del DOM
            cuerpo_json.preguntas.splice(indice, 1);  // Eliminar la pregunta del array

            // Actualizar los índices de las preguntas en la vista
            const enumeracion = document.querySelectorAll('.texto_pregunta');
            enumeracion.forEach((enu, index) => {
                enu.textContent = `Pregunta ${index + 1}:`;  // Actualizar la numeración de las preguntas
            });

            // Mostrar mensaje de éxito
            Swal.fire({
                icon: 'success',
                title: 'Pregunta eliminada',
                text: 'La pregunta ha sido eliminada correctamente.'
            });
        } else {
            // Si el usuario cancela, no hacer nada
            console.log('El usuario canceló la acción de eliminar.');
        }
    });
};

const confirmarEnvio = () => {
    Swal.fire({
        text: '¿Estás seguro de que deseas crear este formulario?',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: 'Sí, crear',
        cancelButtonText: 'Cancelar'
    }).then((result) => {
        if (result.isConfirmed) {
            // Si el usuario confirma, se envían los datos
            enviar_datos();
        } else {
            console.log('El usuario canceló la acción de crear el formulario.');
        }
    });
};


// Función para enviar los datos del formulario
const enviar_datos = async () => {
    const ruta = "/registrar_pregunta";
    console.log(cuerpo_json); // Aquí puedes ver los datos antes de enviarlos

    const response = await fetch(ruta, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(cuerpo_json)
    });

    const resp = await response.json();

    if (resp) {
        Swal.fire({
            icon: 'success',
            title: 'Formulario creado',
            text: 'El formulario ha sido creado y guardado correctamente.'
        });
        // Recargar la página para reflejar los cambios
        location.reload();
    } else {
        Swal.fire({
            icon: 'error',
            title: 'Error',
            text: 'No se pudo crear el formulario.'
        });
    }
};