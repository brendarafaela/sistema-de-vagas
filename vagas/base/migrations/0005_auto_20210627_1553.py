# Generated by Django 3.1.7 on 2021-06-27 18:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_auto_20210625_1747'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuariovaga',
            name='pretensaoSalario',
            field=models.IntegerField(choices=[(0, 'Até 1.000'), (1, 'De 1.000 a 2.000'), (2, 'De 2.000 a 3.000'), (3, 'Acima de 3.000')]),
        ),
    ]
