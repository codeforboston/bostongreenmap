# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Park'
        db.create_table('parkmap_park', (
            ('os_id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('alt_name', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('neighborhood', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('owner', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('friendsgroup', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('access', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('geometry', self.gf('django.contrib.gis.db.models.fields.MultiPolygonField')()),
        ))
        db.send_create_signal('parkmap', ['Park'])

        # Adding model 'Facility'
        db.create_table('parkmap_facility', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('activity', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('greenspace', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['parkmap.Park'], null=True, blank=True)),
            ('geometry', self.gf('django.contrib.gis.db.models.fields.PointField')()),
        ))
        db.send_create_signal('parkmap', ['Facility'])

        # Adding model 'Neighborhood'
        db.create_table('parkmap_neighborhood', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('n_id', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('geometry', self.gf('django.contrib.gis.db.models.fields.MultiPolygonField')()),
        ))
        db.send_create_signal('parkmap', ['Neighborhood'])

    def backwards(self, orm):
        # Deleting model 'Park'
        db.delete_table('parkmap_park')

        # Deleting model 'Facility'
        db.delete_table('parkmap_facility')

        # Deleting model 'Neighborhood'
        db.delete_table('parkmap_neighborhood')

    models = {
        'parkmap.facility': {
            'Meta': {'object_name': 'Facility'},
            'activity': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'geometry': ('django.contrib.gis.db.models.fields.PointField', [], {}),
            'greenspace': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['parkmap.Park']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'})
        },
        'parkmap.neighborhood': {
            'Meta': {'object_name': 'Neighborhood'},
            'geometry': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'n_id': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'parkmap.park': {
            'Meta': {'object_name': 'Park'},
            'access': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'address': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'alt_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'friendsgroup': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'geometry': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'neighborhood': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'os_id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'owner': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['parkmap']