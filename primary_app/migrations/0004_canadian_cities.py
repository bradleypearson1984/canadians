# Generated by Django 4.1.7 on 2023-04-23 22:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('primary_app', '0003_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='canadian',
            name='cities',
            field=models.ManyToManyField(to='primary_app.city'),
        ),
    ]
