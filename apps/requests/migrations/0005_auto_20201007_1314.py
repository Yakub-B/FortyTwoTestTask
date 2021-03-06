# Generated by Django 3.0.8 on 2020-10-07 10:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('requests', '0004_auto_20201006_1655'),
    ]

    operations = [
        migrations.CreateModel(
            name='UrlPriority',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('priority', models.IntegerField(default=1)),
                ('path', models.URLField(max_length=300)),
            ],
        ),
        migrations.RemoveField(
            model_name='requestmodel',
            name='priority',
        ),
        migrations.RemoveField(
            model_name='requestmodel',
            name='url',
        ),
        migrations.AddField(
            model_name='requestmodel',
            name='url_priority',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='requests.UrlPriority'),
        ),
    ]
