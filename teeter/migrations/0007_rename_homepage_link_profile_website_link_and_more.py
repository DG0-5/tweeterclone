# Generated by Django 4.1.4 on 2024-02-29 21:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teeter', '0006_profile_facebook_link_profile_homepage_link_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='homepage_link',
            new_name='website_link',
        ),
        migrations.AlterField(
            model_name='profile',
            name='profile_bio',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
