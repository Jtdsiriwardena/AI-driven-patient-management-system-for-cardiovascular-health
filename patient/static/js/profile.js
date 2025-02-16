
//Change password
const changePasswordLink = document.getElementById('change-password');

const passwordInput = document.getElementById('new_password');

const passwordForm = document.querySelector('.password-form');

changePasswordLink.addEventListener('click', function() {

    passwordForm.style.display = passwordForm.style.display === 'none' ? 'block' : 'none';
});

passwordInput.addEventListener('input', function() {

    passwordInput.type = 'text';
});

passwordInput.addEventListener('blur', function() {

    passwordInput.type = 'password';
});