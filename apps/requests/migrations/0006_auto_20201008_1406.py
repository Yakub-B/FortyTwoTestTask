# Generated by Django 3.0.8 on 2020-10-08 11:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('requests', '0005_auto_20201007_1314'),
    ]

    operations = [
        migrations.AlterField(
            model_name='urlpriority',
            name='priority',
            field=models.IntegerField(blank=True, default=1),
        ),
    ]
