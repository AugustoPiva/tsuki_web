# Generated by Django 2.2.4 on 2019-08-19 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tsuki_app', '0005_auto_20190809_1518'),
    ]

    operations = [
        migrations.AddField(
            model_name='productosordenados',
            name='total',
            field=models.IntegerField(null=True),
        ),
    ]
