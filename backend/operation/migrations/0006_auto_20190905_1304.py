# Generated by Django 2.2.3 on 2019-09-05 05:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operation', '0005_auto_20190904_1851'),
    ]

    operations = [
        migrations.RenameField(
            model_name='operation',
            old_name='processed_image_0',
            new_name='processed_image',
        ),
        migrations.RemoveField(
            model_name='operation',
            name='processed_image_1',
        ),
        migrations.AddField(
            model_name='operation',
            name='net',
            field=models.CharField(default='', max_length=1),
        ),
    ]
