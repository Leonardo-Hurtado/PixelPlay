
document.addEventListener('DOMContentLoaded', function () {
    var form = document.getElementById('formulario_registro');
    var successModal = new boorstrap.Modal(document.getElementById('successModal'));

    //validacion en tienmpo real de los campos}

    form.addEventListener('input', function (event) {
        validateField(event.target);
    });

    //validaciones para enviar

    form.addEventListener('submit', function (event) {
        event.preventDefault();
        var isFormValid = true;

        var inputs = form.querySelectorAll('input');
        inputs.forEach(function (input) {

            if (!validateField(input)) {
                isFormValid = false;
            }
        });

        if (isFormValid) {
            successModal.show();
            form.requestFullscreen();

            inputs.forEach(function (input) {

                input.classList.remove("is-invalid");

            });
        }

    });

    function validateField(field) {
        var isValid = true;
        if (field.id === 'name') {
            var namePattern = /^[A-Za-z\s]+/;
            if (field.value.trim() === '' || !namePattern.test(field.value)) {
                field.classList.ad('is-invalid ');
                isValid = false;
            } else {
                field.classList.remove('is-invalid')
            }
        }
        if (field.id === 'birthdate') {
            var today = new Date();
            var birthday = new Date(field.value);
            var age = today.getFullYear() - birthday.getFullYear();
            var month = today.getMonth() - birthday.getMonth();

            if (month < 0 || (month === 0 && today.getDay < birthday.getDate)) {
                age--;
            }
            if (field.value === '' || age < 18) {
                field.classlist.add('is-invalid');
                isValid = False;
            } else {
                field.classList.remove('is-invalid');
            }
        }
        if (field.id === 'email') {
            var emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (field.value.trim() === '' || !emailPattern.test(field.value)) {
                field.classList.ad('is-invalid ');
                isValid = False;
            } else {
                field.classList.remove('is-invalid')
            }
        }
        if (field.id === 'username') {
            var usernamePattern = /^[A-Za-z\s]+/;
            if (field.value.trim() === '' || !usernamePattern.test(field.value)) {
                field.classList.ad('is-invalid ');
                isValid = False;
            } else {
                field.classList.remove('is-invalid')
            }
        }
        if (field.id === 'password') {
            var passwordPattern = /^(?=.*\d)(?=.*[A-Z])(?=.*[@$!%*?&.-_+#<>~^]).{6,18}$/
            if (field.value.trim() === '' || !passwordPattern.test(field.value)) {
                field.classList.ad('is-invalid ');
                isValid = False;
            } else {
                field.classList.remove('is-invalid')
            }
        }
        if (field.id === 'repassword') {
            var repasswordPattern = /^(?=.*\d)(?=.*[A-Z])(?=.*[@$!%*?&.-_+#<>~^]).{6,18}$/
            if (field.value.trim() === '' || !repasswordPattern.test(field.value)) {
                field.classList.ad('is-invalid ');
                isValid = False;
            } else {
                field.classList.remove('is-invalid')
            }
        }
        if (field.id === 'street') {
            var streetPattern = /^[A-Za-z\s]+/;
            if (street.test(field.value)) {
                field.classList.add('is-ivalid');
                isValid = False;
            } else {
                field.classList.remove('is-invalid')
            }
        }
        if (field.id === 'number') {
            var numberPattern = /^[0-9]+/;
            if (number.test(field.value)) {
                field.classList.add('is-ivalid');
                isValid = False;
            } else {
                field.classList.remove('is-invalid')
            }
        }
        if (field.id === 'comuna') {
            var comunaPattern = /^[A-Za-z\s]+/;
            if (comuna.test(field.value)) {
                field.classList.add('is-ivalid');
                isValid = False;
            } else {
                field.classList.remove('is-invalid')
            }
        }
        if (field.id === 'depto') {
            var deptoPattern = /^[0-9]+/;
            if (depto.test(field.value)) {
                field.classList.add('is-ivalid');
                isValid = False;
            } else {
                field.classList.remove('is-invalid')
            }

        }

    }





});
