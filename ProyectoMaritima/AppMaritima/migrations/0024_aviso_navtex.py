# Generated by Django 4.0.4 on 2022-07-02 23:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppMaritima', '0023_area_orden'),
    ]

    operations = [
        migrations.AddField(
            model_name='aviso',
            name='navtex',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]
