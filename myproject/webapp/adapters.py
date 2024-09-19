from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

class MyAccountAdapter(DefaultAccountAdapter):
    def get_login_redirect_url(self, request):
        # Redirige al dashboard después del inicio de sesión
        return '/dashboard/'

    def save_user(self, request, user, form, commit=True):
        user = super().save_user(request, user, form, commit=False)
        # Agrega cualquier lógica personalizada aquí
        user.save()
        return user

class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        # Si el usuario ya existe, retorna (esto maneja el login)
        if sociallogin.is_existing:
            return

        # Si no existe, crea una cuenta
        user = sociallogin.user
        if not user.pk:
            user.set_unusable_password()  # Marca la contraseña como inutilizable
            user.save()
        sociallogin.connect(request, user)
