from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import URLValidator

from django.template.defaultfilters import slugify
from django.core.validators import URLValidator
import datetime
from django.utils import timezone
year_choices = [
        (1, 'First'),
        (2, 'Second'),
        (3, 'Third'),
        (4, 'Fourth'),
        (5,'Fifth'),
        (6, 'Passout(Only for Startup Fair)'),
    ]

def get_user_image_folder(instance, filename):
    return "technexusers/%s-%s/%s" %(instance.user.first_name,instance.user.last_name, filename)


class College(models.Model):
    collegeId = models.AutoField(primary_key = True)
    collegeName = models.CharField(max_length=250)
    status = models.BooleanField(default = False)
    city = models.CharField(max_length=250,null = True, blank = True)
    state = models.CharField(max_length=250,null = True, blank = True)
    collegeWebsite = models.CharField(max_length = 250, default = '0')
    def __unicode__(self):
        return "%s - %s - %s - %s" %(self.collegeWebsite, self.collegeName, self.city, self.state)
class FbConnect(models.Model):
    uid = models.CharField(max_length = 200, null = True)
    accessToken = models.CharField(max_length = 250, null = True)
    profileImage = models.TextField(validators=[URLValidator()],blank=True,null = True)
    def __unicode__(self):
        return self.uid
class TechProfile(models.Model):
    class Meta:
        permissions = (
            ('permission_code', 'Publicity portal'),
        )
    user = models.OneToOneField(User)
    email = models.EmailField(max_length = 60,null = True, blank = True)
    technexId = models.CharField(max_length = 30,null = True,blank = True)
    year = models.IntegerField(choices=year_choices)
    mobileNumber = models.BigIntegerField()
    college = models.ForeignKey(College,null = True)
    fb = models.OneToOneField(FbConnect,null = True, blank = True)
    botInfo = models.CharField(max_length = 65,null = True, blank = True)
    city = models.CharField(max_length = 65,default = 'varanasi')
    referral = models.EmailField(max_length = 60, null = True, blank = True)
    pin = models.CharField(max_length= 20,null = True,blank = True)
    apploginStatus = models.BooleanField(default = False)
    #profile_photo = models.TextField(validators=[URLValidator()],blank=True)
    notificationToken = models.TextField(null = True,blank = True)
    def __unicode__(self):
        return "%s -%s" %(self.user.first_name, self.college)
class ForgotPass(models.Model):
    user = models.OneToOneField(User)
    key = models.CharField(max_length = 250)
    def __unicode__(self):
        return self.key
        return '%s %s'%(self.title,self.lecturerName)


class PrimaryIndustry(models.Model):
    name = models.CharField(max_length = 100)
    def __unicode__(self):
        return '%s'%(self.name)

class BusinessType(models.Model):
    name = models.CharField(max_length = 3)
    def __unicode__(self):
        return '%s'%(self.name)
 
class PaymentStatusa(models.Model):
    tech = models.ForeignKey(TechProfile, null = True, blank = True)
    email = models.EmailField(max_length = 50, null = True, blank = True)
    status = models.CharField(max_length = 15)
    ticketId = models.CharField(max_length = 100)
    contact = models.CharField(max_length = 20,null = True,blank = True)
    ticketPrice = models.IntegerField(null = True,blank = True)
    timeStamp = models.CharField(max_length = 50,null = True,blank = True)
    ticketName = models.CharField(max_length = 65,null = True,blank = True)
    def __unicode__(self):
        return self.email

class SponsorshipType(models.Model):
    title = models.CharField(max_length  = 100)
    order = models.SmallIntegerField(default = 99)
    def __unicode__(self):
        return '%s %s'%(self.title,self.order)

class Sponsors(models.Model):
    sponsorType  = models.ForeignKey(SponsorshipType)
    order = models.SmallIntegerField(default = 999)
    name = models.CharField(max_length = 100)
    imageLink = models.TextField(validators=[URLValidator()],blank=True,null = True)
    websiteLink = models.TextField(validators=[URLValidator()],blank=True,null = True)
    def __unicode__(self):
        return '%s %s'%(self.name,self.order) 

class Way2smsAccount(models.Model):
    username=models.CharField(max_length=50)
    password=models.CharField(max_length=20)
    messages_left=models.IntegerField(default=100)
    def __unicode__(self):
        return self.username

class Way2smsAccount_Premium(models.Model):
    username=models.CharField(max_length=50)
    password=models.CharField(max_length=20)
    messages_left=models.IntegerField(default=100)
    def __unicode__(self):
        return self.username

class quiz(models.Model):
    quizId = models.AutoField(primary_key = True)
    name = models.CharField(max_length = 50)
    activeStatus = models.SmallIntegerField(default = 0)
    def __unicode__(self):
        return self.name

class quizTeam(models.Model):
    teamId = models.AutoField(primary_key= True)
    quizTeamId = models.CharField(max_length = 10, null = True, blank = True)
    members = models.ManyToManyField(TechProfile , related_name = "quizMembers" , null = True)
    quizAttemptStatus = models.SmallIntegerField(default = 0)
    quiz = models.ForeignKey(quiz , null = True , blank = True)
    slot = models.SmallIntegerField(default = 0)
    def __unicode__(self):
        return self.quizTeamId


class sheetpayment(models.Model):    
    tech = models.ForeignKey(TechProfile, null = True, blank = True)
    email = models.EmailField(max_length = 50, null = True, blank = True)
    status = models.CharField(max_length = 15,null= True,blank = True)
    ticketId = models.CharField(max_length = 100)
    contact = models.CharField(max_length = 20,null = True,blank = True)
    ticketPrice = models.IntegerField(null = True,blank = True)
    timeStamp = models.CharField(max_length = 50,null = True,blank = True)
    ticketName = models.CharField(max_length = 200,null = True,blank = True)
    def __unicode__(self):
        return self.email
        
	