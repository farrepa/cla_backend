# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('legalaid', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='case',
            options={'permissions': (('run_reports', 'Can run reports'), ('run_obiee_reports', 'Can run obiee reports'))},
        ),
    ]
