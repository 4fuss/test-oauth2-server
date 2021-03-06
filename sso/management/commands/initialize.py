from django.contrib.auth import get_user_model
from django.core.management import BaseCommand
from django.urls import reverse
from oauth2_provider.models import Application


class Command(BaseCommand):
    """Database initialization command."""

    ADMIN_USERNAME = 'admin'
    ADMIN_EMAIL = 'admin@example.com'
    ADMIN_PASSWORD = 'admin'

    def create_admin_user(self):
        user_cls = get_user_model()
        user = user_cls.objects.get_or_create(
            username=self.ADMIN_USERNAME,
            email=self.ADMIN_EMAIL,
            is_superuser=True,
            is_staff=True,
            is_active=True,
        )[0]
        user.set_password(self.ADMIN_PASSWORD)
        user.save()
        return user

    @staticmethod
    def create_app():
        return Application.objects.get_or_create(
            client_type=Application.CLIENT_CONFIDENTIAL,
            authorization_grant_type=Application.GRANT_AUTHORIZATION_CODE,
            name='OAuth2 Example Application',
        )[0]

    def print_hello(self, user, app: Application):
        separator = '-' * 79
        host = 'http://127.0.0.1:8880'
        message = (
            f'\n'
            f'{separator}\n'
            f'\n'
            f'OAuth 2.0 test server initialized.\n'
            f'\n'
            f'Admin UI URL:       {host}/admin\n'
            f'Username:           {self.ADMIN_USERNAME}\n'
            f'Password:           {self.ADMIN_PASSWORD}\n'
            f'\n'
            f'Application Credentials:\n'
            f'Client ID:          {app.client_id}\n'
            f'Client Secret:      {app.client_secret}\n'
            f'\n'
            f'OAuth 2.0 endpoints:\n'
            f'Authorize URL:      {host}{reverse("oauth2_provider:authorize")}\n'
            f'Token URL:          {host}{reverse("oauth2_provider:token")}\n'
            f'Revoke Token URL:   {host}{reverse("oauth2_provider:revoke-token")}\n'
            f'Introspect URL:     {host}{reverse("oauth2_provider:introspect")}\n'
            f'\n'
            f'Before the application can be used, you need to go to the '
            f'admin interface and configure whitelisted redirect URIs.'
            f'\n'
            f'{separator}\n'
            f'\n'
        )
        self.stdout.write(message)

    def handle(self, *args, **options):
        user = self.create_admin_user()
        app = self.create_app()
        self.print_hello(user=user, app=app)
