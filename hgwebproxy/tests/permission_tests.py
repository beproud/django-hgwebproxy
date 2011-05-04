#:coding=utf-8:

from django.contrib.auth.models import User
from django.test import TestCase as DjangoTestCase
from django.core.urlresolvers import reverse

from hgwebproxy.tests.base import RepoTestCase
from hgwebproxy.models import Repository

class PermissionTest(RepoTestCase):
    fixtures = ['basic.json']

    def assertReader(self, repo, user):
        self.assertTrue(repo.can_browse(user))
        self.assertTrue(repo.can_pull(user))
        self.assertFalse(repo.can_push(user))

    def assertWriter(self, repo, user):
        self.assertTrue(repo.can_browse(user))
        self.assertTrue(repo.can_pull(user))
        self.assertTrue(repo.can_push(user))

    def test_admin(self):
        user = User.objects.get(username="admin")
        repo = Repository.objects.get(slug='test-repo')

        self.assertWriter(repo, user)

    def test_reader(self):
        user = User.objects.get(username="reader")
        repo = Repository.objects.get(slug='test-repo')

        self.assertReader(repo, user)

    def test_writer(self):
        user = User.objects.get(username="writer")
        repo = Repository.objects.get(slug='test-repo')

        self.assertWriter(repo, user)

    def test_group_reader(self):
        user = User.objects.get(username="group_reader")
        repo = Repository.objects.get(slug='test-repo')

        self.assertReader(repo, user)

    def test_owner(self):
        user = User.objects.get(username="owner")
        repo = Repository.objects.get(slug='test-repo')

        self.assertWriter(repo, user)

    def test_has_view_permission(self):
        admin = User.objects.get(username="admin") 
        repos = Repository.objects.has_change_permission(admin)
        self.assertEqual(repos.count(), 1)

        owner = User.objects.get(username="owner") 
        repos = Repository.objects.has_view_permission(owner)
        self.assertEqual(repos.count(), 1)

        reader = User.objects.get(username="reader") 
        repos = Repository.objects.has_view_permission(reader)
        self.assertEqual(repos.count(), 1)

        writer = User.objects.get(username="writer") 
        repos = Repository.objects.has_view_permission(writer)
        self.assertEqual(repos.count(), 1)

        group_reader = User.objects.get(username="group_reader") 
        repos = Repository.objects.has_view_permission(group_reader)
        self.assertEqual(repos.count(), 1)

        group_writer = User.objects.get(username="group_writer") 
        repos = Repository.objects.has_view_permission(group_writer)
        self.assertEqual(repos.count(), 1)

        model_perms = User.objects.get(username="model_perms") 
        repos = Repository.objects.has_view_permission(model_perms)
        self.assertEqual(repos.count(), 0)

        no_perms = User.objects.get(username="no_perms") 
        repos = Repository.objects.has_view_permission(no_perms)
        self.assertEqual(repos.count(), 0)

    def test_has_change_permission(self):
        admin = User.objects.get(username="admin") 
        repos = Repository.objects.has_change_permission(admin)
        self.assertEqual(repos.count(), 1)

        owner = User.objects.get(username="owner") 
        repos = Repository.objects.has_change_permission(owner)
        self.assertEqual(repos.count(), 1)

        reader = User.objects.get(username="reader") 
        repos = Repository.objects.has_change_permission(reader)
        self.assertEqual(repos.count(), 0)

        writer = User.objects.get(username="writer") 
        repos = Repository.objects.has_change_permission(writer)
        self.assertEqual(repos.count(), 0)

        group_reader = User.objects.get(username="group_reader") 
        repos = Repository.objects.has_change_permission(group_reader)
        self.assertEqual(repos.count(), 0)

        group_writer = User.objects.get(username="group_writer") 
        repos = Repository.objects.has_change_permission(group_writer)
        self.assertEqual(repos.count(), 0)

        model_perms = User.objects.get(username="model_perms") 
        repos = Repository.objects.has_change_permission(model_perms)
        self.assertEqual(repos.count(), 0)

        no_perms = User.objects.get(username="no_perms") 
        repos = Repository.objects.has_change_permission(no_perms)
        self.assertEqual(repos.count(), 0)

    def test_has_delete_permission(self):
        admin = User.objects.get(username="admin") 
        repos = Repository.objects.has_delete_permission(admin)
        self.assertEqual(repos.count(), 1)

        owner = User.objects.get(username="owner") 
        repos = Repository.objects.has_delete_permission(owner)
        self.assertEqual(repos.count(), 1)

        reader = User.objects.get(username="reader") 
        repos = Repository.objects.has_delete_permission(reader)
        self.assertEqual(repos.count(), 0)

        writer = User.objects.get(username="writer") 
        repos = Repository.objects.has_delete_permission(writer)
        self.assertEqual(repos.count(), 0)

        group_reader = User.objects.get(username="group_reader") 
        repos = Repository.objects.has_delete_permission(group_reader)
        self.assertEqual(repos.count(), 0)

        group_writer = User.objects.get(username="group_writer") 
        repos = Repository.objects.has_delete_permission(group_writer)
        self.assertEqual(repos.count(), 0)

        model_perms = User.objects.get(username="model_perms") 
        repos = Repository.objects.has_delete_permission(model_perms)
        self.assertEqual(repos.count(), 0)

        no_perms = User.objects.get(username="no_perms") 
        repos = Repository.objects.has_delete_permission(no_perms)
        self.assertEqual(repos.count(), 0)

    def test_has_push_permission(self):
        admin = User.objects.get(username="admin") 
        repos = Repository.objects.has_push_permission(admin)
        self.assertEqual(repos.count(), 1)

        owner = User.objects.get(username="owner") 
        repos = Repository.objects.has_push_permission(owner)
        self.assertEqual(repos.count(), 1)

        reader = User.objects.get(username="reader") 
        repos = Repository.objects.has_push_permission(reader)
        self.assertEqual(repos.count(), 0)

        writer = User.objects.get(username="writer") 
        repos = Repository.objects.has_push_permission(writer)
        self.assertEqual(repos.count(), 1)

        group_reader = User.objects.get(username="group_reader") 
        repos = Repository.objects.has_push_permission(group_reader)
        self.assertEqual(repos.count(), 0)

        group_writer = User.objects.get(username="group_writer") 
        repos = Repository.objects.has_push_permission(group_writer)
        self.assertEqual(repos.count(), 1)

        model_perms = User.objects.get(username="model_perms") 
        repos = Repository.objects.has_push_permission(model_perms)
        self.assertEqual(repos.count(), 0)

        no_perms = User.objects.get(username="no_perms") 
        repos = Repository.objects.has_push_permission(no_perms)
        self.assertEqual(repos.count(), 0)

    def test_has_pull_permission(self):
        admin = User.objects.get(username="admin") 
        repos = Repository.objects.has_pull_permission(admin)
        self.assertEqual(repos.count(), 1)

        owner = User.objects.get(username="owner") 
        repos = Repository.objects.has_pull_permission(owner)
        self.assertEqual(repos.count(), 1)

        reader = User.objects.get(username="reader") 
        repos = Repository.objects.has_pull_permission(reader)
        self.assertEqual(repos.count(), 1)

        writer = User.objects.get(username="writer") 
        repos = Repository.objects.has_pull_permission(writer)
        self.assertEqual(repos.count(), 1)

        group_reader = User.objects.get(username="group_reader") 
        repos = Repository.objects.has_pull_permission(group_reader)
        self.assertEqual(repos.count(), 1)

        group_writer = User.objects.get(username="group_writer") 
        repos = Repository.objects.has_pull_permission(group_writer)
        self.assertEqual(repos.count(), 1)

        model_perms = User.objects.get(username="model_perms") 
        repos = Repository.objects.has_pull_permission(model_perms)
        self.assertEqual(repos.count(), 0)

        no_perms = User.objects.get(username="no_perms") 
        repos = Repository.objects.has_pull_permission(no_perms)
        self.assertEqual(repos.count(), 0)

