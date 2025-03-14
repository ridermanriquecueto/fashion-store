# Generated by Django 5.1.5 on 2025-02-05 18:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('productos', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='carrito',
            name='items',
        ),
        migrations.RemoveField(
            model_name='pedido',
            name='productos',
        ),
        migrations.RemoveField(
            model_name='pedido',
            name='total',
        ),
        migrations.AddField(
            model_name='itemcarrito',
            name='carrito',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='items', to='productos.carrito'),
        ),
        migrations.AddField(
            model_name='pedido',
            name='carrito',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='productos.carrito'),
        ),
        migrations.AlterField(
            model_name='pedido',
            name='metodo_entrega',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='productos.metodoentrega'),
        ),
        migrations.AlterField(
            model_name='pedido',
            name='metodo_pago',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='productos.metodopago'),
        ),
        migrations.AlterField(
            model_name='producto',
            name='imagen',
            field=models.ImageField(blank=True, null=True, upload_to='productos/'),
        ),
    ]
