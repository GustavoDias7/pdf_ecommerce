# Generated by Django 4.2.6 on 2024-01-27 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_product_stripe_price_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='stripe_product_id',
            field=models.CharField(max_length=35, null=True),
        ),
    ]
