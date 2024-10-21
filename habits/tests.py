import pytest
from django.contrib.auth import get_user_model
from .models import Habit

User = get_user_model()


@pytest.mark.django_db
class TestHabitModel:

    @pytest.fixture
    def user(self):
        return User.objects.create_user(username='testuser', password='password123')

    @pytest.fixture
    def habit(self, user):
        return Habit.objects.create(
            user=user,
            place="Спортзал",
            time="18:00",
            action="Тренировка",
            is_pleasant=True,
            period=3,
            reward="Отдых",
            time_to_complete=60,
            is_public=True
        )

    def test_habit_creation(self, habit):
        """Тест для создания привычки с валидными данными"""
        assert habit.user.username == 'testuser'
        assert habit.place == "Спортзал"
        assert habit.time == "18:00"
        assert habit.action == "Тренировка"
        assert habit.is_pleasant is True
        assert habit.period == 3
        assert habit.reward == "Отдых"
        assert habit.time_to_complete == 60
        assert habit.is_public is True

    def test_str_method(self, habit):
        """Тест для метода __str__"""
        assert str(habit) == "Тренировка в/на Спортзал в 18:00"

    def test_linked_habit(self, user, habit):
        """Тест для связанной привычки"""
        linked_habit = Habit.objects.create(
            user=user,
            place="Парк",
            time="07:00",
            action="Прогулка",
            is_pleasant=True,
            linked_habit=habit,
            period=1,
            reward="Кофе",
            time_to_complete=30,
            is_public=False
        )
        assert linked_habit.linked_habit == habit
        assert linked_habit.linked_habit.action == "Тренировка"

    def test_field_max_length(self):
        """Тест на максимальную длину полей"""
        habit = Habit._meta.get_field('place')
        assert habit.max_length == 255

        action = Habit._meta.get_field('action')
        assert action.max_length == 255
