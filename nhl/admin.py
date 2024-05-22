from django.contrib import admin

from nhl.models import NHLTeam


@admin.register(NHLTeam)
class NHLTeamsAdmin(admin.ModelAdmin):
    list_display = ("name", "conference", 'division')
