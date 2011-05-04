from os.path import join, dirname, abspath
from django.conf import settings
from django.utils.translation import ugettext as _

AUTH_REALM  = getattr(settings, 'HGPROXY_AUTH_RELAM', _('Basic Auth'))
STYLES_PATH = getattr(settings, 'HGWEBPROXY_STYLES_PATH',
                        join(dirname(abspath(__file__)), 'templates/hgstyles'))

DEFAULT_STYLE = getattr(settings, 'HGPROXY_DEFAULT_STYLE', 'django_style')
ALLOW_CUSTOM_STYLE = getattr(settings, 'HGPROXY_ALLOW_CUSTOM_STYLE', True)

STATIC_URL  = getattr(settings, 'HGWEBPROXY_STATIC_URL', settings.MEDIA_URL)
STATIC_PATH = getattr(settings, 'HGWEBPROXY_STATIC_PATH', join(settings.MEDIA_ROOT, '../static/'))

REPO_PERMANENT_DELETE = getattr(settings, 'HGPROXY_REPO_PERMANENT_DELETE', False)

ALLOW_HTTP_PUSH = getattr(settings, 'HGPROXY_ALLOW_HTTP_PUSH', False)

# REPO_ROOT allows for rooting all repositories under a specific path.
REPO_ROOT = getattr(settings, 'HGPROXY_REPO_ROOT', None)

# REPO_PATH_CALLBACK is only used when the REPO_ROOT is set.
# If REPO_ROOT is set this callback accepts the repo model instance
# as an argument and returns the relative path from the REPO_ROOT.
# that resolve outsite the REPO_ROOT will cause errors in your application
# so inputs to your path must be checked beforehand for things like '..'.
REPO_PATH_CALLBACK = lambda repo: join(repo.owner.username, repo.slug)

# This is the REPO_ROOT used when running tests.
TEST_REPO_ROOT = getattr(settings, 'HGPROXY_TEST_REPO_ROOT', join(settings.MEDIA_ROOT, 'hg/'))
