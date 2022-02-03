from django.contrib import admin
from .models import GeneralInformation, Officer, TypesOfOrganization

admin.site.register(GeneralInformation)
admin.site.register(Officer)
admin.site.register(TypesOfOrganization)


