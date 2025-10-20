document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("newPassForm");
  const passwordInput = document.getElementById("password");
  const confirmInput = document.getElementById("confirm_password");
  const passwordError = document.getElementById("passwordError");
  const confirmError = document.getElementById("confirmError");
  const alertContainer = document.getElementById("alertContainer");
  const togglePwd = document.getElementById("togglePwd");
  const togglePwd2 = document.getElementById("togglePwd2");
  const submitBtn = form.querySelector("button[type='submit']");

  const showAlert = (type, message) => {
    alertContainer.innerHTML = `
      <div class="alert alert-${type} alert-dismissible fade show mt-2" role="alert">
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
      </div>`;
  };

  const isStrong = (pwd) =>
    /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).{8,}$/.test(pwd);

  // Mostrar/ocultar contraseñas
  const toggle = (input, btn) => {
    const isText = input.type === "text";
    input.type = isText ? "password" : "text";
    btn.querySelector("i").className = isText ? "bi bi-eye" : "bi bi-eye-slash";
  };
  togglePwd.addEventListener("click", () => toggle(passwordInput, togglePwd));
  togglePwd2.addEventListener("click", () => toggle(confirmInput, togglePwd2));

  // Validación en tiempo real
  const validate = () => {
    let ok = true;
    passwordError.textContent = "";
    confirmError.textContent = "";
    passwordInput.classList.remove("is-invalid");
    confirmInput.classList.remove("is-invalid");

    if (!isStrong(passwordInput.value.trim())) {
      passwordError.textContent =
        "La contraseña debe tener mínimo 8 caracteres, incluir mayúscula, minúscula, número y símbolo.";
      passwordInput.classList.add("is-invalid");
      ok = false;
    }
    if (passwordInput.value.trim() !== confirmInput.value.trim()) {
      confirmError.textContent = "Las contraseñas no coinciden.";
      confirmInput.classList.add("is-invalid");
      ok = false;
    }
    return ok;
  };

  passwordInput.addEventListener("input", validate);
  confirmInput.addEventListener("input", validate);

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    if (!validate()) return;

    const email = sessionStorage.getItem("verified_email");
    if (!email) {
      showAlert("danger", "Sesión de recuperación no encontrada. Repite el proceso.");
      return;
    }

    submitBtn.disabled = true;
    submitBtn.textContent = "Guardando...";

    try {
      const resp = await fetch("/actualizar_contrasena", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
          email,
          nueva_password: passwordInput.value.trim()
        })
      });
      const data = await resp.json();

      if (resp.ok && data.code === 1) {
        showAlert("success", data.message || "Contraseña actualizada correctamente.");
        // limpiar storage y redirigir al login
        sessionStorage.removeItem("reset_email");
        sessionStorage.removeItem("verified_email");
        setTimeout(() => (window.location.href = "/login"), 1500);
      } else {
        showAlert("danger", data.message || "No se pudo actualizar la contraseña.");
      }
    } catch (err) {
      showAlert("danger", "Error de red. Intenta nuevamente.");
      console.error(err);
    } finally {
      submitBtn.disabled = false;
      submitBtn.textContent = "Guardar nueva contraseña";
    }
  });
});
