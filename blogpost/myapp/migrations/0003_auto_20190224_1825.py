# Generated by Django 2.1.5 on 2019-02-24 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_auto_20190224_1804'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='text',
            field=models.TextField(max_length=500),
        ),
    ]
