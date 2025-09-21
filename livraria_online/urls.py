from django.views.generic import RedirectView
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
path('admin/', admin.site.urls),
    path('core/', include('core.urls')),
    path('gestao/', include('gestao.urls')),
    path('loja/', include('loja.urls')),
    path("", RedirectView.as_view(url="/loja/", permanent=False)),
]
