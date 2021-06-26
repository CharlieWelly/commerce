from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    pass


class Listing(models.Model):
    class Status(models.IntegerChoices):
        CLOSE = 0
        OPEN = 1

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="listed_items"
    )
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=300)
    start_bid = models.PositiveIntegerField()
    url = models.URLField(blank=True)
    status = models.IntegerField(choices=Status.choices, default=Status.OPEN)

    def __str__(self):
        return f"{self.title} listed by {self.user.username}"


class Bid(models.Model):
    bid_time = models.DateField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids_placed")
    item = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    bid_price = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.user.username} bid {self.bid_price} on {self.item.title}"


class Comment(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_comments"
    )
    item = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name="item_comments"
    )
    comment_time = models.DateField(auto_now=True)
    comment = models.TextField(max_length=300)

    def __str__(self):
        return f"{self.user.username} comments on {self.item.title}: {self.comment}"


class WatchList(models.Model):
    listing = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name="watched_by"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watching")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["listing", "user"], name="unique_watch")
        ]

    def __str__(self):
        return f"{self.listing.title} watched by {self.user.username}"
