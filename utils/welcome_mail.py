from django.template.loader import render_to_string
from django.utils import timezone

def send_welcome_email(user):
    subject = "Bienvenue sur Staff"
    context = {
        "user": user,
        "app_name": "Staff",
        "year": timezone.now().year,
        "subject": subject,
    }

    html_message = render_to_string("emails/welcome_email.html", context)
    plain_message = f"Bonjour {user.first_name}, votre compte Staff est prêt."

    user.email_user(subject, plain_message, html_message=html_message)
