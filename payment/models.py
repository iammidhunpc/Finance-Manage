from django.db import models


class Invoice(models.Model):
    invoice_id = models.CharField(max_length=100, unique=True)
    client_name = models.CharField(max_length=100)
    client_email = models.EmailField(max_length=100)
    project_name = models.CharField(max_length=100)
    amount = models.IntegerField(default=0)
    closed = models.BooleanField(default=False)
    short_link = models.CharField(max_length=50, null=True, blank=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.invoice_id
