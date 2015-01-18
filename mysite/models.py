from django.db import models

class User(models.Model):
	email = models.CharField(max_length = 50)
	password = models.CharField(max_length = 50)
	first_name = models.CharField(max_length = 50)
	last_name = models.CharField(max_length = 50)
	address = models.CharField(max_length = 50)
	city = models.CharField(max_length = 50)
	state = models.CharField(max_length = 50)
	phone = models.CharField(max_length = 15)
	budget = models.IntegerField()
	allergies = models.CharField(max_length = 500)
	meats = models.CharField(max_length = 500)
	cuisines = models.CharField(max_length = 500)
	is_Healthy = models.BooleanField(default = False)
	schedule = models.CharField(max_length = 500)

