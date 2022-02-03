
import debug_toolbar

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
# django admin header customization
admin.site.site_header = "BulSUan Kawing Administration"
admin.site.site_title = "Welcome to Dashboard"
admin.site.index_title = "Welcome to BulSUan Kawing Portal"

urlpatterns = [
    path('', include('landing.urls'), name="home"),
    path('admin/', admin.site.urls),
    path('accounts/', include('authorization.urls'), name="authorization"),
    path('user/', include('organization.urls'), name='organization'),
    path('cms/', include('bk_admin.urls'), name='admincms'),
    
    # utils
    path('calendar/', include('cal.urls')),

]
urlpatterns += staticfiles_urlpatterns()

if settings.DEBUG:
    urlpatterns += path('__debug__/', include(debug_toolbar.urls)),
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
