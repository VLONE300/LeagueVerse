from django.contrib import admin
from leagues.models import League, NBATeams, NHLTeams

admin.site.register(League)
admin.site.register(NBATeams)
admin.site.register(NHLTeams)
