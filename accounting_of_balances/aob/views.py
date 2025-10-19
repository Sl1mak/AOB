from django.http import JsonResponse
from django.shortcuts import render
from .models import User

def h_f(request):
    username = request.sessions.get("username")

def index(request):
    return render(request, "index.html")

def login(request):
    return render(request, "login.html")

def register(request):
    return render(request, "register.html")

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
    return JsonResponse({"status": "ok", "message": "Выход из аккаунта."})