# Generated by Django 2.2.5 on 2020-03-24 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bdaygifts', '0006_auto_20200323_2319'),
    ]

    operations = [
        migrations.AddField(
            model_name='gift',
            name='hover',
            field=models.CharField(default='', max_length=100),
        ),
    ]
