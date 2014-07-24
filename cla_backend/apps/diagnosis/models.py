import json
from cla_common.constants import DIAGNOSIS_SCOPE
from jsonfield import JSONField
from model_utils.models import TimeStampedModel

from uuidfield import UUIDField

from django.db import models


class DiagnosisTraversal(TimeStampedModel):
    reference = UUIDField(auto=True, unique=True)
    nodes = JSONField(null=True, blank=True)
    current_node_id = models.CharField(blank=True, max_length=50)

    state = models.CharField(blank=True, null=True, max_length=50, default=DIAGNOSIS_SCOPE.UNKNOWN)
    category = models.ForeignKey('legalaid.Category', null=True, blank=True)

