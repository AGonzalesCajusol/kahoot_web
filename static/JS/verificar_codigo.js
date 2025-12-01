document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("verifyForm");
    const inputCodigo = document.getElementById("codigo");
    const alertContainer = document.getElementById("alertContainer");
    const submitBtn = form.querySelector("button[type='submit']");
    const btnReenviar = document.getElementById("btnReenviar");

    const showAlert = (type, message) => {
        alertContainer.innerHTML = `
            <div class="alert alert-${type} alert-dismissible fade show mt-2" role="alert">
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
            </div>`;
    };

    // Funcionalidad de reenvío de código
    if (btnReenviar) {
        btnReenviar.addEventListener("click", async () => {
            const email = sessionStorage.getItem("pending_email");
            
            if (!email) {
                showAlert("danger", "No se encontró el correo asociado. Regístrate nuevamente.");
                return;
            }

            btnReenviar.disabled = true;
            btnReenviar.textContent = "Enviando...";

            try {
                const response = await fetch("/reenviar_codigo", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ email })
                });

                const data = await response.json();

                if (response.ok && data.code === 1) {
                    showAlert("success", data.message || "Código reenviado correctamente.");
                } else {
                    showAlert("danger", data.message || "No se pudo reenviar el código. Intenta nuevamente.");
                }
            } catch (error) {
                console.error("Error al reenviar código:", error);
                showAlert("danger", "Ocurrió un error al reenviar el código.");
            } finally {
                btnReenviar.disabled = false;
                btnReenviar.textContent = "Reenviar código";
            }
        });
    }

    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        const codigo = inputCodigo.value.trim();
        const email = sessionStorage.getItem("pending_email"); 

        if (!email) {
            showAlert("danger", "No se encontró el correo asociado. Regístrate nuevamente.");
            return;
        }

        if (codigo.length !== 6 || isNaN(codigo)) {
            showAlert("warning", "El código debe tener exactamente 6 dígitos numéricos.");
            return;
        }

        // Desactivar botón mientras se verifica
        submitBtn.disabled = true;
        submitBtn.innerText = "Verificando...";

        try {
            const resp = await fetch("/verificar_codigo", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ email, codigo })
            });

            const data = await resp.json();

            if (resp.ok && data.code === 1) {
                showAlert("success", data.message || "Correo verificado con éxito. Redirigiendo...");
                sessionStorage.removeItem("pending_email");

                // Redirigir al login luego de unos segundos
                setTimeout(() => {
                    window.location.href = "/login";
                }, 2000);
            } else {
                showAlert("danger", data.message || "El código es incorrecto o ha expirado.");
            }
        } catch (error) {
            showAlert("danger", "Error al verificar el código. Inténtalo nuevamente.");
        } finally {
            submitBtn.disabled = false;
            submitBtn.innerText = "Verificar Código";
        }
    });
});
