from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.db import transaction
from .models import User, Table, Row, Column, Cell

def h_f(request):
    username = request.session.get("username")

def index(request):
    username = request.session.get("username")
    tables = Table.objects.all()

    table_id = request.GET.get("table_id")
    table = None
    columns = []
    rows_data = []

    if table_id:
        table = get_object_or_404(
            Table.objects.prefetch_related("columns", "rows__cells"), 
            id=table_id
        )

        columns = list(table.columns.all())

        for row in table.rows.all():
            cells = []
            for col in columns:
                cell = next((c for c in row.cells.all() if c.column_id == col.id), None)
                cells.append(cell.value if cell else "")
            rows_data.append(cells)

    context = {
        "username": username,
        "tables": tables,
        "table": table,
        "columns": columns,
        "rows": rows_data
    }

    return render(request, "index.html", context)

def login(request):
    return render(request, "login.html")

def register(request):
    return render(request, "register.html")

def createtable(request):
    return render(request, "createtable.html")

def createUser(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        users = User.objects.filter(username=username)
        if not users.exists():
            user = User.objects.create(username=username, password=password)
            if user:
                request.session["user_id"] = user.id
                request.session["username"] = username
                return JsonResponse({
                    "status": "ok",
                    "message": "Новый пользователь добавлен."
                })
            else:
                return JsonResponse({
                    "status": "error",
                    "message": "Пользователь не добавлен."
                })
        else:
            return JsonResponse ({
                "status": "error",
                "message": "Логин занят."
            })

def loginUser(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if not username or not password:
            return JsonResponse({"status": "error", "message": "Введите логин и пароль."})
        
        users = User.objects.filter(username=username)
        if not users.exists():
            return JsonResponse({"status": "error", "message": "Пользователь не найден."})
        
        user = users.first()
        if user.password == password:
            request.session["user_id"] = user.id
            request.session["username"] = username
            return JsonResponse({"status": "ok", "message": "Вход выполнен."})
        else:
            return JsonResponse({"status": "error", "message": "Ошибка входа."})

def logout(request):
    request.session.flush()
    return JsonResponse({"status": "ok", "message": "Выход из аккаунта.",})

def table_list(request):
    tables = Table.objects.all()
    return render(request, "index.html", {"tables": tables})

def table_view(request):
    table = get_object_or_404(Table.objects.prefetch_related("columns", "rows__cells"), id=table_id)
    columns = list(table.columns.all())
    rows_data = []
    for row in table.rows.all():
        row_map = {col.id: "" for col in columns}
        for cell in row.cells.all():
            row_map[cell.column_id] = cell.value
        rows_data.append({'row': row, 'cells': row_map})
    
    return render(request, "index.html", {'table': table, 'columns': columns, 'rows': rows_data})

@transaction.atomic
def add_row(request, table_id):
    table = get_object_or_404(Table, id=table_id)

    if request.method == "POST":
        row = Row.objects.create(table=table)
        for col in table.columns.all():
            value = request.POST.get(f"col-{col.id}", '')
            Cell.objects.create(row=row, column=col, value=value)
        return redirect(f"/?table_id={table.id}")