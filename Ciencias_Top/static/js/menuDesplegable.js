// menuToggle.js
const menuToggle = document.querySelector('.menu-toggle');
const sidebar = document.querySelector('nav');
const logoutFooter = document.getElementById('logout-footer'); // div del botón de cerrar sesión

const confirmLogoutBtn = document.getElementById('confirmLogout'); // botón de confirmar cierre de sesión


menuToggle.addEventListener('click', () => {
    sidebar.classList.toggle('show');
    // Mostrar u ocultar el botón de cerrar sesión
    if (sidebar.classList.contains('show')) {
        logoutFooter.style.display = 'block'; // Mostrar el botón al abrir el menú
    } else {
        logoutFooter.style.display = 'none'; // Ocultar el botón al cerrar el menú
    }
});
// Confirmar cierre de sesión
function confirmLogout() {
    const logoutModal = new bootstrap.Modal(document.getElementById('logoutModal'));
    logoutModal.show();
    // Añadir evento para confirmar cierre de sesión
    document.getElementById('confirmLogout').addEventListener('click', function() {
        // Enviar el formulario de cierre de sesión cuando se confirma en el modal
        document.getElementById('logout-form').submit();
    }, { once: true }); // { once: true } evita múltiples adiciones del listener
    
   
}
