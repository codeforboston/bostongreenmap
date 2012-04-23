# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Event'
        db.create_table('parkmap_event', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=100, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('parkmap', ['Event'])

        # Adding model 'Park'
        db.create_table('parkmap_park', (
            ('os_id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=100, null=True, blank=True)),
            ('alt_name', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('owner', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('friendsgroup', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('access', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('geometry', self.gf('django.contrib.gis.db.models.fields.MultiPolygonField')()),
        ))
        db.send_create_signal('parkmap', ['Park'])

        # Adding M2M table for field neighborhood on 'Park'
        db.create_table('parkmap_park_neighborhood', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('park', models.ForeignKey(orm['parkmap.park'], null=False)),
            ('neighborhood', models.ForeignKey(orm['parkmap.neighborhood'], null=False))
        ))
        db.create_unique('parkmap_park_neighborhood', ['park_id', 'neighborhood_id'])

        # Adding M2M table for field events on 'Park'
        db.create_table('parkmap_park_events', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('park', models.ForeignKey(orm['parkmap.park'], null=False)),
            ('event', models.ForeignKey(orm['parkmap.event'], null=False))
        ))
        db.create_unique('parkmap_park_events', ['park_id', 'event_id'])

        # Adding model 'Activity'
        db.create_table('parkmap_activity', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal('parkmap', ['Activity'])

        # Adding model 'Facility'
        db.create_table('parkmap_facility', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=100, null=True, blank=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('park', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['parkmap.Park'], null=True, blank=True)),
            ('geometry', self.gf('django.contrib.gis.db.models.fields.PointField')()),
        ))
        db.send_create_signal('parkmap', ['Facility'])

        # Adding M2M table for field activity on 'Facility'
        db.create_table('parkmap_facility_activity', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('facility', models.ForeignKey(orm['parkmap.facility'], null=False)),
            ('activity', models.ForeignKey(orm['parkmap.activity'], null=False))
        ))
        db.create_unique('parkmap_facility_activity', ['facility_id', 'activity_id'])

        # Adding model 'Neighborhood'
        db.create_table('parkmap_neighborhood', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('n_id', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=100, null=True, blank=True)),
            ('geometry', self.gf('django.contrib.gis.db.models.fields.MultiPolygonField')()),
        ))
        db.send_create_signal('parkmap', ['Neighborhood'])

    def backwards(self, orm):
        # Deleting model 'Event'
        db.delete_table('parkmap_event')

        # Deleting model 'Park'
        db.delete_table('parkmap_park')

        # Removing M2M table for field neighborhood on 'Park'
        db.delete_table('parkmap_park_neighborhood')

        # Removing M2M table for field events on 'Park'
        db.delete_table('parkmap_park_events')

        # Deleting model 'Activity'
        db.delete_table('parkmap_activity')

        # Deleting model 'Facility'
        db.delete_table('parkmap_facility')

        # Removing M2M table for field activity on 'Facility'
        db.delete_table('parkmap_facility_activity')

        # Deleting model 'Neighborhood'
        db.delete_table('parkmap_neighborhood')

    models = {
        'parkmap.activity': {
            'Meta': {'object_name': 'Activity'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        'parkmap.event': {
            'Meta': {'object_name': 'Event'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        'parkmap.facility': {
            'Meta': {'object_name': 'Facility'},
            'activity': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['parkmap.Activity']", 'symmetrical': 'False'}),
            'geometry': ('django.contrib.gis.db.models.fields.PointField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'park': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['parkmap.Park']", 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'})
        },
        'parkmap.neighborhood': {
            'Meta': {'object_name': 'Neighborhood'},
            'geometry': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'n_id': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        'parkmap.park': {
            'Meta': {'object_name': 'Park'},
            'access': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'address': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'alt_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'events': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['parkmap.Event']", 'null': 'True', 'blank': 'True'}),
            'friendsgroup': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'geometry': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'neighborhood': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['parkmap.Neighborhood']", 'symmetrical': 'False'}),
            'os_id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'owner': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['parkmap']