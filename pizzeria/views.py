from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, Http404

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
		for value in order_info.values():
			if value == '' or value == ' ':
				print('mal')
				raise Http404()
			else:
				print('bien')
				return HttpResponse('Vamos bien.')

def order_summary(request):
	return render(request, 'pizzeria/index.html')