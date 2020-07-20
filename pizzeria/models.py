from django.db import models

class Size(models.Model):
	name = models.CharField(max_length=20, unique=True)
	price = models.PositiveIntegerField()
	
	def __str__(self):
		return self.name
	
class Topping(models.Model):
	name = models.CharField(max_length=20, unique=True)
	price = models.FloatField()
	
	def __str__(self):
		return self.name
	
class Order(models.Model):
	first_name = models.CharField(max_length=60)
	last_name = models.CharField(max_length=60)
	order_date = models.DateTimeField()
	
	class Meta:
		ordering = ['-order_date']
	
	def __str__(self):
		return self.full_name
	
	@property
	def full_name(self):
		return "{} {}".format(self.first_name, self.last_name)
	
	@property
	def total(self):
		total = 0.00
		for pizza in self.pizzas.all():
			total += pizza.total
		return round(total, 2)
	
class Pizza(models.Model):
	size = models.ForeignKey(Size, on_delete=models.CASCADE)
	order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='pizzas') # related_name lets me do this: order = Order.objects.get(id=1) -> order.pizzas.all() instead of order.pizza_set.all()
	toppings = models.ManyToManyField(Topping, through='ToppingAmount')
	
	class Meta:
		order_with_respect_to = 'order' # it's something like this: order1->pizza1,pizza2. order2->pizza1. order3->pizza1 ; instead of order1->pizza1. order2->pizza1. order1->pizza2...
		
	def __str__(self):
		return "Pizza ({}), {}".format(self.id, self.order.full_name)
	
	@property
	def total(self):
		total = 0.00
		total += self.size.price
		for topping in self.toppings.all():			
			t_amount = self.getToppingAmount(topping)
			for i in range(t_amount):
				total += topping.price
		return round(total, 2)
	
	def getToppingAmount(self, topping): # is there a way to check the ammount via the pizza object?
		t_a = ToppingAmount.objects.get(pizza=self, topping=topping)
		if not t_a: return 0 # if topping was not found 
		return t_a.amount
	
class ToppingAmount(models.Model):
	"""Through model needed to store the ammount of toppings in a pizza (see Pizza.toppings)"""
	topping = models.ForeignKey(Topping, on_delete=models.CASCADE)
	pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE)
	amount = models.PositiveIntegerField()
