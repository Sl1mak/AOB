"""
URL configuration for accounting_of_balances project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from aob import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path("", views.index, name='index'),
    path("createUser/", views.createUser, name='createUser'),
    path("loginUser/", views.loginUser, name='loginUser'),

    path("login", views.login),
    path("register", views.register),
    path("create_table", views.create_table, name='create_table'),
    path("delete_table/<int:table_id>/", views.delete_table, name='delete_table'),
 
    path("logout/", views.logout, name='logout'),

    path("table/<int:table_id>/add_row/", views.add_row, name='add_row'),
    path("table/<int:table_id>/edit_row/<int:row_id>/", views.edit_row, name='edit_row'),
    path("table/<int:table_id>/delete_row/<int:row_id>/", views.delete_row, name='delete_row'),
]
