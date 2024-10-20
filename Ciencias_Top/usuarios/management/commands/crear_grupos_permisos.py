from django.core.management.base import BaseCommand
from usuarios.gestionar_permisos import crear_grupos_y_permisos

class Command(BaseCommand):
    help = 'Crea grupos y asigna permisos'

    def handle(self, *args, **kwargs):
        crear_grupos_y_permisos()
        self.stdout.write(self.style.SUCCESS('Grupos y permisos creados exitosamente.'))
