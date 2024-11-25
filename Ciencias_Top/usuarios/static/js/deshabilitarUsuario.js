
// Estado inicial del switch al cargar la página
let estadoInicial = document.getElementById('estado-switch').checked;
    // Mostrar modal de confirmación al cambiar el estado del switch
    document.getElementById('estado-switch').addEventListener('change', function() {
        const numeroCuenta = this.getAttribute('data-numero-cuenta');
        const isActive = this.checked;

        console.log('Estado del switch para el usuario', numeroCuenta, ':', isActive ? 'Activado' : 'Desactivado');

        // Si el estado del switch cambia a "Desactivado", mostramos el modal
        if (!isActive) {
            // Mostrar el modal de confirmación
            var mensajeModal = new bootstrap.Modal(document.getElementById('modalConfirmacion'));
            mensajeModal.show();

            const modaleElement = document.getElementById('modalConfirmacion');
            modaleElement.addEventListener('hidden.bs.modal', function() {
                // Si el modal se cierra sin confirmar, regresamos el switch a su estado original
                document.getElementById('estado-switch').checked = estadoInicial;
            });
        }else{
            
            var mensajeModal =  new bootstrap.Modal(document.getElementById('messageModal'), {
                keyboard: false
            });
            var messageContent = document.getElementById('messageContent');
            messageContent.innerText = "Habilitar un usuario aun no esta permitido en el sistema";  // El contenido del mensaje
            mensajeModal.show();
            mensajeModal._element.addEventListener('hidden.bs.modal', function() {
                // Si el modal se cierra sin confirmar, regresamos el switch a su estado original
                document.getElementById('estado-switch').checked = estadoInicial;
            });

        }
    });

    // Al confirmar deshabilitar, se envía el formulario
    document.getElementById('confirmarDeshabilitar').addEventListener('click', function() {
        const form = document.getElementById('deshabilitar-form');
        const modal = bootstrap.Modal.getInstance(document.getElementById('modalConfirmacion'));
        modal.hide(); // Ocultar el modal
        form.submit(); // Enviar el formulario para deshabilitar al usuario
    });
    



