from django.conf.urls.i18n import i18n_patterns
from django.urls import path, include
from django.contrib import admin
from webapp.views import microsoft_login_redirect

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),  # URL para cambiar el idioma
]

# Configuración de i18n_patterns
urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('accounts/microsoft/login/', microsoft_login_redirect, name='microsoft_login'),  # URL personalizada
    path('auth/', include('social_django.urls', namespace='social')),  # Incluye las URLs de social_django
    path('accounts/', include('allauth.urls')),  # Incluye las URLs de allauth
    path('', include('webapp.urls')),  # Incluye las URLs de tu aplicación web
    prefix_default_language=False  # Deshabilita el prefijo de idioma en las URLs
)
