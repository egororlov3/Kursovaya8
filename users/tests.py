import pytest
from django.core.exceptions import ValidationError
from users.models import User


@pytest.mark.django_db
class TestUserModel:

    @pytest.fixture
    def user_data(self):
        return {
            "username": "testuser",
            "email": "testuser@example.com",
            "phone": "+123456789",
            "avatar": None,
            "country": "Россия",
            "telegram_chat_id": "123456789",
        }

    def test_user_creation(self, user_data):
        """Тест создания пользователя с валидными данными"""
        user = User.objects.create_user(**user_data, password="testpassword123")
        assert user.username == "testuser"
        assert user.email == "testuser@example.com"
        assert user.phone == "+123456789"
        assert user.country == "Россия"
        assert user.telegram_chat_id == "123456789"

    def test_user_unique_email(self, user_data):
        """Тест уникальности поля email"""
        User.objects.create_user(**user_data, password="testpassword123")
        with pytest.raises(ValidationError):
            user_data["username"] = "testuser"  # Изменим только имя пользователя
            user2 = User(**user_data)
            user2.full_clean()  # Это вызовет ошибку уникальности

    def test_nullable_fields(self, user_data):
        """Тест для проверки nullable полей (phone, avatar, telegram_chat_id)"""
        user_data["phone"] = None
        user_data["avatar"] = None
        user_data["telegram_chat_id"] = None
        user = User.objects.create_user(**user_data, password="testpassword123")

        assert user.phone is None
        assert user.avatar.name is None
        assert user.telegram_chat_id is None
