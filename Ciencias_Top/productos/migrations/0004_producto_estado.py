# Generated by Django 5.1.3 on 2024-11-26 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0003_alter_producto_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='estado',
            field=models.CharField(choices=[('A', 'Disponible'), ('R', 'Rentado'), ('N', 'No disponible')], default='A', max_length=1, verbose_name='Estado del producto'),
        ),
    ]