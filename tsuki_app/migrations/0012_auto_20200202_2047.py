# Generated by Django 2.2.4 on 2020-02-02 23:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tsuki_app', '0011_auto_20200202_2029'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listaprecios',
            name='categoria_producto',
            field=models.CharField(choices=[('rolls', 'Rolls'), ('calientes', 'Calientes'), ('barcos', 'Barcos'), ('puentes', 'Puentes'), ('bd', 'Barcos descartables'), ('laja', 'Lajas'), ('varios', 'Varios'), ('eliminados', 'Eliminados')], max_length=20),
        ),
    ]
