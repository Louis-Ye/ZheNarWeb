# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'PlaceType'
        db.create_table(u'places_placetype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('color', self.gf('django.db.models.fields.SmallIntegerField')(default=9)),
        ))
        db.send_create_signal(u'places', ['PlaceType'])

        # Adding model 'Place'
        db.create_table(u'places_place', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('status', self.gf('django.db.models.fields.SmallIntegerField')(default=1)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('place_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['places.PlaceType'])),
            ('latitude', self.gf('django.db.models.fields.FloatField')()),
            ('longitude', self.gf('django.db.models.fields.FloatField')()),
            ('create_time', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal(u'places', ['Place'])


    def backwards(self, orm):
        # Deleting model 'PlaceType'
        db.delete_table(u'places_placetype')

        # Deleting model 'Place'
        db.delete_table(u'places_place')


    models = {
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
            'color': ('django.db.models.fields.SmallIntegerField', [], {'default': '9'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['places']