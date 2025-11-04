from django.urls import path
from .views import ItemListView, CartView, AddToCartView, RemoveFromCartView, UpdateCartItemView, ClearCartView, ItemDetailView

urlpatterns = [
    path("", ItemListView.as_view(), name="items_list"),
    path("add-to-cart/<int:item_id>/", AddToCartView.as_view(), name="add_to_cart"),
    path("items/<int:pk>/", ItemDetailView.as_view(), name="item_detail"),
    path("cart/", CartView.as_view(), name="cart"),
    path("cart/remove/<int:item_id>/", RemoveFromCartView.as_view(), name="remove_from_cart"),
    path("cart/update/<int:item_id>/", UpdateCartItemView.as_view(), name="update_cart_item"),
    path("cart/clear/", ClearCartView.as_view(), name="clear_cart")
]