from django.contrib import admin


from .models import Organization, Program


class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'program', 'category',
                    'year_established', 'state')
    list_filter = ('category', 'state')
    search_fields = ['name', 'program']
    
    
class ProgramAdmin(admin.ModelAdmin):
    list_filter = ['college']
    search_fields = ['name', 'college', 'acronym']

admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Program, ProgramAdmin)
