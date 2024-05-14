from django.contrib import admin
from leagues.models import League, NBATeams, NHLTeams


@admin.register(NBATeams)
class NBATeamsAdmin(admin.ModelAdmin):
    list_display = ("name", "conference", 'division')


@admin.register(NHLTeams)
class NHLTeamsAdmin(admin.ModelAdmin):
    list_display = ("name", "conference", 'division')


admin.site.register(League)
