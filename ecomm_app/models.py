from django.conf import settings
from django.db import models
from django.shortcuts import reverse
from django_countries.fields import CountryField
from PIL import Image

# Create your models here.
CATEGORY_CHOICES = (
    ('Shirt','Shirt'),
    ('Trouser', 'Trouser'),
    ('Shoe','Shoe'),
)

LABEL_CHOICES = (
    ('P','primary'),
    ('S', 'secondary'),
    ('D','danger'),
)

TAG_CHOICES = (
    ('B','BestSeller'),
    ('N', 'New'),
)


class Item(models.Model):
    title = models.CharField(max_length = 100)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)
    category = models.CharField(choices = CATEGORY_CHOICES, max_length = 20, default= 'Shirt')
    label = models.CharField(choices = LABEL_CHOICES, max_length = 20, default= 'P')
    tag = models.CharField(choices = TAG_CHOICES, max_length = 20, default= 'N')
    slug = models.SlugField()
    description = models.TextField()
    image1 = models.ImageField(default = 'default2.jpg', upload_to = 'products_pics')
    image2 = models.ImageField(default = 'default2.jpg', upload_to = 'products_pics')
    image3 = models.ImageField(upload_to = 'products_pics', blank=True, null=True)

    def save(self, force_insert=False, force_update=False, using=None):
        super().save()

        img = Image.open(self.image1.path)
        if img.height > 450 or img.width > 450:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image1.path)

        img = Image.open(self.image2.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image2.path)

        if self.image3:
            img = Image.open(self.image3.path)
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.image3.path)


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("ecomm_app:product", kwargs = {
            'slug': self.slug
        })

    def get_add_to_cart_url(self):
        return reverse("ecomm_app:add-to-cart", kwargs = {
            'slug': self.slug
        })

    def get_remove_from_cart_url(self):
        return reverse("ecomm_app:remove-from-cart", kwargs = {
            'slug': self.slug
        })



class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    ordered = models.BooleanField(default = False)
    item = models.ForeignKey(Item, on_delete = models.CASCADE)
    quantity = models.IntegerField(default = 1)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_total_item_discount_price(self):
        return self.quantity * self.item.discount_price

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_item_discount_price()

    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_item_discount_price()
        return self.get_total_item_price()


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add = True)
    ordered = models.BooleanField(default = False)
    ordered_date = models.DateTimeField()
    billing_address = models.ForeignKey(
        'BillingAddress', on_delete = models.SET_NULL, blank = True, null = True
    )

    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        return total


class BillingAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE)
    street_address = models.CharField(max_length = 100)
    region = models.CharField( max_length = 100)
    country = CountryField(multiple = False)

    def __str__(self):
        return self.user.username
