from celery import shared_task
from django.conf import settings
from django.utils import timezone

from agir.people.actions.mailing import send_mosaico_email


def interleave_spaces(s, n=3):
    return ' '.join([s[i:i+n] for i in range(0, len(s), n)])


@shared_task
def send_login_email(email, short_code, expiry_time):
    utc_expiry_time = timezone.make_aware(timezone.datetime.utcfromtimestamp(expiry_time), timezone.utc)
    local_expiry_time = timezone.localtime(utc_expiry_time)

    send_mosaico_email(
        code='LOGIN_MESSAGE',
        subject="Connexion à agir.lafranceinsoumise.fr",
        from_email=settings.EMAIL_FROM,
        bindings={
            'CODE': interleave_spaces(short_code),
            'EXPIRY_TIME': local_expiry_time.strftime("%H:%M")
        },
        recipients=[email]
    )
