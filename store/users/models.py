from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.db import models
from django.urls import reverse
from django.utils.timezone import now


class User(AbstractUser):
    image = models.ImageField(upload_to='users_images', null=True, blank=True)
    is_email_verification = models.BooleanField(default=False)


class EmailVerification(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    code = models.UUIDField(unique=True)
    created = models.DateTimeField(auto_now_add=True)
    expiration = models.DateTimeField()

    def __str__(self):
        return f'EmailVerification object {self.user.email}'

    def send_verification_email(self):
        link = reverse('users:email_verification',
                       kwargs={'email': self.user.email, 'code': self.code})
        verification_link = f'{settings.DOMAIN_NAME}{link}'
        subject = 'Подтврждение почты для учетной записи в StoreMust'
        message = '''Здравствуйте, {}
        Для подтвержения учетной записи в онлайн-магазине StoreMust {} перейдите по ссылке ниже
        {}'''.format(self.user.first_name, self.user.email, verification_link)
        send_mail(
            subject=subject,
            message=message,
            from_email='dedstasa@yandex.ru',
            recipient_list=(self.user.email,),
            fail_silently=False
        )

    def is_expired(self):
        return now() >= self.expiration
