from django.urls import path
from . import views

app_name = 'pizzeria'
urlpatterns = [
	path('', views.index, name='index'),
	path('ordenar/', views.place_order, name='place_order'),
]
