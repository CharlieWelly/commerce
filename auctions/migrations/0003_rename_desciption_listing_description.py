# Generated by Django 3.2.4 on 2021-06-22 01:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_bid_comment_listing'),
    ]

    operations = [
        migrations.RenameField(
            model_name='listing',
            old_name='desciption',
            new_name='description',
        ),
    ]
