const startBtn = document.getElementById('startBtn');
const timerDisplay = document.getElementById('timer');
const minutesInput = document.getElementById('minutes');
const secondsInput = document.getElementById('seconds');
let interval;

const socket = io();
const id = window.idCuestionario; 

socket.emit('unirme_sala', { sala: id });

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

const pregunta = document.querySelector('.cuest');
const tiempo = document.querySelector('.temp');
const puntaje = document.querySelector('.punt');

socket.on('actualizar_tiempoAD', (data) => {
    const tiempo = data.tiempo;
    console.log(tiempo);
    if(tiempo <=0){
        document.querySelector('.preguntas').classList.remove('d-none');
        document.querySelector('.tempo').classList.add('d-none');
    }
    document.getElementById('timer').textContent = tiempo;

});

socket.on('datos_cuestionario', (data) => {
    pregunta.textContent = data.pregunta;
    puntaje.textContent = data.puntaje;
    tiempo.textContent = data.tiempo;
});
socket.on('actualiza_tiempocuestionario', (data) => {
    tiempo.textContent = data.tiempo;
});
socket.on('pantalla_finalizada', (data) => {
    const preguntasDiv = document.querySelector('.preguntas');
    let tiempo = 5; // segundos antes de redirigir

    preguntasDiv.textContent = `Se finalizó el cuestionario. Serás redirigido en ${tiempo} segundos.`;

    const interval = setInterval(() => {
        tiempo--;
        if (tiempo > 0) {
            preguntasDiv.textContent = `Se finalizó el cuestionario. Serás redirigido en ${tiempo} segundos.`;
        } else {
            clearInterval(interval);
            window.location.href =  `/resultados_inter/${id}`;
        }
    }, 1000);
});


const inicio_preguntas = () =>{
    console.log(datos)
    for (let index = 0; index < datos.length; index++) {
        const element = datos[index];
        pregunta.textContent = element.pregunta;
        let tp  = element.tiempo_respuesta;
        puntaje.textContent = element.puntaje;
        let alternativas = element.alternativas;
        console.log(element);
        socket.emit('juego', {sala: id, id_alternativa : element.id_alternativa ,tiempo: tp, puntaje: element.puntaje , alt: alternativas})

        const interval = setInterval(() => {
            tp--;
            socket.emit('enviar_temporizador', { sala: id, tiempo: tp });
            tiempo.textContent = tp;
            if(tp == 0){
                clearInterval(interval);
                tiempo.textContent = "¡Tiempo terminado!";
            }
        }, 1000);
        console.log(tp);
    }
}

