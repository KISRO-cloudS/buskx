# Generated by Django 5.0.6 on 2024-09-15 15:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_campaign_visible_to_followers'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='campaign',
            name='allowed_viewers',
        ),
    ]
