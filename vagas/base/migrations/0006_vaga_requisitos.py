# Generated by Django 3.1.7 on 2021-06-27 18:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_auto_20210627_1553'),
    ]

    operations = [
        migrations.AddField(
            model_name='vaga',
            name='requisitos',
            field=models.TextField(default=''),
        ),
    ]
