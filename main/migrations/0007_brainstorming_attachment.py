# Generated by Django 5.0.6 on 2025-02-05 05:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_rename_is_verified_profile_profile_verified'),
    ]

    operations = [
        migrations.AddField(
            model_name='brainstorming',
            name='attachment',
            field=models.FileField(blank=True, null=True, upload_to='brainstorming_attachments/'),
        ),
    ]
