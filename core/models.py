from django.db import models


# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=30)
    price = models.IntegerField()
    description = models.TextField(max_length=400)
    image = models.ImageField(upload_to="images/", null=True)
    pdf = models.FileField(upload_to="pdfs/", null=True)

    def __str__(self):
        return f"product {self.name}"
