# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ClassificationRequest'
        db.create_table(u'emotion_classificationrequest', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('type', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal(u'emotion', ['ClassificationRequest'])

        # Adding model 'ImageClassification'
        db.create_table(u'emotion_imageclassification', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('request', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['emotion.ClassificationRequest'])),
            ('image', self.gf('django.db.models.fields.TextField')()),
            ('rank1', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('rank1_prob', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('rank2', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('rank2_prob', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('rank3', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('rank3_prob', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('rank4', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('rank4_prob', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('rank5', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('rank5_prob', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('rank6', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('rank6_prob', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('rank7', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('rank7_prob', self.gf('django.db.models.fields.CharField')(max_length=15)),
        ))
        db.send_create_signal(u'emotion', ['ImageClassification'])


    def backwards(self, orm):
        # Deleting model 'ClassificationRequest'
        db.delete_table(u'emotion_classificationrequest')

        # Deleting model 'ImageClassification'
        db.delete_table(u'emotion_imageclassification')


    models = {
        u'emotion.classificationrequest': {
            'Meta': {'object_name': 'ClassificationRequest'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        u'emotion.imageclassification': {
            'Meta': {'object_name': 'ImageClassification'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.TextField', [], {}),
            'rank1': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'rank1_prob': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'rank2': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'rank2_prob': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'rank3': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'rank3_prob': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'rank4': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'rank4_prob': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'rank5': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'rank5_prob': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'rank6': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'rank6_prob': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'rank7': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'rank7_prob': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'request': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['emotion.ClassificationRequest']"})
        }
    }

    complete_apps = ['emotion']