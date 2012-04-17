# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Facility.green_space'
        db.delete_column('parkmap_facility', 'green_space')

        # Adding field 'Facility.greenspace'
        db.add_column('parkmap_facility', 'greenspace',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['parkmap.Greenspace'], null=True, blank=True),
                      keep_default=False)

    def backwards(self, orm):
        # Adding field 'Facility.green_space'
        db.add_column('parkmap_facility', 'green_space',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Deleting field 'Facility.greenspace'
        db.delete_column('parkmap_facility', 'greenspace_id')

    models = {
        'parkmap.facility': {
            'Meta': {'object_name': 'Facility'},
            'activity': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'geometry': ('django.contrib.gis.db.models.fields.PointField', [], {}),
            'greenspace': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['parkmap.Greenspace']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'})
        },
        'parkmap.greenspace': {
            'Meta': {'object_name': 'Greenspace'},
            'access': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'address': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'alt_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'friendsgroup': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'geometry': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'neighborhood': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'owner': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'parkmap.neighborhood': {
            'Meta': {'object_name': 'Neighborhood'},
            'geometry': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'n_id': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['parkmap']