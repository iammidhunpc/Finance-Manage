# Generated by Django 3.2 on 2021-04-15 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0003_alter_invoice_invoice_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='short_link',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
    ]
