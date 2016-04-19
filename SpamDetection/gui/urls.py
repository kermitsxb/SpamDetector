from django.conf.urls import url
from gui import views

urlpatterns = [
    url(r'^$', views.upload, name='upload'),
    url(r'^upload/$', views.upload, name='upload'),
    url(r'^graph/(?P<cols>\w+)/$', views.graphique, name='graph')
] 