document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector("form");
    const submitBtn = form.querySelector('button[type="submit"]');
    const passwordInput = document.getElementById("password");
    const confirmPasswordInput = document.getElementById("confirm_password");
    const passwordError = document.getElementById("passwordError");
    const confirmError = document.getElementById("confirmError");

    let alerts = document.getElementById("formAlerts");
    if (!alerts) {
        alerts = document.createElement("div");
        alerts.id = "formAlerts";
        alerts.className = "mt-3";
        form.parentElement.appendChild(alerts);
    }

    const showAlert = (type, message) => {
        alerts.innerHTML = `
          <div class="alert alert-${type} alert-dismissible fade show" role="alert">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
          </div>`;
    };

    const isStrongPassword = (pwd) => /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).{8,}$/.test(pwd);

    form.addEventListener("submit", async (event) => {
        // 1) Validación UI existente
        let valid = true;
        passwordError.textContent = "";
        confirmError.textContent = "";
        passwordInput.classList.remove("is-invalid");
        confirmPasswordInput.classList.remove("is-invalid");

        const password = passwordInput.value.trim();
        const confirmPassword = confirmPasswordInput.value.trim();

        if (!isStrongPassword(password)) {
            passwordError.textContent = "La contraseña debe tener al menos 8 caracteres, e incluir una mayúscula, una minúscula, un número y un símbolo.";
            passwordInput.classList.add("is-invalid");
            valid = false;
        }
        if (password !== confirmPassword) {
            confirmError.textContent = "Las contraseñas no coinciden.";
            confirmPasswordInput.classList.add("is-invalid");
            valid = false;
        }
        if (!valid) {
            event.preventDefault();
            return;
        }

        // 2) Interceptar envío para mandar código por correo
        event.preventDefault();

        // Tomar datos del form
        const payload = {
            nombres: form.querySelector('#nombre')?.value?.trim(),
            apellidos: form.querySelector('#apellidos')?.value?.trim(),
            email: form.querySelector('#email')?.value?.trim(),
            password: password
        };

        // UI: deshabilitar botón
        const originalText = submitBtn.innerText;
        submitBtn.disabled = true;
        submitBtn.innerText = "Enviando código...";

        try {
            const resp = await fetch("/enviar_codigo", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload)
            });

            const data = await resp.json();

            if (resp.ok && data.code === 1) {
                showAlert("success", data.message || "Código enviado al correo.");
                sessionStorage.setItem("pending_email", payload.email);
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
