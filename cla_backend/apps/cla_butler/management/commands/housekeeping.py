# -*- coding: utf-8 -*-
import datetime

from django.core.management.base import BaseCommand

from ...tasks import DeleteOldData


class Command(BaseCommand):

    help = 'Deletes public diagnosis that are more than a day old'

    def handle(self, *args, **options):
        DeleteOldData().run()
