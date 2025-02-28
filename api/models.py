from django.db import models

# Create your models here.

# User Role Choices
USER_ROLES = (
    ('student', 'Student'),
    ('lecturer', 'Lecturer'),
)

# Room Model
class Room(models.Model):
    name = models.CharField(max_length=100, unique=True)
    capacity = models.IntegerField()

    def __str__(self):
        return self.name

# Course Model
class Course(models.Model):
    code = models.CharField(max_length=20, unique=True)  
    name = models.CharField(max_length=100)
    lecturer = models.ForeignKey('User', on_delete=models.CASCADE, limit_choices_to={'role': 'lecturer'})
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.code} - {self.name}"

# User Model (Student or Lecturer)
class User(models.Model):
    reg_no = models.CharField(max_length=50, unique=True)  # Registration number or staff ID
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=10, choices=USER_ROLES)
    password = models.CharField(max_length=128)  # Store hashed password

    def __str__(self):
        return f"{self.name} ({self.reg_no})"

# Timetable Model
class Timetable(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    day = models.CharField(max_length=10)
    start_time = models.TimeField()  
    end_time = models.TimeField()  
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True)
    is_canceled = models.BooleanField(default=False)

    class Meta:
        unique_together = ('room', 'day', 'start_time')  # Prevent clashes

    def __str__(self):
        return f"{self.course.code} on {self.day} at {self.start_time}"

# Attendance Model
class Attendance(models.Model):
    timetable = models.ForeignKey(Timetable, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    attended = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('timetable', 'user')  # One attendance per user per class

    def __str__(self):
        return f"{self.user.name} - {self.timetable}"