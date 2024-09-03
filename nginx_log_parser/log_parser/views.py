from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from api.v1.serializers import LogEntrySerializer
from log_parser.models import LogEntry
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend


class LogEntryViewSet(viewsets.ModelViewSet):
    """
    ViewSet для управления записями логов.

    Этот ViewSet обеспечивает CRUD операции для модели LogEntry.

    Атрибуты:
        queryset (QuerySet): Набор данных для этого ViewSet. По умолчанию содержит все записи модели LogEntry.
        serializer_class (Serializer): Класс сериализатора для преобразования данных модели LogEntry в формат JSON и обратно.
        filter_backends (list): Список классов фильтрации для применения фильтров, поиска и сортировки.
            - DjangoFilterBackend: Позволяет фильтрацию по полям модели.
            - SearchFilter: Позволяет осуществлять поиск по заданным полям.
            - OrderingFilter: Позволяет сортировку результатов по указанным полям.
        filterset_fields (list): Поля модели LogEntry, по которым можно фильтровать записи.
            - http_method: HTTP метод запроса.
            - response_code: Код ответа сервера.
        search_fields (list): Поля модели LogEntry, по которым можно осуществлять поиск.
            - ip_address: IP адрес запроса.
            - url: URI запроса.
        ordering_fields (list): Поля модели LogEntry, по которым можно сортировать результаты.
            - timestamp: Время запроса.
        permission_classes (list): Список классов разрешений, определяющих, кто имеет доступ к данным.
            - IsAdminUser: Доступ разрешен только для пользователей с правами администратора.

    Методы:
        - list(): Список всех записей LogEntry.
        - create(): Создание новой записи LogEntry.
        - retrieve(): Получение одной записи LogEntry по первичному ключу.
        - update(): Обновление существующей записи LogEntry.
        - partial_update(): Частичное обновление записи LogEntry.
        - destroy(): Удаление записи LogEntry.
    """

    queryset = LogEntry.objects.all()
    serializer_class = LogEntrySerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['http_method', 'response_code']
    search_fields = ['ip_address', 'url']
    ordering_fields = ['timestamp']
    permission_classes = [IsAdminUser]
