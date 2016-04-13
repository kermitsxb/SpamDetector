from django.conf.urls import url
from . import views

urlpatterns = [
    # ex: /emails/
    url(r'^$', views.index, name='index'),
    # ex: /emails/5/
    url(r'^(?P<email_id>[0-9]+)/$', views.detail, name='detail'),
    # ex: /emails/5/resultats/
    url(r'^(?P<email_id>[0-9]+)/resultats/$', views.resultats, name='resultats'),
]