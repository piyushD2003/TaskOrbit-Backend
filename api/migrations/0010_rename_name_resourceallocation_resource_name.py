# Generated by Django 5.1.3 on 2024-11-30 16:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_resourceallocation'),
    ]

    operations = [
        migrations.RenameField(
            model_name='resourceallocation',
            old_name='name',
            new_name='resource_name',
        ),
    ]
