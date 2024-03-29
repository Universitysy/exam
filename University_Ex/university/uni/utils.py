# https://django-scheduler.readthedocs.io/en/latest/install.html
# The code you provided is a custom implementation of HTMLCalendar for a Django application. The class TeacherCalendar inherits from the HTMLCalendar class and overrides some of its methods to accommodate the specific requirements of the application. Let's dive into the details of each method:
# __init__(self, year=None, month=None, teacher=None):
# This method initializes the TeacherCalendar object with the given year, month, and teacher.
# It then calls the parent class's __init__() method to set up the basic properties of the calendar.
# formatday(self, day, events):
# This method takes a day and a list of events as input and returns an HTML table cell (<td>) with the events for the given day.
# It filters the events to include only those that match the given day.
# For each event, it creates an HTML list item with the event's start and end times.
# If the day is not zero (a valid day), it returns an HTML table cell with the day number and the list of events. Otherwise, it returns an empty table cell.
# formatweek(self, theweek):
# This method takes a week (a list of days and their corresponding week day numbers) as input and returns an HTML table row (<tr>) with the formatted days.
# It calls the formatday() method for each day in the week and concatenates the results.
# formatmonth(self, withyear=True):
# This method returns an HTML table with the calendar for the given month and year.
# It retrieves the teacher's availability records for the specified month and year from the Teacher_Availability model.
# It filters the Selected_exam objects based on the teacher's availability records.
# It then calls the parent class's formatmonth() method with the modified events list.
# Here's a step-by-step explanation of how this custom calendar works:

# When you create a TeacherCalendar object, you pass the year, month, and teacher as arguments.
# When you call the formatmonth() method on the TeacherCalendar object, it retrieves the teacher's availability records and the selected exams for the given month and year.
# The formatmonth() method calls the parent class's formatmonth() method, which in turn calls the overridden formatweek() and formatday() methods to generate the calendar's HTML structure.
# The formatday() method adds the events (teacher's availability and selected exams) to the corresponding days in the calendar.

# In summary, this custom TeacherCalendar class generates an HTML calendar with the teacher's availability and selected exams for a given month and year. It inherits from Python's HTMLCalendar class and overrides some methods to include the specific details of the application (paulgrajewski.medium.com, huiwenteo.com).
from calendar import HTMLCalendar
from .models import Selected_exam, Teacher_Availability

class TeacherCalendar(HTMLCalendar):
    def __init__(self, year=None, month=None, teacher=None):
        self.year = year
        self.month = month
        self.teacher = teacher
        super(TeacherCalendar, self).__init__()

    def formatday(self, day, events):
        events_per_day = [event for event in events if event.t_a.date.day == day]
        d = ''
        for event in events_per_day:
            hour_start = event.t_a.time_start.hour
            min_start = event.t_a.time_start.minute
            hour_end = event.t_a.time_end.hour
            min_end = event.t_a.time_end.minute
            room = event.e_x.assigned_room.name
            d += f'<div style="color:blue; font-decoration:bold;"> ROOM :  <span style="color:red;"> {room} </span> FROM  <span style="color:red;">{hour_start}:{min_start:02d} to {hour_end}:{min_end:02d} </span> </div>'

        if day != 0:
                return f"<td><span class='date'>{day}</span><ul>{d}</ul></td>"
        return '<td></td>'


    def formatweek(self, theweek):
        s = ''.join(self.formatday(d, self.events) for (d, wd) in theweek)
        return f'<tr> {s} </tr>'

    def formatmonth(self, withyear=True):
        teacher_availability = Teacher_Availability.objects.filter(teacher_av=self.teacher, date__year=self.year, date__month=self.month)
        self.events = Selected_exam.objects.filter(t_a__in=teacher_availability)
        return super().formatmonth(self.year, self.month, withyear)



class AdminCalendar(HTMLCalendar):
    def __init__(self, year=None, month=None, teacher=None):
        self.year = year
        self.month = month
        self.teacher = teacher
        super(AdminCalendar, self).__init__()

    def formatday(self, day, events):
        availabilities_per_day = [event for event in events if event.t_a.date.day == day]
        d = ''
        for availability in availabilities_per_day:
            teacher_first_name =  availability.t_a.teacher_av.first_name
            teacher_name = teacher_first_name + " " + availability.t_a.teacher_av.last_name
            hour_start = availability.t_a.time_start.hour
            min_start = availability.t_a.time_start.minute
            hour_end = availability.t_a.time_end.hour
            min_end = availability.t_a.time_end.minute
            room = availability.e_x.assigned_room.name
            course = availability.e_x.course_exam.name

            d += f'<ul><li style="color:blue" >{room}: <ul> <li style="color:red;"> {teacher_name} - [{course}] <ul> <li style="color:red;"> {hour_start}:{min_start:02d} <span style="color:blue";> to </span> {hour_end}:{min_end:02d}</li> </ul>  </li> </ul> </ul>'
        if day != 0:
            return f"<td><span class='date'>{day}</span><ul> {d} </ul></td>"
        return '<td></td>'

    def formatweek(self, theweek):
        s = ''.join(self.formatday(d, self.events) for (d, wd) in theweek)
        return f'<tr> {s} </tr>'

    def formatmonth(self, withyear=True):
        teacher_availability = Teacher_Availability.objects.filter(date__year=self.year, date__month=self.month)
        self.events = Selected_exam.objects.filter(t_a__in=teacher_availability)
        return super().formatmonth(self.year, self.month, withyear)
