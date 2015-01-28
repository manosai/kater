import requests
import json 
import os
import urllib
import yelp 

from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect, StreamingHttpResponse
from django.template import RequestContext
from mysite.models import User, Preferences
from random import randint
from bs4 import BeautifulSoup

#User
postmates_user = 'cus_Jy38b8wN9VhNjF'

#API
api = '658d38f2-8a09-4b71-9c60-c6b286fbd4bb'

def home(request):
	return render_to_response('home.html', {}, RequestContext(request))

def signup(request):
	return render_to_response('signup.html', {}, RequestContext(request))

def login(request):
	return render_to_response('login.html', {}, RequestContext(request))

def create_user(request):
	email = request.GET.get('email', '')
	password = request.GET.get('pass', '')
	first_name = request.GET.get('fname', '')
	last_name = request.GET.get('lname', '')
	address = request.GET.get('address', '')
	city = request.GET.get('city', '')
	state = request.GET.get('state', '')
	phone = request.GET.get('phone', '')
	budget = float(request.GET.get('budget', ''))
	allergies = request.GET.get('allergies', '')
	meats = request.GET.get('meats', '') 
	cuisines = request.GET.get('cuisines', '')
	is_Healthy = request.GET.get('healthy', '')
	schedule = request.GET.get('meals', '')

	user = User(email = email, password = password, first_name = first_name, last_name = last_name, address = address, \
			city = city, state = state, phone = phone, budget = budget, allergies = allergies, meats = meats, \
			cuisines = cuisines, is_Healthy = is_Healthy, schedule = schedule)
	
	user.save()

	user_id = user.id

	day = 1
	meal = 1

	for s in schedule: 
		if (day > 7):
			day = 1
		if (meal <= 7):
			meal = 1
		elif (meal <= 14):
			meal = 2
		else:
			meal = 3
		if (s == '1'):
			meal_slot = str(day) + '_' + str(meal)
			print meal_slot
			get_restaurant(user_id, cuisines, meal_slot, budget, allergies, meats, city)
		meal += 1
		day += 1


	#get_restaurant(cuisines, meal_slot, city)
	return HttpResponse(user.id)

def get_restaurant(user_id, cuisines, meal_slot, meal_budget, allergies, meats, city):
	"""get a cuisine """
	all_cuisines = cuisines.split(",")
	length = len(all_cuisines)
	ind = randint(0, length-1)
	curr_cuisine = all_cuisines[ind]

	response = yelp.query_api(curr_cuisine, meal_slot, city)
	restaurant_search(user_id, cuisines, response[0], response[1], response[2], response[3], meal_budget, allergies, meats, city)
	return None 

def isfloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False

def restaurant_search(user_id, cuisines, restaurant, restaurant_address, restaurant_phone, meal_slot, meal_budget, allergies, meats, city):
	menupages_url = "http://philadelphia.menupages.com/restaurants/"
	restaurant_dash = restaurant.replace(" ", "-")
	r = requests.get(menupages_url + restaurant_dash + "/menu")
	soup = BeautifulSoup(r.text)
	raw_menu = str(soup.find(id="restaurant-menu"))
	menu_list = [x for x in raw_menu.split("</td></tr><tr><th><cite>")]
	menu_list2 = [x.split("</th><td>\xc2\xa0</td><td>\xc2\xa0</td><td>\xc2\xa0") for x in menu_list]
	menu_list3 = [x for x in menu_list2 if len(x) > 1 and len(x[1]) > 1]
	menu_list4 = [[x[0].replace("</cite>\xc2\xa0", "*"), x[1]] for x in menu_list3]
	menu_list5 = [[BeautifulSoup(x[0]).getText().encode('utf-8'), BeautifulSoup(x[1]).getText().encode('utf-8')] for x in menu_list4 if isfloat(x[1]) or x[1].isdigit()]
	menu_list6 = [[x[0].replace('\xc2\xa0', " "), x[1].replace('\xc2\xa0', " ")] for x in menu_list5]
	if (len(menu_list6) == 0):  
		get_restaurant(user_id, cuisines, meal_slot, meal_budget, allergies, meats, city)
	else:
		response = find_item(user_id, restaurant, restaurant_address, restaurant_phone, meal_slot, menu_list6, meal_budget, allergies, meats)
	return None

def find_item(user_id, restaurant, restaurant_address, restaurant_phone, meal_slot, menu, meal_budget, allergies, meats):
	"""filter for one specific item"""
	meat_options = set([])
	meat_options.add("Chicken")
	meat_options.add("Pork")
	meat_options.add("Beef")
	meat_options.add("Seafood")
	
	# first, filter out all items greater than meal budget
	allergies = set([x.replace(" ", "") for x in str(allergies).split(",")])
	
	meats = set([x.replace(" ", "") for x in str(meats).split(",")])
	meat_options = meat_options.difference(meats)
	meat_options2 = set([x.lower() for x in meat_options])

	
	new_menu = [x for x in menu if not float(x[1]) > meal_budget]
	new_menu2 = [x for x in new_menu if not float(x[1]) < 8.00]
	new_menu_inter = [[x[0].lower(), x[1]] for x in new_menu2]
	new_menu3 = [x for x in new_menu_inter if not len(allergies.intersection(set(x[0].split(" ")))) > 0]
	new_menu4 = [x for x in new_menu3 if not len(meat_options2.intersection(set(x[0].split(" ")))) > 0]

	length = len(new_menu4)
	if (length != 0):
		ind = randint(0, length-1)
		item = new_menu4[ind][0]
		price = new_menu4[ind][1]
	else:
		return None

	add_item(user_id, restaurant, restaurant_address, restaurant_phone, item, price, meal_slot)
	return None

def add_item(user_id, restaurant_name, restaurant_address, restaurant_number, item, item_price, timeslot):
	pref = Preferences(user_id =user_id, restaurant_name = restaurant_name, restaurant_address=restaurant_number, restaurant_number=restaurant_address, item= item, item_price = item_price, timeslot=timeslot)
	pref.save()
	return None	

def get_items(request):
	user_id = request.GET['user_id']

	# get items
	items = Preferences.objects.raw('SELECT * FROM mysite_preferences WHERE user_id = %s', [user_id])
	output = []
	for item in items:
		data = {}
		data['restaurant_name'] = item.restaurant_name
		data['restaurant_number'] = item.restaurant_number
		data['restaurant_address'] = item.restaurant_address
		data['item'] = item.item
		data['item_price'] = item.item_price
		data['timeslot'] = item.timeslot
		output.append(data)
	return HttpResponse(json.dumps(output))

def get_delivery_quote (dropoff_address, pickup_address):
	payload = {'dropoff_address': dropoff_address, 'pickup_address': pickup_address}
	print payload
	r = requests.post('https://api.postmates.com/v1/customers/'+postmates_user+'/delivery_quotes', auth = (api, ""), data = payload)
	return r

def make_delivery (manifest, pickup_name, pickup_address, pickup_phone_number, pickup_notes, dropoff_name, dropoff_address, dropoff_phone_number, quote_id):
	payload = {'manifest': manifest,'pickup_name': pickup_name, 'pickup_address': pickup_address, 'pickup_phone_number': pickup_phone_number, 'pickup_notes': pickup_notes, 'dropoff_name': dropoff_name, 'dropoff_address': dropoff_address, 'dropoff_phone_number': dropoff_phone_number, 'quote_id': quote_id}
	r = requests.post('https://api.postmates.com/v1/customers/'+postmates_user+'/deliveries', auth = (api, ""), data = payload)
	return r

def check_updates (delivery_id):
	r = requests.get('https://api.postmates.com/v1/customers/'+postmates_user+'/deliveries/'+delivery_id, auth = (api, ""))
	return r

# when defu clicks order now
def order_now(request):
	user_id = request.GET['user_id']
	timeslot = request.GET.get('timeslot', '')

	
	manifest = 'some order'
	pickup_name = str(request.GET['restaurant_name'])
	pickup_address = str(request.GET.get('restaurant_address', ''))
	pickup_phone_number = request.GET['restaurant_number']
	pickup_phone_number = pickup_phone_number[1:]
	pickup_notes = 'food'


	# get user data
	user = User.objects.raw('SELECT * FROM mysite_user WHERE id = %s', [user_id])
	dropoff_name = ''
	dropoff_address = ''
	dropoff_phone_number = ''

	for u in user:
		dropoff_name = str(u.first_name+' '+u.last_name)
		dropoff_address = str(u.address) + ' Philadephia, PA'
		dropoff_phone_number = u.phone

	response = get_delivery_quote(dropoff_address, pickup_address)
	data = response.json()
	quote_id = data['id']
	fee = str(data['fee'])
	if (len(fee) == 4):
		fee = '$'+ fee[:2] + '.' + fee[2:]
	else:
		fee = '$'+ fee[:1] + '.' + fee[1:]
	

	r = make_delivery(manifest, pickup_name, pickup_address, pickup_phone_number, pickup_notes, dropoff_name, dropoff_address, dropoff_phone_number, quote_id)
	resp = r.json()
	##delivery_id = r
	##r = check_updates(delivery_id)

	output = []
	data2 = {}
	data2['quote_id'] = quote_id
	data2['fee'] = fee
	data2['status'] = resp['status']
	output.append(data2)

	return HttpResponse(json.dumps(output))


