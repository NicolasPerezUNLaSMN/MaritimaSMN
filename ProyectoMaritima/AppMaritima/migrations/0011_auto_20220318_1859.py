# Generated by Django 3.2.6 on 2022-03-18 21:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppMaritima', '0010_auto_20220318_1857'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aviso',
            name='desde',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='aviso',
            name='hasta',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='boletin',
            name='valido',
            field=models.DateField(),
        ),
    ]
