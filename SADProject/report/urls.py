__author__ = 'Sina'
from django.conf.urls import patterns, include, url
urlpatterns = patterns('SADProject.report.views', url(r'^goods/$', 'goodReportView'),
                       (r'^damaged/$','damagedReportView'),
    (r'^orders/$','orderReportView'))