# Generated by Django 3.2.6 on 2022-03-18 18:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppMaritima', '0008_aviso_area'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aviso',
            name='tipo',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='situacion',
            name='evolucion',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]
