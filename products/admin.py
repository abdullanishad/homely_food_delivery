from django.contrib import admin
from .models import Item, Seller, Order, OrderItem

admin.site.register(Seller)
admin.site.register(OrderItem)


class OrderItemInline(admin.TabularInline):
    """Defines format of inline book insertion (used in AuthorAdmin)"""
    model = OrderItem


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['price', 'category', 'seller']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [ 'user', 'fullname', 'ordered', 'delivery_date', 'ordered_date']
    list_display_links = ['user',]
    list_filter = ['ordered', 'delivery_date']
    search_fields = ['user__username', 'order_id']
    inlines = [OrderItemInline]
