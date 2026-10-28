from django.db import models
from django.utils import timezone


class Task(models.Model):
    title = models.CharField('Название', max_length=200)
    description = models.TextField('Описание', blank=True)
    created_at = models.DateTimeField('Дата создания', default=timezone.now)
    completed = models.BooleanField('Выполнено', default=False)
    priority = models.CharField(
        'Приоритет',
        max_length=10,
        choices=[
            ('low', 'Низкий'),
            ('medium', 'Средний'),
            ('high', 'Высокий'),
        ],
        default='medium'
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'
        ordering = ['-created_at']