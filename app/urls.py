from django.urls import path
from app.views import CurrentKrsView, AvailableCoursesView

urlpatterns = [
    path("students/<str:nim>/krs/current", CurrentKrsView.as_view(), name="current-krs"),
    path('students/<str:nim>/courses/available/', AvailableCoursesView.as_view(), name='available-courses'),
]
