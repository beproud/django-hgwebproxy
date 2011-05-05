#:coding=utf-8:

import os

from django.contrib.auth.models import User
from django.test import TestCase as DjangoTestCase
from django.core.urlresolvers import reverse
from django.utils.http import urlencode
from django.conf import settings

from hgwebproxy.tests.base import RepoTestCase, RequestTestCaseMixin
from hgwebproxy import settings as hgwebproxy_settings

class HgWebTest(RequestTestCaseMixin, RepoTestCase):
    fixtures = ['basic.json']

    def test_hgwebdir_top(self):
        response = self.client.get(reverse("repo_index"))
        self.assertOk(response)
        self.assertHtml(response)

    def test_repo_detail(self):
        self.client.login(username="owner", password="owner")

        response = self.client.get(reverse('repo_detail',  kwargs={
            'username':'owner',
            'pattern': 'test-repo/',
        }))
        self.assertOk(response)
        self.assertHtml(response)

    def test_repo_detail_forbidden(self):
        self.client.login(username="no_perms", password="no_perms")
        response = self.client.get(reverse('repo_detail',  kwargs={
            'username': 'owner',
            'pattern':'test-repo/',
        }))
        self.assertForbidden(response)
