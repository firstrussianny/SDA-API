from dataclasses import dataclass

import requests
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


@dataclass
class OEmbedData:
    object_id: str
    title: str
    thumbnail_url: str


def oembed_from_id(object_id, oembed_url, service, field, pattern):
    if not object_id:
        raise ValidationError(
            _("This field does match expected pattern %(pattern)s.") % locals()
        )

    try:
        r = requests.get(oembed_url)
    except requests.RequestException:
        # TODO log exeption
        raise ValidationError(
            _("Could not connect to %(service)s to validate %(field)s.") % locals()
        )

    if r.status_code == 404:
        raise ValidationError(_("%(service)s %(field)s not found.") % locals())

    elif r.status_code != 200:
        # TODO log error
        raise ValidationError(
            _("Could not validate %(field)s due to %(service)s error.") % locals()
        )

    try:
        data = r.json()
    except ValueError:
        raise ValidationError(
            _("Could not validate %(field)s due to invalid response from %(service)s.")
            % locals()
        )

    return OEmbedData(
        object_id=object_id,
        title=data.get("title"),
        thumbnail_url=data.get("thumbnail_url"),
    )
