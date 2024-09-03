from django.db import models


class LogEntry(models.Model):
    """
    Модель данных из лога.

    Атрибуты
        ip_address (GenericIPAddressField): IP адрес.
        timestamp (DateTimeField): Время запроса.
        http_method (str): http метод (GET, POST,...).
        uri (str): URI запроса.
        response_code (int): Код ответов.
        response_size (int): Размер ответа.
    """

    ip_address = models.GenericIPAddressField(
        verbose_name='IP Адрес',
        db_comment='IP адрес юзера оценивающего рецензию, защита от накрутки'
    )
    timestamp = models.DateTimeField(
        verbose_name='Время запроса',
        db_comment='Время запроса из лога',
        null=True,
        blank=True,
    )
    http_method = models.CharField(
        max_length=10,
        default='',
        verbose_name='http метод',
        db_comment='http метод (GET, POST,...)'
    )
    uri = models.CharField(
        max_length=255,
        default='',
        verbose_name='URI запроса',
        db_comment='URI запроса'
    )
    response_code = models.IntegerField(
        default=0,
        verbose_name='Код ответа',
        db_comment='Код ответа из лога'
    )
    response_size = models.IntegerField(
        default=0,
        verbose_name='Размер ответа',
        db_comment='Размер ответа из лога'
    )

    def str(self):
        return f"{self.ip_address} - {self.http_method} {self.uri}"

    class Meta:
        db_table = 'log_data'
        indexes = [models.Index(
            fields=['-timestamp', 'ip_address'])]
        ordering = ['-timestamp']
        verbose_name = 'Запрос'
        verbose_name_plural = 'Запросы'
