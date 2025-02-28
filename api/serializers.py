from rest_framework import serializers
from .models import User, Timetable, Attendance, Course, Room

class LoginSerializer(serializers.Serializer):
    reg_no = serializers.CharField()
    password = serializers.CharField()

class TimetableSerializer(serializers.ModelSerializer):
    course = serializers.StringRelatedField()
    room = serializers.StringRelatedField()

    class Meta:
        model = Timetable
        fields = ['id', 'course', 'day', 'start_time', 'end_time', 'room', 'is_canceled']

class AttendanceSerializer(serializers.ModelSerializer):
    timetable = TimetableSerializer()

    class Meta:
        model = Attendance
        fields = ['id', 'timetable', 'attended', 'timestamp']