document.addEventListener('DOMContentLoaded', () => {
    function clearSearch() {
        const searchInput = document.querySelector('.search-input');
        if (searchInput) {
            searchInput.value = ''; // Limpia el campo de búsqueda
            console.log('Campo limpiado');
        } else {
            console.error('No se encontró el campo .search-input');
        }
    }

    // Asocia el evento manualmente si `onclick` en HTML no funciona
    document.querySelector('.clear-button').addEventListener('click', clearSearch);
});