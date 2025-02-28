from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import check_password
from .models import User, Timetable, Attendance
from .serializers import LoginSerializer, TimetableSerializer, AttendanceSerializer
from .ai_scheduler import generate_timetable

# Create your views here.

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            reg_no = serializer.validated_data['reg_no']
            password = serializer.validated_data['password']
            try:
                user = User.objects.get(reg_no=reg_no)
                if check_password(password, user.password):
                    request.session['user_id'] = user.id  # Store user in session
                    return Response({"role": user.role}, status=status.HTTP_200_OK)
                return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
            except User.DoesNotExist:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TimetableView(APIView):
    def get(self, request):
        user_id = request.session.get('user_id')
        if not user_id:
            return Response({"error": "Not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)

        user = User.objects.get(id=user_id)
        if user.role == 'lecturer':
            timetables = Timetable.objects.filter(course__lecturer=user)
        else:  # student
            timetables = Timetable.objects.all()  #assume all courses for students
        serializer = TimetableSerializer(timetables, many=True)
        return Response(serializer.data)

class CancelClassView(APIView):
    def post(self, request, timetable_id):
        user_id = request.session.get('user_id')
        if not user_id or User.objects.get(id=user_id).role != 'lecturer':
            return Response({"error": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)

        try:
            timetable = Timetable.objects.get(id=timetable_id)
            timetable.is_canceled = True
            timetable.save()
            return Response({"message": "Class canceled"})
        except Timetable.DoesNotExist:
            return Response({"error": "Timetable not found"}, status=status.HTTP_404_NOT_FOUND)

class AttendanceView(APIView):
    def post(self, request, timetable_id):
        user_id = request.session.get('user_id')
        if not user_id:
            return Response({"error": "Not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            timetable = Timetable.objects.get(id=timetable_id)
            Attendance.objects.create(
                timetable=timetable,
                user_id=user_id,
                attended=True
            )
            return Response({"message": "Attendance marked"})
        except Timetable.DoesNotExist:
            return Response({"error": "Timetable not found"}, status=status.HTTP_404_NOT_FOUND)

class GenerateTimetableView(APIView):
    def get(self, request):
        # Admin-only endpoint
        generate_timetable()
        return Response({"message": "Timetable generated successfully"})