# Generated by Django 2.0.7 on 2019-01-31 08:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductPrice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Price period name', max_length=25)),
                ('price', models.PositiveIntegerField(help_text='Price of product in cents')),
                ('date_start', models.DateField()),
                ('date_end', models.DateField(blank=True, null=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prices', to='products.Product')),
            ],
        ),
    ]
