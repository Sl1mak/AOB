async function login(username, password) {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const response = await fetch("/loginUser/", {
        method: "POST",
        headers: {
            "X-CSRFToken": csrfToken,
            "Content-Type": "application/x-www-form-urlencoded",
        },
        body: `username=${username}&password=${password}`,
    });

    const data = await response.json();

    if (response.ok && data.status === "ok") {
        window.location.href = '/';
        return true;
    } else {
        console.log("Error: ", data.message);
        return false;
    }
}

document.addEventListener("DOMContentLoaded",  () => {
    const log_button = document.getElementById("auth_button");
    const log_name = document.getElementById("log_name");
    const log_pass = document.getElementById("log_pass");
    const log_error_pass = document.getElementById("error");

    log_error_pass.style.display = 'none';

    log_button.addEventListener("click", async () => {
        const name_text = log_name.value.trim();
        const pass_text = log_pass.value.trim();

        log_error_pass.textContent = '';
        log_error_pass.style.display = 'none';

        let hasError = false;

        if (name_text.length < 6) {
            hasError = true;
        }
        else if (name_text.length > 50) {
            hasError = true;
        }

        if (pass_text.length < 8) {
            hasError = true;
        }
        else if (pass_text.length > 50) {
            hasError = true;
        }

        if (hasError) {
            if (log_error_pass) {
                log_error_pass.textContent = "Ошибка логина или пароля.";
                log_error_pass.style.display = 'block';
            }
        } else {
            const loginSuccess = await login(name_text, pass_text);
            if (!loginSuccess) {
                if (log_error_pass) {
                    log_error_pass.textContent = "Ошибка логина или пароля.";
                    log_error_pass.style.display = 'block';
                }
            } else {
                console.log("Успешный вход");
            }
        }
    });
});