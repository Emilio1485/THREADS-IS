document.addEventListener('DOMContentLoaded', function() {
    const messagesElement = document.getElementById('messages-data');
    if (messagesElement) {
        const messages = JSON.parse(messagesElement.textContent);
        messages.forEach(message => {
            var modal = new bootstrap.Modal(document.getElementById('messageModal'), {
                keyboard: false
            });
            var messageContent = document.getElementById('messageContent');
            messageContent.innerText = message;  // El contenido del mensaje
            modal.show();
        });
    }
});