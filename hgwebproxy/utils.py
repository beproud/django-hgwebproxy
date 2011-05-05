import re
from django.contrib.auth import authenticate

def is_mercurial(request):
    """
    User agent processor to determine whether the incoming
    user is someone using a browser, or a mercurial client

    In order to qualify as a mercurial user they must have a user
    agent value that starts with mercurial and an Accept header that
    starts with application/mercurial. This guarantees we only force
    those who are actual mercurial users to use Basic Authentication
    """
    agent = re.compile(r'^(mercurial).*')
    accept = request.META.get('HTTP_ACCEPT', None)
    result = agent.match(request.META.get('HTTP_USER_AGENT', ""))

    if result and accept.startswith('application/mercurial-'):
        return True
    else:
        return False

def basic_auth(request, realm, repo):
    """
    Very simple Basic authentication handler
    """

    if request.user.is_authenticated():
        user = request.user
        username = request.user.username
    else:
        auth_string = request.META.get('HTTP_AUTHORIZATION')
        
        if auth_string is None or not auth_string.startswith("Basic"):
            return False

        _, basic_hash = auth_string.split(' ', 1)
        username, password = basic_hash.decode('base64').split(':', 1)
        user = authenticate(username=username, password=password)

        if request.method == "POST":
            #   User can push to any repo?
            if user and repo.has_push_permission(user):
                return username
        else:
            #   User can pull to any repo?
            if repo.is_public:
                # If the repo is public return a "*" to
                # indicate any user
                return "*"
            elif user and repo.has_pull_permission(user):
                return username

    return False
