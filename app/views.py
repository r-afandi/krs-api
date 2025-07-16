from rest_framework.views import APIView
from rest_framework.response import Response
from app.services.services import get_krs_mahasiswa, get_available_courses_for_student
from rest_framework import status

class CurrentKrsView(APIView):

    def get(self, request, nim):
        try:
            data = get_krs_mahasiswa(nim)
            return Response(data, status=status.HTTP_200_OK)
        except ValueError as ve:
            return Response({"error": str(ve)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print("DEBUG: Unhandled Exception:", e)  # Tampilkan ke terminal
            return Response(
                {"error": "An unexpected error occurred."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
class AvailableCoursesView(APIView):
    def get(self, request, nim):

        try:
            available_courses = get_available_courses_for_student(nim)
            return Response(available_courses, status=status.HTTP_200_OK)
        except ValueError as ve:
            return Response({"error": str(ve)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print("DEBUG: Unhandled Exception:", e)  # Tampilkan ke terminal
            return Response(
                {"error": "An unexpected error occurred."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        