# Generated by Django 4.0 on 2022-01-12 21:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainApp', '0009_buyer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buyer',
            name='addressLine1',
            field=models.CharField(blank=True, default=None, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='buyer',
            name='addressLine2',
            field=models.CharField(blank=True, default=None, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='buyer',
            name='addressLine3',
            field=models.CharField(blank=True, default=None, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='buyer',
            name='city',
            field=models.CharField(blank=True, default=None, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='buyer',
            name='pin',
            field=models.CharField(blank=True, default=None, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='buyer',
            name='state',
            field=models.CharField(blank=True, default=None, max_length=50, null=True),
        ),
    ]
