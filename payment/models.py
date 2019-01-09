from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import URLValidator
from django.template.defaultfilters import slugify
from django.core.validators import URLValidator
import datetime
from django.utils import timezone
from reg.models import *

class Facility(models.Model):
	name = models.CharField(max_length = 40)
	maxPrice = models.IntegerField()
	offeredPrice = models.IntegerField()
	facilityType = models.CharField(max_length = 65) 	
	def __unicode__(self):
		return '%s %s'%(self.name,self.maxPrice)

class DeskTeam(models.Model):
	user = models.OneToOneField(User)
	authorityLevel = models.SmallIntegerField(default = 0)
	def __unicode__(self):
		return '%s %s'%(self.user.first_name,self.authorityLevel)

class Transaction(models.Model):
	creditor = models.ForeignKey(TechProfile)
	amount = models.IntegerField(default = 0)
	timeStamp = models.DateTimeField(auto_now = True)
	facility = models.ForeignKey(Facility)
	reciever = models.ForeignKey(DeskTeam)
	def __unicode__(self):
		return '%s %s %s'%(self.facility.name,self.amount,self.facility.maxPrice)

class Hostel(models.Model):
	name = models.CharField(max_length = 40)
	capacity = models.IntegerField(default=0)
	genderType = models.SmallIntegerField(default = 1) #1 means Male,0 Means Female
	bufferSize = models.IntegerField(default = 0)
	order = models.IntegerField(default = 0)
	code = models.CharField(max_length = 1,null = True, blank = True)
	def __unicode__(self):
		return '%s %s'%(self.name,self.capacity)

class OffLineProfile(models.Model):
	techProfile = models.OneToOneField(TechProfile)
	hostel = models.ForeignKey(Hostel,null = True,blank = True)
	gender = models.SmallIntegerField(default = 1) #1 means Male,0 means Female
	def __unicode__(self):
		try:
			hostelName = self.hostel.name
		except:
			hostelName = ""
		return '%s %s'%(self.techProfile.user.first_name,hostelName)

class IdCard(models.Model):
	techProfile = models.ForeignKey(TechProfile)
	attemptNumber = models.SmallIntegerField(default = 1)
	idCardNumber = models.IntegerField(default = 0) #Lateset Idcard Number
	facility = models.ForeignKey(Facility) #The IdCard Facility

class CurrentHostel(models.Model):
	hostel = models.OneToOneField(Hostel)
	bufferSize = models.IntegerField(default = 0)

