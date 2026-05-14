from django.urls import path
from . import views

urlpatterns = [
    path("", views.front_page, name="front_page"),

    # AUTH
    path("register/", views.register, name="register"),
    path("logout/", views.logout_view, name="logout"),

    # ORDERS
    path("create-order/", views.create_order, name="create_order"),
    path("order-status/<int:id>/", views.order_status, name="order_status"),
    path("orders-list/", views.orders_list, name="orders_list"),

    # ADMIN DASHBOARD
    path("admin-dashboard/", views.admin_dashboard, name="admin_dashboard"),

    # PRODUCTS
    path("products/men/", views.men_products, name="men_products"),
    path("products/women/", views.women_products, name="women_products"),
    path("products/kids/", views.kids_products, name="kids_products"),

    # CART
    path("add-to-cart/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path("cart/", views.cart, name="cart"),
    path("remove-from-cart/<int:item_id>/", views.remove_from_cart, name="remove_from_cart"),
    path("update-cart/<int:item_id>/", views.update_cart, name="update_cart"),

    # CHECKOUT
    path("checkout/", views.checkout, name="checkout"),
]




