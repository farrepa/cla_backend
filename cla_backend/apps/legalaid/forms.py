from datetime import timedelta

from django.utils import timezone
from django.conf import settings
from django.utils import timezone

from cla_common.call_centre_availability import OpeningHours, available_days, time_slots
from cla_eventlog.forms import BaseCaseLogForm


def is_in_business_hours(dt):
    if not dt.tzinfo:
        dt = timezone.make_aware(dt, timezone.get_default_timezone())

    OPERATOR_HOURS = OpeningHours(**settings.OPERATOR_HOURS)
    in_business_hours = dt in OPERATOR_HOURS
    if in_business_hours:
        return (True, None)
    else:
        available_slots = time_slots(dt.date())
        remainder = timedelta(minutes=15)
        if available_slots:
            end_of_day = timezone.make_aware(available_slots[-1] + timedelta(minutes=15), timezone.get_default_timezone())
            remainder = dt - end_of_day

        return (False, remainder)

def get_sla_time(start_time, minutes):
    simple_delta = start_time + timedelta(minutes=minutes)
    in_business_hours, remainder_delta = is_in_business_hours(simple_delta)
    if not in_business_hours:
        next_business_day = filter(lambda x: x.date() > start_time.date(), available_days(365))[0]
        start_of_next_business_day = timezone.make_aware(time_slots(next_business_day.date())[0], timezone.get_default_timezone())
        return start_of_next_business_day + remainder_delta

    return simple_delta

class BaseCallMeBackForm(BaseCaseLogForm):
    LOG_EVENT_KEY = 'call_me_back'

    def get_requires_action_at(self):
        raise NotImplementedError()

    def get_context(self):
        requires_action_at = self.get_requires_action_at()

        return {
            'requires_action_at': requires_action_at,
            'sla_15': get_sla_time(requires_action_at, 15),
            'sla_120': get_sla_time(requires_action_at, 120)
        }

    def get_notes(self):
        dt = timezone.localtime(self.get_requires_action_at())
        return u"Callback scheduled for {dt}. {notes}".format(
            dt=dt.strftime("%d/%m/%Y %H:%M"),
            notes=self.cleaned_data['notes'] or ""
        )

    def save(self, user):
        super(BaseCallMeBackForm, self).save(user)
        dt = self.get_requires_action_at()
        self.case.set_requires_action_at(dt)
