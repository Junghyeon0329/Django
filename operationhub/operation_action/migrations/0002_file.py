# Generated by Django 4.2.14 on 2024-12-13 12:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('operation_action', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='uploads/%Y/%m/%d/')),
                ('name', models.CharField(max_length=255)),
                ('file_size', models.PositiveIntegerField()),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('board', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='files', to='operation_action.board')),
            ],
            options={
                'db_table': 'board_files',
            },
        ),
    ]