__author__ = 'joe'
from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
    url('^$', views.start_page),
    url('^experiment', views.experiment_page),
    url('^survey', views.survey),
    )