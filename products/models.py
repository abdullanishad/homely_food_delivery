from django.db import models
from django.contrib.auth.models import User
from datetime import date
from django.conf import settings
from django.urls import reverse
from django.contrib.auth.models import User
import uuid  # Required for unique book instances
from PIL import Image



class Seller(models.Model):
    name = models.CharField(max_length=20)
    mobile_num = models.CharField(max_length=10)
    address = models.TextField()
    upi_id = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Item(models.Model):
    photo = models.ImageField(upload_to="gallery", default='default.jpg', null=True)
    title = models.CharField(unique=True, max_length=20, null=False)
    slug = models.SlugField(null=True)
    price = models.IntegerField()
    category_lists = (
        ('cakes', 'cakes'),
        ('cupcakes', 'cupcakes'),
        ('brownies', 'brownies'),
        ('macrons', 'macrons'),
    )
    category = models.CharField(
        max_length=20,
        choices=category_lists,
        blank=False,
        help_text='select category',
    )
    seller = models.ForeignKey('Seller', on_delete=models.SET_NULL, null=True)
    description = models.CharField(max_length=99)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("item-detail", kwargs={'slug': self.slug})

    def get_add_to_cart_url(self):
        return reverse("add-to-cart", kwargs={'slug': self.slug})

    def save(self):
        super().save()

        img = Image.open(self.photo.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.photo.path)

    # def get_remove_from_cart_url(self):
    #     return reverse("products:remove-from-cart", kwargs={'title': self.title})


class Order(models.Model):
    order_id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID ")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    fullname = models.CharField(max_length=30, null=True)
    ordered_date = models.DateTimeField(auto_now_add=True, null=True)
    delivery_date = models.DateField(null=True)
    ordered = models.BooleanField(default=False, null=True)
    phone_number = models.IntegerField(null=True)
    address = models.CharField(max_length=30, null=True)
    lists = (('kasaragod', 'kasaragod'),('kumbala', 'kumbala'), ('eriyal', 'eriyal'),('chowki', 'chowki'),)
    location = models.CharField(max_length=20,choices=lists,blank=False, help_text='select location', null=True)
    total_order_price = models.IntegerField(default=0,null=True)

    def __str__(self):
        return str(self.order_id)

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        return total


class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, null=True)
    ordered = models.BooleanField(default=False)
    delivered = models.BooleanField(default=False)
    quantity = models.PositiveIntegerField(default=1, null=True)
    message = models.CharField(max_length=49, null=True, blank=True)
    instructions = models.CharField(max_length=49, null=True, blank=True)
    total_orderitem_price = models.IntegerField(null=True)

    def __str__(self):
        return self.item.title

    def get_total_item_price(self):
        return self.quantity * self.item.price
