# Generated by Django 4.2.5 on 2024-07-02 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hrapi', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='name',
            field=models.CharField(max_length=200),
        ),
    ]
