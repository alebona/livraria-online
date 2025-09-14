from django.views.generic import RedirectView
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("core.urls")),
    path('gestao/', include('gestao.urls')),
    path('loja/', include('loja.urls')),

    # Redireciona a raiz para /loja/
    path("", RedirectView.as_view(url="/loja/", permanent=False)),
]
