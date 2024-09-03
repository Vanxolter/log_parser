import json
from django.core.management.base import BaseCommand
from log_parser.models import LogEntry
from datetime import datetime
from django.db import transaction


class Command(BaseCommand):
    help = 'Imports log file from the given URL or local file path'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the log file (.txt format)')

    def handle(self, *args, **options):
        """Главная функция процесса парсинга"""
        file_path = options['file_path']
        try:
            self.read_and_save_log_file(file_path)
            self.stdout.write(self.style.SUCCESS('Лог импортирован успешно'))
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'Файл не найден: {file_path}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Неожиданная ошибка: {e}'))

    def read_and_save_log_file(self, file_path):
        """Построчное чтение файла и пакетное сохранение данных для избегания проблем с памятью"""
        batch_size = 1000  # Размер пачки для сохранения в БД
        log_entries = []  # Список для накопления записей

        with open(file_path, 'r') as file:
            for line in file:
                try:
                    log_entry = self.process_log_line(line)
                    if log_entry:
                        log_entries.append(log_entry)

                    # Сохраняем записи пачками
                    if len(log_entries) >= batch_size:
                        self.save_log_entries(log_entries)
                        log_entries = []  # Очистка списка после сохранения
                except (json.JSONDecodeError, ValueError) as e:
                    self.stdout.write(self.style.ERROR(f"Ошибка в строке: {e}"))

        # Сохраняем оставшиеся записи
        if log_entries:
            self.save_log_entries(log_entries)

    def process_log_line(self, line):
        """Парсинг отдельной строки, валидация и подготовка данных"""
        log_entry = json.loads(line.strip())
        self.validate_log_entry(log_entry)

        # Парсим поле request
        request_parts = log_entry['request'].split()
        if len(request_parts) < 2:
            raise ValueError("Неверный формат поля request")

        http_method = request_parts[0]
        url = request_parts[1]

        # Возвращаем инстанс в LogEntry
        return LogEntry(
            ip_address=log_entry['remote_ip'],
            timestamp=datetime.strptime(log_entry['time'], "%d/%b/%Y:%H:%M:%S %z"),
            http_method=http_method,
            url=url,
            response_code=int(log_entry['response']),
            response_size=int(log_entry['bytes']),
        )

    @staticmethod
    def validate_log_entry(log_entry):
        """Валидация обязательных полей"""
        required_fields = ['remote_ip', 'time', 'request', 'response', 'bytes']
        for field in required_fields:
            if field not in log_entry:
                raise ValueError(f"Отсутствует обязательное поле: {field}")

    @staticmethod
    def save_log_entries(log_entries):
        """Пакетное сохранение записей в базу данных"""
        with transaction.atomic():
            LogEntry.objects.bulk_create(log_entries)
