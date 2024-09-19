from django.urls import path
from .views import index
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import set_language
from . import views
# from django.contrib.auth import views as auth_views  # Descomentado si decides usar vistas de Django para el restablecimiento de contraseña
from django.views.generic.base import TemplateView
from .views import blog_list, blog_create, blog_update, blog_delete
from .views import authenticate_google_user, get_user_data
# from .views import authenticate_microsoft_user
from django.urls import path, include
from webapp.views import facebook_register_redirect, microsoft_register_redirect

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('itservices/', views.itservices, name='itservices'),
    path('webservices/', views.webservices, name='webservices'),
    path('crmservices/', views.crmservices, name='crmservices'),
    path('chatbotservices/', views.chatbotservices, name='chatbotservices'),
    path('privacy/', views.privacy, name='privacy'),
    path('terms/', views.terms, name='terms'),
    path('services/', views.services, name='services'),
    path('calendly/', views.calendly, name='calendly'),
    path('portfolio/', views.portfolio, name='portfolio'),
    path('portfolio/home-v1/', views.portfolio_home_v1, name='portfolio_home_v1'),
    path('portfolio/home-v2/', views.portfolio_home_v2, name='portfolio_home_v2'),
    path('portfolio/home-v3/', views.portfolio_home_v3, name='portfolio_home_v3'),
    path('portfolio/home-v4/', views.portfolio_home_v4, name='portfolio_home_v4'),
    path('portfolio/home-v5/', views.portfolio_home_v5, name='portfolio_home_v5'),
    path('portfolio/home-v6/', views.portfolio_home_v6, name='portfolio_home_v6'),
    path('portfolio/home-v7/', views.portfolio_home_v7, name='portfolio_home_v7'),
    path('portfolio/home-v8/', views.portfolio_home_v8, name='portfolio_home_v8'),
    path('portfolio/home-v9/', views.portfolio_home_v9, name='portfolio_home_v9'),
    path('portfolio/home-v10/', views.portfolio_home_v10, name='portfolio_home_v10'),
    path('portfolio/home-v11/', views.portfolio_home_v11, name='portfolio_home_v11'),
    path('portfolio/home-v12/', views.portfolio_home_v12, name='portfolio_home_v12'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('set_language/', set_language, name='set_language'),
    path('password_reset/', views.password_reset_view, name='password_reset'),
    path('password_reset/done/', views.password_reset_done_view, name='password_reset_done'),
    path('reset/<uidb64>/<token>/', views.password_reset_confirm_view, name='password_reset_confirm'),
    path('reset/done/', views.password_reset_complete_view, name='password_reset_complete'),
    path('blogs/', blog_list, name='blog_list'),
    path('blogs/create/', blog_create, name='blog_create'),
    path('blogs/update/<int:pk>/', blog_update, name='blog_update'),
    path('blogs/delete/<int:pk>/', blog_delete, name='blog_delete'),
    path('<int:pk>/', views.blog_post_detail, name='blog_post_detail'),
    path('auth/register/facebook/', facebook_register_redirect, name='facebook_register'),
    path('auth/register/microsoft/', microsoft_register_redirect, name='microsoft_register'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'webapp.views.error_404_view'
handler500 = 'webapp.views.error_500_view'
