from django.contrib import admin

from .models import Announcement


class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'published', 'last_modified')
    search_fields = ('title',  'description')


admin.site.register(Announcement, AnnouncementAdmin)
