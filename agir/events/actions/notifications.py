from django.db import transaction

from agir.activity.models import Activity


@transaction.atomic()
def new_event_around_people_notification(event, recipients):
    activity_config = {
        "type": Activity.TYPE_NEW_EVENT_AROUNDME,
        "event": event,
        "status": Activity.STATUS_UNDISPLAYED,
    }
    if event.organizers_groups.count() > 0:
        activity_config["supportgroup"] = event.organizers_groups.first()
    else:
        activity_config["individual"] = event.organizers.first()

    Activity.objects.bulk_create(
        [Activity(**activity_config, recipient=recipient,) for recipient in recipients]
    )
