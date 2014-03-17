from django.conf.urls import patterns, url
from main.views import *
from main.cms import *

urlpatterns = patterns('',
    url(r'^$', index),
    url(r'^index.html$', index),
    url(r'^list-(?P<id>[0-9]+)\.html$', list),
    url(r'^art-(?P<id>[0-9]+)\.html$', article),
    url(r'^introduce\.html', introduce),
    url(r'^teachers\.html', teacherls),
    url(r'^tea-(?P<id>[0-9]+)\.html$', teacherdetail),
    url(r'^teaedit-(?P<id>[0-9]+)\.html$', teacheredit),
    url(r'^teaedit-(?P<id>[0-9]+)\.html/(?P<method>[a-z]{5})/$', teacheredit),

    url(r'^login/$', login),
    url(r'^cms/$', cms),
    url(r'^cms/index.html', cms),
    url(r'^cms/(?P<method>[a-z]{4,5})\.html$', cms),
    url(r'^cms/(?P<method>[a-z]{4})-(?P<id>[0-9]+)\.html$', cms),
    url(r'^logout/$', logout),
)