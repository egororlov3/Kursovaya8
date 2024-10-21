from django.db import models
from users.models import User, NULLABLE


class Habit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="habits",
                             verbose_name='пользователь')
    place = models.CharField(max_length=255,
                             verbose_name='место, в котором выполняется привычка')
    time = models.TimeField(verbose_name='время, в которое выполняется привычка')
    action = models.CharField(max_length=255,
                              verbose_name='действие, которое представляет собой привычка')
    is_pleasant = models.BooleanField(default=False,
                                      verbose_name='полезность привычки')
    linked_habit = models.ForeignKey('self', **NULLABLE, on_delete=models.SET_NULL,
                                     related_name="linked_to", verbose_name='связанность привычки')
    period = models.PositiveIntegerField(default=1,
                                         verbose_name='переодичность')
    reward = models.CharField(max_length=255, **NULLABLE,
                              verbose_name='вознаграждение')
    time_to_complete = models.PositiveIntegerField(default=0,
                                                   verbose_name='время на выполнение')
    is_public = models.BooleanField(default=False,
                                    verbose_name='признак публичности')

    def __str__(self):
        return f"{self.action} в/на {self.place} в {self.time}"

    class Meta:
        verbose_name = 'привычка'
        verbose_name_plural = 'привычки'
