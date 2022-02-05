
from django.urls import path
from . import views

app_name = 'cal'
urlpatterns = [
    path('', views.CalendarView.as_view(), name="calendar"),
    path('event/new/', views.create_event, name='event_new'),
    path('event/edit/(?P<event_id>\d+)/', views.view_event, name='event_edit'),
]
