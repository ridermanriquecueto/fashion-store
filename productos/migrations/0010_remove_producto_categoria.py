# Generated by Django 5.1.5 on 2025-02-19 20:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0009_alter_producto_categoria'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='producto',
            name='categoria',
        ),
    ]
