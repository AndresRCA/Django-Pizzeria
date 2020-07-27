from datetime import datetime
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseBadRequest, HttpResponse
from django.views.generic import View
import json

from .models import Size, Topping, Order, Pizza, ToppingAmount

def index(request):
	return render(request, 'pizzeria/index.html')

class PlaceOrder(View):
	def get(self, request, *args, **kwargs):
		context = {}
		context['sizes'] = json.dumps(list(Size.objects.all().values()))
		context['toppings'] = json.dumps(list(Topping.objects.all().values()))		
		return render(request, 'pizzeria/place_order.html', context)
	
	def post(self, request, *args, **kwargs):
		order_info = json.loads(request.body) # Obtains de info from the poll.
		error, key = self.validateOrder(order_info)
		if error:
			return HttpResponseBadRequest(f'ERROR: el parametro {key} no puede estar vacio.')
		else:
			request.session['_order'] = order_info # session var used in pizzeria:confirm_order url.
			return HttpResponse('No hay campos vacios.')
	
	def validateOrder(self, order):
		"""Returns boolean that determines if an error ocurred and the key where the error ocurred"""
		error = False
		key = ''
		for k, v in order.items(): # Checks each value of the dictionary if the value is empty returns a erorr 400
			if v == '':
				error = True
				key = k
		return error, key

class ConfirmOrder(View):
	def get(self, request, *args, **kwargs):
		"""generates the necessary data for the summary"""
		if request.session.get('_summary'):
			del request.session['_summary'] # delete previous summary if it exists
		
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

class FinalizeOrder(View):
	def get(self, request, *args, **kwargs):
		if request.session.get('_order'):
			order_info = request.session['_summary']
			order = Order.objects.create(first_name=order_info.get('first_name'), 
										last_name=order_info.get('last_name'),
										order_date=datetime.now()) # If i dont do this seconds will show a lot of decimal points.
			order.save()

			for pizza in order_info.get('pizzas'):
				size = pizza.get('size')
				pizza_object = Pizza.objects.create(size=Size.objects.get(name=size.get('name')), order=order)
				pizza_object.save()

				for topping in pizza.get('toppings'):
					toppings_object = ToppingAmount.objects.create(
						amount=topping.get('amount'),
						pizza_id=pizza_object.id,
						topping_id=Topping.objects.get(name=topping.get('name')).id
						)
					toppings_object.save()
			#del request.session['_order'] # delete variable from session
			return render(request, 'pizzeria/finalize_order.html', {'status': 'SUCCESS'}) # if a database error occurred send {'status': 'ERROR'}
		else:
			return HttpResponseBadRequest() # will show error for someone that didn't make an order and is trying to access the url
		
def generateSummary(request):
	if request.session.get('_summary'):
		# generate summary to send
		return HttpResponse('here goes the summary')
	else:
		return HttpResponseBadRequest()