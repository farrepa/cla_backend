# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.core.management import call_command
from django.db import models, migrations
import django.utils.timezone
import model_utils.fields


def create_default_categories(apps, schema_editor):
    call_command('loaddata', 'complaint_categories')


def delete_all_categories(apps, schema_editor):
    Category = apps.get_model('complaints', 'Category')
    Category.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('legalaid', '0004_auto_20150803_1443'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'ordering': ['name'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Complaint',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('description', models.TextField(null=True, blank=True)),
                ('source', models.CharField(max_length=15, choices=[(b'EMAIL', b'email'), (b'PHONE', b'phone'), (b'LETTER', b'letter')])),
                ('level', models.PositiveSmallIntegerField(choices=[(29, b'HIGH'), (21, b'MODERATE'), (11, b'MINOR')])),
                ('justified', models.NullBooleanField()),
                ('category', models.ForeignKey(to='complaints.Category')),
                ('created_by', models.ForeignKey(related_name='complaints_complaint_created_by', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('eod', models.ForeignKey(to='legalaid.EODDetails')),
                ('owner', models.ForeignKey(related_name='complaints_complaint_owner', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.RunPython(create_default_categories, delete_all_categories),
    ]
