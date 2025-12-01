document.addEventListener("DOMContentLoaded", () => {

    const formulario = document.getElementById("registroJugadorForm");
    const botonEnviar = formulario.querySelector('button[type="submit"]');

    const camposJugador = {
        email: document.getElementById("email"),
        password: document.getElementById("password"),
        confirm_password: document.getElementById("confirm_password"),
        passwordError: document.getElementById("passwordError"),
        confirmError: document.getElementById("confirmError")
    };

    // Alternador para mostrar/ocultar contraseñas
    const alternarContrasena = document.getElementById('togglePassword');
    const alternarConfirmarContrasena = document.getElementById('toggleConfirmPassword');
    const iconoOjoContrasena = document.getElementById('passwordEyeIcon');
    const iconoOjoConfirmarContrasena = document.getElementById('confirmPasswordEyeIcon');
    
    if (alternarContrasena && iconoOjoContrasena) {
        alternarContrasena.addEventListener('click', function() {
            const tipo = camposJugador.password.getAttribute('type') === 'password' ? 'text' : 'password';
            camposJugador.password.setAttribute('type', tipo);
            
            if (tipo === 'text') {
                iconoOjoContrasena.classList.remove('bi-eye');
                iconoOjoContrasena.classList.add('bi-eye-slash');
            } else {
                iconoOjoContrasena.classList.remove('bi-eye-slash');
                iconoOjoContrasena.classList.add('bi-eye');
            }
        });
    }
    
    if (alternarConfirmarContrasena && iconoOjoConfirmarContrasena) {
        alternarConfirmarContrasena.addEventListener('click', function() {
            const tipo = camposJugador.confirm_password.getAttribute('type') === 'password' ? 'text' : 'password';
            camposJugador.confirm_password.setAttribute('type', tipo);
            
            if (tipo === 'text') {
                iconoOjoConfirmarContrasena.classList.remove('bi-eye');
                iconoOjoConfirmarContrasena.classList.add('bi-eye-slash');
            } else {
                iconoOjoConfirmarContrasena.classList.remove('bi-eye-slash');
                iconoOjoConfirmarContrasena.classList.add('bi-eye');
            }
        });
    }

    let alertas = document.getElementById("formAlerts");
    if (!alertas) {
        alertas = document.createElement("div");
        alertas.id = "formAlerts";
        alertas.className = "mt-3";
        formulario.parentElement.appendChild(alertas);
    }

    const mostrarAlerta = (tipo, mensaje) => {
        alertas.innerHTML = `
          <div class="alert alert-${tipo} alert-dismissible fade show animate__animated animate__fadeInDown" role="alert">
            ${mensaje}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Cerrar"></button>
          </div>`;
    };

    const esContrasenaFuerte = (contrasena) => /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).{8,}$/.test(contrasena);

    let tipoUsuario = "jugador";

    formulario.addEventListener("submit", async (evento) => {
        evento.preventDefault();

        // Limpiar errores
        camposJugador.passwordError.textContent = "";
        camposJugador.confirmError.textContent = "";
        camposJugador.password.classList.remove("is-invalid");
        camposJugador.confirm_password.classList.remove("is-invalid");

        // Obtener valores
        const contrasena = camposJugador.password.value.trim();
        const confirmarContrasena = camposJugador.confirm_password.value.trim();
        const email = camposJugador.email.value.trim();

        // Validaciones locales
        let valido = true;
        if (!esContrasenaFuerte(contrasena)) {
            camposJugador.passwordError.textContent = "La contraseña debe tener al menos 8 caracteres, incluir mayúscula, minúscula, número y símbolo.";
            camposJugador.password.classList.add("is-invalid");
            valido = false;
        }
        if (contrasena !== confirmarContrasena) {
            camposJugador.confirmError.textContent = "Las contraseñas no coinciden.";
            camposJugador.confirm_password.classList.add("is-invalid");
            valido = false;
        }
        if (!valido) return;

        Swal.fire({
            text: `¿Quieres registrarte como ${tipoUsuario}?`,
            icon: 'warning',
            showCancelButton: true,
            confirmButtonText: 'Sí, registrarme',
            cancelButtonText: 'Cancelar'
        }).then(async (resultado) => {
            if (!resultado.isConfirmed) return;

            try {
                const respuestaValidacion = await fetch("/validar_correo", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ email })
                });
                const datosValidacion = await respuestaValidacion.json();

                if (datosValidacion.code === 0) {
                    mostrarAlerta("danger", datosValidacion.message || "Este correo ya está registrado.");
                    return; 
                }
            } catch (error) {
                mostrarAlerta("danger", "Error al validar el correo. Intenta nuevamente.");
                return;
            }

            // Obtener datos faciales si fueron capturados
            const rostroDataInput = document.getElementById('rostro_data');
            const rostroData = rostroDataInput ? rostroDataInput.value : null;

            let datosEnvio = { 
                email, 
                password: contrasena, 
                tipo_usuario: "jugador",
                rostro: rostroData  // Incluir datos faciales si están disponibles
            };

            // Interfaz: deshabilitar botón
            const textoOriginal = botonEnviar.innerText;
            botonEnviar.disabled = true;
            botonEnviar.innerText = "Registrando...";

            try {
                const respuesta = await fetch("/enviar_codigo", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(datosEnvio)
                });

                const datos = await respuesta.json();

                if (respuesta.ok && datos.code === 1) {
                    mostrarAlerta("success", datos.message || "Código enviado al correo.");
                    sessionStorage.setItem("pending_email", email);
                    sessionStorage.setItem("tipo_usuario", tipoUsuario);
                    setTimeout(() => {
                        window.location.href = "/verificarcodigo";
                    }, 800);
                } else {
                    mostrarAlerta("danger", datos.message || "No se pudo enviar el código. Intenta nuevamente.");
                }
            } catch (error) {
                mostrarAlerta("danger", "Ocurrió un error al enviar el código. Verifica tu conexión.");
            } finally {
                botonEnviar.disabled = false;
                botonEnviar.innerText = textoOriginal;
            }
        });
    });
});






















