from django.test import TestCase
from django.conf import settings

from model_mommy import mommy

from legalaid.models import CaseOutcome

from ..forms import OutcomeForm


def make_recipe(model_name, **kwargs):
    return mommy.make_recipe('legalaid.tests.%s' % model_name, **kwargs)


class OutcomeFormTestCase(TestCase):
    def test_save(self):
        outcome_codes = make_recipe('outcome_code', _quantity=2)
        case = make_recipe('case')
        user = mommy.make(settings.AUTH_USER_MODEL)

        form = OutcomeForm(data={
            'outcome_code': outcome_codes[0].code,
            'outcome_notes': 'lorem ipsum',
        })

        self.assertTrue(form.is_valid())
        self.assertEqual(CaseOutcome.objects.count(), 0)

        form.save(case, user)

        self.assertEqual(CaseOutcome.objects.count(), 1)
        self.assertEqual(CaseOutcome.objects.all()[0].case, case)