import pytest
from django.utils import timezone

from log_parser.models import LogEntry


@pytest.mark.django_db
def test_log_entry_creation():
    """
    Проверяет создание объекта LogEntry с заданными полями.

    Этот тест создаёт запись LogEntry с заданными значениями для всех полей и проверяет, что
    сохранённые значения совпадают с ожидаемыми. Также проверяется, что поле timestamp установлено.
    """
    log_entry = LogEntry.objects.create(
        ip_address='192.168.1.1',
        timestamp=timezone.now(),
        http_method='GET',
        url='/some-url/',
        response_code=200,
        response_size=1234
    )

    assert log_entry.ip_address == '192.168.1.1'
    assert log_entry.http_method == 'GET'
    assert log_entry.url == '/some-url/'
    assert log_entry.response_code == 200
    assert log_entry.response_size == 1234
    assert log_entry.timestamp is not None


@pytest.mark.django_db
def test_log_entry_str_method():
    """
    Проверяет метод str модели LogEntry.

    Этот тест создаёт объект LogEntry и проверяет, что метод __str__ возвращает строку в
    ожидаемом формате: "<ip_address> - <http_method> <url>".
    """
    log_entry = LogEntry.objects.create(
        ip_address='192.168.1.1',
        timestamp=timezone.now(),
        http_method='POST',
        url='/another-url/',
        response_code=404,
        response_size=5678
    )

    assert str(log_entry) == '192.168.1.1 - POST /another-url/'


@pytest.mark.django_db
def test_log_entry_defaults():
    """
    Проверяет значения по умолчанию для полей модели LogEntry.

    Этот тест создаёт объект LogEntry с заданным ip_address и timestamp, но оставляет
    остальные поля по умолчанию. Проверяется, что поля по умолчанию установлены корректно.
    """
    log_entry = LogEntry.objects.create(
        ip_address='10.0.0.1',
        timestamp=timezone.now(),
    )

    assert log_entry.http_method == ''
    assert log_entry.url == ''
    assert log_entry.response_code == 0
    assert log_entry.response_size == 0