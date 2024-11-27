document.addEventListener('DOMContentLoaded', () => {
    function clearSearch(event) {
        const searchInput = document.querySelector('.search-input');
        if (searchInput) {
            searchInput.value = ''; // Limpia el campo de búsqueda
            console.log('Campo limpiado');
            // Agregar clase de desvanecimiento
            document.body.classList.add('fade-out');
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
});