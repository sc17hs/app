# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Module)
admin.site.register(Professor)
admin.site.register(Rating)
admin.site.register(User)