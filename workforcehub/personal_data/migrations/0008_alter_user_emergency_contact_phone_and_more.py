# Generated by Django 4.2.14 on 2024-12-16 22:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('personal_data', '0007_rename_permission_date_user_approval_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='emergency_contact_phone',
            field=models.CharField(default='N/A', max_length=20),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=models.CharField(default='N/A', max_length=100),
        ),
    ]
