# Generated by Django 4.2.6 on 2024-01-25 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_alter_user_first_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='stripe_price_id',
            field=models.CharField(max_length=35, null=True),
        ),
    ]