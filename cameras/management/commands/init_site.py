import os
import shutil
from pathlib import Path

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.core.management.base import BaseCommand

from cameras.models import Camera


class Command(BaseCommand):
    help = 'Подготовка сайта к работе: медиа, начальные данные, суперпользователь'

    def handle(self, *args, **options):
        self.seed_media()
        self.load_initial_data()
        self.create_superuser()

    def seed_media(self):
        seed_dir = settings.BASE_DIR / 'seed_media'
        if not seed_dir.exists():
            return

        copied = 0
        for item in seed_dir.rglob('*'):
            if not item.is_file():
                continue
            rel_path = item.relative_to(seed_dir)
            dest = settings.MEDIA_ROOT / rel_path
            if dest.exists():
                continue
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(item, dest)
            copied += 1

        if copied:
            self.stdout.write(self.style.SUCCESS(f'Скопировано медиафайлов: {copied}'))

    def load_initial_data(self):
        if Camera.objects.exists():
            self.stdout.write('База уже содержит камеры, пропускаем загрузку fixture')
            return

        fixture = Path(__file__).resolve().parent.parent.parent / 'fixtures' / 'initial_data.json'
        if not fixture.exists():
            self.stdout.write(self.style.WARNING('Fixture initial_data.json не найден'))
            return

        call_command('loaddata', str(fixture), verbosity=0)
        self.stdout.write(self.style.SUCCESS('Начальные данные загружены'))

    def create_superuser(self):
        user_model = get_user_model()
        if user_model.objects.filter(is_superuser=True).exists():
            self.stdout.write('Суперпользователь уже существует')
            return

        username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')

        if not password:
            self.stdout.write(
                self.style.WARNING(
                    'Задайте DJANGO_SUPERUSER_PASSWORD в переменных окружения, '
                    'чтобы создать вход в /admin/'
                )
            )
            return

        user_model.objects.create_superuser(username, email, password)
        self.stdout.write(self.style.SUCCESS(f'Создан суперпользователь: {username}'))
