const contenido = document.querySelector('.cont_formulario');

const guardar_detalle = () =>{
    contenido.innerHTML = "";
    const cards_continue = document.querySelector('.cards_continue');
    const tarjeta = `
        <div class="detalle_inicial card shadow-lg p-3" id="detalle_card">
            <button class="btn btn-danger rounded-circle " style="width: 2.5rem; height: 2.5rem;"><i class="bi bi-trash3 fs-6"></i></button>
            <p class="text-secondary">Pregunta</p> <span class="nombre_pregunta"> </span>
        </div>
    `;
    cards_continue.innerHTML += tarjeta;

}