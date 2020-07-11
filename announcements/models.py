# -*- coding: utf-8 -*-
import uuid

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django_auxilium.models import BaseModel
from files.models import Attachment
from utils.models import BleachRichTextField


class Announcement(BaseModel):
    ALERT_LEVELS = [
        ("INFO", "Info"),
        ("WARNING", "Warning"),
        ("DANGER", "Danger"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    slug = models.SlugField(
        _("Slug"),
        max_length=64,
        blank=True,
        unique=True,
        db_index=True,
        help_text=_(
            "Announcement title as it will appear in the URL. "
            "Can only be alphanumeric with hyphens as word delimiter."
        ),
    )

    title = models.CharField(_("Title"), max_length=128)
    description = BleachRichTextField(_("Description"), allowed_tags=["a"])
    announcement_html = BleachRichTextField(_("Announcement"), blank=True)

    is_featured = models.BooleanField(_("Is Featured"), default=False)
    alert_level = models.CharField(
        _("Alert Level"), max_length=8, choices=ALERT_LEVELS, blank=True
    )
    start_date = models.DateField(_("Start Date"), null=True)
    end_date = models.DateField(_("End Date"), null=True)

    attachments = models.ManyToManyField(
        Attachment,
        related_name="announcements",
        verbose_name=Attachment._meta.verbose_name_plural,
        blank=True,
    )

    class Meta:
        verbose_name = _("Announcement")
        verbose_name_plural = _("Announcements")

    def clean(self) -> None:
        self.clean_slug()
        super().clean()

    def clean_slug(self) -> None:
        if not self.slug:
            if self.title_en:
                self.slug = slugify(self.title_en)
            else:
                raise ValidationError(
                    {"slug": self._meta.get_field("slug").error_messages["blank"]}
                )

    def __str__(self) -> str:
        return f"{self.start_date}-{self.end_date} - {self.title}"
