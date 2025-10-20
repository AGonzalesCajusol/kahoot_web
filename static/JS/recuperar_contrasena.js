document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("recuperarForm");
    const emailInput = document.getElementById("email");
    const alertContainer = document.getElementById("alertContainer");
    const submitBtn = form.querySelector("button[type='submit']");

    const showAlert = (type, message) => {
        alertContainer.innerHTML = `
            <div class="alert alert-${type} alert-dismissible fade show mt-2" role="alert">
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
            </div>`;
    };

    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        const email = emailInput.value.trim();
        if (!email) {
            showAlert("warning", "Por favor, ingresa tu correo electrónico.");
            return;
        }

        submitBtn.disabled = true;
        submitBtn.innerText = "Enviando código...";

        try {
            const response = await fetch("/api_recuperar_contrasena", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ email })
            });

            const data = await response.json();

            if (response.ok && data.code === 1) {
                showAlert("success", data.message || "Se ha enviado un código a tu correo.");

                sessionStorage.setItem("reset_email", email);

                setTimeout(() => {
                    window.location.href = "/verificar_codigo_recuperacion";
                }, 1000);
            } else {
                showAlert("danger", data.message || "No se pudo enviar el código. Intenta nuevamente.");
            }

        } catch (error) {
            console.error("Error al enviar el código:", error);
            showAlert("danger", "Ocurrió un error al procesar la solicitud.");
        } finally {
            submitBtn.disabled = false;
            submitBtn.innerText = "Enviar código";
        }
    });
});
