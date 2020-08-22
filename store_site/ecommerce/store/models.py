from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
	name = models.CharField(max_length=64, null=True)
	email = models.EmailField(max_length=64, null=True)

	def __str__(self):
		return self.name

class Product(models.Model):
	name = models.CharField(max_length=64, null=True)
	price = models.DecimalField(max_digits=7, decimal_places=2)
	digital = models.BooleanField(default=False, null=True, blank=False)
	image = models.ImageField(null=True, blank=True)

	def __str__(self):
		return self.name

	@property	
	def imageURL(self): #checks if an image is available for the product
		try:
			url = self.image.url
		except:
			url = ''
		return url
class Order(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
	date_ordered = models.DateTimeField(auto_now_add=True)
	complete = models.BooleanField(default=False, null=True, blank=False)
	transaction_id = models.CharField(max_length=200, null=True)

	def __str__(self):
		return str(self.id)
	@property
	def getCartTotal(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.getTotal for item in orderitems])
		return total
	@property
	def getCartItems(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.quantity for item in orderitems])
		return total
	@property
	def shipping(self):
		shipping = False
		orderitems = self.orderitem_set.all()
		for i in orderitems:
			if i.product.digital == False:
				shipping = True
		return shipping
	
	

class OrderItem(models.Model):
	product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
	quantity = models.IntegerField(default=0, null=True, blank=True)
	date_added = models.DateTimeField(auto_now_add=True)

	@property
	def getTotal(self):
		total = self.product.price * self.quantity
		return total
	

class ShippingAddress(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
	address = models.CharField(max_length=64, null=True)
	city = models.CharField(max_length=64, null=True)
	state = models.CharField(max_length=64, null=True)
	country = models.CharField(max_length=64, null=True)
	zipcode = models.CharField(max_length=64, null=True)
	date_added = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.address


# Create your models here.
