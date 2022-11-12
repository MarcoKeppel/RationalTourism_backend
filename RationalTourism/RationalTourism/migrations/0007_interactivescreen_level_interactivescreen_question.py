# Generated by Django 4.1.3 on 2022-11-12 05:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RationalTourism', '0006_alter_interactivescreen_target'),
    ]

    operations = [
        migrations.AddField(
            model_name='interactivescreen',
            name='level',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='interactivescreen',
            name='question',
            field=models.CharField(default='', max_length=200),
        ),
    ]