const startBtn = document.getElementById('startBtn');
const timerDisplay = document.getElementById('timer');
const minutesInput = document.getElementById('minutes');
const secondsInput = document.getElementById('seconds');
let interval;

const socket = io();
    let id = 2;

socket.emit('unirme_sala', {sala: id})

startBtn.addEventListener('click', () => {
    clearInterval(interval);
    let totalSeconds = parseInt(minutesInput.value || 0) * 60 + parseInt(secondsInput.value || 0);

    if (totalSeconds <= 0) {
        alert("Por favor selecciona un tiempo válido");
        return;
    }

    startBtn.disabled = true;
    startBtn.innerText = "Contando...";

    interval = setInterval(() => {
        if (totalSeconds <= 0) {
            clearInterval(interval);
            timerDisplay.innerText = "¡Tiempo terminado!";
            startBtn.disabled = false;
            startBtn.innerText = "Iniciar";
            document.querySelector('.tempo').classList.add('d-none');
            document.querySelector('.preguntas').classList.remove('d-none');
            inicio_preguntas();
            return;
        }

        totalSeconds--;
        socket.emit('enviar_temporizador', { sala: id, tiempo: totalSeconds });
        const mins = String(Math.floor(totalSeconds / 60)).padStart(2, '0');
        const secs = String(totalSeconds % 60).padStart(2, '0');
        timerDisplay.innerText = `${mins}:${secs}`;
    }, 1000);
});

const pregunta = document.querySelector('.cuest');
const tiempo = document.querySelector('.temp');
const puntaje = document.querySelector('.punt');

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

