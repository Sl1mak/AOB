document.getElementById("logout_button").addEventListener("click", async () => {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const response = await fetch("/logout/", {
        method: "POST",
        headers: {
            "X-CSRFToken": csrfToken,
            "Content-Type": "application/x-www-form-urlencoded",
        },
    });

    const data = await response.json();

    if (data.status === "ok") {
        window.location.reload(); 
    }
});