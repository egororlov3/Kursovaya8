from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_related_habit_and_reward(linked_habit, reward):
    if linked_habit and reward:
        raise ValidationError(_("Нельзя одновременно указать связанную привычку и вознаграждение."))


def validate_duration(time_to_complete):
    if time_to_complete is None:
        raise ValidationError("Время на выполнение должно быть задано и не может быть пустым.")

    if time_to_complete <= 0:
        raise ValidationError("Время на выполнение должно быть положительным числом.")

    if time_to_complete > 120:
        raise ValidationError(_("Продолжительность не должна превышать 120 секунд."))


def validate_related_habit_is_pleasurable(linked_habit):
    if linked_habit and not linked_habit.is_pleasurable:
        raise ValidationError(_("Связанной может быть только приятная привычка."))


def validate_pleasurable_habit(is_pleasant, reward, linked_habit):
    if is_pleasant and (reward or linked_habit):
        raise ValidationError(_("Приятная привычка не может иметь вознаграждений или связанных привычек."))


def validate_frequency(period):
    if period > 7:
        raise ValidationError(_("Частота выполнения привычки должна быть не реже одного раза в 7 дней."))
