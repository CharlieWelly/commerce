from django import template

register = template.Library()


@register.filter(name="mod_four")
def mod_four(value):
    return value % 4


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
