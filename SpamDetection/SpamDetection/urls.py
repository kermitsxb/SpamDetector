from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns('',
    url(r'^emails/', include('emails.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^$', include('gui.urls')),
    url(r'^gui/', include('gui.urls')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)