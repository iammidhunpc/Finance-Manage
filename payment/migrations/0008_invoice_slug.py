# Generated by Django 3.2 on 2021-04-15 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0007_remove_invoice_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='slug',
            field=models.SlugField(default=2, unique=True),
            preserve_default=False,
        ),
    ]
