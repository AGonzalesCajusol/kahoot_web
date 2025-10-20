// Esperar a que el DOM cargue completamente
document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector("form"); // Captura el formulario
    const passwordInput = document.getElementById("password");
    const confirmPasswordInput = document.getElementById("confirm_password");

    form.addEventListener("submit", (event) => {
        const password = passwordInput.value.trim();
        const confirmPassword = confirmPasswordInput.value.trim();

        const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).{8,}$/;

        if (!passwordRegex.test(password)) {
            event.preventDefault();
            alert(
                "La contraseña debe tener al menos 8 caracteres, e incluir:\n- Una letra mayúscula\n- Una letra minúscula\n- Un número\n- Un símbolo"
            );
            return;
        }
        
        if (password !== confirmPassword) {
            event.preventDefault();
            alert("Las contraseñas no coinciden. Verifica e inténtalo de nuevo.");
            return;
        }

    });
});
