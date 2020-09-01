# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . models import ClearedLogs, UnClearedLogs

from django.contrib import admin

admin.site.register(ClearedLogs)
admin.site.register(UnClearedLogs)
# Register your models here.
