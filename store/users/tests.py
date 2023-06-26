from datetime import timedelta
from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse
from django.utils.timezone import now

from users.models import EmailVerification, User


class TestRegistrationView(TestCase):

    def setUp(self) -> None:
        self.path = reverse('users:registration')
        self.test_user = {
            'first_name': 'Stas',
            'last_name': 'Belosludcev',
            'username': 'stas224',
            'email': 'stas@stas.ru',
            'password1': '1234567890Qq',
            'password2': '1234567890Qq',
        }

    def test_user_registration_get(self):
        response = self.client.get(self.path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.context_data['title'], 'StoreMust - Регистрация')
        self.assertTemplateUsed(response, 'users/registration.html')

    def test_user_registration_post(self):
        username = self.test_user['username']
        self.assertFalse(User.objects.filter(username=username))

        response = self.client.post(self.path, self.test_user)

        # check creating of user
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('users:login'))
        self.assertTrue(User.objects.filter(username=username).exists())

        # check email verification
        email_verification = EmailVerification.objects.filter(user__username=username)
        self.assertTrue(email_verification.exists())
        self.assertEqual(
            email_verification.first().expiration.date(),
            (now() + timedelta(hours=48)).date()
        )

    def test_user_registration_error(self):
        username = self.test_user['username']
        User.objects.create(username=username)
        response = self.client.post(self.path, self.test_user)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, 'Пользователь с таким именем уже существует.', html=True)

