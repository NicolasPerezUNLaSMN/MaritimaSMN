# Generated by Django 3.2.6 on 2022-03-18 21:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppMaritima', '0009_auto_20220318_1553'),
    ]

    operations = [
        migrations.AddField(
            model_name='aviso',
            name='horaDesde',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='aviso',
            name='horaHasta',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='boletin',
            name='hora',
            field=models.IntegerField(null=True),
        ),
    ]
