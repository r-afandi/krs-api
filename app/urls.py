from django.urls import path
from app.views import CurrentKrsView, AvailableCoursesView, KrsCourseRegistrationView, DeleteKRSItemView, KrsStatusView

urlpatterns = [
    path("students/<str:nim>/krs/current/", CurrentKrsView.as_view(), name="current-krs"),
    path('students/<str:nim>/courses/available/', AvailableCoursesView.as_view(), name='available-courses'),
    path('students/<str:nim>/krs/courses/', KrsCourseRegistrationView.as_view(), name='krs-course-registration'),
    path('students/<str:nim>/krs/courses/<str:id_jadwal>/', DeleteKRSItemView.as_view(), name='delete-krs-course'),
    path('students/<str:nim>/krs/status/', KrsStatusView.as_view()),
]
