from django.test import TestCase

from nba.models import NBATeam
from nba.serializers import NBATeamSerializer


class NBATeamSerializerTestCase(TestCase):
    def test_ok(self):
        team_1 = NBATeam.objects.create(id=1, name="Team 1", conference="Western", division='Pacific',
                                        team_logo='images/team_logo1.png')
        team_2 = NBATeam.objects.create(id=2, name="Team 2", conference="Eastern", division='South West',
                                        team_logo='images/team_logo2.png')

        data = NBATeamSerializer([team_1, team_2], many=True).data

        expected_data = [
            {
                "id": team_1.id,
                "name": "Team 1",
                "conference": "Western",
                "division": "Pacific",
                "team_logo": "/media/images/team_logo1.png",
            },
            {
                "id": team_2.id,
                "name": "Team 2",
                "conference": "Eastern",
                "division": "South West",
                "team_logo": "/media/images/team_logo2.png",
            }
        ]
        self.assertEqual(data, expected_data)