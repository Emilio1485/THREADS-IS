// menuToggle.js
const menuToggle = document.querySelector('.menu-toggle');
const sidebar = document.querySelector('nav');

menuToggle.addEventListener('click', () => {
    sidebar.classList.toggle('show');
});