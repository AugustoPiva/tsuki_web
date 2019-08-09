# Generated by Django 2.1.7 on 2019-08-09 18:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tsuki_app', '0004_pedidos_fecha_creacion'),
    ]

    operations = [
        migrations.AddField(
            model_name='productosordenados',
            name='lotienen',
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AlterField(
            model_name='listaprecios',
            name='sub_categoria_producto',
            field=models.CharField(choices=[('hotroll', 'Hot Rolls'), ('otros', 'Otros'), ('clasicos', 'Clasicos'), ('especiales', 'Especiales'), ('premiums', 'Premiums'), ('veggies', 'Veggies'), ('salsa', 'Salsas'), ('bocados', 'Bocados'), ('surtido', 'Surtido'), ('salmon', 'Salmon')], max_length=20),
        ),
    ]
