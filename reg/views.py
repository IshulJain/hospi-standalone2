from django.shortcuts import render, HttpResponse, redirect,HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
import requests
from django.views.decorators.csrf import csrf_exempt
import json
import os
import facebook
from reg.models import *
from payment.models import *
from django_mobile import get_flavour
from user_agents import parse
from django.db.models import Q
from django.contrib.auth.decorators import user_passes_test
from django.contrib.staticfiles.templatetags.staticfiles import static
import dropbox
from django.db.models import Sum,Max
import urllib2
import cookielib
from ast import literal_eval
from xlrd import open_workbook
from xlwt import Workbook
import random
from django.utils.crypto import get_random_string
import cStringIO
from PIL import Image
import urllib
import cloudinary
import cloudinary.uploader
import cloudinary.api
import base64
from io import BytesIO
from django.core import serializers

@csrf_exempt
def register(request):
    response = {}
    if 1:#try:
        data = request.POST
        #form = RegisterForm(data)
        email = data.get('email',None)
        try:
            techProfile = TechProfile.objects.get(email = email)
            #user = User.objects.get(email = email)
            #messages.warning(request,"Email Already Registered !")
            #return HttpResponse("Email Already Registered!") #redirect('/register')
            return False
        except:
            bugUsername = User.objects.latest('id').id
            user = User.objects.create_user(username=str(bugUsername+1))
            techprofile = TechProfile(user = user,email = email)
        user.first_name = data.get('name','')
        password = data.get('password',"techTeam")
        user.set_password(password)
        user.save()
        print 'code base 1'
        try:
            college = College.objects.get(collegeName = data.get('college').strip())
        except:
            college = College(collegeName = data.get('college').strip())
            college.save()
        try:
        	techprofile = TechProfile.objects.get(user = user)
        except:
			techprofile = TechProfile(user = user)
        techprofile.email = email
        techprofile.technexId = "TX"+str(10000+user.id)
        techprofile.college = college
        techprofile.mobileNumber = data.get('mobileNumber')
        techprofile.year = data.get('year')
        #techprofile.apploginStatus = True
		#print "codeBaes 2"
        pins = TechProfile.objects.all().values_list("pin")
        while True:
            stringR = get_random_string(3,allowed_chars='ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
            if stringR not in pins:
                techprofile.pin = stringR
                techprofile.save()
                break
        return techprofile
    else:#except:
        return False


def intro(request):
	emails = TechProfile.objects.all().values_list('email')
	totalHostels_ = Hostel.objects.all()
	facilities = Facility.objects.all()
	datas = json.loads(serializers.serialize('json',totalHostels_,fields = ('name','capacity','bufferSize')))
	totalHostels = []
	for data in datas:
		count = Hostel.objects.get(name = data['fields']['name']).offlineprofile_set.all().count()
		data['fields']['currentCapacity'] = data['fields']['capacity'] - count - data['fields']['bufferSize']
		totalHostels.append(data['fields'])
	return render(request,'mainPage.html',{'emails': emails,"hostels":totalHostels,'facilities':facilities})

@csrf_exempt
def offLineRegister(request):
	response = {}
	post = request.POST
	try:
		offLineProfile = OffLineProfile.objects.get(techProfile__email = post['email'])
		response['status'] = 2 # Already registered 
		return JsonResponse(response)
	except:
		try:
			techprofile = TechProfile.objects.get(email = post['email'])
		except:
			techprofile = register(request)
		offLineProfile = OffLineProfile(techProfile = techprofile,gender = int(post['gender']))
		
		if int(post['security']) == 1:
			response['security'] = 'Reached'
			security  = Facility.objects.get(name = 'Security')
			securityTransaction = Transaction(creditor = techprofile, amount = 200, facility  = security, reciever = request.user.deskteam)
			securityTransaction.save()
		if int(post['accom']) == 1:
			response['accom'] = "Reached"
			hostel = Hostel.objects.get(name = post['hostel'])
			count = hostel.offlineprofile_set.all().count()
			if hostel.capacity <= count:
				response['status'] = 0
				return JsonResponse(response)
			accomFacility = Facility.objects.get(name = 'Accommodation')
			accomtransaction = Transaction(creditor = techprofile, amount = 500, facility = accomFacility, reciever = request.user.deskteam)
			accomtransaction.save()
			offLineProfile.hostel = hostel
		transactions = Transaction.objects.filter(creditor = techprofile)
		transactionsData = json.loads(serializers.serialize('json',transactions, fields=('amount','timeStamp','facility')))
		for transactionData in transactionsData:
			transactionData['fields']['facility'] = Facility.objects.get(id=transactionData['fields']['facility']).name
		response['paymentData'] = transactionsData
		offLineProfile.save()
		response['status'] = 1
		return JsonResponse(response)

@csrf_exempt
def details(request):
	response = {}
	post = request.POST
	try:
		offLineProfile = OffLineProfile.objects.get(techProfile__email = post['email'])
		response['status'] = 2 # Already registered
		techprofile = offLineProfile.techProfile
		total = 0
		transactions = Transaction.objects.filter(creditor = techprofile)
		transactionsData = json.loads(serializers.serialize('json',transactions, fields=('amount','timeStamp','facility')))
		for transactionData in transactionsData:
			transactionData['fields']['facility'] = Facility.objects.get(id=transactionData['fields']['facility']).name
			total += transactionData['fields']['amount']
		techProfile = [techprofile]
		data = json.loads(serializers.serialize('json', techProfile, fields=('technexId','city','year','mobileNumber')))		
		data[0]['fields']['name'] = techProfile[0].user.first_name
		data[0]['fields']['college'] = techProfile[0].college.collegeName
		try:
			response['hostel'] = offLineProfile.hostel.name
		except:
			response['hostel'] = 'Not Alloted'
		response['data'] = data[0]['fields']
		response['paymentData'] = transactionsData
		response['total'] = total 
		return JsonResponse(response)
	except:
		try:
			techProfile = TechProfile.objects.filter(email = post['email'])
			data = json.loads(serializers.serialize('json', techProfile, fields=('technexId','city','year','mobileNumber')))		
			data[0]['fields']['name'] = techProfile[0].user.first_name
			data[0]['fields']['college'] = techProfile[0].college.collegeName
			response['status'] = 1 #For Registered techprofile but not registered offlineProfile
			response['data'] = data[0]['fields']
			return JsonResponse(response)
		except:
			response['status'] = 0 #Not registered TechProfile
			return JsonResponse(response)


def assignHostel(gender):
	hostels = Hostel.objects.filter(genderType=gender).order_by("order")
	print gender
	currentHostel = CurrentHostel.objects.get(hostel__genderType = int(gender))
	count = currentHostel.hostel.offlineprofile_set.all().count()
	if currentHostel.hostel.capacity - count > currentHostel.hostel.bufferSize:
		return currentHostel.hostel
	else:
		for hostel in hostels:
			count_ = hostel.offlineprofile_set.all().count()
			if hostel.capacity - count_ > hostel.bufferSize:
				currentHostel.hostel = hostel
				currentHostel.save()
				return hostel
	return False


@csrf_exempt
def hostelPortal(request):
	response = {}
	currentHostels = CurrentHostel.objects.all()
	totalHostels_ = Hostel.objects.all()
	datas = json.loads(serializers.serialize('json',totalHostels_,fields = ('name','capacity','bufferSize')))
	totalHostels = []
	for data in datas:
		count = Hostel.objects.get(name = data['fields']['name']).offlineprofile_set.all().count()
		data['fields']['currentCapacity'] = data['fields']['capacity'] - count - data['fields']['bufferSize']
		totalHostels.append(data['fields'])
	if request.method == 'POST':
		post = request.POST
		hostel = Hostel.objects.get(name = post['name'])
		count = hostel.offlineprofile_set.all().count()
		if hostel.capacity < count:
			return render(request,'hostel.html',{'error':"Hostel Already Filled","currentHostels":currentHostels,"hostels":totalHostels})
		currentHostel = CurrentHostel.objects.get(hostel__genderType = hostel.genderType)
		currentHostel.hostel = hostel
		currentHostel.save()

	return render(request,'hostel.html',{'error':"",'currentHostels':currentHostels,"hostels":totalHostels})

def generateCode(techprofile):
	position = random.randint(0,3)
	response = {}
	x = techprofile.pin
	y = ['X','X','X','X','X']
	y[4] = str(position)
	try:
		print position
		print techprofile
		offtech = OffLineProfile.objects.get(techProfile = techprofile)
		
		hostel = offtech.hostel.code
		y[position] = hostel
		l = 0	
		for ch in range(0,2):
			if l is position:
				l = l+1
			y[l] = x[ch]
		print y
		z = "".join(y)
		print z
		response['status'] = 1
		response['pin'] = z
		return response
	except:
		response['status'] = 0
		return response			





@csrf_exempt
def hostelAllot(request):
	response = {}
	post = request.POST
	hostel = Hostel.objects.get(name = post['hostelName'])
	profile = OffLineProfile.objects.get(techProfile__email = post['email'])
	facility = Facility.objects.get(name = 'Accommodation')
	
	count = hostel.offlineprofile_set.all().count()
	if hostel.capacity <= count:
		response['status'] = 0
		return JsonResponse(response)
	else:
		transactions = Transaction.objects.filter(creditor = profile.techProfile)
		if transactions.count() == 0:
			response['status'] = 2
			return JsonResponse(response)	
		profile.hostel = hostel
		response['hostelName'] = hostel.name
		response['status'] = 1
	profile.save()
	return JsonResponse(response)