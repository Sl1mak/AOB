from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.db import transaction
from .models import User, Table, Row, Column, Cell

def h_f(request):
    username = request.session.get("username")

def index(request):
    username = request.session.get("username")
    user_id = request.session.get("user_id")

    tables = Table.objects.filter(user_id=user_id)

    table_id = request.GET.get("table_id")
    table = None
    columns = []
    rows_data = []

    if table_id:
        table = get_object_or_404(
            Table.objects.prefetch_related("columns", "rows__cells"), 
            id=table_id,
            user_id=user_id
        )

        columns = list(table.columns.all())
        rows = list(table.rows.all())

        rows_data = []
        for row in table.rows.all():
            cell_value = []
            for col in columns:
                cell = next((c for c in row.cells.all() if c.column_id == col.id), None)
                cell_value.append(cell.value if cell else "")
            rows_data.append({
                "row": row,
                "cells": cell_value
            })

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
    user_id = request.session.get("user_id")    
    tables = Table.objects.filter(username_id=user_id)
    return render(request, "index.html", {"tables": tables, "username": request.session.get("username")})

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
def create_table(request):
    if request.method == "POST":
        user_id = request.session.get("user_id")
        if not user_id:
            return JsonResponse({"status": "error", "message": "Пользователь не авторизован."})

        user = get_object_or_404(User, id=user_id)
        name = request.POST.get("name")
        columns_names = request.POST.getlist("column_name[]")

        if not name:
            return JsonResponse({"status": "error", "message": "Введите название таблицы."})
        
        if Table.objects.filter(name=name, user=user).exists():
            return JsonResponse({"status": "error", "message": "Таблица с таким названием уже существует."})
        
        for col_name in columns_names:
            if not col_name:
                return JsonResponse({"status": "error", "message": "Введите названия всех колонок."})

        table = Table.objects.create(name=name, user=user)
        for col_name in columns_names:
            Column.objects.create(table=table, name=col_name)
        
        return JsonResponse({"status": "ok", "message": "Таблица успешно создана.", "table_id": table.id})

    return JsonResponse({"status": "error", "message": "Метод не поддерживается."}, status=400)

@transaction.atomic
def delete_table(request, table_id):
    table = get_object_or_404(Table, id=table_id)
    table.delete()
    return JsonResponse({"status": "ok", "message": "Таблица успешно удалена."})

@transaction.atomic
def add_row(request, table_id):
    table = get_object_or_404(Table, id=table_id)

    if request.method == "POST":
        row = Row.objects.create(table=table)
        for col in table.columns.all():
            value = request.POST.get(f"col-{col.id}", '')
            Cell.objects.create(row=row, column=col, value=value)
        return redirect(f"/?table_id={table.id}")

def delete_row(request, table_id, row_id):
    row = get_object_or_404(Row, id=row_id)
    row.delete()
    return redirect(f"/?table_id={table_id}")

def edit_row(request, table_id, row_id):
    row = get_object_or_404(Row, id=row_id)
    if request.method == "POST":
        for col in row.table.columns.all():
            value = request.POST.get(f"col-{col.id}", '')
            cell, _ = Cell.objects.get_or_create(row=row, column=col)
            cell.value = value
            cell.save()
        return redirect(f"/?table_id={table_id}")