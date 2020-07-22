from django.shortcuts import render
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
		# collect order object