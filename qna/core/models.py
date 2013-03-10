from django.db import models

from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from django.db.models.signals import post_save
from datetime import date, datetime

class Education(models.Model):
	school_id = models.CharField(max_length=200, blank=True, null=True)
	school_name = models.CharField(max_length=200, blank=True, null=True)
	school_type = models.CharField(max_length=200, blank=True, null=True)
	year = models.CharField(max_length=200, blank=True, null=True)


class Concentration(models.Model):
	conc_id = models.CharField(max_length=200, blank=True, null=True)
	conc_name = models.CharField(max_length=200, blank=True, null=True)
	education = models.ForeignKey(Education)


class UserProfile(models.Model):
	user = models.OneToOneField(User, blank= True, null=True)
	username = models.CharField(max_length=128, unique=False, blank=True, null=True)
	anonymous = models.BooleanField()
	ip = models.IPAddressField(verbose_name=('user\'s IP'), null=True, blank=True)
	full_name = models.CharField(max_length=128, unique=True, blank=True, null=True)
	created_at = models.DateTimeField(auto_now_add = True)
	last_login = models.DateTimeField(blank=True, null=True)
	fb_id = models.CharField(max_length=200, null=True, blank = True)
	fb_access_token = models.CharField(max_length=200, null = True, blank = True)
	first_name = models.CharField(max_length=200, blank=True, null=True)
	last_name = models.CharField(max_length=200, blank=True, null=True)
	name = models.CharField(max_length=200, blank=True, null=True)
	locale = models.CharField(max_length=200, blank=True, null=True)
	gender = models.CharField(max_length=200, blank=True, null=True)
	hometown = models.CharField(max_length=200, blank=True, null=True)
	location = models.CharField(max_length=200, blank=True, null=True)
	work_position_id = models.CharField(max_length=200, blank=True, null=True)
	work_position_name = models.CharField(max_length=200, blank=True, null=True)
	work_start_date = models.CharField(max_length=200, blank=True, null=True)
	work_location_id = models.CharField(max_length=200, blank=True, null=True)
	work_location_name = models.CharField(max_length=200, blank=True, null=True)
	work_employer_id = models.CharField(max_length=200, blank=True, null=True)
	work_employer_name = models.CharField(max_length=200, blank=True, null=True)
	email = models.EmailField(blank=True, null=True)
	updated_time = models.DateTimeField(blank=True, null=True)
	birthday = models.DateTimeField(blank=True, null=True)
	timezone = models.CharField(max_length=200, blank=True, null=True)
	educations = models.ManyToManyField(Education)
	friends = models.ManyToManyField('self')
	age = models.IntegerField(blank=True, null=True)