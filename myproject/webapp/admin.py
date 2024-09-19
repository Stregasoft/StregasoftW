from django.contrib import admin
from django.shortcuts import redirect
from .models import PasswordResetAttempt

class PasswordResetAttemptAdmin(admin.ModelAdmin):
    # Muestra las columnas user y attempts en la lista del panel de administración
    list_display = ('user', 'attempts')
    
    # Añade una acción personalizada al administrador
    actions = ['reset_selected_attempts']

    # Define la acción para reiniciar intentos de restablecimiento
    def reset_selected_attempts(self, request, queryset):
        queryset.update(attempts=0)  # Reinicia el contador de intentos
        self.message_user(request, 'Se han reiniciado los intentos de restablecimiento seleccionados.')

    # Define la descripción corta de la acción para la interfaz
    reset_selected_attempts.short_description = 'Reiniciar intentos seleccionados'

# Registra el modelo con las opciones de administración personalizadas
admin.site.register(PasswordResetAttempt, PasswordResetAttemptAdmin)


# Restricción para el acceso al panel de administración
def admin_only(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_superuser:
            return redirect('index')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

# Aplicar la restricción al panel de administración
admin.site.login = admin_only(admin.site.login)