from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from nba.models import NBATeam
from nba.serializers import NBATeamSerializer


class TeamsAPITestCase(APITestCase):
    def test_get(self):
        team_1 = NBATeam.objects.create(id=1, name="Team 1", conference="Western", division='Pacific',
                                        team_logo='images/team_logo1.png')
        team_2 = NBATeam.objects.create(id=2, name="Team 2", conference="Eastern", division='South West',
                                        team_logo='images/team_logo2.png')

        url = reverse('nba_teams-list')
        response = self.client.get(url)
        serializer_data = NBATeamSerializer([team_1, team_2], many=True).data

        for team in serializer_data:
            team['team_logo'] = f'http://testserver{team["team_logo"]}'

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(serializer_data, response.data)
