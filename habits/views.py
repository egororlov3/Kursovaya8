from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .models import Habit
from .serializers import HabitSerializer
from .pagination import HabitPagination


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
        print("Errors:", serializer.errors)  # Вывод ошибок для отладки
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

    def put(self, request, habit_id):  # Параметр остается habit_id
        # Изменяет привычку по ID
        habit = self.get_object(habit_id, request.user)
        if habit is None:
            return Response({"error": "Habit not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = HabitSerializer(habit, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()  # Не обязательно передавать user, так как он уже связан с объектом
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, habit_id):
        # Удаляет привычку по ID
        habit = self.get_object(habit_id, request.user)
        if habit is None:
            return Response({"error": "Habit not found."}, status=status.HTTP_404_NOT_FOUND)

        habit.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
