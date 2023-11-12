# Generated by Django 4.2.6 on 2023-11-09 19:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('price', models.IntegerField()),
                ('description', models.TextField(max_length=400)),
                ('image', models.ImageField(null=True, upload_to='images/')),
                ('pdf', models.FileField(null=True, upload_to='pdfs/')),
            ],
        ),
    ]
