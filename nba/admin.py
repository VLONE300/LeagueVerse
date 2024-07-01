from django.contrib import admin

from nba.models import NBATeam, NBAGame, NBABoxScore, NBATeamStats


@admin.register(NBATeam)
class NBATeamsAdmin(admin.ModelAdmin):
    list_display = ("name", "conference", 'division')


@admin.register(NBAGame)
class NBAGamesAdmin(admin.ModelAdmin):
    list_display = ('date', "visitor_team", 'visitor_pts', 'home_team', 'home_pts',)


admin.site.register(NBABoxScore)
admin.site.register(NBATeamStats)
