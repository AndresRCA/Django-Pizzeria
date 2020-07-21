# Diseño de página web para realizar pedidos de pizzas

## Componentes

* Back-end: Django.
* Front-end: Vue.js, Bulma.css.

Django maneja los aspectos MVC de la mayoria del proyecto mientras que Vue maneja la vista en los lugares donde sea conveniente.

## Esquema de la base de datos

...

## Funcionalidades

1. Ordenar pizzas.
2. Generar resumenes de órden.
2. A través del sitio de administración se  pueden acceder a los registros de la base de datos de manera intuitiva.

## Instrucciones de instalación

1. Crea ambiente virtual e instale las dependencias corriendo el comando `pipenv install`, para instalar las dependecias de desarrollo agregue la opción `--dev`.

> #### Usando requirements.txt
> 
> Cree un ambiente virtual de python e instale las dependecias con el comando `pip install -r requirements.txt`.

2. Cambie el nombre del archivo .env.example a .env y configure el archivo con los valores adecuados.

3. Corra el comando `python manage.py migrate`, si `ENV_MODE == 'DEV'` se crearan registros de prueba en la base de datos.

4. Para acceder al sitio admin corra `python manage.py createsuperuser` y sigua los pasos para crear un usuario.
