from django.urls import path
from .views import (
    wishlist_view,
    wishlist_add_view,
    wishlist_del_view,
    wishlist_json,
    wishlist_remove_view,
)

app_name = "wishlist"

urlpatterns = [
    path("", wishlist_view, name="wishlist_view"),
    path("api/add/<str:id_product>", wishlist_add_view),
    path("api/del/<str:id_product>", wishlist_del_view, name="remove_from"),
    path("api/", wishlist_json),
]
