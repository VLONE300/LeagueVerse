from django.contrib import admin

from nba.models import NBATeam


@admin.register(NBATeam)
class NBATeamsAdmin(admin.ModelAdmin):
    list_display = ("name", "conference", 'division')
