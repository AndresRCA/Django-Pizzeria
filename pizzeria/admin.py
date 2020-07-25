from django.contrib import admin
from django.db.models import F, ExpressionWrapper, DecimalField

# Register your models here.
from .models import Sale, Order, Pizza, Topping, Size

#============= Order ==============#

class PizzaInline(admin.StackedInline):
	model = Pizza
	extra = 1

class OrderAdmin(admin.ModelAdmin):
	inlines = [PizzaInline]
	list_filter = ['order_date', 'pizzas__size', 'pizzas__toppings']
	search_fields = ['first_name', 'last_name', 'order_date__day']
	list_display = ('fullName', 'order_date', 'countPizzas', 'total')
	date_hierarchy = 'order_date'
	ordering = ['-sale__total']
	
	def fullName(self, obj):
		return obj.full_name
	fullName.short_description = 'Name'

	def countPizzas(self, obj):
		return obj.pizzas.all().count()
	countPizzas.short_description = 'Pizzas'
	
	def total(self, obj):
		return "${:.2f}".format(obj.sale.total)

admin.site.register(Order, OrderAdmin)

#============= Pizza ==============#

class ToppingAmountInline(admin.TabularInline):
	model = Pizza.toppings.through
	extra = 1
	
class PizzaAdmin(admin.ModelAdmin):
	inlines = [ToppingAmountInline]

admin.site.register(Pizza, PizzaAdmin)

#============= Topping ==============#

admin.site.register(Topping)

#============= Size ==============#

admin.site.register(Size)
