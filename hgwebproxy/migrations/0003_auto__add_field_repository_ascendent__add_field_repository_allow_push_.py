# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Repository.ascendent'
        db.add_column('hgwebproxy_repository', 'ascendent', self.gf('django.db.models.fields.related.ForeignKey')(related_name='descendents', null=True, to=orm['hgwebproxy.Repository']), keep_default=False)

        # Adding field 'Repository.allow_push_ssl'
        db.add_column('hgwebproxy_repository', 'allow_push_ssl', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)

        # Adding field 'Repository.is_private'
        db.add_column('hgwebproxy_repository', 'is_private', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Repository.ascendent'
        db.delete_column('hgwebproxy_repository', 'ascendent_id')

        # Deleting field 'Repository.allow_push_ssl'
        db.delete_column('hgwebproxy_repository', 'allow_push_ssl')

        # Deleting field 'Repository.is_private'
        db.delete_column('hgwebproxy_repository', 'is_private')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'hgwebproxy.repository': {
            'Meta': {'ordering': "['name']", 'object_name': 'Repository'},
            'admin_groups': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'repository_admin_set'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['auth.Group']"}),
            'admins': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'repository_admin_set'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['auth.User']"}),
            'allow_archive': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'allow_push_ssl': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'ascendent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'descendents'", 'null': 'True', 'to': "orm['hgwebproxy.Repository']"}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_private': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'reader_groups': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'repository_readable_set'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['auth.Group']"}),
            'readers': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'repository_readable_set'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['auth.User']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'}),
            'style': ('django.db.models.fields.CharField', [], {'default': "'django_style'", 'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'writer_groups': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'repository_writeable_set'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['auth.Group']"}),
            'writers': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'repository_writeable_set'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['auth.User']"})
        }
    }

    complete_apps = ['hgwebproxy']
