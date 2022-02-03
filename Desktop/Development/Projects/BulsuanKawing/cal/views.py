
import calendar
from datetime import date, datetime, timedelta

from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.http.response import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils.safestring import mark_safe
from .forms import EventForm

from .utils import Calendar
from django.views import generic

from events.models import Event

def check_admin (user):
    return user.is_superuser


@login_required(login_url="/accounts/login/")
@user_passes_test(check_admin)
def view_event(request, event_id=None):
    ev = Event
    if event_id:
        ev = get_object_or_404(Event, pk=event_id)
    else:
        ev = Event
    form = EventForm(request.POST or None, instance=ev)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('cal:calendar'))
    return render(request, 'cal/event.html', {'form': form})


@login_required(login_url="/accounts/login/")
@user_passes_test(check_admin)
def create_event(request):
    form = EventForm(request.POST or None)
    if request.POST and form.is_valid():
        src_ID = form.cleaned_data['src_ID']
        title = form.cleaned_data['title']
        time_begin = form.cleaned_data['time_begin']
        time_end = form.cleaned_data['time_end']
        description = form.cleaned_data['description']
        img_ID = form.cleaned_data['img_ID']
        Event.objects.get_or_create(
            src_ID=src_ID,
            title=title,
            time_begin=time_begin,
            time_end=time_end,
            description=description,
            img_ID=img_ID
        )
        return HttpResponseRedirect(reverse('cal:calendar'))
    return render(request, 'cal/event.html', {'form': form})


class CalendarView(LoginRequiredMixin, generic.ListView):
    login_url = "/accounts/login/"
    model = Event
    template_name = 'cal/calendar.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # use today's date for the calendar
        d = get_date(self.request.GET.get('month', None))

        # Instantiate calendar class with today's year and date
        cal = Calendar(d.year, d.month)

        # Call the formatmonth method, which returns our calendar as a table
        eventview = 1#event view level
        html_cal = cal.formatmonth(False,eventview,withyear=True)
        context['calendar'] = mark_safe(html_cal)

        # call previous or next month
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)

        return context


def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return date(year, month, day=1)
    return datetime.today()


def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month


def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month
