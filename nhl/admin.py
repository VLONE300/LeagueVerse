from django.contrib import admin

from nhl.models import NHLTeam, NHLGame, NHLBoxScore, NHLTeamStats


@admin.register(NHLTeam)
class NHLTeamsAdmin(admin.ModelAdmin):
    list_display = ("name", "conference", 'division')


@admin.register(NHLGame)
class NBAGamesAdmin(admin.ModelAdmin):
    list_display = ('date', "visitor_team", 'visitor_pts', 'home_team', 'home_pts',)


admin.site.register(NHLBoxScore)
admin.site.register(NHLTeamStats)
