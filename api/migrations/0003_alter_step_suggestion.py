# Generated by Django 5.1.3 on 2024-11-29 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_remove_member_assign_project_member_assign_project'),
    ]

    operations = [
        migrations.AlterField(
            model_name='step',
            name='suggestion',
            field=models.TextField(default=''),
        ),
    ]
