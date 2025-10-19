async function addNewUser(username, password) {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const response = await fetch("/createUser/", {
        method: "POST",
        headers: {
            "X-CSRFToken": csrfToken,
            "Content-Type": "application/x-www-form-urlencoded",
        },
        body: `username=${username}&password=${password}`,
    });

    const data = await response.json();

    if (response.ok && data.status === "ok") {
        console.log("Все добавилось");
        window.location.href = '/';
        return true;
    } else {
        console.log("Не добавилось. ", data.message);
        return false;
    }
}

document.addEventListener("DOMContentLoaded",  () => {
    const log_button = document.getElementById("auth_button");
    const log_name = document.getElementById("log_name");
    const log_pass1 = document.getElementById("log_pass1");
    const log_pass2 = document.getElementById("log_pass2");
    const log_error_pass = document.getElementById("error_pass");
    const log_error_name = document.getElementById("error_name");

    log_error_name.style.display = 'none';
    log_error_pass.style.display = 'none';

    log_button.addEventListener("click", async () => {
        const name_text = log_name.value.trim();
        const pass1_text = log_pass1.value.trim();
        const pass2_text = log_pass2.value.trim();

        log_error_name.textContent = '';
        log_error_name.style.display = 'none';
        log_error_pass.textContent = '';
        log_error_pass.style.display = 'none';

        let hasError = false;

        if (name_text.length < 6) {
            log_error_name.textContent = "Логин должен быть больше 6 символов.";
            log_error_name.style.display = 'block';
            hasError = true;
        }
        else if (name_text.length > 50) {
            log_error_name.textContent = "Логин должен быть меньше 50 символов.";
            log_error_name.style.display = 'block';
            hasError = true;
        }

        if (pass1_text.length < 8) {
            log_error_pass.textContent = "Пароль должен быть больше 8 символов.";
            log_error_pass.style.display = 'block';
            hasError = true;
        }
        else if (pass1_text.length > 50) {
            log_error_pass.textContent = "Пароль должен быть меньше 50 символов.";
            log_error_pass.style.display = 'block';
            hasError = true;
        }
        else if (pass1_text !== pass2_text) {
            log_error_pass.textContent = "Пароли не совпадают.";
            log_error_pass.style.display = 'block';
            hasError = true;
        }

        if (!hasError) {
            const regSuccess = await addNewUser(name_text, pass1_text);
            if (!regSuccess) {
                log_error_pass.textContent = "Логин занят.";
                log_error_pass.style.display = 'block';
            }
        }
    });
});