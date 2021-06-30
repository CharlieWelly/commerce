from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing/", views.create_listing, name="create_listing"),
    path("listing/<int:listing_id>/", views.listing, name="listing"),
    path("listing/bid/<int:listing_id>/", views.bid, name="bid"),
    path("listing/watch/<int:listing_id>", views.watch, name="watch"),
    path("listing/close_bid/<int:listing_id>/", views.close_bid, name="close_bid"),
    path("listing/comment/<int:listing_id>/", views.comment, name="comment"),
    path("watch_list/", views.watch_list, name="watch_list"),
    path("categories/", views.categories, name="categories"),
    path("categories/<int:category_value>/", views.category, name="category"),
]
