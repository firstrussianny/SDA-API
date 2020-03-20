# -*- coding: utf-8 -*-
from rest_framework import routers

from .viewsets import AnnouncementViewSet


router = type("Router", (routers.DefaultRouter,), {"include_root_view": False})()

router.register(r"announcements", AnnouncementViewSet)
