const contenido = document.querySelector('.cont_formulario');

const cuerpo_json = {
    detallle: {
        nombre_cuestionario : '',
        tipo_formulario : '',
        descripcion_formulario : ''
    },
    preguntas : '' 
}

const guardar_detalle = () =>{
    const nombre_cuestionario = document.getElementById('nombre_cuestionario');
    const tipo_formulario = document.getElementById('tipo_cuestionario');
    const descripcion_formulario = document.getElementById('descripcion');

    cuerpo_json.detallle.nombre_cuestionario = nombre_cuestionario.value;
    cuerpo_json.detallle.tipo_formulario = tipo_formulario.value;
    cuerpo_json.detallle.descripcion_formulario = descripcion_formulario.value;

    contenido.innerHTML = "";
    const cards_continue = document.querySelector('.cards_continue');
    const tarjeta = `
        <div class="detalle_inicial card shadow-lg p-3 enfocar " id="detalle_card">
            <div class="row">
                <div class="col-9">
                    <p class="text-secondary">Pregunta 1:</p> 
                    <p class="name_cuestion">
                        ¿asdasdsd?
                    </p>
                </div>
                <div class="col-2">
                    <button class="btn btn-danger rounded-circle " style="width: 2.5rem; height: 2.5rem;"><i class="bi bi-trash3 fs-9"></i></button>
                </div>
            </div>

        </div>
    `;
    cards_continue.innerHTML += tarjeta;

}

const detalle = () =>{
    contenido.innerHTML = `
        <form class="cont_formulario card shadow-lg p-4" style="padding: 2rem;">
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
                        <option value="" disabled ${cuerpo_json.detallle.tipo_formulario === "" ? "selected" : ""}>Seleccione una opción</option>
                        <option value="I" ${cuerpo_json.detallle.tipo_formulario === "I" ? "selected" : ""}>Individual</option>
                        <option value="G" ${cuerpo_json.detallle.tipo_formulario === "G" ? "selected" : ""}>Grupal</option>
                    </select>
                </div>
                <div class="d-flex flex-column flex-grow-1">
                    <label for="descripcion" class="fw-bold mb-2">
                        <i class="bi bi-card-text"></i>
                        Descripción del formulario
                    </label>
                    <textarea  id="descripcion" class="form-control" name="descripcion" rows="7" placeholder="Ingrese la descripción del cuestionario" >${cuerpo_json.detallle.descripcion_formulario}</textarea>
                </div>
            </div>
            <div class="mt-4 text-end">
                <button type="button" class="btn btn-primary" onclick="guardar_detalle()">
                    <i class="bi bi-save"></i> Guardar detalle
                </button>
            </div>
        </form>
    
    
    `;

}