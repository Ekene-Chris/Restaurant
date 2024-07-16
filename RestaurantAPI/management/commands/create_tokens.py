from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class Command(BaseCommand):
    help = 'Creates tokens for all users that don\'t have one'

    def handle(self, *args, **kwargs):
        for user in User.objects.all():
            Token.objects.get_or_create(user=user)
            self.stdout.write(f'Token created for user: {user.username}')