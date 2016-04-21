from django.conf.urls import url
from gui import views

urlpatterns = [
    url(r'^$', views.upload, name='upload'),
    url(r'^upload/$', views.upload, name='upload'),
    url(r'^stats/$', views.statistiques, name='stats'),
    url(r'^stats/graph$', views.graphique, name='graph'),
    url(r'^stats/step', views.updateKMean, name='step')
    #url(r'^graph/(\d+)/(\d+)/(\d+)/$', views.graphique, name='graph')
] 