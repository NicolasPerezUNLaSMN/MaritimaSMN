# Generated by Django 4.0.4 on 2022-06-14 19:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppMaritima', '0013_situacion_activo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='situacion',
            name='boletin',
        ),
        migrations.AddField(
            model_name='situacion',
            name='boletin',
            field=models.ManyToManyField(to='AppMaritima.boletin'),
        ),
    ]
