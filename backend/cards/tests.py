import datetime
import json

from dateutil.relativedelta import relativedelta
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from .models import CardSeries, CardNumber


class CardsTests(APITestCase):
    def setUp(self):
        data = {
            'username': 'SimpleUser',
            'password': 'SimplePassword',
        }
        self.user = User(username=data['username'])
        self.user.set_password(data['password'])
        self.user.save()
        self.user_token = Token.objects.create(user=self.user)
        self.now_date = datetime.datetime.now().date()

        CardSeries.objects.create(series=1)
        series_3 = CardSeries.objects.create(series=3)
        series_199 = CardSeries.objects.create(series=199)
        series_9999 = CardSeries.objects.create(series=9999)

        cards = [
            CardNumber(
                series=series_3,
                number=number,
                end_date=self.now_date + relativedelta(months=+3),
            )
            for number in range(1, 100)
        ]
        CardNumber.objects.bulk_create(cards)
        cards = [
            CardNumber(
                series=series_199,
                number=number,
                end_date=self.now_date + relativedelta(months=+12),
            )
            for number in range(199, 300)
        ]
        CardNumber.objects.bulk_create(cards)
        cards = [
            CardNumber(
                series=series_9999,
                number=number,
                end_date=self.now_date + relativedelta(months=+12),
            )
            for number in range(9999, 10849)
        ]
        CardNumber.objects.bulk_create(cards)

    def test_get_series(self):
        url = reverse('cards_api:series', kwargs={'series': '0001'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.user_token.key
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            json.loads(response.content),
            {
                'series': '0001',
                'max_number': 0,
                'available_numbers_count': 999999,
            },
        )

        url = reverse('cards_api:series', kwargs={'series': '002'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        url = reverse('cards_api:series', kwargs={'series': '03'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            json.loads(response.content),
            {
                'series': '0003',
                'max_number': 99,
                'available_numbers_count': 999900,
            },
        )

        url = reverse('cards_api:series', kwargs={'series': '199'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            json.loads(response.content),
            {
                'series': '0199',
                'max_number': 299,
                'available_numbers_count': 999700,
            },
        )

        url = reverse('cards_api:series', kwargs={'series': '9999'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            json.loads(response.content),
            {
                'series': '9999',
                'max_number': 10848,
                'available_numbers_count': 989151,
            },
        )

    def test_get_cards(self):
        url = reverse('cards_api:cards')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.user_token.key
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        content = json.loads(response.content)

        self.assertEqual(
            content[0],
            {
                'series': '0003',
                'number': '000001',
                'is_active': True,
                'start_date': self.now_date.isoformat(),
                'end_date': (
                        self.now_date + relativedelta(months=+3)
                ).isoformat()
            }
        )
        self.assertEqual(
            content[-1],
            {
                'series': '9999',
                'number': '010848',
                'is_active': True,
                'start_date': self.now_date.isoformat(),
                'end_date': (
                        self.now_date + relativedelta(months=+12)
                ).isoformat()
            }
        )
