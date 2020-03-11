# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
# Create your models here.


RATING_CHOICES = (
    (1,1),
    (2,2),
    (3,3),
    (4,4),
    (5,5)
)


class Professor(models.Model):
    name = models.CharField(max_length=250)
    code = models.CharField(max_length=250, primary_key= True)

    def __str__(self):
        return u'%s , %s' % (self.name, self.code)


class Module(models.Model):
    name = models.CharField(max_length=250)
    code = models.CharField(max_length=250)
    year = models.IntegerField()
    semester = models.IntegerField()
    teachers = models.ManyToManyField(Professor)

    def __str__(self):
        return u'%s - %s'%(self.name, self.year)


class Rating(models.Model):
    professorid = models.ForeignKey(Professor, on_delete=models.CASCADE)
    module_code = models.ForeignKey(Module, on_delete=models.CASCADE)
    year = models.IntegerField()
    rating = models.IntegerField(choices = RATING_CHOICES)

    def __str__(self):
        return u'%s - %s , %s' % (self.professorid,self.module_code,self.rating)


class User(AbstractUser):
    username = models.CharField(blank=True,max_length= 40, null=True)
    email = models.CharField(max_length=250, unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return "{}".format(self.email)


