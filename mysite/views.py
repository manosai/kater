import requests
import json 
import os
import urllib

from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from mysite.models import User

def home(request):
	return render_to_response('home.html', {}, RequestContext(request))

def signup(request):
	return render_to_response('signup.html', {}, RequestContext(request))

def create_user(request):
	first = request.GET['first_name']
	last = request.GET['last_name']

	user = User(first_name = first, last_name = last)
	user.save()
	return HttpResponse('success')

def scrape_restaurants(restaurant):
	restuarant_items = []
	menupages_url = "philadelphia.menupages.com"
	
