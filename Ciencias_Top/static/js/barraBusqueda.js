document.addEventListener('DOMContentLoaded', () => {
    function clearSearch() {
        const searchInput = document.querySelector('.search-input');
        if (searchInput) {
            searchInput.value = ''; // Limpia el campo de búsqueda
            console.log('Campo limpiado');
             // Agregar clase de desvanecimiento
             document.body.classList.add('fade-out');
             // Esperar a que la animación termine antes de redirigir
             setTimeout(() => {
                 window.location.href = '/usuarios/';
             }, 500); // Ajusta el tiempo según la duración de la animación
        } else {
            console.error('No se encontró el campo .search-input');
        }
    }

    const clearButton = document.querySelector('.clear-button');
    if (clearButton) {
        clearButton.addEventListener('click', clearSearch);
    } else {
        console.error('No se encontró el botón .clear-button');
    }

    // Asocia el evento manualmente si `onclick` en HTML no funciona
    document.querySelector('.clear-button').addEventListener('click', clearSearch);
});