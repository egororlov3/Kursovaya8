from django.urls import path

from .apps import HabitsConfig
from .views import UserHabitsView, PublicHabitsView, HabitCreateView, HabitDetailView

app_name = HabitsConfig.name

urlpatterns = [
    path('my-habits/', UserHabitsView.as_view(), name='my_habits'),
    path('public-habits/', PublicHabitsView.as_view(), name='public_habits'),
    path('habits/', HabitCreateView.as_view(), name='create_habit'),
    path('habits/<int:habit_id>/', HabitDetailView.as_view(), name='habit_detail'),
]
