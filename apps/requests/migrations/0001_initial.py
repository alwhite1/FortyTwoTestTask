# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Requests'
        db.delete_table('Requests')
        db.create_table('Requests', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('path', self.gf('django.db.models.fields.CharField')(default='', max_length=64)),
            ('request', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'requests', ['Requests'])


    def backwards(self, orm):
        # Deleting model 'Requests'
        db.delete_table('Requests')


    models = {
        u'requests.requests': {
            'Meta': {'object_name': 'Requests', 'db_table': "'Requests'"},
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'path': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '64'}),
            'request': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['requests']