## Website design for ordering pizzas

## Components

* Back-end: Django.
* Front-end: Vue.js, Bulma.css.

Django handles the MVC aspects of most of the project while Vue handles the view where it is appropriate.

## Database schema

![Schema](/doc/Models.png)

## Functionalities

1. Order pizzas.
2. Generate order summaries.
2. Through the administration site you can access to the database records in an intuitive way.

## Installation instructions

1. Create virtual environment and install the dependencies by running the `pipenv install` command, to install the development dependencies add the `--dev` option.

> #### Using requirements.txt
> 
> Create a python virtual environment and install the dependencies with the `pip install -r requirements.txt` command.

2. Rename the .env.example file to .env and configure the file with the appropriate values.

3. Run the `python manage.py migrate` command, if `MODE == 'DEV'` in the .env file, test records will be created in the database.

4. To access the admin site run `python manage.py createsuperuser` and follow the steps to create a user.

## P.S

This is a project that was required in a class I took, so if the website doesn't look that good in different viewports know that minimal effort was put on the style aspect of things, the code and functionality however was took seriously during development.
