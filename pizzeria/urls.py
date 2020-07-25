from django.urls import path
from .views import index, PlaceOrder, ConfirmOrder

app_name = 'pizzeria'
urlpatterns = [
	path('', index, name='index'),
	path('ordenar/', PlaceOrder.as_view(), name='place_order'),
	path('ordenar/confirmar/', ConfirmOrder.as_view(), name='confirm_order')
]
