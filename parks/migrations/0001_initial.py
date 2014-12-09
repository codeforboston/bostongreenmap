# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Event'
        db.create_table(u'parks_event', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=100, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'parks', ['Event'])

        # Adding model 'Neighborhood'
        db.create_table(u'parks_neighborhood', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('n_id', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=100, null=True, blank=True)),
            ('geometry', self.gf('django.contrib.gis.db.models.fields.MultiPolygonField')(srid=26986)),
        ))
        db.send_create_signal(u'parks', ['Neighborhood'])

        # Adding model 'Parktype'
        db.create_table(u'parks_parktype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
        ))
        db.send_create_signal(u'parks', ['Parktype'])

        # Adding model 'Parkowner'
        db.create_table(u'parks_parkowner', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
        ))
        db.send_create_signal(u'parks', ['Parkowner'])

        # Adding model 'Friendsgroup'
        db.create_table(u'parks_friendsgroup', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
        ))
        db.send_create_signal(u'parks', ['Friendsgroup'])

        # Adding model 'Parkimage'
        db.create_table(u'parks_parkimage', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('caption', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
        ))
        db.send_create_signal(u'parks', ['Parkimage'])

        # Adding model 'Park'
        db.create_table(u'parks_park', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('os_id', self.gf('django.db.models.fields.CharField')(max_length=9, null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=100, unique=True, null=True, blank=True)),
            ('alt_name', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('parktype', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['parks.Parktype'], null=True, blank=True)),
            ('parkowner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['parks.Parkowner'], null=True, blank=True)),
            ('friendsgroup', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['parks.Friendsgroup'], null=True, blank=True)),
            ('access', self.gf('django.db.models.fields.CharField')(max_length=1, null=True, blank=True)),
            ('area', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('geometry', self.gf('django.contrib.gis.db.models.fields.MultiPolygonField')(srid=26986)),
        ))
        db.send_create_signal(u'parks', ['Park'])

        # Adding M2M table for field neighborhoods on 'Park'
        m2m_table_name = db.shorten_name(u'parks_park_neighborhoods')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('park', models.ForeignKey(orm[u'parks.park'], null=False)),
            ('neighborhood', models.ForeignKey(orm[u'parks.neighborhood'], null=False))
        ))
        db.create_unique(m2m_table_name, ['park_id', 'neighborhood_id'])

        # Adding M2M table for field events on 'Park'
        m2m_table_name = db.shorten_name(u'parks_park_events')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('park', models.ForeignKey(orm[u'parks.park'], null=False)),
            ('event', models.ForeignKey(orm[u'parks.event'], null=False))
        ))
        db.create_unique(m2m_table_name, ['park_id', 'event_id'])

        # Adding M2M table for field images on 'Park'
        m2m_table_name = db.shorten_name(u'parks_park_images')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('park', models.ForeignKey(orm[u'parks.park'], null=False)),
            ('parkimage', models.ForeignKey(orm[u'parks.parkimage'], null=False))
        ))
        db.create_unique(m2m_table_name, ['park_id', 'parkimage_id'])

        # Adding model 'Activity'
        db.create_table(u'parks_activity', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal(u'parks', ['Activity'])

        # Adding model 'Facilitytype'
        db.create_table(u'parks_facilitytype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('icon', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
        ))
        db.send_create_signal(u'parks', ['Facilitytype'])

        # Adding model 'Facility'
        db.create_table(u'parks_facility', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('facilitytype', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['parks.Facilitytype'])),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('park', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['parks.Park'], null=True, blank=True)),
            ('notes', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('access', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('geometry', self.gf('django.contrib.gis.db.models.fields.PointField')(srid=26986)),
        ))
        db.send_create_signal(u'parks', ['Facility'])

        # Adding M2M table for field activity on 'Facility'
        m2m_table_name = db.shorten_name(u'parks_facility_activity')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('facility', models.ForeignKey(orm[u'parks.facility'], null=False)),
            ('activity', models.ForeignKey(orm[u'parks.activity'], null=False))
        ))
        db.create_unique(m2m_table_name, ['facility_id', 'activity_id'])

        # Adding model 'Story'
        db.create_table(u'parks_story', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('rating', self.gf('django.db.models.fields.CharField')(default='0', max_length=1)),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=100)),
            ('park', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['parks.Park'], blank=True)),
            ('objectionable_content', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'parks', ['Story'])


    def backwards(self, orm):
        # Deleting model 'Event'
        db.delete_table(u'parks_event')

        # Deleting model 'Neighborhood'
        db.delete_table(u'parks_neighborhood')

        # Deleting model 'Parktype'
        db.delete_table(u'parks_parktype')

        # Deleting model 'Parkowner'
        db.delete_table(u'parks_parkowner')

        # Deleting model 'Friendsgroup'
        db.delete_table(u'parks_friendsgroup')

        # Deleting model 'Parkimage'
        db.delete_table(u'parks_parkimage')

        # Deleting model 'Park'
        db.delete_table(u'parks_park')

        # Removing M2M table for field neighborhoods on 'Park'
        db.delete_table(db.shorten_name(u'parks_park_neighborhoods'))

        # Removing M2M table for field events on 'Park'
        db.delete_table(db.shorten_name(u'parks_park_events'))

        # Removing M2M table for field images on 'Park'
        db.delete_table(db.shorten_name(u'parks_park_images'))

        # Deleting model 'Activity'
        db.delete_table(u'parks_activity')

        # Deleting model 'Facilitytype'
        db.delete_table(u'parks_facilitytype')

        # Deleting model 'Facility'
        db.delete_table(u'parks_facility')

        # Removing M2M table for field activity on 'Facility'
        db.delete_table(db.shorten_name(u'parks_facility_activity'))

        # Deleting model 'Story'
        db.delete_table(u'parks_story')


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