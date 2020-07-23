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
		order_info = json.loads(request.body)
		request.session['_order'] = order_info
		error = 0
		key = ''
		for k, v in order_info.items():
			if v == '':
				error = 1
				key = k
		if error == 1:
			return HttpResponseBadRequest(f'ERROR: el parametro {key} no puede estar vacio.')
		else:
			return HttpResponse('No hay campos vacios.')

def order_summary(request):
	order_info = request.session['_order']
	print(order_info)
	return render(request, 'pizzeria/index.html')
