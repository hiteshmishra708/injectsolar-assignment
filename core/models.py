# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class ClearedLogs(models.Model):
    device = models.CharField(max_length=120)
    inverter_name = models.CharField(max_length=120)
    alarm = models.CharField(max_length=120)
    occurance_time = models.CharField(max_length=120)
    message = models.CharField(max_length=500)

class UnClearedLogs(models.Model):
    device = models.CharField(max_length=120)
    inverter_name = models.CharField(max_length=120)
    alarm = models.CharField(max_length=120)
    occurance_time = models.CharField(max_length=120)
    clearance_time = models.CharField(max_length=120)
    message = models.CharField(max_length=500)