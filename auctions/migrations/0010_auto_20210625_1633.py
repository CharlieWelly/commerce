# Generated by Django 3.2.4 on 2021-06-25 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0009_watchlist_unique_watch'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='watchlist',
            name='unique_watch',
        ),
        migrations.RenameField(
            model_name='watchlist',
            old_name='item',
            new_name='listing',
        ),
        migrations.AddConstraint(
            model_name='watchlist',
            constraint=models.UniqueConstraint(fields=('listing', 'user'), name='unique_watch'),
        ),
    ]
