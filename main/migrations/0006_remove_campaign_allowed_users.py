# Generated by Django 5.0.6 on 2024-09-19 06:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_remove_campaign_allowed_viewers'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='campaign',
            name='allowed_users',
        ),
    ]