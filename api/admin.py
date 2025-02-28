from django.contrib import admin

from .models import User, Room, Course, Timetable, Attendance
from .ai_scheduler import generate_timetable

# Register your models here.


# Custom Action for Timetable Generation
def generate_timetable_action(modeladmin, request, queryset):
    generate_timetable()
    modeladmin.message_user(request, "Timetable has been generated successfully.")
generate_timetable_action.short_description = "Generate AI Timetable"

# User Admin
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('reg_no', 'name', 'role')  # Columns to display
    list_filter = ('role',)  # Filter by role (student/lecturer)
    search_fields = ('reg_no', 'name')  # Search by reg_no or name
    ordering = ('reg_no',)  # Sort by registration number

    # Prevent adding users via admin if you want strict control
    # def has_add_permission(self, request):
    #     return False

# Room Admin
@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'capacity')
    search_fields = ('name',)
    ordering = ('name',)

# Course Admin
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'lecturer', 'room')
    list_filter = ('lecturer',)
    search_fields = ('code', 'name')
    autocomplete_fields = ('lecturer', 'room')  # Searchable dropdowns for foreign keys

# Timetable Admin
@admin.register(Timetable)
class TimetableAdmin(admin.ModelAdmin):
    list_display = ('course', 'day', 'start_time', 'end_time', 'room', 'is_canceled')
    list_filter = ('day', 'is_canceled', 'room')
    search_fields = ('course__code', 'course__name')
    ordering = ('day', 'start_time')
    actions = [generate_timetable_action]  # Add custom action to generate timetable

    # Prevent manual timetable edits if AI handles it
    # def has_change_permission(self, request, obj=None):
    #     return False

# Attendance Admin
@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('user', 'timetable', 'attended', 'timestamp')
    list_filter = ('attended', 'timetable__day')
    search_fields = ('user__reg_no', 'user__name', 'timetable__course__code')
    ordering = ('-timestamp',)  # Most recent first