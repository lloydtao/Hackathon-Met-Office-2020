# Generated by Django 2.1.5 on 2020-01-25 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cycloneapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cyclone',
            name='id',
        ),
        migrations.AlterField(
            model_name='cyclone',
            name='date',
            field=models.DateTimeField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='cyclone',
            name='lat',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='cyclone',
            name='long',
            field=models.FloatField(),
        ),
    ]
