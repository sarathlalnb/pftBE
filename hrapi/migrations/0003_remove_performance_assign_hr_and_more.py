# Generated by Django 4.2.5 on 2024-07-03 15:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hrapi', '0002_alter_employee_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='performance_assign',
            name='hr',
        ),
        migrations.AddField(
            model_name='performance_assign',
            name='teamlead',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='hrapi.teamlead'),
        ),
    ]
