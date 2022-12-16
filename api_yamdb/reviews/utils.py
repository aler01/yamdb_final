import random
import string

from django.core.mail import send_mail

CONFIRMATION_CODE_LEN = 8


def send_mail_to_user(email, confirmation_code):
    send_mail(
        subject='Подтверждение регистрации на Yamdb',
        message='Благодарим за регистрацию на нашем сервисе. '
                f'Код подтверждения: {confirmation_code}',
        from_email='noreply@yamdb.local',
        recipient_list=[email],
        fail_silently=False,
    )


def generate_confirmation_code():
    return ''.join(random.choices(string.digits + string.ascii_uppercase,
                                  k=CONFIRMATION_CODE_LEN))
