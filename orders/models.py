import uuid
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

class MenuItem(models.Model):
    category = models.ForeignKey(Category, related_name='items', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=500, blank=True, null=True) # Added for spec match
    price = models.DecimalField(max_digits=6, decimal_places=2)
    cost_price = models.DecimalField(max_digits=6, decimal_places=2, default=0.00) # Added for finance tracking
    # Using URL or placeholder for image simplicity in this prototype
    image = models.ImageField(upload_to='menu_items/', blank=True, null=True)
    is_available = models.BooleanField(default=True)

    class Meta:
        unique_together = ('category', 'name')

    def __str__(self):
        return self.name

class Order(models.Model):
    ORDER_STATUS = (
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('DELIVERED', 'Delivered'),
        ('UNDELIVERED', 'Undelivered'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    )
    
    PAYMENT_STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('PAID', 'Paid'),
        ('FAILED', 'Failed'),
    )
    
    FULFILLMENT_CHOICES = (
        ('DELIVERY', 'Delivery'),
        ('DINE_IN', 'Dine In'),
        ('TAKEAWAY', 'Takeaway'),
    )
    
    order_id = models.CharField(max_length=40, default=uuid.uuid4, unique=True, editable=False)
    customer_name = models.CharField(max_length=100, default='Guest')
    customer_number = models.CharField(max_length=15, blank=True, null=True) # Added number field
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    payment_method = models.CharField(max_length=10, default='CASH')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='PENDING')
    fulfillment_type = models.CharField(max_length=20, choices=FULFILLMENT_CHOICES, default='DELIVERY')
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.order_id}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=6, decimal_places=2) # Snapshot selling price
    cost_price = models.DecimalField(max_digits=6, decimal_places=2, default=0.00) # Snapshot cost price

    def save(self, *args, **kwargs):
        if not self.price and self.menu_item:
            self.price = self.menu_item.price
        if not self.cost_price and self.menu_item:
            self.cost_price = self.menu_item.cost_price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.quantity}x {self.menu_item.name}"