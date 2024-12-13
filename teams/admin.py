from django.contrib import admin
from .models import Team, TeamMembership
# Register your models here.

class TeamMembershipInline(admin.TabularInline):
    model = TeamMembership
    extra = 1
    
class TeamAdmin(admin.ModelAdmin):
    inlines = (TeamMembershipInline,)

admin.site.register(Team, TeamAdmin)
admin.site.register(TeamMembership)