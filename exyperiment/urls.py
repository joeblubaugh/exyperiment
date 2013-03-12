__author__ = 'joe'
from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
    url('^$', views.start_page),
    url('^query$', views.query_page),
    )