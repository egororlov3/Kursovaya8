import json
from datetime import datetime

import requests
from django.conf import settings

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from users.models import User
from .models import Habit
from .serializers import HabitSerializer
from .pagination import HabitPagination
from .tasks import schedule_reminder


class UserHabitsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Получает привычки текущего пользователя
        habits = Habit.objects.filter(user=request.user)
        paginator = HabitPagination()
        paginated_habits = paginator.paginate_queryset(habits, request)
        serializer = HabitSerializer(paginated_habits, many=True)
        return paginator.get_paginated_response(serializer.data)


class PublicHabitsView(APIView):
    def get(self, request):
        # Получает публичные привычки
        habits = Habit.objects.filter(is_public=True)
        paginator = HabitPagination()
        paginated_habits = paginator.paginate_queryset(habits, request)
        serializer = HabitSerializer(paginated_habits, many=True)
        return paginator.get_paginated_response(serializer.data)


class HabitCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        print("Received data:", request.data)  # Для отладки
        serializer = HabitSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print("Errors:", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class HabitDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, habit_id, user):
        # Находит привычку по ID
        try:
            return Habit.objects.get(id=habit_id, user=user)
        except Habit.DoesNotExist:
            return None

    def get(self, request, habit_id):
        # Получает привычку по ID
        habit = self.get_object(habit_id, request.user)
        if habit is None:
            return Response({"error": "Habit not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = HabitSerializer(habit)
        return Response(serializer.data)

    def put(self, request, habit_id):
        # Изменяет привычку по ID
        habit = self.get_object(habit_id, request.user)
        if habit is None:
            return Response({"error": "Habit not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = HabitSerializer(habit, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, habit_id):
        # Удаляет привычку по ID
        habit = self.get_object(habit_id, request.user)
        if habit is None:
            return Response({"error": "Habit not found."}, status=status.HTTP_404_NOT_FOUND)

        habit.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# TELEGRAM
@csrf_exempt
def handle_telegram_message(request):
    if request.method == "POST":
        try:
            message = json.loads(request.body.decode('utf-8'))
            chat_id = message['message']['chat']['id']
            username = message['message']['from'].get('username', '')
            text = message['message'].get('text', '')

            user, created = User.objects.get_or_create(username=username)
            user.telegram_chat_id = chat_id
            user.save()

            if text.lower() == '/start':
                reply_message = "Привет! Я ваш помощник по привычкам."
                send_telegram_message(chat_id, reply_message)

            elif text.lower().startswith('/add_habit'):
                # Извлечение названия привычки и времени
                parts = text.split()
                if len(parts) < 3:
                    reply_message = "Используйте формат: /add_habit <название> <место> <время(HH:MM)>."
                    send_telegram_message(chat_id, reply_message)
                    return JsonResponse({'status': 'ok'}, status=200)

                habit_action = parts[1]
                habit_place = " ".join(parts[2:-1])
                reminder_time_str = parts[-1]

                add_habit(user, habit_action, habit_place, reminder_time_str)
                return JsonResponse({'status': 'ok'}, status=200)

            return JsonResponse({'status': 'ok'}, status=200)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return JsonResponse({'error': 'Invalid method'}, status=405)


def send_telegram_message(chat_id, text):
    url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': text,
    }
    response = requests.post(url, json=payload)


def is_valid_time_format(time_str):
    try:
        datetime.strptime(time_str, "%H:%M")
        return True
    except ValueError:
        return False


def add_habit(user, habit_action, habit_place, reminder_time_str, is_pleasant=False, linked_habit=None, period=1,
              reward=None, time_to_complete=0, is_public=False):
    # Проверка формата времени
    if not is_valid_time_format(reminder_time_str):
        send_telegram_message(user.telegram_chat_id, "Пожалуйста, используйте формат времени HH:MM.")
        return

    reminder_time = datetime.strptime(reminder_time_str, "%H:%M").time()
    reminder_datetime = datetime.combine(datetime.now(), reminder_time)

    if reminder_datetime > datetime.now():
        habit = Habit.objects.create(
            user=user,
            action=habit_action,
            place=habit_place,
            time=reminder_time,
            is_pleasant=is_pleasant,
            linked_habit=linked_habit,
            period=period,
            reward=reward,
            time_to_complete=time_to_complete,
            is_public=is_public
        )

        schedule_reminder(habit.id, reminder_time)

        send_telegram_message(user.telegram_chat_id,
                              f"Привычка '{habit_action}' добавлена! Напоминание установлено на {reminder_time_str}.")
    else:
        send_telegram_message(user.telegram_chat_id, "Пожалуйста, укажите будущее время для напоминания.")
