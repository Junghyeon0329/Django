# Generated by Django 4.2.14 on 2024-12-08 21:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('personal_data', '0003_remove_user_password'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='name',
            new_name='username',
        ),
    ]