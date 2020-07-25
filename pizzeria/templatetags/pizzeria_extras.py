from django import template

register = template.Library()

#--------- Custom filters -----------

@register.filter
def currency(value):
	"""Returns a float number in currency format"""
	return "${:.2f}".format(value)

#------------------------------------

