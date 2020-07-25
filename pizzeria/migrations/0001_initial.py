# Generated by Django 3.0.8 on 2020-07-25 03:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=60)),
                ('last_name', models.CharField(max_length=60)),
                ('order_date', models.DateTimeField()),
            ],
            options={
                'ordering': ['-order_date'],
            },
        ),
        migrations.CreateModel(
            name='Pizza',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pizzas', to='pizzeria.Order')),
            ],
        ),
        migrations.CreateModel(
            name='Size',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True)),
                ('price', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Topping',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True)),
                ('price', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('order', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='pizzeria.Order')),
                ('total', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='ToppingAmount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveIntegerField()),
                ('pizza', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pizzeria.Pizza')),
                ('topping', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pizzeria.Topping')),
            ],
        ),
        migrations.AddField(
            model_name='pizza',
            name='size',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pizzeria.Size'),
        ),
        migrations.AddField(
            model_name='pizza',
            name='toppings',
            field=models.ManyToManyField(through='pizzeria.ToppingAmount', to='pizzeria.Topping'),
        ),
        migrations.AlterOrderWithRespectTo(
            name='pizza',
            order_with_respect_to='order',
        ),
    ]
