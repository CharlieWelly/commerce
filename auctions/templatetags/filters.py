from django import template

register = template.Library()


@register.filter(name="mod")
def mod(value, x):
    return value % x


@register.filter(name="bid_user")
def bid_user(listing):
    if listing.bids.last():
        return listing.bids.last().user.username
    else:
        return None


@register.filter(name="bid_count")
def bid_count(listing):
    if listing.bids:
        return listing.bids.count()
    else:
        return 0


@register.filter(name="current_price")
def current_price(listing):
    if listing.bids.last():
        return listing.bids.last().bid_price
    else:
        return listing.start_bid


@register.filter(name="watched")
def watched(listing, user):
    if user.is_authenticated and listing.watched_by.filter(user=user):
        return True
    else:
        return False
