document.addEventListener("DOMContentLoaded", async () => {
    const add_row_modal = document.getElementById("add_row_modal");
    const add_row_button = document.getElementById("add_row_button");
    const add_row_span = document.getElementsByClassName("close")[0];

    const create_table_button = document.getElementById("create_table_open_modal_button");
    const create_table_modal = document.getElementById("create_table_modal");
    const create_table_span = document.getElementById("close_table_modal");
    const create_table_form = document.getElementById("create_table_form");
    const columns_cont = document.getElementById("columns_container");
    const add_column_button = document.getElementById("add_column_button");
    const status_message = document.getElementById("status_message");
    const delete_table_button = document.getElementById("delete_table_button");

    const editModal = document.getElementById("edit_row_modal");
    const editForm = document.getElementById("edit_row_form");
    const closeEditModal = document.getElementById("close_edit_row_modal");

    /*Add row*/
    if (add_row_button) {
        add_row_button.onclick = () => {
            add_row_modal.style.display = "block";
        }   
    }

    if (add_row_span) {
        add_row_span.onclick = () => {
            add_row_modal.style.display = "none";
        }
        window.onclick = (event) => {if (event.target == add_row_modal ) add_row_modal.style.display = "none"; }
    }


    /*Add table*/
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    create_table_button.addEventListener("click", () => {
        create_table_modal.style.display = "block";
    });

    create_table_span.addEventListener("click", () => {
        create_table_modal.style.display = "none";
    });

    window.addEventListener("click", (event) => {
        if (event.target === create_table_modal) create_table_modal.style.display = "none";
    });

    columns_cont.addEventListener("click", (event) => {
        if (event.target.classList.contains("delete_column_button")) {
            event.preventDefault();
            event.target.closest(".column_item").remove();
        }
    })

    add_column_button.addEventListener("click", () => {
        const div = document.createElement("div");
        div.classList.add("column_item");
        div.innerHTML = `
            <input type="text" name="column_name[]" placeholder="Название колонки" class="column_input">
            <button type="button" class="delete_column_button">Удалить</button>
        `;

        columns_cont.appendChild(div);
    });

    if (delete_table_button) {
        delete_table_button.addEventListener("click", async () => {
        const table_id = delete_table_button.getAttribute("data-table-id");
        const response = await fetch(`/delete_table/${table_id}/`, {
            "method": "POST",
            "headers": {
                "X-CSRFToken": csrfToken,
            },
            });
            const data = await response.json();

            if (data.status === "ok") {
                alert(data.message);
                window.location.href = '/';
            } else {
                alert("Ошибка при удалении таблицы");
            } 
        });
    }

    create_table_form.addEventListener("submit", async (event) => {
        event.preventDefault();

        const formData = new FormData(create_table_form);

        const response = await fetch("/create_table", {
            "method": "POST",
            "headers": {
                "X-CSRFToken": csrfToken,
            },
            "body": formData,
        });

        const data = await response.json();

        status_message.textContent = data.message;
        if (data.status === "ok") {
            status_message.style.color = "limegreen";
            create_table_form.reset();
            create_table_modal.style.display = "none";
            window.location.reload();
        } else {
            status_message.style.color = "red";
        }
    });

    /*Edit row*/
    document.querySelectorAll(".edit_row_button").forEach((button) => {
        button.addEventListener("click", () => {
            const rowId = button.dataset.rowId;
            const tableId = button.dataset.tableId;

            // Меняем action формы на нужную строку
            editForm.action = `/table/${tableId}/edit_row/${rowId}/`;

            // (опционально) можно заполнить поля из таблицы, если хочешь
            editModal.style.display = "block";
        });
    });

    // закрытие модалки
    closeEditModal.addEventListener("click", () => {
        editModal.style.display = "none";
    });

    window.addEventListener("click", (event) => {
        if (event.target === editModal) editModal.style.display = "none";
    });
});
