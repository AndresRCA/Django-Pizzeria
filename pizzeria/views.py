from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseBadRequest, HttpResponse
import json

from .models import Size, Topping, Order, Pizza

def index(request):
	return render(request, 'pizzeria/index.html')

def place_order(request):
	if request.method == 'GET':
		context = {}
		context['sizes'] = json.dumps(list(Size.objects.all().values()))
		context['toppings'] = json.dumps(list(Topping.objects.all().values()))		
		return render(request, 'pizzeria/place_order.html', context)
	elif request.method == 'POST':
		order_info = json.loads(request.body) # Obtains de info from the poll.
		error = False
		key = ''
		for k, v in order_info.items(): # Checks each value of the dictionary if the value is empty returns a erorr 400
			if v == '':
				error = True
				key = k
		if error:
			return HttpResponseBadRequest(f'ERROR: el parametro {key} no puede estar vacio.')
		else:
			request.session['_order'] = order_info # session var used in pizzeria:confirm_order url.
			return HttpResponse('No hay campos vacios.')

def confirm_order(request):
	"""generates the necessary data for the summary"""
	order_info = request.session['_order'] # Get te data from the session var

	# context object blueprint
	summary = {
		'first_name': '',
		'last_name': '',
		'pizzas': [], # [{size: {size.name, size.price}, toppings: [{topping.name, topping.amount, topping.total}], total: 0.00}]
		'total': 0.00
	}

	summary['first_name'] = order_info['first_name']
	summary['last_name'] = order_info['last_name']

	from collections import Counter
	order_total = 0.00
	for pizza in order_info['pizzas']:
		pizza_total = 0.00

		# add size price to pizza total
		pizza_total += pizza['size']['price']

		# create size dic for summary['pizzas'][i]['size']
		size = {'name': pizza['size']['name'], 'price': pizza['size']['price']}

		# generate neccesary data for summary['toppings']
		topping_ids = [topping['id'] for topping in pizza['toppings']] # get [topping.id, ...]
		t_counter = Counter(topping_ids) # get [{'topping.id': amount}, ...]
		topping_list = [] # [{topping.name, topping.amount, topping.total}, ...], this is appended to summary['pizzas'][i]['toppings']
		
		for topping_id, topping_amount in t_counter.items():
			topping = Topping.objects.get(pk=topping_id)
			topping_total = topping.price * topping_amount
			topping_list.append({'name': topping.name, 'amount': topping_amount, 'total': topping_total})
			
			pizza_total += topping_total # update pizza total

		# insert pizza summary
		summary['pizzas'].append({'size': size, 'toppings': topping_list, 'total': pizza_total})
		order_total += pizza_total

	summary['total'] = order_total

	request.session['_summary'] = summary # useful variable in case the user prints a summary of the order

	return render(request, 'pizzeria/confirm_order.html', summary)
	
	# Separate each data from de object
	print('-'*50)
	#print(order_info)
	total = 0
	number_of_pizzas = 0
	value_per_pizza = {}
	topping_list= {}
	pizzas = order_info.get('pizzas')
	for each_pizza in pizzas: # pizzas is a list populated with dictionaries, each dictionary have the info from the pizza
		pizza_total = 0
		number_of_pizzas += 1
		items_found = []
		new_datalist= []
		pizza_size_info = each_pizza.get('size')
		size_price = pizza_size_info.get('price')
		pizza_total += size_price
		pizza_toppings_info = each_pizza.get('toppings')
		for each_topping in pizza_toppings_info:
			if (not each_topping in items_found):
				items_found.append(each_topping)
				topping_count = pizza_toppings_info.count(each_topping) # Se cuentan los elementos
				new_elem = {}
				new_elem['id'] = each_topping['id']
				new_elem['name'] = each_topping['name']
				new_elem['price'] = each_topping['price']
				new_elem['cantidad'] = topping_count 
				new_datalist.append(new_elem)
			topping_price = each_topping.get('price')
			pizza_total += topping_price
		topping_list[number_of_pizzas] = new_datalist
		value_per_pizza[number_of_pizzas] = pizza_total
		total += pizza_total
	order_info['Total_Toppings'] = topping_list
	order_info['each_pizza'] = value_per_pizza
	order_info['total_price'] = total
	print(order_info)
	request.session['_summary'] = order_info
	return render(request, 'pizzeria/index.html')
