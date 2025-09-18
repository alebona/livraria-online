from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import CustomUserCreationForm, PerfilUsuarioForm
from django.contrib.auth.decorators import login_required
from core.models import UserProfile


def registrar(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Cadastro realizado com sucesso! Faça login.")
            return redirect('login')  # redireciona para o login
        else:
            messages.error(request, "Ocorreu um erro no cadastro. Verifique os campos abaixo.")
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'core/registrar.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, f"Bem-vindo(a), {user.username}!")
            return redirect('home')  # redireciona para a home
        else:
            messages.error(request, "Usuário ou senha inválidos.")
    return render(request, 'core/login.html')

def logout_view(request):
    logout(request)
    messages.success(request, "Você saiu com sucesso.")
    return redirect('home')

@login_required
def perfil_usuario(request):
    user = request.user

    if request.method == 'POST':
        form = PerfilUsuarioForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Perfil atualizado com sucesso!")
            return redirect('perfil_usuario')  # redireciona para limpar o POST
    else:
        form = PerfilUsuarioForm(instance=user)

    return render(request, 'core/perfil_usuario.html', {'form': form})
