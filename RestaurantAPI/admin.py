from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.admin import TokenAdmin


# Register out own model admin, based on the default TokenAdmin
admin.register(Token)