# Generated by Django 4.2.6 on 2024-02-26 18:55

from django.db import migrations, models
import gdstorage.storage


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0028_alter_product_image_alter_product_pdf'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(null=True, storage=gdstorage.storage.GoogleDriveStorage(), upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='product',
            name='pdf',
            field=models.FileField(null=True, storage=gdstorage.storage.GoogleDriveStorage(), upload_to='pdfs/'),
        ),
    ]
