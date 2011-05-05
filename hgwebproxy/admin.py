#:coding=utf-8:

__docformat__ = "restructedtext"

import re
import os

from django.utils.translation import ugettext as _
from django.contrib.admin.util import unquote
from django.contrib import admin
from django import forms

from hgwebproxy.models import Repository
from hgwebproxy.settings import *

class RepositoryAdminForm(forms.ModelForm):
    """
    TODO: List available themes
    """ 
    class Meta:
        model = Repository

    def clean_location(self):
        """
        Checks the repository location to make sure it exists and
        is writable. 
        """
        location = self.cleaned_data["location"]

        if re.match("[\w\d]+://", location):
            raise forms.ValidationError(_("Remote repository locations are not supported"))

        if not os.path.exists(os.path.join(location, '.hg')):
            perm_check_path = location
            if not os.path.exists(location):
                parent_dir = os.path.normpath(os.path.join(location, ".."))
                if not os.path.exists(parent_dir):
                    raise forms.ValidationError(_("This path does not exist."))
                perm_check_path = parent_dir

            if not os.access(perm_check_path, os.W_OK):
                raise forms.ValidationError(_("You don't have sufficient permissions to create a repository at this path."))

        return self.cleaned_data["location"]

class RepositoryAdmin(admin.ModelAdmin):
    actions = None
    list_display = ['name', 'owner', 'description']
    list_filter = ('owner',)
    prepopulated_fields = {
        'slug': ('name',)
    }
    filter_horizontal = (
        'readers','reader_groups',
        'writers','writer_groups',
        'admins', 'admin_groups',
    )
    fieldsets = (
            (None, {
                'fields': (
                    'name', 'slug', 'location',
                    'owner', 'description',
                ),
            }),
            ('Permissions', {
                'fields': (
                    'is_private',
                    'readers', 'writers', 'admins',
                    'reader_groups', 'writer_groups', 'admin_groups',
                ),
                'classes': ('collapse',)
            }),
            ('Options', {
                'fields': (
                    'style', 
                    'allow_archive',
                    'allow_push_ssl',
                ),
                'classes': ('collapse',)
            }),
        )

    
    form = RepositoryAdminForm

admin.site.register(Repository, RepositoryAdmin)
