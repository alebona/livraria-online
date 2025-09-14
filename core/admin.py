from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, UserProfile

# Inline para exibir UserProfile dentro do CustomUser
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Perfil'

# Customização do UserAdmin
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    inlines = (UserProfileInline,)  # adiciona o perfil no user
    list_display = ("username", "email", "nome_completo", "cidade", "estado", "is_staff")
    search_fields = ("username", "email", "nome_completo")
    
    fieldsets = UserAdmin.fieldsets + (
        (None, {"fields": ("nome_completo", "endereco", "numero_endereco", "bairro", "cidade", "estado", "cep")}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {"fields": ("nome_completo", "endereco", "numero_endereco", "bairro", "cidade", "estado", "cep")}),
    )

# Opcional: manter UserProfile como modelo separado
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'perfil')
    list_filter = ('perfil',)
    search_fields = ('user__username', 'user__email')

