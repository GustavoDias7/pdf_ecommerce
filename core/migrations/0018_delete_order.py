# Generated by Django 4.2.6 on 2024-02-06 15:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0017_alter_order_discount'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Order',
        ),
    ]
