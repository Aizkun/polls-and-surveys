from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Poll

admin.site.register(Poll)
