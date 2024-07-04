from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from nba.models import NBATeam, NBAStanding
from nba.serializers import NBATeamSerializer, NBAStandingsSerializer


class TeamsAPITestCase(APITestCase):
    def setUp(self):
        pass

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


class StandingsAPITestCase(APITestCase):
    def setUp(self):
        self.team = NBATeam.objects.create(id=1, name="Team 1", conference="Western", division='Pacific',
                                           team_logo='images/team_logo1.png')

        self.standings = NBAStanding.objects.create(
            wins=1, losses=1, team=self.team, winning_percentage=0.6,
            games_back='19.0', points_percentage_game=0.5, oop_points_percentage_game=0.5)

    def test_get(self):
        url = reverse('nba_standings-list')
        response = self.client.get(url)

        serializer_data = NBAStandingsSerializer(self.standings).data
        serializer_data['team']['team_logo'] = f'http://testserver{serializer_data["team"]["team_logo"]}'
        expected_data = {
            self.team.conference: [serializer_data]
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(expected_data, response.data)
