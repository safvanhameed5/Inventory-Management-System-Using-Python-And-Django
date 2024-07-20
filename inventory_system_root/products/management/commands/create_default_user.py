from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Creates a default user'

    def handle(self, *args, **kwargs):
        if not User.objects.filter(username='defaultuser').exists():
            User.objects.create_user(
                username='defaultuser',
                password='defaultpassword',
                email='default@example.com'
            )
            self.stdout.write(self.style.SUCCESS('Successfully created default user'))
        else:
            self.stdout.write(self.style.SUCCESS('Default user already exists'))
