# Generated by Django 4.0.4 on 2022-06-15 02:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppMaritima', '0015_remove_hielo_boletin_hielo_boletin'),
    ]

    operations = [
        migrations.AddField(
            model_name='hielo',
            name='activo',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]