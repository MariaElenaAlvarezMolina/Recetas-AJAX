var loginform = document.getElementById('loginForm');

loginform.onsubmit = function (event) {
    
    event.preventDefault();

    var formulario = new FormData(loginForm);

    fetch('/login', {method: 'POST', body: formulario})
        .then(response => response.json())
        .then(data => {
            console.log(data);
            if(data.message == 'correcto') {
                window.location.href = "/dashboard";
            }
            else {
                var mensajeAlerta = document.getElementById('mensajeAlerta');
                mensajeAlerta.innerHTML = data.message;

                mensajeAlerta.classList.add('alert');
                mensajeAlerta.classList.add('alert-danger');
            }
        })
}