import re
import os

from django.db import models
from django.db.models.signals import pre_save, post_save, post_delete
from django.db.models import permalink, Q
from django.contrib.auth.models import User, Group
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from django.contrib.sites.models import Site

from hgwebproxy.api import *
from hgwebproxy import settings as hgwebproxy_settings

class RepositoryManager(models.Manager):
    def has_view_permission(self, user):
        return self._readable(user)

    def has_pull_permission(self, user):
        if not self._has_model_perm(user, 'pull'):
            return self.none()
        else:
            return self._readable(user)

    def has_push_permission(self, user):
        if not self._has_model_perm(user, 'push'):
            return self.none()
        else:
            return self._writable(user)

    def has_change_permission(self, user):
        if not self._has_model_perm(user, 'change'):
            return self.none()
        else:
            return self._admin(user)

    def has_delete_permission(self, user):
        if not self._has_model_perm(user, 'delete'):
            return self.none()
        else:
            return self._admin(user)

    def _has_model_perm(self, user, perm):
        opts = Repository._meta
        # Special case for custom permissions.
        if perm in ('push', 'pull'):
            perm_name = '%s_repository' % perm
        else:
            perm_name = getattr(opts, 'get_%s_permission' % perm, lambda: False)()
        return user.has_perm(opts.app_label + '.' + perm_name)

    def _readable(self, user):
        if user.is_superuser:
            return self.all()
        return self.distinct().filter(
            Q(is_private = False) |
            Q(owner = user) | 
            Q(readers = user) |
            Q(writers = user) |
            Q(admins = user) |
            Q(reader_groups__in=user.groups.all()) |
            Q(writer_groups__in=user.groups.all()) |
            Q(admin_groups__in=user.groups.all())
        )

    def _writable(self, user): 
        if user.is_superuser:
            return self.all()
        return self.distinct().filter(
            Q(owner = user) | 
            Q(writers = user) |
            Q(admins = user) |
            Q(writer_groups__in=user.groups.all()) |
            Q(admin_groups__in=user.groups.all())
        )

    def _admin(self, user):
        if user.is_superuser:
            return self.all()
        return self.distinct().filter(
            Q(owner = user) | 
            Q(admins = user) |
            Q(admin_groups__in=user.groups.all())
        )

def validate_slug(value):
    """
    Checks the repository slug
    """
    if not value.isalnum():
        raise ValidationError(_('%s is not a valid name') % value)

def validate_location(value):
    """
    TODO:
    Checks the repository location to make sure it exists and is writable.
    """
    if re.match("[\w\d]+://", value):
        raise ValidationError(_("Remote repository locations are not supported"))

    if not os.path.exists(os.path.join(value, '.hg')):
        if not os.path.exists(value):
            parent_dir = os.path.normpath(os.path.join(value, ".."))
            if not os.path.exists(parent_dir):
                raise ValidationError(_("This path does not exist."))
            perm_check_path = parent_dir
        else:
            perm_check_path = value

        if not os.access(perm_check_path, os.W_OK):
            raise ValidationError(_("You don't have sufficient permissions to create a repository at this path."))

def validate_archive(value):
    """
    TODO: Validate archive declaration to the form "zip, bz2, gz"
    """
    pass

def validate_style(value):
    """
    TODO: Validate style setting, it must be an existing style in mercurial
          and also in the Project
    """
    if not is_template(value):
        raise ValidationError(_("'%s' is not an available style." % value))

class Repository(models.Model):
    name = models.CharField(max_length=140)
    slug = models.SlugField(help_text='Would be the name of the repo. Do not use "-" inside the name')
    owner = models.ForeignKey(User)
    parent_repo = models.ForeignKey('self', null=True, related_name='descendents',
        editable=False)
    location = models.CharField(max_length=200,
            help_text=_('The absolute path to the repository. If the repository does not exist it will be created.'))
    description = models.TextField(blank=True, null=True)

    allow_archive = models.CharField(max_length=100, blank=True, null=True,
        help_text=_("Same as in hgrc config, as: zip, bz2, gz"))
    allow_push_ssl = models.BooleanField(_('Require SSL for push?'), default=False, help_text=_("You must set your webserver to handle secure http connection"))
    is_private = models.BooleanField(_('Private?'), default=False,
        help_text=_('Private repositories It can only be seen by the owner and allowed users'))
    style = models.CharField(max_length=256, blank=True, null=True, default=hgwebproxy_settings.DEFAULT_STYLE,
        help_text=_('The hgweb style'), )

    readers = models.ManyToManyField(User, related_name="repository_readable_set", blank=True, null=True)
    writers = models.ManyToManyField(User, related_name="repository_writeable_set", blank=True, null=True)
    admins = models.ManyToManyField(User, related_name="repository_admin_set", blank=True, null=True)
    reader_groups = models.ManyToManyField(Group, related_name="repository_readable_set", blank=True, null=True)
    writer_groups = models.ManyToManyField(Group, related_name="repository_writeable_set", blank=True, null=True)
    admin_groups = models.ManyToManyField(Group, related_name="repository_admin_set", blank=True, null=True)

    objects = RepositoryManager()

    def __unicode__(self):
        return u"%s's %s" % (self.owner.username, self.name)

    def _is_reader(self, user):
        return not user.is_anonymous() and (
            self.readers.filter(pk=user.pk).exists() or
            self.reader_groups.filter(
                pk__in=map(lambda g: g.pk, user.groups.all())
            ).exists()
        )

    def _is_writer(self, user):
        return not user.is_anonymous() and (
            self.writers.filter(pk=user.pk).exists() or
            self.writer_groups.filter(
                pk__in=map(lambda g: g.pk, user.groups.all())
            ).exists()
        )

    def _is_admin(self, user):
        return not user.is_anonymous() and (
            user.is_superuser or
            user.pk == self.owner_id or
            self.admins.filter(pk=user.pk).exists() or
            self.admin_groups.filter(
                pk__in=map(lambda g: g.pk, user.groups.all())
            ).exists()
        )
    has_change_permission = _is_admin
    has_delete_permission = _is_admin

    def has_view_permission(self, user):
        return (
            not self.is_private or
            self._is_reader(user) or
            self._is_writer(user) or
            self._is_admin(user)
        )
    can_browse = has_view_permission
    has_pull_permission = has_view_permission
    can_pull = has_pull_permission
    
    def has_push_permission(self, user):
        return (
            self._is_writer(user) or
            self._is_admin(user)
        )
    can_push = has_push_permission

    @permalink
    def get_absolute_url(self):
        return ('repo_detail', (), {
            'username': self.owner.username,
            'pattern': self.slug + "/",
        })

    @property
    def get_clone_url(self):
        current_site = Site.objects.get_current()
        return 'http://%s%s' % (current_site.domain, self.get_absolute_url())

    @property
    def lastchange(self):
        tip_info = get_changeset_info(self.location, 'tip')
        if tip_info:
            return tip_info['date']
        else:
            return None

    class Meta:
        verbose_name = _('repository')
        verbose_name_plural = _('repositories')
        ordering = ['name']
        unique_together = ('slug', 'owner')
        permissions = (
            ("push_repository", "Can push to repository"),
            ("pull_repository", "Can pull from repository"),
        )

def _repo_post_save(sender, instance, **kwargs):
    create_repository(instance.location)
post_save.connect(_repo_post_save, sender=Repository)

def _repo_post_delete(sender, instance, **kwargs):
    delete_repository(instance.location)
post_delete.connect(_repo_post_delete, sender=Repository)
