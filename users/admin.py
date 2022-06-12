from django.contrib import admin
from .models import Profile


@admin.site.register(Profile)
class ProfileAdmin(admin.AdminSite):
    readonly_field = ('id',)

