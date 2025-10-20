document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("verifyCodeForm");
    const inputCodigo = document.getElementById("codigo");
    const alertContainer = document.getElementById("alertContainer");
    const submitBtn = form.querySelector("button[type='submit']");

    // Mostrar alerta visual con Bootstrap
    const showAlert = (type, message) => {
        alertContainer.innerHTML = `
            <div class="alert alert-${type} alert-dismissible fade show mt-2" role="alert">
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
            </div>`;
    };

    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        const codigo = inputCodigo.value.trim();
        const email = sessionStorage.getItem("reset_email");

        if (!email) {
            showAlert("danger", "No se encontró un correo asociado. Intenta nuevamente desde la recuperación.");
            return;
        }

        if (codigo.length !== 6 || isNaN(codigo)) {
            showAlert("warning", "El código debe tener exactamente 6 dígitos numéricos.");
            return;
        }

        // Deshabilitar botón durante la verificación
        submitBtn.disabled = true;
        submitBtn.innerText = "Verificando...";

        try {
            const resp = await fetch("/verificar_codigo_recuperacion", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ email, codigo })
            });

            const data = await resp.json();

            if (resp.ok && data.code === 1) {
                showAlert("success", data.message || "Código verificado correctamente.");
                // Guardamos el email confirmado para usarlo al crear nueva contraseña
                sessionStorage.setItem("verified_email", email);
                // Redirigir a la página de nueva contraseña
                setTimeout(() => {
                window.location.href = "/nueva_contrasena";
                }, 1500);

            } else {
                showAlert("danger", data.message || "El código es incorrecto o ha expirado.");
            }

        } catch (error) {
            console.error("Error verificando el código:", error);
            showAlert("danger", "Ocurrió un error al verificar el código. Inténtalo nuevamente.");
        } finally {
            submitBtn.disabled = false;
            submitBtn.innerText = "Verificar código";
        }
    });
});
