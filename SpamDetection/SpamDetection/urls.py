from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^emails/', include('emails.urls')),
    url(r'^admin/', admin.site.urls),
]