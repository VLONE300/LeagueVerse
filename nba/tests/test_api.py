from django.urls import reverse
from rest_framework.test import APITestCase


class TeamsAPITestCase(APITestCase):
    def test_get(self):
        url = reverse('nba_teams')
        print(url)
        response = self.client.get(url)
        print(response)