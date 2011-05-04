#:coding=utf-8:
from django.conf.urls.defaults import *
from django.conf import settings

urlpatterns = patterns('hgwebproxy.views',
    url('^$', 'repo_index', name='repo_index'),
    url('^(?P<username>[\w-]+)/$', 'user_repos', name='user_repos'),
    url('^(?P<username>[\w-]+)/(?P<pattern>[\w-]+)', 'repo_detail', name='repo_detail'),
)

if settings.DEBUG:
    urlpatterns += patterns('hgwebproxy.views',
        url('^static/(?P<file_name>.+)$', 'static_file', name='repo_static_file'),
    )
