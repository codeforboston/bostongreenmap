# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models
from django.template.defaultfilters import slugify

class Migration(DataMigration):

    def forwards(self, orm):
        "Write your forwards methods here."
        for park in orm.Park.objects.all():
            park.slug = '%s-%d' % (slugify(park.name), park.id)
            park.save()
        # Note: Don't use "from appname.models import ModelName". 
        # Use orm.ModelName to refer to models in this application,
        # and orm['appname.ModelName'] for models in other applications.

    def backwards(self, orm):
        "Write your backwards methods here."

    models = {
        u'parks.activity': {
            'Meta': {'ordering': "['name']", 'object_name': 'Activity'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        u'parks.event': {
            'Meta': {'object_name': 'Event'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        u'parks.facility': {
            'Meta': {'object_name': 'Facility'},
            'access': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'activity': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'activity'", 'symmetrical': 'False', 'to': u"orm['parks.Activity']"}),
            'facilitytype': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['parks.Facilitytype']"}),
            'geometry': ('django.contrib.gis.db.models.fields.PointField', [], {'srid': '26986'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'park': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['parks.Park']", 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'})
        },
        u'parks.facilitytype': {
            'Meta': {'object_name': 'Facilitytype'},
            'icon': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'})
        },
        u'parks.friendsgroup': {
            'Meta': {'object_name': 'Friendsgroup'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'parks.neighborhood': {
            'Meta': {'ordering': "['name']", 'object_name': 'Neighborhood'},
            'geometry': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {'srid': '26986'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'n_id': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        u'parks.park': {
            'Meta': {'object_name': 'Park'},
            'access': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'address': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'alt_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'area': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'events': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'events'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['parks.Event']"}),
            'featured': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'friendsgroup': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['parks.Friendsgroup']", 'null': 'True', 'blank': 'True'}),
            'geometry': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {'srid': '26986'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'images': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'parks'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['parks.Parkimage']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'neighborhoods': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'neighborhoods'", 'blank': 'True', 'to': u"orm['parks.Neighborhood']"}),
            'os_id': ('django.db.models.fields.CharField', [], {'max_length': '9', 'null': 'True', 'blank': 'True'}),
            'parkowner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['parks.Parkowner']", 'null': 'True', 'blank': 'True'}),
            'parktype': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['parks.Parktype']", 'null': 'True', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '100', 'unique': 'True', 'null': 'True', 'blank': 'True'})
        },
        u'parks.parkimage': {
            'Meta': {'ordering': "['pk']", 'object_name': 'Parkimage'},
            'caption': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'})
        },
        u'parks.parkowner': {
            'Meta': {'object_name': 'Parkowner'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'})
        },
        u'parks.parktype': {
            'Meta': {'object_name': 'Parktype'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'})
        },
        u'parks.story': {
            'Meta': {'ordering': "('-date',)", 'object_name': 'Story'},
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'objectionable_content': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'park': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['parks.Park']", 'blank': 'True'}),
            'rating': ('django.db.models.fields.CharField', [], {'default': "'0'", 'max_length': '1'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['parks']
    symmetrical = True
