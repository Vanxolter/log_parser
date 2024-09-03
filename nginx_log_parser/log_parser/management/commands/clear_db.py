from django.core.management.base import BaseCommand

from log_parser.models import LogEntry


class Command(BaseCommand):
    """
    Команда для быстрой очистки данных в базе,
    можно использовать при ручном тестировании
    """
    help = "Очистить базу"

    def handle(self, *args, **options):
        LogEntry.objects.all().delete()
