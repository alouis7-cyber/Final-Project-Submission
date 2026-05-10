from django.db import models
from django.contrib.auth.models import User


# ---------------------------
# ORDER MODEL
# ---------------------------
class Order(models.Model):
    STATUS_CHOICES = [
        ('received', 'Received'),
        ('in_progress', 'In Progress'),
        ('ready', 'Ready'),
        ('completed', 'Completed'),
        ('delayed', 'Delayed'),
    ]

    customer_name = models.CharField(max_length=100)
    email = models.EmailField()
    garment_type = models.CharField(max_length=100)
    alteration_type = models.CharField(max_length=200)
    notes = models.TextField(blank=True)
    image = models.ImageField(upload_to='order_images/', blank=True, null=True)

    price_estimate = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='received')
    created_at = models.DateTimeField(auto_now_add=True)
    deadline = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.customer_name} - {self.garment_type}"


# ---------------------------
# PRODUCT MODEL
# ---------------------------
class Product(models.Model):
    CATEGORY_CHOICES = [
        ("men", "Men"),
        ("women", "Women"),
        ("kids", "Kids"),
    ]

    name = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.TextField(blank=True)

    sizes = models.CharField(max_length=200)   # Example: "S,M,L,XL"
    colors = models.CharField(max_length=200)  # Example: "Black,White,Blue"

    image = models.ImageField(upload_to="product_images/", blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# ---------------------------
# CART ITEM MODEL
# ---------------------------
class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

    @property
    def total_price(self):
        return self.product.price * self.quantity
