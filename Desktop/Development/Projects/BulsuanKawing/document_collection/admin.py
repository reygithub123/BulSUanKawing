from django.contrib import admin

from .models import DocumentCollection, Document, Category


class DocumentCollectionAdmin(admin.ModelAdmin):
    list_display = ('__str__',  'category', 'state','submitted')
    list_filter = ['category', 'state']
    search_fields = ('name', 'src_ID__name')


class DocumentAdmin (admin.ModelAdmin):
    list_display = ['collection','name']



admin.site.register(DocumentCollection, DocumentCollectionAdmin)
admin.site.register(Document, DocumentAdmin)
admin.site.register(Category)
