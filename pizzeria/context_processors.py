import os

# used in settings.py: templates.options.context_processors
# this allows me to use custom variables inside templates

def export_vars(request):
	data = {}
	data['ENV_MODE'] = os.getenv('MODE')
	return data
