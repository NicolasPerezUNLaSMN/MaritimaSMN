# Generated by Django 4.0.4 on 2022-06-16 20:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppMaritima', '0016_hielo_activo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pronostico',
            name='boletin',
        ),
        migrations.AddField(
            model_name='pronostico',
            name='boletin',
            field=models.ManyToManyField(to='AppMaritima.boletin'),
        ),
    ]
