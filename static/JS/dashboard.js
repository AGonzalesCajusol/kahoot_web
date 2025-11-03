document.addEventListener('DOMContentLoaded', () => {
    
    const sidebar = document.getElementById('sidebar');
    const mainContent = document.querySelector('.main-content');

    const searchInput = document.querySelector('input[type="text"]');
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            const searchTerm = searchInput.value.toLowerCase();
            const questionnaires = document.querySelectorAll('.questionnaire-card');

            questionnaires.forEach(card => {
                const title = card.querySelector('h4').textContent.toLowerCase();
                if (title.includes(searchTerm)) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    }
});
function confirmarCerrarSesion() {    
    Swal.fire({
        text: '¿Quieres cerrar sesión?',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: 'Sí, cerrar sesión',
        cancelButtonText: 'Cancelar'
    }).then((result) => {
        if (result.isConfirmed) {        
            window.location.href = "/logout"; 
        } else {            
            console.log('El usuario canceló el cierre de sesión.');
        }
    });
}

