# Generated by Django 4.2.14 on 2024-10-18 06:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('phone_number', models.CharField(max_length=50)),
                ('email_id', models.CharField(max_length=500)),
                ('password', models.CharField(max_length=500)),
            ],
            options={
                'db_table': 'user',
            },
        ),
    ]
