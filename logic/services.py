import json
import os
from store.models import DATABASE
from django.contrib.auth import get_user


def filtering_category(
    database: dict,
    category_key: [None, str] = None,
    ordering_key: [None, str] = None,
    reverse: bool = False,
):
    if category_key:
        result = [
            item for item in database.values() if category_key == item["category"]
        ]

    else:
        result = list(database.values())

    if ordering_key:
        result.sort(key=lambda x: x[ordering_key], reverse=reverse)

    return result


def view_in_cart(request) -> dict:
    if os.path.exists("cart.json"):
        with open("cart.json", encoding="utf-8") as file:
            return json.load(file)

    user = get_user(request).username
    cart = {user: {"products": {}}}
    with open("cart.json", mode="x", encoding="utf-8") as file:
        json.dump(cart, file)

    return cart


def add_to_cart(request, id_product: str) -> bool:
    cart_users = view_in_cart(request)
    cart = cart_users[get_user(request).username]

    if id_product in cart["products"]:
        if id_product in DATABASE.keys():
            cart["products"][id_product] += 1

    else:
        if id_product in DATABASE.keys():
            cart["products"][id_product] = 1

    with open("cart.json", mode="w", encoding="utf-8") as file:
        json.dump(cart_users, file)

    return True


def remove_from_cart(request, id_product: str) -> bool:
    cart_users = view_in_cart(request)
    cart = cart_users[get_user(request).username]

    if id_product in cart["products"]:
        del cart["products"][id_product]
        with open("cart.json", mode="w", encoding="utf-8") as file:
            json.dump(cart_users, file)

    else:
        return False

    return True


def add_user_to_cart(request, username: str) -> None:
    cart_users = view_in_cart(request)
    cart = cart_users.get(username)

    if not cart:
        with open("cart.json", mode="w", encoding="utf-8") as file:
            cart_users[username] = {"products": {}}
            json.dump(cart_users, file)


def view_in_wishlist(request) -> dict:
    if os.path.exists("wishlist.json"):
        with open("wishlist.json", encoding="utf-8") as file:
            return json.load(file)

    user = get_user(request).username
    wishlist = {user: {"products": []}}
    with open("wishlist.json", mode="x", encoding="utf-8") as file:
        json.dump(wishlist, file)

    return wishlist


def add_to_wishlist(request, id_product: str) -> bool:
    wishlist_users = view_in_wishlist(request)
    wishlist = wishlist_users[get_user(request).username]

    if DATABASE.get(id_product):
        if id_product not in wishlist["products"]:
            wishlist["products"].append(id_product)

    else:
        return False

    with open("wishlist.json", mode="w", encoding="utf-8") as file:
        json.dump(wishlist_users, file)

    return True


def remove_from_wishlist(request, id_product: str) -> bool:
    wishlist_users = view_in_wishlist(request)
    wishlist = wishlist_users[get_user(request).username]

    if id_product in wishlist_users["products"]:
        wishlist["products"].remove(id_product)

    else:
        return False

    with open("wishlist.json", mode="w", encoding="utf-8") as file:
        json.dump(wishlist_users, file)

    return True


def add_user_to_wishlist(request, username: str) -> None:
    wishlist_users = view_in_wishlist(request)
    wishlist = wishlist_users.get(username)

    if not wishlist:
        with open("wishlist.json", mode="w", encoding="utf-8") as file:
            wishlist_users[username] = {"products": []}
            json.dump(wishlist_users, file)
