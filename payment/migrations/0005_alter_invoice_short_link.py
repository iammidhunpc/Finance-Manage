# Generated by Django 3.2 on 2021-04-15 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0004_invoice_short_link'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='short_link',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
