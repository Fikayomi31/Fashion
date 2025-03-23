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
    