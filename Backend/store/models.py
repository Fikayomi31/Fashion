from enum import unique
from django.db import models
from shortuuid.django_fields import ShortUUIDField
from django.utils.text import slugify

from userauth.models import User, CustomerProfile, VendorProfile


CATEGORY_TYPE = (
    ('MEN', 'MEN'),
    ('WOMEN', 'WOMEN'),
    ('TEEN', 'TEEN'),
    ('UNISEX', 'UNISEX')
)

STATUS = (
    ('Draft', 'Draft'),
    ('Disable', 'Disable'),
    ('In_Review', 'In Review'),
    ('Published', 'Published'),
)

PAYMENT_STATUS_CHOICES = (
    ('pending', 'Pending'),
    ('completed', 'Completed'),
    ('failed', 'Failed'),
)

ORDER_STATUS = (
    ('Pending', 'Pending'),
    ('Shipped', 'Shipped'),
    ('Delivered', 'Delivered'),
    ('Cancelled', 'Cancelled'),
)

PAYMENT_STATUS = (
    ('Pending', 'Pending'),
    ('Processing', 'Processing'),
    ('Failed', 'Failed'),
)

class Category(models.Model):
    title = models.CharField(max_length=100, choices=CATEGORY_TYPE, default='MEN')
    image = models.FileField(upload_to='category', default='category.jpg', null=True, blank=True)
    active = models.BooleanField(default=True)
    slug = models.SlugField(unique=True, blank=True)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name_plural = 'Category'
        ordering = ['title']

    def save(self, *args, **kwargs):
        if self.slug == "" or self.slug == None:
            self.slug = slugify(self.title)
        super(Category, self).save(*args, **kwargs)
         

class Product(models.Model):
    title = models.CharField(max_length=100)
    image = models.FileField(upload_to='products', default='product.jpg', null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    price = models.DecimalField(decimal_places=2, max_digits=12, default=0.00)
    old_price = models.DecimalField(decimal_places=2, max_digits=12, default=0.00)
    shipping_amount = models.DecimalField(decimal_places=2, max_digits=12, default=0.00)
    
    stock_qty = models.PositiveIntegerField(default=1)
    in_stock = models.BooleanField(default=True)

    status = models.CharField(max_length=100, choices=STATUS, default='Published')
    featured = models.BooleanField(default=False)
    views = models.PositiveIntegerField(default=0)
    rating = models.PositiveIntegerField(default=0)
    vendor = models.ForeignKey(VendorProfile, on_delete=models.CASCADE)
    pid = ShortUUIDField(unique=True, length=10, alphabet='abcdefg12345')
    slug = models.SlugField(unique=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.slug == "" or self.slug == None:
            self.slug = slugify(self.title)
        super(Product, self).save(*args, **kwargs)
         
    def __str__(self):
        return self.title
    
class Gallery(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.FileField(upload_to='products', default='product.jpg')
    active = models.BooleanField(default=True)
    gid = ShortUUIDField(unique=True, length=10, alphabet='abcdefg12345')

    def __str__(self):
        return self.product.title
    

class Specification(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    title = models.CharField(max_length=1000)
    content = models.CharField(max_length=1000)

    def __str__(self):
        return self.product.title
    
class Size(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=1000)
    price = models.DecimalField(decimal_places=2, max_digits=12, default=0.00)

    def __str__(self):
        return self.name
    
class Color(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=1000)
    color_code = models.CharField(max_length=1000)

    def __str__(self):
        return self.name


class Cart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE)
    qty = models.PositiveIntegerField(default=0)
    price = models.DecimalField(default=0.00, max_digits=12, decimal_places=2)
    sub_total = models.DecimalField(default=0.00, max_digits=12, decimal_places=2)
    shipping_amount = models.DecimalField(default=0.00, max_digits=12, decimal_places=2)
    service_fee = models.DecimalField(default=0.00, max_digits=12, decimal_places=2)
    tax_fee = models.DecimalField(default=0.00, max_digits=12, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=12, decimal_places=2)
    country = models.CharField(max_length=100, null=True, blank=True)
    size = models.CharField(max_length=1000, null=True, blank=True)
    color = models.CharField(max_length=1000, null=True, blank=True)
    cart_id = models.CharField(max_length=1000, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.cart_id} - {self.product.title}'
    
class CartOrder(models.Model):
    vendor = models.ManyToManyField(VendorProfile, blank=True)
    buyer = models.ForeignKey(CustomerProfile, on_delete=models.SET_NULL, null=True, blank=True)
    
    sub_total = models.DecimalField(decimal_places=2, max_digits=12, default=0.00)
    shipping_amount = models.DecimalField(decimal_places=2, max_digits=12, default=0.00)
    tax_fee = models.DecimalField(decimal_places=2, max_digits=12, default=0.00)
    service_fee = models.DecimalField(decimal_places=2, max_digits=12, default=0.00)
    total = models.DecimalField(decimal_places=2, max_digits=12, default=0.00)

    payment_status = models.CharField(choices=PAYMENT_STATUS, max_length=100, default='Pending')
    order_status = models.CharField(choices=ORDER_STATUS, max_length=100, default='Pending')

    #coupon
    initial_cost = models.DecimalField(decimal_places=2, max_digits=12, default=0.00)
    saved = models.DecimalField(decimal_places=2, max_digits=12, default=0.00)

    #Bio data
    full_name = models.CharField(max_length=100, null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    mobile = models.CharField(max_length=100, null=True, blank=True)

    #Shipping Address
    address= models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)

    oid = ShortUUIDField(unique=True, length=10, alphabet='abcdefg12345')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.oid
    
class CartOrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(CartOrder, on_delete=models.CASCADE)
    vendor = models.ForeignKey(VendorProfile, on_delete=models.CASCADE)

    qty = models.CharField(default=0, max_length=100)
    price = models.DecimalField(decimal_places=2, max_digits=12, default=0.00)
    
    sub_total = models.DecimalField(decimal_places=2, max_digits=12, default=0.00)
    shipping_amount = models.DecimalField(decimal_places=2, max_digits=12, default=0.00)
    tax_fee = models.DecimalField(decimal_places=2, max_digits=12, default=0.00)
    service_fee = models.DecimalField(decimal_places=2, max_digits=12, default=0.00)
    total = models.DecimalField(decimal_places=2, max_digits=12, default=0.00)
    country = models.CharField(max_length=100, null=True, blank=True)

    size = models.CharField(max_length=100, null=True, blank=True)
    color = models.CharField(max_length=100, null=True, blank=True)

    #coupon
    initial_cost = models.DecimalField(decimal_places=2, max_digits=12, default=0.00)
    saved = models.DecimalField(decimal_places=2, max_digits=12, default=0.00)

    oid = ShortUUIDField(unique=True, length=10, alphabet='abcdefg12345')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.oid
    