import os
from pizzeria.models import Size, Topping, Order, Pizza, Sale
from django.db import migrations

def dummyOrders(apps, schema_editor):
	dev_mode = os.getenv('MODE')
	if dev_mode != 'DEV': return # don't add dummy data on production

	from faker import Faker
	from collections import Counter
	import random
	
	fake = Faker()
	
	sizes_set = Size.objects.all()
	toppings_set = Topping.objects.all()
	
	# logic: create order -> create pizza (related to order) -> generate toppings -> insert toppings through ToppingAmount model -> create sale with total calculated by order 
	for i in range(10):
		order = Order.objects.create(first_name=fake.first_name(), last_name=fake.last_name(), order_date=fake.date_time_this_year())
		for j in range(random.randint(1, 3)): # generate up to 3 pizzas
			pizza = Pizza.objects.create(size=random.choice(sizes_set), order=order)
			
			# generate up to 4 toppings (this code looks ugly and is probably inefficient, I want to improve it)
			topping_ids = [random.choice(toppings_set).id for i in range(random.randint(1, 4))] # generate list filled with Topping.id's
			c = Counter(topping_ids) # get a dict like this: {id_1: amount_1, id_2: amount_2}
			toppings = [{'topping': Topping.objects.get(id=id), 'amount': amount} for id, amount in c.items()] # generate list filled with {'topping': Topping, 'amount': amount}
			for item in toppings:
				pizza.toppings.add(item['topping'], through_defaults={'amount': item['amount']}) # ToppingAmount is the through model for Pizza.toppings ManyToMany, extra data goes in through_defaults
				pizza.save() # save the last topping added
		Sale.objects.create(order=order, total=order.total)

class Migration(migrations.Migration):

    dependencies = [
        ('pizzeria', '0002_populate'),
    ]

    operations = [
		migrations.RunPython(dummyOrders)
    ]
