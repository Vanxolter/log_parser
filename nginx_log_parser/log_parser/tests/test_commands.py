import json
import pytest
from unittest.mock import patch
from django.core.management import call_command
from log_parser.models import LogEntry
from io import StringIO
import tempfile


@pytest.fixture
def valid_log_line():
    """
    Фикстура для создания валидной строки лога.

    Возвращает строку JSON, содержащую все необходимые поля для корректной обработки лога.
    """
    return json.dumps({
        "time": "17/May/2015:08:05:32 +0000",
        "remote_ip": "93.180.71.3",
        "remote_user": "-",
        "request": "GET /downloads/product_1 HTTP/1.1",
        "response": 304,
        "bytes": 0,
        "referrer": "-",
        "agent": "Debian APT-HTTP/1.3 (0.8.16~exp12ubuntu10.21)"
    })


@pytest.fixture
def invalid_log_line():
    """
    Фикстура для создания невалидной строки лога.

    Возвращает строку JSON, в которой отсутствуют обязательные поля для корректной обработки лога.
    """
    return json.dumps({
        "time": "17/May/2015:08:05:32 +0000",
        "remote_ip": "93.180.71.3",
        "response": 304,
        "bytes": 0
    })


@pytest.mark.django_db
def test_command_imports_valid_logs(valid_log_line):
    """
    Тест на успешный импорт правильного лога.

    Создаёт временный файл с валидной строкой лога и вызывает команду импорта. Проверяет,
    что запись добавлена в базу данных с правильными значениями.
    """
    with tempfile.NamedTemporaryFile(mode='w+', delete=False) as temp_file:
        temp_file.write(valid_log_line + '\n')
        temp_file.seek(0)

        call_command('import_log', temp_file.name)

    # Проверяем, что запись добавлена в базу данных
    assert LogEntry.objects.count() == 1
    log_entry = LogEntry.objects.first()
    assert log_entry.ip_address == "93.180.71.3"
    assert log_entry.http_method == "GET"
    assert log_entry.url == "/downloads/product_1"
    assert log_entry.response_code == 304


def test_command_raises_file_not_found_error():
    """
    Тест на ошибку при отсутствии файла.

    Проверяет, что команда импорта лога корректно обрабатывает случай, когда указанный файл не существует,
    и выводит соответствующее сообщение об ошибке.
    """
    with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
        call_command('import_log', 'non_existent_file.txt')
        output = mock_stdout.getvalue()
        assert "Файл не найден" in output


@pytest.mark.django_db
def test_command_handles_invalid_log_line(invalid_log_line):
    """
    Тест на обработку неправильной строки лога.

    Создаёт временный файл с невалидной строкой лога и вызывает команду импорта. Проверяет, что команда
    корректно обрабатывает ошибку в строке лога и выводит соответствующее сообщение, не добавляя запись в базу данных.
    """
    with tempfile.NamedTemporaryFile(mode='w+', delete=False) as temp_file:
        temp_file.write(invalid_log_line + '\n')
        temp_file.seek(0)

        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            call_command('import_log', temp_file.name)
            output = mock_stdout.getvalue()
            assert "Ошибка в строке:" in output

    # Проверяем, что данные не были добавлены в базу
    assert LogEntry.objects.count() == 0


@pytest.mark.django_db
@patch('log_parser.management.commands.import_log.LogEntry.objects.bulk_create')
def test_bulk_create_called_with_correct_data(mock_bulk_create, valid_log_line):
    """
    Тест на вызов bulk_create с правильными данными.

    Создаёт временный файл с валидной строкой лога и вызывает команду импорта. Проверяет, что метод
    bulk_create был вызван с правильными данными.
    """
    with tempfile.NamedTemporaryFile(mode='w+', delete=False) as temp_file:
        temp_file.write(valid_log_line + '\n')
        temp_file.seek(0)

        call_command('import_log', temp_file.name)

    # Проверяем, что bulk_create был вызван
    assert mock_bulk_create.called
    assert len(mock_bulk_create.call_args[0][0]) == 1


@pytest.mark.django_db
def test_process_log_line_with_invalid_request_format():
    """
    Тест на обработку строки с неправильным форматом request.

    Создаёт временный файл с некорректным форматом строки запроса и вызывает команду импорта. Проверяет, что
    команда правильно обрабатывает ошибку формата поля request и не добавляет запись в базу данных.
    """
    invalid_request_log_line = json.dumps({
        "time": "17/May/2015:08:05:32 +0000",
        "remote_ip": "93.180.71.3",
        "request": "GET",
        "response": 304,
        "bytes": 0
    })
    with tempfile.NamedTemporaryFile(mode='w+', delete=False) as temp_file:
        temp_file.write(invalid_request_log_line + '\n')
        temp_file.seek(0)

        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            call_command('import_log', temp_file.name)
            output = mock_stdout.getvalue()
            assert "Неверный формат поля request" in output

    # Убедимся, что запись не была добавлена
    assert LogEntry.objects.count() == 0
