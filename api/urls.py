from django.urls import path
from . import views

urlpatterns = [
    path('check-timetable/', views.get_timetable_updates),
]
