from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseBadRequest, HttpResponse
import json

from .models import Size, Topping, Order, Pizza

# Create your views here.
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
		request.session['_order'] = order_info # Session var so it can be use in another function.
		error = 0
		key = ''
		for k, v in order_info.items(): # Checks each value of the dictionary if the value is empty returns a erorr 400
			if v == '':
				error = 1
				key = k
		if error == 1:
			return HttpResponseBadRequest(f'ERROR: el parametro {key} no puede estar vacio.')
		else:
			return HttpResponse('No hay campos vacios.')

def order_summary(request):
	"""generates de necessaire data for the summary"""
	order_info = request.session['_order'] # Get te data from the session var
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
