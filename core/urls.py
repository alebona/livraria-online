from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("registrar/", views.registrar, name="registrar"),
    path("login/", auth_views.LoginView.as_view(template_name="core/login.html"), name="login"),
    path('logout/', views.logout_view, name='logout'),
]
