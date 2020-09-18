from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase


class UsersTests(APITestCase):
    def test_register_user(self):
        url = reverse('users_api:register')
        data = {
            'username': 'SimpleUser',
            'password': 'SimplePassword',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'SimpleUser')

    def test_get_token(self):
        url = reverse('users_api:token')
        data = {
            'username': 'SimpleUser',
            'password': 'SimplePassword',
        }
        user = User(username=data['username'])
        user.set_password(data['password'])
        user.save()
        user_token = Token.objects.create(user=user)

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['token'], user_token.key)
