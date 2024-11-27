function setDeleteUrl(url) {
    const deleteForm = document.getElementById('deleteForm');
    deleteForm.action = url;  // Establecer la acción del formulario
}

function setEditProductData(codigo, nombre, descripcion, existencia, pumapuntos, dias_renta, imagenUrl) {
    // Actualizar la URL del formulario para que apunte al producto correcto
    const form = document.getElementById('editarProductoForm');
    form.action = `/editar_producto/${codigo}/`;

    // Actualizar los valores en los campos del formulario
    document.getElementById('producto-nombre').value = nombre;
    document.getElementById('producto-descripcion').value = descripcion;
    document.getElementById('producto-existencia').value = existencia;
    document.getElementById('producto-pumapuntos').value = pumapuntos;
    document.getElementById('producto-dias-renta').value = dias_renta;

    const imagePreview = document.getElementById('image-preview');
    const imagePreviewContainer = document.getElementById('image-preview-container');
    const fileChosen = document.getElementById('file-chosen');
    
    if (imagenUrl && imagenUrl !== '') {
        imagePreview.src = imagenUrl;
        imagePreviewContainer.style.display = 'block';
        fileChosen.textContent = 'Imagen actual cargada';
    } else {
        imagePreview.src = '';
        imagePreviewContainer.style.display = 'none';
        fileChosen.textContent = 'No se ha seleccionado ningún archivo';
    }
}

// Manejo de la selección de archivo
document.getElementById('custom-button').addEventListener('click', function() {
    document.getElementById('actual-input').click();
});

document.getElementById('actual-input').addEventListener('change', function() {
    const file = this.files[0];
    const fileChosen = document.getElementById('file-chosen');
    const imagePreview = document.getElementById('image-preview');
    const imagePreviewContainer = document.getElementById('image-preview-container');

    if (file) {
        fileChosen.textContent = 'Archivo seleccionado: ' + file.name;

        const reader = new FileReader();
        reader.onload = function(e) {
            imagePreview.src = e.target.result;
            imagePreviewContainer.style.display = 'block';
        };
        reader.readAsDataURL(file);
    } else {
        fileChosen.textContent = 'No se ha seleccionado ningún archivo';
        imagePreviewContainer.style.display = 'none';
    }
}); 