# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Icon'
        db.create_table(u'places_icon', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('icon', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'places', ['Icon'])


        # Renaming column for 'PlaceType.icon' to match new field type.
        db.rename_column(u'places_placetype', 'icon', 'icon_id')
        # Changing field 'PlaceType.icon'
        db.alter_column(u'places_placetype', 'icon_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['places.Icon']))
        # Adding index on 'PlaceType', fields ['icon']
        db.create_index(u'places_placetype', ['icon_id'])


    def backwards(self, orm):
        # Removing index on 'PlaceType', fields ['icon']
        db.delete_index(u'places_placetype', ['icon_id'])

        # Deleting model 'Icon'
        db.delete_table(u'places_icon')


        # Renaming column for 'PlaceType.icon' to match new field type.
        db.rename_column(u'places_placetype', 'icon_id', 'icon')
        # Changing field 'PlaceType.icon'
        db.alter_column(u'places_placetype', 'icon', self.gf('django.db.models.fields.CharField')(max_length=20))

    models = {
        u'places.icon': {
            'Meta': {'object_name': 'Icon'},
            'icon': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'places.place': {
            'Meta': {'ordering': "['name']", 'object_name': 'Place'},
            'create_time': ('django.db.models.fields.DateField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {}),
            'longitude': ('django.db.models.fields.FloatField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'place_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['places.PlaceType']"}),
            'status': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'})
        },
        u'places.placetype': {
            'Meta': {'object_name': 'PlaceType'},
            'icon': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['places.Icon']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'status': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'})
        }
    }

    complete_apps = ['places']