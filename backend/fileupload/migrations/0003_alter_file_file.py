# Generated by Django 5.0.3 on 2024-03-29 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fileupload', '0002_alter_file_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='file',
            field=models.FileField(upload_to='./pdf'),
        ),
    ]