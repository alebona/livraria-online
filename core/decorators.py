from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

""" Decorador para verificar perfil do usuário """
def perfil_required(perfil):
    def decorator(view_func):
        @login_required
        def _wrapped_view(request, *args, **kwargs):
            if hasattr(request.user, 'userprofile') and request.user.userprofile.perfil == perfil:
                return view_func(request, *args, **kwargs)
            return redirect('home')  # ou outra página de acesso negado
        return _wrapped_view
    return decorator
