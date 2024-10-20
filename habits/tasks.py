import logging
from datetime import datetime, timedelta
from celery import shared_task
import requests
from django.conf import settings
from .models import Habit
from celery import current_app

TELEGRAM_API_URL = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"


@shared_task
def send_telegram_reminder(habit_id):
    try:
        habit = Habit.objects.get(id=habit_id)
        user = habit.user
        chat_id = user.telegram_chat_id

        if chat_id:
            message = f"Не забудьте выполнить привычку: {habit.action}."
            data = {
                'chat_id': chat_id,
                'text': message,
            }

            response = requests.post(TELEGRAM_API_URL, data=data)
            response.raise_for_status()

            if response.ok:
                return f"Успешно отправлено уведомление для {user.username} о привычке {habit.action}"
            else:
                return f"Ошибка отправки уведомления: {response.text}"

        return f"Пользователь {user.username} не указал Telegram chat_id."

    except Habit.DoesNotExist:
        return f"Привычка с id {habit_id} не найдена."
    except Exception as e:
        return f"Произошла ошибка: {str(e)}"


@shared_task
def send_telegram_reminder(habit_id):
    try:
        habit = Habit.objects.get(id=habit_id)
        user = habit.user
        chat_id = user.telegram_chat_id

        if chat_id:
            message = f"Не забудьте выполнить привычку: {habit.action}."
            data = {
                'chat_id': chat_id,
                'text': message,
            }

            response = requests.post(TELEGRAM_API_URL, data=data)
            response.raise_for_status()

            if response.ok:
                return f"Успешно отправлено уведомление для {user.username} о привычке {habit.action}"
            else:
                return f"Ошибка отправки уведомления: {response.text}"

        return f"Пользователь {user.username} не указал Telegram chat_id."

    except Habit.DoesNotExist:
        return f"Привычка с id {habit_id} не найдена."
    except Exception as e:
        return f"Произошла ошибка: {str(e)}"


def schedule_reminder(habit_id, reminder_time):
    # Удаляем старую задачу, если она существует
    task_name = f"send-reminder-for-habit-{habit_id}"
    remove_task(task_name)

    # Вычисляем время до выполнения
    now = datetime.now()
    reminder_datetime = datetime.combine(now.date(), reminder_time)

    # Если время напоминания уже прошло, переносим его на завтра
    if reminder_datetime < now:
        reminder_datetime += timedelta(days=1)

    delay = (reminder_datetime - now).total_seconds()  # Разница в секундах

    if delay < 0:
        return

    send_telegram_reminder.apply_async((habit_id,), countdown=delay)


def remove_task(task_name):
    """Удаление старой задачи Celery по имени"""
    try:
        current_app.control.revoke(task_name)
    except Exception as e:
        pass


def test_message(chat_id):
    message = "Тестовое сообщение"
    data = {
        'chat_id': chat_id,
        'text': message,
    }
    response = requests.post(TELEGRAM_API_URL, data=data)

