# Generated by Django 4.1.3 on 2022-11-11 20:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RationalTourism', '0002_interactivescreen'),
    ]

    operations = [
        migrations.AlterField(
            model_name='interactivescreen',
            name='latitude',
            field=models.CharField(max_length=15),
        ),
        migrations.AlterField(
            model_name='interactivescreen',
            name='longitude',
            field=models.CharField(max_length=15),
        ),
    ]