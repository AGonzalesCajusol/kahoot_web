document.addEventListener("DOMContentLoaded", () => {

    const form = document.querySelector("form");
    const submitBtn = form.querySelector('button[type="submit"]');

    const docenteFields = {
        nombre: document.getElementById("nombre"),
        apellidos: document.getElementById("apellidos"),
        email: document.getElementById("email"),
        password: document.getElementById("password"),
        confirm_password: document.getElementById("confirm_password"),
        passwordError: document.getElementById("passwordError"),
        confirmError: document.getElementById("confirmError")
    };

    let alerts = document.getElementById("formAlerts");
    if (!alerts) {
        alerts = document.createElement("div");
        alerts.id = "formAlerts";
        alerts.className = "mt-3";
        form.parentElement.appendChild(alerts);
    }

    const showAlert = (type, message) => {
        alerts.innerHTML = `
          <div class="alert alert-${type} alert-dismissible fade show animate__animated animate__fadeInDown" role="alert">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
          </div>`;
    };

    const isStrongPassword = (pwd) => /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).{8,}$/.test(pwd);

    const tipoToggle = document.createElement("div");
    tipoToggle.className = "mb-3 text-center";
    tipoToggle.innerHTML = `
        <div class="btn-group w-100" role="group">
            <button type="button" class="btn btn-outline-primary active" id="btnDocente">Docente</button>
            <button type="button" class="btn btn-outline-primary" id="btnJugador">Jugador</button>
        </div>`;
    form.insertBefore(tipoToggle, form.firstChild);

    let tipoUsuario = "docente"; // default

    const mostrarCampos = () => {
        if (tipoUsuario === "docente") {
            docenteFields.nombre.parentElement.parentElement.style.display = "block";
            docenteFields.apellidos.parentElement.parentElement.style.display = "block";
            docenteFields.nombre.required = true;
            docenteFields.apellidos.required = true;
        } else {
            docenteFields.nombre.parentElement.parentElement.style.display = "none";
            docenteFields.apellidos.parentElement.parentElement.style.display = "none";
            docenteFields.nombre.required = false;
            docenteFields.apellidos.required = false;
        }
    };

    mostrarCampos();

    document.getElementById("btnDocente").addEventListener("click", () => {
        tipoUsuario = "docente";
        document.getElementById("btnDocente").classList.add("active");
        document.getElementById("btnJugador").classList.remove("active");
        mostrarCampos();
    });
    document.getElementById("btnJugador").addEventListener("click", () => {
        tipoUsuario = "jugador";
        document.getElementById("btnJugador").classList.add("active");
        document.getElementById("btnDocente").classList.remove("active");
        mostrarCampos();
    });

    form.addEventListener("submit", async (event) => {
        event.preventDefault();

        // Limpiar errores
        docenteFields.passwordError.textContent = "";
        docenteFields.confirmError.textContent = "";
        docenteFields.password.classList.remove("is-invalid");
        docenteFields.confirm_password.classList.remove("is-invalid");

        // Obtener valores
        const password = docenteFields.password.value.trim();
        const confirmPassword = docenteFields.confirm_password.value.trim();
        const email = docenteFields.email.value.trim();
        const nombres = docenteFields.nombre?.value?.trim() || "";
        const apellidos = docenteFields.apellidos?.value?.trim() || "";

        // Validaciones locales
        let valid = true;
        if (!isStrongPassword(password)) {
            docenteFields.passwordError.textContent = "La contraseña debe tener al menos 8 caracteres, incluir mayúscula, minúscula, número y símbolo.";
            docenteFields.password.classList.add("is-invalid");
            valid = false;
        }
        if (password !== confirmPassword) {
            docenteFields.confirmError.textContent = "Las contraseñas no coinciden.";
            docenteFields.confirm_password.classList.add("is-invalid");
            valid = false;
        }
        if (!valid) return;

        // Confirmación con SweetAlert2
        Swal.fire({
            text: `¿Quieres registrarte como ${tipoUsuario}?`,
            icon: 'warning',
            showCancelButton: true,
            confirmButtonText: 'Sí, registrarme',
            cancelButtonText: 'Cancelar'
        }).then(async (result) => {
            if (!result.isConfirmed) return;

            // --- VALIDAR CORREO ANTES DE ENVIAR EL CÓDIGO ---
            try {
                const respValid = await fetch("/validar_correo", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ email })
                });
                const dataValid = await respValid.json();

                if (dataValid.code === 0) {
                    showAlert("danger", dataValid.message || "Este correo ya está registrado.");
                    return; // detener flujo
                }
            } catch (e) {
                showAlert("danger", "Error al validar el correo. Intenta nuevamente.");
                return;
            }

            // Construir payload según tipo
            let payload = { email, password, tipo_usuario: tipoUsuario };
            if (tipoUsuario === "docente") {
                payload.nombres = nombres;
                payload.apellidos = apellidos;
            }

            // UI: deshabilitar botón
            const originalText = submitBtn.innerText;
            submitBtn.disabled = true;
            submitBtn.innerText = "Registrando...";

            try {
                const resp = await fetch("/enviar_codigo", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(payload)
                });

                const data = await resp.json();

                if (resp.ok && data.code === 1) {
                    showAlert("success", data.message || "Código enviado al correo.");
                    sessionStorage.setItem("pending_email", email);
                    sessionStorage.setItem("tipo_usuario", tipoUsuario);
                    setTimeout(() => {
                        window.location.href = "/verificarcodigo";
                    }, 800);
                } else {
                    showAlert("danger", data.message || "No se pudo enviar el código. Intenta nuevamente.");
                }
            } catch (e) {
                showAlert("danger", "Ocurrió un error al enviar el código. Verifica tu conexión.");
            } finally {
                submitBtn.disabled = false;
                submitBtn.innerText = originalText;
            }
        });
    });

});

