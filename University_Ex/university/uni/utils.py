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
            d += f'<li class="calendar_list" style="color:green;"> {event.t_a.time_start} - {event.t_a.time_end} </li>'

        if day != 0:
            return f"<td><span class='date'  >{day}</span><ul> {d} </ul></td>"
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

    def formatday(self, day, teacher_availabilities):
        availabilities_per_day = teacher_availabilities.filter(date__day=day)
        d = ''
        for availability in availabilities_per_day:
            d += f'<li style="color:blue";>{availability.teacher_av.username}: {availability.time_start} - {availability.time_end}  </li>'
        if day != 0:
            return f"<td><span class='date'>{day}</span><ul> {d} </ul></td>"
        return '<td></td>'

    def formatweek(self, theweek, teacher_availabilities):
        week = ''
        for d, weekday in theweek:
            week += self.formatday(d, teacher_availabilities)
        return f'<tr> {week} </tr>'

    def formatmonth(self, withyear=True):
        teacher_availabilities = Teacher_Availability.objects.filter(date__year=self.year, date__month=self.month)
        cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
        cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        cal += f'{self.formatweekheader()}\n'
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(week, teacher_availabilities)}\n'
        return cal
