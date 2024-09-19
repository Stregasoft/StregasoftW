from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from django.http import HttpResponseRedirect, HttpResponseServerError, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import EmailMessage, send_mail, EmailMultiAlternatives
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.utils import translation
from django.contrib.auth.views import (
    PasswordResetView, 
    PasswordResetDoneView, 
    PasswordResetConfirmView, 
    PasswordResetCompleteView
)
from .tokens import generate_token
from .models import PasswordResetAttempt, BlogPost
from .forms import ContactForm, BlogPostForm
import requests  # Este es el correcto, no se necesita google.auth.transport.requests
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import user_passes_test
from django.utils.translation import gettext as _
from django.http import JsonResponse
import json
from jwt import algorithms
from urllib.parse import urlencode
from django.shortcuts import redirect
from django.utils.html import strip_tags

MICROSOFT_CLIENT_ID = "181cfc29-d421-4aad-aced-46ddeb4c323f"
COOKIE_SECRET = "6zuN6HJp5I"

def is_admin(user):
    return user.is_superuser

# Decorador para permitir el acceso solo a los usuarios no autenticados
def unauthenticated_user(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def index(request):
    return render(request, 'index.html')

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == "POST":
        username = request.POST["username"]
        pass1 = request.POST["pass1"]
        user = authenticate(request, username=username, password=pass1)
        if user is not None:
            auth_login(request, user)
            # Mensaje de éxito al iniciar sesión en inglés
            messages.success(request, _("Successfully logged in as {0}.").format(user.username))
            return redirect('index')
        else:
            # Mensaje de error en inglés
            messages.error(request, _("Bad credentials!"))
            return redirect('login')
    
    return render(request, "login.html")


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == "POST":
        username = request.POST["username"]
        fname = request.POST["fname"]
        lname = request.POST["lname"]
        email = request.POST["email"]
        pass1 = request.POST["pass1"]
        pass2 = request.POST["pass2"]
        recaptcha_response = request.POST.get('g-recaptcha-response')

        data = {
            'secret': settings.RECAPTCHA_SECRET_KEY,
            'response': recaptcha_response
        }
        r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
        result = r.json()

        if not result['success']:
            messages.error(request, _("Invalid reCAPTCHA. Please try again."))
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, _("Username already exists! Please try some other username."))
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, _("Email Already Registered!"))
            return redirect('register')

        if len(username) > 20:
            messages.error(request, _("Username must be under 20 characters!"))
            return redirect('register')

        if pass1 != pass2:
            messages.error(request, _("Passwords didn't match!"))
            return redirect('register')

        if not username.isalnum():
            messages.error(request, _("Username must be Alpha-Numeric!"))
            return redirect('register')

        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.is_active = False
        myuser.save()
        messages.success(request, _("Your Account has been created successfully! Please check your email to confirm your email address in order to activate your account."))

        # Enviar correo de bienvenida con HTML y CSS
        subject = _("Welcome to Stregasoft!")
        html_message = """
        <html>
            <body>
                <h2 style="color: #1D4999;">{subject}</h2>
                <p>{greeting} {name},</p>
                <p>{welcome_message}</p>
                <p>{thank_you},<br>{company}</p>
            </body>
        </html>
        """.format(
            subject=subject,
            greeting=_("Hello"),
            name=myuser.first_name,
            welcome_message=_("Welcome to Stregasoft! Thank you for visiting our website. We have also sent you a confirmation email, please confirm your email address."),
            thank_you=_("Thanking You"),
            company="Stregasoft"
        )
        
        # Convertir el mensaje HTML a texto sin formato
        text_message = strip_tags(html_message)

        # Enviar correo con formato HTML
        email = EmailMultiAlternatives(
            subject=subject,
            body=text_message,
            from_email=settings.EMAIL_HOST_USER,
            to=[myuser.email]
        )
        email.attach_alternative(html_message, "text/html")
        email.send(fail_silently=True)

        # Preparar el correo de confirmación de email con CSS y HTML
        current_site = get_current_site(request)
        email_subject = _("Confirm your Email @ Stregasoft!")
        message2 = render_to_string('email_confirmation.html', {
            'name': myuser.first_name,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
            'token': generate_token.make_token(myuser)
        })

        # Convertir el mensaje HTML a texto sin formato
        text_message = strip_tags(message2)

        # Enviar correo con formato HTML
        email = EmailMultiAlternatives(
            subject=email_subject,
            body=text_message,
            from_email=settings.EMAIL_HOST_USER,
            to=[myuser.email]
        )
        email.attach_alternative(message2, "text/html")
        email.send(fail_silently=True)

        return redirect('login')

    return render(request, "register.html", {'RECAPTCHA_SITE_KEY': settings.RECAPTCHA_SITE_KEY})

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and generate_token.check_token(user, token):
        user.is_active = True
        user.save()
        auth_login(request, user)
        messages.success(request, _("Your Account has been activated!"))
        return redirect('index')
    else:
        return render(request, 'activation_failed.html')

def logout_view(request):
    auth_logout(request)
    messages.success(request, _("Logged out successfully!"))
    return redirect("login")

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

# Otras vistas
def about(request):
    return render(request, 'about.html')

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        recaptcha_response = request.POST.get('g-recaptcha-response')
        recipient_list = ['admin@stregasoft.com']  # Correo al que llegan los mensajes

        # Validación de campos obligatorios
        if not name or not last_name or not message:
            messages.error(request, _('Name, Last Name, and Message are required fields.'))
            return render(request, 'contact.html', {
                'RECAPTCHA_SITE_KEY': settings.RECAPTCHA_SITE_KEY
            })

        # Validar reCAPTCHA
        data = {
            'secret': settings.RECAPTCHA_SECRET_KEY,
            'response': recaptcha_response
        }
        r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
        result = r.json()

        if not result['success']:
            messages.error(request, _("Invalid reCAPTCHA. Please try again."))
            return render(request, 'contact.html', {
                'RECAPTCHA_SITE_KEY': settings.RECAPTCHA_SITE_KEY
            })

        # Preparar el mensaje HTML con estilo
        html_message = """
        <html>
            <head></head>
            <body>
                <h2 style="color: #1D4999;">Contact Form Submission</h2>
                <p><strong>Name:</strong> {0} {1}</p>
                <p><strong>Email:</strong> {2}</p>
                <p><strong>Phone:</strong> {3}</p>
                <p><strong>Message:</strong></p>
                <p>{4}</p>
            </body>
        </html>
        """.format(name, last_name, email, phone or _('N/A'), message)

        # Convertir el mensaje HTML a texto sin formato
        text_message = strip_tags(html_message)

        # Enviar correo con formato HTML
        try:
            email = EmailMultiAlternatives(
                subject=_("Contact Form Submission"),
                body=text_message,
                from_email='admin@stregasoft.com',
                to=recipient_list
            )
            email.attach_alternative(html_message, "text/html")
            email.send(fail_silently=False)
            messages.success(request, _('The message has been sent successfully. We will reach back soon!'))
        except Exception as e:
            messages.error(request, _('Error sending email: {0}').format(e))
    
    return render(request, 'contact.html', {
        'RECAPTCHA_SITE_KEY': settings.RECAPTCHA_SITE_KEY
    })
    
def itservices(request):
    return render(request, 'itservices.html')

def webservices(request):
    return render(request, 'webservices.html')

def crmservices(request):
    return render(request, 'crmservices.html')

def chatbotservices(request):
    return render(request, 'chatbotservices.html')

def privacy(request):
    return render(request, 'privacy.html')

def terms(request):
    return render(request, 'terms.html')

def services(request):
    return render(request, 'services.html')

def calendly(request):
    return render(request, 'calendly.html')

def portfolio(request):
    return render(request, 'portfolio.html')

def portfolio_home_v1(request):
    return render(request, 'portfolio_home_v1.html')

def portfolio_home_v2(request):
    return render(request, 'portfolio_home_v2.html')

def portfolio_home_v3(request):
    return render(request, 'portfolio_home_v3.html')

def portfolio_home_v4(request):
    return render(request, 'portfolio_home_v4.html')

def portfolio_home_v5(request):
    return render(request, 'portfolio_home_v5.html')

def portfolio_home_v6(request):
    return render(request, 'portfolio_home_v6.html')

def portfolio_home_v7(request):
    return render(request, 'portfolio_home_v7.html')

def portfolio_home_v8(request):
    return render(request, 'portfolio_home_v8.html')

def portfolio_home_v9(request):
    return render(request, 'portfolio_home_v9.html')

def portfolio_home_v10(request):
    return render(request, 'portfolio_home_v10.html')

def portfolio_home_v11(request):
    return render(request, 'portfolio_home_v11.html')

def portfolio_home_v12(request):
    return render(request, 'portfolio_home_v12.html')

def error_404_view(request, exception):
    return render(request, '404.html', status=404)

def error_500_view(request):
    return render(request, '500.html', status=500)

def password_reset_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            try:
                user = User.objects.get(email=email)
                reset_attempt, created = PasswordResetAttempt.objects.get_or_create(user=user)
                if reset_attempt.attempts >= 3:
                    messages.error(request, _("You have exceeded the password reset limit. Please contact support."))
                    return redirect('password_reset')

                reset_attempt.attempts += 1
                reset_attempt.save()

                subject = _("Password Reset Request")
                html_message = render_to_string('password_reset_email.html', {
                    'user': user,
                    'domain': get_current_site(request).domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': generate_token.make_token(user),
                })
                text_message = strip_tags(html_message)

                email_message = EmailMultiAlternatives(
                    subject=subject,
                    body=text_message,
                    from_email=settings.EMAIL_HOST_USER,
                    to=[email]
                )
                email_message.attach_alternative(html_message, "text/html")
                email_message.send(fail_silently=False)

                messages.success(request, _("A password reset link has been sent to your email."))
                return redirect('login')
            except User.DoesNotExist:
                messages.error(request, _("Email address not found. Please check and try again."))
                return redirect('password_reset')
    return render(request, 'password_reset.html')


def password_reset_done_view(request):
    return render(request, 'password_reset_done.html')


def password_reset_confirm_view(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and generate_token.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, _("Your password has been reset successfully. You can now log in with your new password."))
                return redirect('login')
            else:
                messages.error(request, _("Passwords do not match or are empty. Please try again."))
        else:
            form = SetPasswordForm(user)
        return render(request, 'password_reset_confirm.html', {'form': form})
    else:
        messages.error(request, _("The reset link is invalid or has expired. Please try resetting your password again."))
        return redirect('password_reset')


def password_reset_complete_view(request):
    return render(request, 'password_reset_complete.html')

#blog view


def blog_list(request):
    posts = BlogPost.objects.all()
    return render(request, 'blog_list.html', {'posts': posts})

@user_passes_test(lambda u: u.is_superuser)
def blog_create(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)  # Maneja archivos
        if form.is_valid():
            blog_post = form.save(commit=False)
            blog_post.author = request.user
            blog_post.save()
            return redirect('blog_list')
    else:
        form = BlogPostForm()
    return render(request, 'blog_form.html', {'form': form})

@user_passes_test(lambda u: u.is_superuser)
def blog_update(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES, instance=post)  # Maneja archivos
        if form.is_valid():
            form.save()
            return redirect('blog_list')
    else:
        form = BlogPostForm(instance=post)
    return render(request, 'blog_form.html', {'form': form})

@user_passes_test(lambda u: u.is_superuser)
def blog_delete(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    if request.method == 'POST':
        post.delete()
        return redirect('blog_list')
    return render(request, 'blog_confirm_delete.html', {'post': post})


def blog_post_detail(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    return render(request, 'blog_post_detail.html', {'post': post})


@csrf_exempt
def authenticate_google_user(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            token = data.get('id_token')
            idinfo = id_token.verify_oauth2_token(token, requests.Request(), GOOGLE_CLIENT_ID)
            user_id = idinfo["sub"]

            auth_cookie = jwt.encode({"user_id": user_id}, COOKIE_SECRET_KEY, algorithm="HS256")
            response = JsonResponse({"status": "success"})
            response.set_cookie(key="auth_cookie", value=auth_cookie)
            return response

        except ValueError as e:
            return JsonResponse({"status": "error", "message": str(e)})
    return JsonResponse({"status": "error", "message": "Invalid request"})

def get_user_data(request):
    auth_cookie = request.COOKIES.get('auth_cookie')
    if auth_cookie:
        try:
            payload = jwt.decode(auth_cookie, settings.SECRET_KEY, algorithms=["HS256"])
            user_id = payload.get("user_id")
            return JsonResponse({"status": "success", "data": "user data"})
        except jwt.exceptions.InvalidTokenError:
            return JsonResponse({"status": "error", "message": "Invalid token"})
    return JsonResponse({"status": "error", "message": "No token provided"})



def microsoft_login_redirect(request):
    base_url = "https://login.microsoftonline.com/common/oauth2/v2.0/authorize"
    params = {
        "client_id": settings.SOCIALACCOUNT_PROVIDERS['microsoft']['APP']['client_id'],
        "response_type": "code",
        "redirect_uri": settings.SOCIALACCOUNT_PROVIDERS['microsoft']['AUTH_PARAMS']['redirect_uri'],
        "scope": "User.Read",
    }
    
    login_url = f"{base_url}?{urlencode(params)}"
    return redirect(login_url)


def facebook_register_redirect(request):
    base_url = "https://www.facebook.com/v9.0/dialog/oauth"
    params = {
        "client_id": settings.SOCIAL_AUTH_FACEBOOK_KEY,
        "redirect_uri": settings.SOCIAL_AUTH_FACEBOOK_REDIRECT_URI,
        "scope": ','.join(settings.SOCIAL_AUTH_FACEBOOK_SCOPE),
        "response_type": "code",
    }
    register_url = f"{base_url}?{urlencode(params)}"
    return redirect(register_url)

def microsoft_register_redirect(request):
    base_url = "https://login.microsoftonline.com/common/oauth2/v2.0/authorize"
    params = {
        "client_id": settings.SOCIALACCOUNT_PROVIDERS['microsoft']['APP']['client_id'],
        "response_type": "code",
        "redirect_uri": settings.SOCIALACCOUNT_PROVIDERS['microsoft']['AUTH_PARAMS']['redirect_uri'],
        "scope": "User.Read",
    }
    register_url = f"{base_url}?{urlencode(params)}"
    return redirect(register_url)