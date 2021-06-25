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
        return None
