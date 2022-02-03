from django.contrib import admin

from .models import Event, EventState


class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'src_ID', 'time_begin', 'time_end')
    search_fields = ('title', 'src_ID__name')





admin.site.register(Event, EventAdmin)
admin.site.register(EventState)
