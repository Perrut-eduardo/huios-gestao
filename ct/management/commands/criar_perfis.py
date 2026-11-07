"""Cria grupos básicos sem atribuir permissões financeiras a professores."""
from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Cria os grupos Coordenacao e Professor e ajusta as permissões."

    def handle(self, *args, **kwargs):
        coordenacao, _ = Group.objects.get_or_create(name="Coordenacao")
        professor, _ = Group.objects.get_or_create(name="Professor")
        todas = Permission.objects.filter(content_type__app_label="ct")
        coordenacao.permissions.set(todas)
        professor.permissions.set(Permission.objects.filter(
            content_type__app_label="ct", codename="view_necessidade"
        ))
        self.stdout.write(self.style.SUCCESS("Grupos de acesso atualizados."))
