"""Cria usuario de demonstracao opcional, apenas se credenciais vierem do ambiente."""
import os
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Cria usuario de teste no primeiro deploy, sem expor senha no codigo."

    def handle(self, *args, **options):
        username = os.environ.get("HUIOS_DEMO_USERNAME", "").strip()
        password = os.environ.get("HUIOS_DEMO_PASSWORD", "")
        if not username and not password:
            self.stdout.write("Acesso demo nao solicitado.")
            return
        if not username or len(password) < 12:
            raise CommandError("Defina HUIOS_DEMO_USERNAME e uma HUIOS_DEMO_PASSWORD de 12+ caracteres.")
        User = get_user_model()
        if User.objects.filter(username=username).exists():
            self.stdout.write("Usuario demo ja existe; senha nao foi modificada.")
            return
        group = Group.objects.get(name="Coordenacao")
        user = User.objects.create_user(username=username, password=password)
        user.groups.add(group)
        self.stdout.write(self.style.SUCCESS("Usuario de demonstracao criado com permissao de Coordenacao."))
