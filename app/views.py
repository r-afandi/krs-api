
from rest_framework.views import APIView
from rest_framework.response import Response
from app.serializers import (MahasiswaDinusSerializer, MatkulKurikulumSerializer,
                            HariSerializer, JadwalTawarSerializer, SesiKuliahSerializer,
                            TahunAjaranSerializer, KrsRecordSerializer,KrsStatusSerializer)
from app.models import MahasiswaDinus,JadwalTawar,KrsRecord
from app.services.services import get_krs_mahasiswa, get_available_courses_for_student, add_course_to_krs, remove_krs_course, get_krs_status
from rest_framework import status

class CurrentKrsView(APIView):

    def get(self, request, nim):
        mahasiswa = MahasiswaDinus.objects.get(nim_dinus=nim)
        print('DEBUG: Mahasiswa:', mahasiswa.nim_dinus)
        record= KrsRecord.objects.filter(nim_dinus=mahasiswa)
        
        for r in record:
            print('DEBUG: Record:', r.id_jadwal)
        
 
        krs, error = get_krs_mahasiswa(nim)
        if error:
            return Response({"error": error}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = KrsRecordSerializer(krs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class AvailableCoursesView(APIView):
    def get(self, request, nim):
        print("DEBUG: AvailableCoursesView called with NIM =", nim)
        query, error = get_available_courses_for_student(nim)
        if error:
            return Response({"error": error}, status=status.HTTP_404_NOT_FOUND)

        serializer = JadwalTawarSerializer(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
class KrsCourseRegistrationView(APIView):

    def post(self, request, nim):
        id_jadwal = request.data.get("id_jadwal")

        if not id_jadwal:
            return Response({"error": "ID jadwal diperlukan."}, status=status.HTTP_400_BAD_REQUEST)
        krs_record, error = add_course_to_krs(nim, id_jadwal)

        if error:
            return Response({"error": error}, status=status.HTTP_400_BAD_REQUEST)

        serialized = KrsRecordSerializer(krs_record)
        return Response({
        "message": "Mata kuliah berhasil ditambahkan ke KRS.",
        "data": serialized.data
        }, status=status.HTTP_201_CREATED)

class DeleteKRSItemView(APIView):
    def delete(self, request, nim, id_jadwal):
        try:
            result = remove_krs_course(nim, id_jadwal)
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class KrsStatusView(APIView):
    def get(self, request, nim):
        print(f"DEBUG: KRSStatusView called with NIM = {nim}")
        try:
            data = get_krs_status(nim)
            serializer = KrsStatusSerializer(data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
