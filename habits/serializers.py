from rest_framework import serializers
from .models import Habit
from .validators import (
    validate_related_habit_and_reward,
    validate_duration,
    validate_related_habit_is_pleasurable,
    validate_pleasurable_habit,
    validate_frequency,
)


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = '__all__'

    def validate(self, data):
        user = self.context['request'].user

        # Проверка пользователя
        if self.instance and self.instance.user != user:
            raise serializers.ValidationError("Вы можете изменять только свои привычки!")

        validate_related_habit_and_reward(data.get('linked_habit'), data.get('reward'))
        validate_duration(data.get('time_to_complete'))
        validate_related_habit_is_pleasurable(data.get('linked_habit'))
        validate_pleasurable_habit(data.get('is_pleasant'), data.get('reward'), data.get('linked_habit'))
        validate_frequency(data.get('period'))

        return data
