from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib.auth import logout

from .forms import CustomerRegistrationForm
from .models import CartItem, Product


# ---------------------------
# FRONT PAGE (PRODUCT GALLERY + SEARCH)
# ---------------------------
def front_page(request):
    query = request.GET.get("q", "")

    products = Product.objects.all()

    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(category__icontains=query) |
            Q(description__icontains=query)
        )

    paginator = Paginator(products, 9)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "front_page.html", {
        "page_obj": page_obj,
        "query": query,
    })


# ---------------------------
# LOGOUT
# ---------------------------
def logout_view(request):
    logout(request)
    return redirect("front_page")


# ---------------------------
# REGISTER
# ---------------------------
def register(request):
    if request.method == "POST":
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account created successfully!")
            return redirect("login")
    else:
        form = CustomerRegistrationForm()

    return render(request, "register.html", {"form": form})


# ---------------------------
# NOTIFICATIONS
# ---------------------------
@login_required
def notifications(request):
    return render(request, "notifications.html")


# ---------------------------
# PRODUCT LISTING
# ---------------------------
def men_products(request):
    products = Product.objects.filter(category="men")
    return render(request, "product_list.html", {"products": products, "title": "Men"})


def women_products(request):
    products = Product.objects.filter(category="women")
    return render(request, "product_list.html", {"products": products, "title": "Women"})


def kids_products(request):
    products = Product.objects.filter(category="kids")
    return render(request, "product_list.html", {"products": products, "title": "Kids"})


# ---------------------------
# ADD TO CART
# ---------------------------
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == "POST":
        cart_item, created = CartItem.objects.get_or_create(
            user=request.user,
            product=product,
            defaults={"quantity": 1}
        )

        if not created:
            cart_item.quantity += 1
            cart_item.save()

    return redirect("cart")


# ---------------------------
# CART PAGE
# ---------------------------
@login_required
def cart(request):
    items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.total_price for item in items)
    return render(request, "cart.html", {
        "items": items,
        "total_price": total_price
    })


# ---------------------------
# REMOVE FROM CART
# ---------------------------
@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, user=request.user)
    item.delete()
    messages.success(request, "Item removed from cart.")
    return redirect("cart")


# ---------------------------
# UPDATE CART
# ---------------------------
@login_required
def update_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, user=request.user)

    if request.method == "POST":
        qty = int(request.POST.get("quantity", 1))
        item.quantity = max(1, qty)
        item.save()
        messages.success(request, "Cart updated.")

    return redirect("cart")


# ---------------------------
# SEND RECEIPT EMAIL
# ---------------------------
def send_receipt_email(user, items, total_price, payment_method):
    subject = "Your Order Receipt"

    message = render_to_string("emails/receipt_email.html", {
        "user": user,
        "items": items,
        "total_price": total_price,
        "payment_method": payment_method,
    })

    send_mail(
        subject,
        message,
        None,
        [user.email],
        fail_silently=False,
    )


# ---------------------------
# CHECKOUT
# ---------------------------
@login_required
def checkout(request):
    items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.total_price for item in items)

    if request.method == "POST":
        payment_method = request.POST.get("payment_method")

        send_receipt_email(
            user=request.user,
            items=items,
            total_price=total_price,
            payment_method=payment_method
        )

        items.delete()

        messages.success(request, "Checkout complete! Receipt sent to your email.")
        return redirect("cart")

    return render(request, "checkout.html", {
        "items": items,
        "total_price": total_price,
        "payment_methods": [
            ("cash", "Cash"),
            ("card", "Credit/Debit Card"),
            ("zelle", "Zelle"),
            ("PayPal", "PayPal"),
        ],
    })