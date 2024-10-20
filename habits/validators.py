from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_related_habit_and_reward(related_habit, reward):
    if related_habit and reward:
        raise ValidationError(_("Нельзя одновременно указать связанную привычку и вознаграждение."))


def validate_duration(duration):
    if duration > 120:
        raise ValidationError(_("Продолжительность не должна превышать 120 секунд."))


def validate_related_habit_is_pleasurable(related_habit):
    if related_habit and not related_habit.is_pleasurable:
        raise ValidationError(_("Связанной может быть только приятная привычка."))


def validate_pleasurable_habit(is_pleasurable, reward, related_habit):
    if is_pleasurable and (reward or related_habit):
        raise ValidationError(_("Приятная привычка не может иметь вознаграждений или связанных привычек."))


def validate_frequency(frequency):
    if frequency > 7:
        raise ValidationError(_("Частота выполнения привычки должна быть не реже одного раза в 7 дней."))
