from .models import Course, Room, Timetable
import random
from datetime import time

DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
TIMESLOTS = [(time(9, 0), time(12, 0)), (time(13, 0), time(16, 0))]  # 3-hour slots

def generate_timetable():
    courses = Course.objects.all()
    rooms = Room.objects.all()

    # Clear existing timetable
    Timetable.objects.all().delete()

    for course in courses:
        allocated = False
        while not allocated:
            day = random.choice(DAYS)
            timeslot = random.choice(TIMESLOTS)
            room = random.choice(rooms)

            # Check for clashes
            clash = Timetable.objects.filter(
                day=day, start_time=timeslot[0], room=room
            ).exists()

            if not clash:
                Timetable.objects.create(
                    course=course,
                    day=day,
                    start_time=timeslot[0],
                    end_time=timeslot[1],
                    room=room
                )
                allocated = True

    return True