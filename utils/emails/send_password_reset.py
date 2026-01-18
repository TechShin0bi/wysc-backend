from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils import timezone
from django.urls import reverse
from django.core.mail import EmailMultiAlternatives
from utils.emails.send_password_reset import password_reset_token , account_activation_token , send_password_reset_email

def send_password_reset_email(user, request):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = password_reset_token.make_token(user)
    reset_url = request.build_absolute_uri(f"/auth/reset-password/{uid}/{token}/")

    html_content = render_to_string("emails/password_reset_email.html", {
        "user": user,
        "reset_url": reset_url,
    })

    message = EmailMultiAlternatives(
        subject="Réinitialisation du mot de passe",
        body="",
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user.email],
    )
    message.attach_alternative(html_content, "text/html")
    message.send()



def send_activation_email(request, user):
    subject = "Activez votre compte Staff"

    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = account_activation_token.make_token(user)

    activation_url = f"{request.scheme}://{request.get_host()}{reverse('activate-account', kwargs={'uidb64': uid, 'token': token})}"

    context = {
        "user": user,
        "activation_url": activation_url,
        "app_name": "Staff",
        "year": timezone.now().year,
        "subject": subject,
    }

    html_message = render_to_string("emails/activate_account.html", context)
    text_message = f"Bonjour {user.first_name}, activez votre compte: {activation_url}"

    user.email_user(subject, text_message, html_message=html_message)




def send_password_reset_email(user, request):
	token = PasswordResetTokenGenerator().make_token(user)
	uid = urlsafe_base64_encode(force_bytes(user.pk))
	reset_url = f"http://{request.get_host()}/reset-password-confirm/?uid={uid}&token={token}"
	send_mail(
		'Password Reset',
		f'Click the link to reset your password: {reset_url}',
		settings.DEFAULT_FROM_EMAIL,
		[user.email],
		fail_silently=False,
	)
