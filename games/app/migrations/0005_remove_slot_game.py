# Generated by Django 4.2.19 on 2025-02-12 16:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_remove_slot_end_time_remove_slot_start_time_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='slot',
            name='game',
        ),
    ]
