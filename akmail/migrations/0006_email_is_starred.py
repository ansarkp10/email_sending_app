# Generated by Django 5.0.6 on 2024-07-11 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('akmail', '0005_email_folder_alter_email_from_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='email',
            name='is_starred',
            field=models.BooleanField(default=False),
        ),
    ]
