# Generated by Django 3.2 on 2021-04-15 07:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='closed',
            field=models.BooleanField(default=False),
        ),
    ]
