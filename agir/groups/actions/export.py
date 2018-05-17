import csv
from operator import attrgetter
import bleach
from html import unescape
from django.conf import settings
from django.urls import reverse

from agir.lib.export import dicts_to_csv_lines
from agir.api import front_urls


__all__ = ['groups_to_csv', 'groups_to_csv_lines']


COMMON_FIELDS = ['name', 'published', 'contact_email', 'contact_phone', 'description',]
ADDRESS_FIELDS = ['location_name', 'location_address1', 'location_zip', 'location_city']
LINK_FIELDS = ['link', 'admin_link']

FIELDS = COMMON_FIELDS + ['address', 'animators'] + LINK_FIELDS

ANIMATOR_SIMPLE_FIELDS = ['email', 'last_name', 'first_name', 'contact_phone']
ANIMATOR_FIELDS = ANIMATOR_SIMPLE_FIELDS + ['group_name', 'admin_link', 'group_link', 'group_admin_link']

common_extractor = attrgetter(*COMMON_FIELDS)
address_parts_extractor = attrgetter(*ADDRESS_FIELDS)

animator_extractor = attrgetter(*ANIMATOR_SIMPLE_FIELDS)

address_template = "{}, {}, {} {}"
initiator_template = "{first_name} {last_name} {contact_phone} <{email}>"


def memberships_to_csv(queryset, output):
    w = csv.DictWriter(output, fieldnames=ANIMATOR_FIELDS)
    w.writeheader()
    w.writerows(memberships_to_dict(queryset))


def groups_to_csv(queryset, output):
    w = csv.DictWriter(output, fieldnames=FIELDS)
    w.writeheader()
    w.writerows(groups_to_dicts(queryset))


def groups_to_csv_lines(queryset):
    return dicts_to_csv_lines(groups_to_dicts(queryset), fieldnames=FIELDS)


def groups_to_dicts(queryset):
    for g in queryset.iterator():
        d = {k: v for k, v in zip(COMMON_FIELDS, common_extractor(g))}
        d['description'] = unescape(bleach.clean(d['description'].replace('<br />', '\n'), tags=[], strip=True))
        d['address'] = address_template.format(*address_parts_extractor(g))

        animators = (initiator_template.format(**dict(
            zip(ANIMATOR_SIMPLE_FIELDS, animator_extractor(m.person))
        )) for m in g.memberships.filter(is_referent=True))

        d['animators'] = ' / '.join(animators)

        d['link'] = settings.FRONT_DOMAIN + reverse('manage_group', urlconf=front_urls, args=[g.id])
        d['admin_link'] = settings.API_DOMAIN + reverse('admin:groups_supportgroup_change', args=[g.id])

        yield d

def memberships_to_dict(queryset):
    for m in queryset:
        d = {k : v for k, v in zip(ANIMATOR_SIMPLE_FIELDS, animator_extractor(m.person))}
        d['group_name'] = m.supportgroup.name
        d['admin_link'] = settings.API_DOMAIN + reverse('admin:people_person_change', args=[m.person_id])
        d['group_link'] = settings.FRONT_DOMAIN + reverse('manage_group', urlconf=front_urls, args=[m.supportgroup_id])
        d['group_admin_link'] = settings.API_DOMAIN + reverse('admin:groups_supportgroup_change', args=[m.supportgroup_id])

        yield d