__docformat__ = "restructedtext"

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
    
    form = RepositoryAdminForm

    def get_fieldsets(self, request, obj=None):
        fields = ['name', 'slug']
        
        # If we are ROOTing the repositories don't allow
        # changing of the repository location.
        # However, if the user is a superuser then show
        # the location as read-only.
        if request.user.is_superuser or REPO_ROOT is None:
            fields += ['location']

        # Only allow superusers to change the owner.
        if request.user.is_superuser:
            fields += ['owner']

        fields += ['description']

        return (
            (None, {
                'fields': fields,
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

    def get_form(self, request, obj=None, **kwargs):
        exclude = []

        # If we are ROOTing the repositories don't allow
        # changing of the repository location.
        # However, if the user is a superuser then show
        # the location as read-only.
        if not request.user.is_superuser and REPO_ROOT is not None:
            exclude.append('location')

        # Don't allow users other than superusers to change the owner.
        if not request.user.is_superuser:
            exclude.append('owner')

        exclude.extend(kwargs.get("exclude", []))
        exclude.extend(self.get_readonly_fields(request, obj))
        kwargs["exclude"] = exclude

        formcls = super(RepositoryAdmin, self).get_form(request, obj, **kwargs)
        # Add the request to the newly created form class
        formcls.request = request
        return formcls

    def get_readonly_fields(self, request, *args, **kwargs):
        fields = list(super(RepositoryAdmin, self).get_readonly_fields(request, *args, **kwargs))
        # Allow superusers to see the location but not modify it
        # if we are rooting the repos
        if request.user.is_superuser and REPO_ROOT is not None:
            fields = fields + ['location']

        return fields

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "owner":
            # Set the initial value to the current user.
            kwargs['initial'] = request.user
            
            # NOTE: Owner should only be displayed for superusers.
            # This is here for completeness really.
            if not request.user.is_superuser:
                queryset = kwargs.get('queryset', User.objects.all())
                kwargs["queryset"] = queryset.filter(pk=request.user.pk)
        return super(RepositoryAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def change_view(self, request, object_id, extra_context=None):
        # Redirect the user to the public repository view if
        # The user does not have permission to change the repository.
        obj = self.get_object(request, object_id)
        if (self.has_view_permission(request, obj) and not
                self.has_change_permission(request, obj)):
            return redirect(obj)
        else:
            return super(RepositoryAdmin, self).change_view(request, object_id, extra_context)

    def queryset(self, request):
        # Only show repositories we can view in the changelist
        return Repository.objects.has_view_permission(request.user)

    def save_model(self, request, obj, form, change):
        # In the case where the owner was not set 
        # set it to the current user. Owner is not present in the form
        # for non-superusers.
        if not obj.owner_id:
            obj.owner = request.user
        obj.save()

    def has_view_permission(self, request, obj=None):
        opts = self.opts
        perm_name = 'view_repository'
        has_perm = request.user.has_perm(opts.app_label + '.' + perm_name)
        if obj:
            has_perm = has_perm and obj.has_view_permission(request.user)
        return has_perm 
    
    def has_change_permission(self, request, obj=None):
        has_perm = super(RepositoryAdmin, self).has_change_permission(request, obj)
        if obj:
            has_perm = has_perm and obj.has_change_permission(request.user)
        return has_perm

    def has_delete_permission(self, request, obj=None):
        has_perm = super(RepositoryAdmin, self).has_delete_permission(request, obj)
        if obj:
            has_perm = has_perm and obj.has_delete_permission(request.user)
        return has_perm

admin.site.register(Repository, RepositoryAdmin)
