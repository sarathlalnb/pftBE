# Generated by Django 4.2.5 on 2024-05-16 07:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hrapi', '0009_rename_description_meeting_title_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='meeting',
            old_name='Title',
            new_name='title',
        ),
    ]
