$(document).ready(function () {
    // Al hacer clic en un botón de eliminar
    $(document).on('click', '.btn-danger', function () {
        var button = $(this); // El botón que activó el modal
        var usuarioId = button.data('usuario-id'); // ID del usuario
        var usuarioNombre = button.data('usuario-nombre'); // Nombre del usuario

        // Selecciona el modal correspondiente
        var modal = $('#modal-eliminar-usuario-' + usuarioId);

        // Actualiza el contenido dinámico dentro del modal
        modal.find('#usuario-nombre-' + usuarioId).text(usuarioNombre);

        // Configura la acción del formulario dinámicamente
        var form = modal.find('#form-eliminar-usuario-' + usuarioId);
        form.attr('action', '/eliminar_usuario/' + usuarioId + '/');

        // Muestra el modal
        modal.modal('show');
    });

    // Al cerrar cualquier modal
    $(document).on('hidden.bs.modal', '.modal', function () {
        var modal = $(this);

        // Limpia el contenido dinámico del modal
        modal.find('form').trigger('reset'); // Limpia el formulario
        modal.find('.modal-body span').text(''); // Limpia textos dinámicos

        // Elimina cualquier evento asociado al formulario
        modal.find('form').off('submit');

        $('.modal-backdrop').remove(); // Elimina cualquier fondo residual del modal
        $('body').removeClass('modal-open'); // Elimina la clase modal-open
    $('body').css('overflow', ''); // Restaura el scroll
    });
});
