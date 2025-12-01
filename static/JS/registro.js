document.addEventListener("DOMContentLoaded", () => {

    const formulario = document.querySelector("form");
    const botonEnviar = formulario.querySelector('button[type="submit"]');

    const camposDocente = {
        nombre: document.getElementById("nombre"),
        apellidos: document.getElementById("apellidos"),
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
            const tipo = camposDocente.password.getAttribute('type') === 'password' ? 'text' : 'password';
            camposDocente.password.setAttribute('type', tipo);
            
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
            const tipo = camposDocente.confirm_password.getAttribute('type') === 'password' ? 'text' : 'password';
            camposDocente.confirm_password.setAttribute('type', tipo);
            
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

    let tipoUsuario = "docente"; // Solo docentes pueden registrarse desde aquí

    formulario.addEventListener("submit", async (evento) => {
        evento.preventDefault();

        // Limpiar errores
        camposDocente.passwordError.textContent = "";
        camposDocente.confirmError.textContent = "";
        camposDocente.password.classList.remove("is-invalid");
        camposDocente.confirm_password.classList.remove("is-invalid");

        // Obtener valores
        const contrasena = camposDocente.password.value.trim();
        const confirmarContrasena = camposDocente.confirm_password.value.trim();
        const email = camposDocente.email.value.trim();
        const nombres = camposDocente.nombre?.value?.trim() || "";
        const apellidos = camposDocente.apellidos?.value?.trim() || "";

        // Validaciones locales
        let valido = true;
        if (!esContrasenaFuerte(contrasena)) {
            camposDocente.passwordError.textContent = "La contraseña debe tener al menos 8 caracteres, incluir mayúscula, minúscula, número y símbolo.";
            camposDocente.password.classList.add("is-invalid");
            valido = false;
        }
        if (contrasena !== confirmarContrasena) {
            camposDocente.confirmError.textContent = "Las contraseñas no coinciden.";
            camposDocente.confirm_password.classList.add("is-invalid");
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
            const rostroData = obtenerRostroData();
            
            let datosEnvio = { 
                email, 
                password: contrasena, 
                tipo_usuario: "docente",
                nombres: nombres,
                apellidos: apellidos,
                rostro: rostroData || null  // Agregar datos faciales (opcional)
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

