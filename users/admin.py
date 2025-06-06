from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import GameUsers

# Register your models here.
admin.site.register(GameUsers, UserAdmin)
