from datetime import datetime, timedelta
from calendar import HTMLCalendar
from events.models import Event
from django.db.models import Q 

class Calendar(HTMLCalendar):
    def __init__(self, year=None, month=None):
        self.year = year
        self.month = month
        super(Calendar, self).__init__()

    # formats a day as a td
    # filter events by day
    def formatday(self, day, events,eventview):
        events_per_day = events.filter(time_begin__day=day)
        d = ''
        hasevent = False
        if events_per_day:
            hasevent = True
        evlink=""
        for event in events_per_day:
            hasevent=True
            if eventview == 0 or eventview ==3:
                
                if eventview == 3:
                    eventstate = event.state
                    evlink = event.get_event_edit_link
                else:
                    eventstate=""
                    evlink = event.get_org_view_event_html

                d += f'''<li> <img src="/media/{event.src_ID.logo}"><p class= "fillremaining"> {evlink}  <br> {eventstate}</p></li> '''
            elif eventview == 1:
                evlink = event.get_html_url
                d += f'<li> <img src="/media/{event.src_ID.logo}"> <p class= "fillremaining">{evlink} <br>{event.src_ID.acronym}</p> </li>  '
            elif eventview==4:
                eventstate = event.state
                evlink = event.get_cms_edit_link
                d += f'''<li> <img src="/media/{event.src_ID.logo}"><p class= "fillremaining"> {evlink}  <br>{eventstate}</p></li> '''
        if day != 0:
            if hasevent:
                return f"<td class ='eventtd'><span class='date'>{day}</span><ul> {d} </ul></td>"
            else:
                return f"<td><span class='date'>{day}</span><ul> {d} </ul></td>"
        
        
        return "<td></td>"

    # formats a week as a tr
    def formatweek(self, theweek, events, eventview):
        week = ''
        for d, weekday in theweek:
            week += self.formatday(d, events,eventview)
        return f'<tr> {week} </tr>'

    # formats a month as a table
    # filter events by year and month
    def formatmonth(self, org_id, eventview, withyear=True):
        if org_id:
            if eventview ==3:
                events = Event.objects.filter(
                    time_begin__year=self.year, time_begin__month=self.month, src_ID=org_id)
            else:
                events = Event.objects.filter(
                    time_begin__year=self.year, time_begin__month=self.month, src_ID=org_id, state__status="Approved")
        else:
            events = Event.objects.filter(
                time_begin__year=self.year, time_begin__month=self.month, )
            events = events.filter(Q(state__status="Approved")
                           |Q(state__status="OSOA"))
            if eventview ==4:
                events = Event.objects.filter(
                time_begin__year=self.year, time_begin__month=self.month, )
            

        cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar clearfix">\n'
        cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
        cal += f'{self.formatweekheader()}\n'
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f'{self.formatweek(week, events,eventview)}\n'
        return cal
