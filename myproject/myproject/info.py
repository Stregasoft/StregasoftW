EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.office365.com'  # Cambiar el host al de Outlook
EMAIL_HOST_USER = 'admin@stregasoft.com'  # Reemplaza con tu dirección de correo de Outlook
EMAIL_HOST_PASSWORD = 'kxbbntgyfjdwdhxd'  # Usa una contraseña generada en la página de seguridad de tu cuenta Microsoft (App Password)
EMAIL_PORT = 587  # El puerto sigue siendo el mismo

