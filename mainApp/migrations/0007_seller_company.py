# Generated by Django 4.0 on 2022-01-12 19:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0006_seller_pic'),
    ]

    operations = [
        migrations.AddField(
            model_name='seller',
            name='company',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
    ]